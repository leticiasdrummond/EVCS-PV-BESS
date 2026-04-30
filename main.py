from pathlib import Path

import matplotlib.pyplot as plt

from pyomo.environ import (
    AbstractModel,
    Binary,
    Constraint,
    NonNegativeReals,
    Objective,
    Param,
    RangeSet,
    SolverFactory,
    Var,
    maximize,
    value,
)
from pyomo.opt import SolverStatus, TerminationCondition


"""
Modelo Pyomo (AbstractModel) para microrrede de eletroposto em rodovia.

Base conceitual: Secao 3.2 do artigo, com foco no despacho integrado PV-BESS-Rede.

Simplificacoes adotadas neste modelo:
1) Objetivo economico simplificado:
   - Maximizacao de lucro operacional (receita de recarga + receita de exportacao - custo de importacao)
     menos CAPEX inicial (PV, BESS, transformador).
    - Custos de CO2 e depreciações/valor do dinheiro no tempo complexos foram desconsiderados.
2) Versao "mais proxima do artigo" disponivel:
    - Inclui custo anualizado de investimento via CRF e O&M anual por capacidade instalada.
    - A escolha entre objetivo simplificado e objetivo anualizado e controlada pelo parametro
      use_article_like_objective (0=simplificado, 1=anualizado com CRF+O&M).
3) Horizonte operacional:
   - Serie de 24h representativa.
   - Para comparar com CAPEX (investimento unico), aplica-se o fator
     operational_days_equivalent para anualizar o resultado operacional representativo.
4) BESS linear:
   - Dinamica de SOC linear com eficiencias separadas de carga e descarga.
    - Nao simultaneidade carga/descarga imposta via variavel binaria por hora.
    - Linearizacao Big-M fisicamente derivada de um limite superior de capacidade do BESS.
5) Restricao anti-load-shedding:
   - Variavel de corte de carga (LoadShedding) existe para rastreabilidade,
     mas e forçada a zero em todas as horas (servico ininterrupto da Bolsa #7).

Mapeamento de parametros tecnicos:
- irradiance_cf[t]: fator de capacidade PV por hora (0 a 1), mapeando irradiancia para
  potencia disponivel por kW instalado.
- eta_charge, eta_discharge: eficiencias de carga/descarga do BESS (tipicamente 90-95%).
- c_rate_charge, c_rate_discharge: limites de potencia do BESS em funcao da energia instalada.
- soc_min_frac, soc_max_frac, soc_initial_frac: limites e condicao inicial/final de SOC.
- grid_price[t]: tarifa horaria de energia da rede (BRL/kWh).
- tariff_ev: tarifa de venda para recarga de VE (BRL/kWh).
"""


def build_model() -> AbstractModel:
    model = AbstractModel()


    # Horizonte horario.
    # Interpretacao fisica: discretiza a operacao da microrrede em 24 intervalos,
    # usualmente associados a 24 horas tipicas de um dia representativo.
    # Interpretacao economica: essa discretizacao permite calcular receitas e custos
    # por periodo tarifario, capturando arbitragem temporal de energia.
    # Interpretacao de modelagem: RangeSet define o indice temporal do problema
    # deterministico de programacao matematica, base para todas as variaveis e
    # restricoes acopladas no tempo (especialmente SOC do BESS).
    model.T = RangeSet(1, 24)

    # Parametros economicos.
    # - delta_t converte potencia (kW) em energia (kWh) no periodo.
    # - operational_days_equivalent anualiza a operacao diaria representativa.
    # - tariff_ev e o preco de venda do servico de recarga ao usuario final.
    # - export_price_factor reduz a remuneracao da exportacao em relacao ao preco
    #   de compra da rede (mecanismo de compensacao/mercado menos favoravel).
    # - use_article_like_objective atua como seletor continuo entre duas funcoes
    #   objetivo lineares; na pratica, usar 0 ou 1 preserva interpretacao clara.
    model.delta_t = Param(within=NonNegativeReals, default=1.0)  # horas
    model.operational_days_equivalent = Param(within=NonNegativeReals, default=365.0)
    model.tariff_ev = Param(within=NonNegativeReals)  # BRL/kWh
    model.export_price_factor = Param(within=NonNegativeReals, default=0.7)
    model.allow_grid_export = Param(within=NonNegativeReals, default=1.0)
    model.use_article_like_objective = Param(within=NonNegativeReals, default=0.0)

    # CAPEX (BRL por unidade de capacidade).
    # Interpretacao fisica: cada decisao de investimento dimensiona um ativo real
    # (arranjo PV em kW, BESS em kWh, transformador em kW).
    # Interpretacao economica: representa desembolso inicial para habilitar a
    # operacao da estacao de recarga e a flexibilidade energetica.
    # Interpretacao de modelagem: custo linear por capacidade instalada, sem
    # economias de escala, preservando problema MILP/LP linear.
    model.capex_pv_kw = Param(within=NonNegativeReals)
    model.capex_bess_kwh = Param(within=NonNegativeReals)
    model.capex_trafo_kw = Param(within=NonNegativeReals)

    # Parametros de anualizacao (versao mais proxima do artigo).
    # CRF converte CAPEX em fluxo anual equivalente (custo de capital), enquanto
    # O&M adiciona custo operacional fixo por capacidade instalada.
    # Em termos de planejamento, aproxima comparacao entre beneficio anual e
    # encargo anualizado dos ativos, evitando mistura direta de fluxos e estoque.
    model.crf_pv = Param(within=NonNegativeReals, default=0.0)
    model.crf_bess = Param(within=NonNegativeReals, default=0.0)
    model.crf_trafo = Param(within=NonNegativeReals, default=0.0)
    model.om_pv_kw_year = Param(within=NonNegativeReals, default=0.0)
    model.om_bess_kwh_year = Param(within=NonNegativeReals, default=0.0)
    model.om_trafo_kw_year = Param(within=NonNegativeReals, default=0.0)

    # Parametros tecnicos BESS.
    # Interpretacao fisica:
    # - eta_charge/eta_discharge modelam perdas eletroquimicas e de conversao.
    # - limites SOC evitam sobrecarga e descarga profunda, preservando vida util.
    # - c-rate relaciona potencia maxima com energia instalada.
    # Interpretacao de modelagem:
    # - todos entram linearmente, mantendo formulacao tratavel por solver MILP.
    # - E_bess_cap_max e um limite exogeno de projeto usado para Big-M robusto.
    model.eta_charge = Param(within=NonNegativeReals)
    model.eta_discharge = Param(within=NonNegativeReals)
    model.soc_min_frac = Param(within=NonNegativeReals)
    model.soc_max_frac = Param(within=NonNegativeReals)
    model.soc_initial_frac = Param(within=NonNegativeReals)
    model.c_rate_charge = Param(within=NonNegativeReals)
    model.c_rate_discharge = Param(within=NonNegativeReals)
    model.E_bess_cap_max = Param(within=NonNegativeReals, default=2000.0)
    model.P_pv_cap_max = Param(within=NonNegativeReals, default=1000.0)
    model.P_trafo_cap_max = Param(within=NonNegativeReals, default=500.0)

    # Series horarias.
    # irradiance_cf: recurso renovavel exogeno por hora.
    # grid_price: sinal economico temporal para importacao/exportacao.
    # P_ev_load_kw: demanda inelastica de recarga a ser atendida sem interrupcao.
    model.irradiance_cf = Param(model.T, within=NonNegativeReals)
    model.grid_price = Param(model.T, within=NonNegativeReals)
    model.P_ev_load_kw = Param(model.T, within=NonNegativeReals)

    # Variaveis de investimento (primeiro estagio implito).
    # Essas variaveis sintetizam decisoes de planejamento da infraestrutura e
    # acoplam todos os periodos operacionais, pois capacidade e compartilhada no dia.
    model.P_pv_cap = Var(within=NonNegativeReals)  # kW
    model.E_bess_cap = Var(within=NonNegativeReals)  # kWh
    model.P_trafo_cap = Var(within=NonNegativeReals)  # kW

    # Variaveis operacionais (segundo estagio de despacho horario).
    # Interpretacao fisica: fluxos de potencia e estado energetico da bateria.
    # Interpretacao economica: cada fluxo participa de receitas/custos no objetivo.
    # Interpretacao de modelagem: y_bess torna explicita a logica disjuntiva
    # carga-versus-descarga via linearizacao Big-M (classe MILP).
    model.P_pv_gen = Var(model.T, within=NonNegativeReals)  # kW
    model.P_grid_import = Var(model.T, within=NonNegativeReals)  # kW
    model.P_grid_export = Var(model.T, within=NonNegativeReals)  # kW
    model.P_bess_charge = Var(model.T, within=NonNegativeReals)  # kW
    model.P_bess_discharge = Var(model.T, within=NonNegativeReals)  # kW
    model.SOC = Var(model.T, within=NonNegativeReals)  # kWh
    model.LoadShedding = Var(model.T, within=NonNegativeReals)  # kW
    model.y_bess = Var(model.T, within=Binary)

    # ---------------------------------------------------------------------
    # BLOCO DE RESTRICOES
    # ---------------------------------------------------------------------
    # Em leitura de sistema eletrico, as restricoes reproduzem:
    # - disponibilidade de recurso (PV),
    # - limites de interface com rede (transformador),
    # - limites eletroenergeticos do BESS,
    # - conservacao de energia por periodo,
    # - requisito de continuidade de atendimento da carga de VE.
    # Em leitura de otimizacao, esse conjunto define o poliedro viavel do MILP.

    # limite de geracao fotovoltaica por fator de capacidade
    # Eq. de disponibilidade PV.
    # Fisico: potencia PV injetada nao pode exceder potencia nominal instalada
    # multiplicada pelo fator horario de irradiancia.
    # Economico: investir em mais PV amplia teto de geracao e reduz dependencia de
    # compra da rede em horas solares.
    # Modelagem: restricao linear de acoplamento entre variavel de investimento
    # (P_pv_cap) e variavel de operacao (P_pv_gen[t]).
    def pv_generation_limit_rule(m, t):
        return m.P_pv_gen[t] <= m.P_pv_cap * m.irradiance_cf[t]

    model.PVGenerationLimit = Constraint(model.T, rule=pv_generation_limit_rule)

    # Limites de transformador (importacao/exportacao).
    # Fisico: a interface com a rede possui capacidade aparente contratada/instalada
    # que limita fluxo em qualquer sentido.
    # Economico: maior trafo aumenta opcao de arbitragem e seguranca de suprimento,
    # mas cobra CAPEX adicional.
    # Modelagem: limite linear por periodo para importacao e exportacao.
    def trafo_import_limit_rule(m, t):
        return m.P_grid_import[t] <= m.P_trafo_cap

    def trafo_export_limit_rule(m, t):
        return m.P_grid_export[t] <= m.P_trafo_cap * m.allow_grid_export

    model.TrafoImportLimit = Constraint(model.T, rule=trafo_import_limit_rule)
    model.TrafoExportLimit = Constraint(model.T, rule=trafo_export_limit_rule)

    # Limites de potencia de carga/descarga do BESS.
    # Fisico: conversores e a propria quimica impõem taxa maxima de carga/descarga
    # proporcional ao tamanho energetico instalado (c-rate).
    # Economico: baterias maiores permitem maiores rampas de arbitragem, potencialmente
    # aumentando captura de spread tarifario.
    # Modelagem: vinculacao linear P <= c_rate * E_cap.
    def bess_charge_power_limit_rule(m, t):
        return m.P_bess_charge[t] <= m.c_rate_charge * m.E_bess_cap

    def bess_discharge_power_limit_rule(m, t):
        return m.P_bess_discharge[t] <= m.c_rate_discharge * m.E_bess_cap

    model.BESSChargePowerLimit = Constraint(model.T, rule=bess_charge_power_limit_rule)
    model.BESSDischargePowerLimit = Constraint(model.T, rule=bess_discharge_power_limit_rule)

    """ # Limite superior fisico da capacidade de BESS para derivar Big-M.
    # Fisico/economico: impede crescimento irrealista da capacidade instalada.
    # Modelagem: fortalece numericamente a MILP, pois Big-M fica calibrado por
    # limite plausivel e nao por constante arbitrariamente grande.
    """
    def bess_capacity_upper_bound_rule(m):
        return m.E_bess_cap <= m.E_bess_cap_max
    model.BESSCapacityUpperBound = Constraint(rule=bess_capacity_upper_bound_rule)

    # Limites de capacidade de investimento para manter o problema fisicamente
    # plausivel e evitar expansao ilimitada de ativos.
    def pv_capacity_upper_bound_rule(m):
        return m.P_pv_cap <= m.P_pv_cap_max

    def trafo_capacity_upper_bound_rule(m):
        return m.P_trafo_cap <= m.P_trafo_cap_max

    model.PVCapacityUpperBound = Constraint(rule=pv_capacity_upper_bound_rule)
    model.TrafoCapacityUpperBound = Constraint(rule=trafo_capacity_upper_bound_rule)

    # Nao simultaneidade de carga/descarga (MILP linearizado).
    # Fisico: em um mesmo intervalo, a bateria opera predominantemente em modo
    # carga ou descarga (evita ciclo artificial instantaneo).
    # Economico: evita solucao espuria que "compra e vende" internamente energia
    # sem significado operacional, distorcendo lucro.
    # Modelagem: variavel binaria y_bess[t] ativa um dos modos via Big-M.

    def bess_charge_limit_milp(m, t):
        return m.P_bess_charge[t] <= m.c_rate_charge * m.E_bess_cap_max * m.y_bess[t]

    def bess_discharge_limit_milp(m, t):
        return m.P_bess_discharge[t] <= m.c_rate_discharge * m.E_bess_cap_max * (1 - m.y_bess[t])

    model.BESSChargeModeMILP = Constraint(model.T, rule=bess_charge_limit_milp)
    model.BESSDischargeModeMILP = Constraint(model.T, rule=bess_discharge_limit_milp)

    # Limites de SOC.
    # Fisico: janela operacional segura da bateria (reserva minima e teto maximo).
    # Economico: manter SOC minimo reduz risco de indisponibilidade para carga critica.
    # Modelagem: desigualdades lineares dependentes da capacidade decidida.
    def soc_min_rule(m, t):
        return m.SOC[t] >= m.soc_min_frac * m.E_bess_cap

    def soc_max_rule(m, t):
        return m.SOC[t] <= m.soc_max_frac * m.E_bess_cap

    model.SOCMin = Constraint(model.T, rule=soc_min_rule)
    model.SOCMax = Constraint(model.T, rule=soc_max_rule)

    # Dinamica do SOC.
    # Fisico: conservacao de energia no armazenamento, com perdas na carga/descarga.
    # Economico: desloca energia no tempo para aproveitar diferencas de preco e
    # reduzir importacao em horarios caros.
    # Modelagem: equacoes lineares recursivas acoplam periodos consecutivos,
    # tornando o problema intertemporal.
    def soc_balance_rule(m, t):
        if t == m.T.first():
            return m.SOC[t] == m.soc_initial_frac * m.E_bess_cap + m.delta_t * (
                m.eta_charge * m.P_bess_charge[t] - m.P_bess_discharge[t] / m.eta_discharge
            )
        t_prev = m.T.prev(t)
        return m.SOC[t] == m.SOC[t_prev] + m.delta_t * (
            m.eta_charge * m.P_bess_charge[t] - m.P_bess_discharge[t] / m.eta_discharge
        )

    model.SOCBalance = Constraint(model.T, rule=soc_balance_rule)

    # Condicao ciclica: SOC final igual ao inicial.
    # Fisico: evita "esvaziar" ou "encher" artificialmente a bateria no ultimo
    # periodo para inflar resultado de um dia representativo.
    # Economico: assegura comparabilidade interdiaria e neutralidade energetica do
    # estado final no calculo anualizado.
    # Modelagem: fecha o horizonte com restricao terminal de consistencia.
    def terminal_soc_rule(m):
        return m.SOC[m.T.last()] == m.soc_initial_frac * m.E_bess_cap

    model.TerminalSOC = Constraint(rule=terminal_soc_rule)

    # Equilibrio de energia (inspirado na Eq. 483): Fontes = Usos.
    # Fisico: lei de conservacao de potencia em cada hora no barramento equivalente
    # da microrrede (balanco nodal agregado).
    # Economico: toda decisao de despacho aparece no caixa, direta ou indiretamente,
    # por custos de compra, receitas de venda e atendimento da carga de recarga.
    # Modelagem: igualdade linear central da formulacao, acoplando todas as
    # variaveis operacionais do periodo t.
    def energy_balance_rule(m, t):
        return (
            m.P_pv_gen[t] + m.P_grid_import[t] + m.P_bess_discharge[t]
            == m.P_ev_load_kw[t] - m.LoadShedding[t] + m.P_bess_charge[t] + m.P_grid_export[t]
        )

    model.EnergyBalance = Constraint(model.T, rule=energy_balance_rule)

    # Restricao de continuidade de servico: sem load shedding.
    # Fisico: impõe atendimento integral da demanda de recarga em todas as horas.
    # Economico: representa compromisso de qualidade de servico (Bolsa #7), sem
    # aceitar perda de receita por demanda nao atendida.
    # Modelagem: LoadShedding e mantida no modelo para rastreabilidade/expansao
    # futura, mas fixada a zero nesta versao.
    def no_shedding_rule(m, t):
        return m.LoadShedding[t] == 0.0

    model.NoLoadShedding = Constraint(model.T, rule=no_shedding_rule)

    # Objetivo: maximizacao de desempenho economico com duas leituras.
    # Leitura economica:
    # - receita principal: venda de energia para recarga VE (tariff_ev * demanda).
    # - receita secundaria: exportacao para rede com fator redutor de preco.
    # - custo principal: importacao de energia da rede.
    # - penalizacao de investimento: CAPEX unico (forma simplificada) ou CAPEX
    #   anualizado + O&M (forma artigo-like).
    # Leitura de modelagem:
    # - ambas as funcoes sao lineares e combinadas por parametro exogeno,
    #   preservando estrutura MILP sem nao linearidades.
    # - como a carga de VE e parametro exogeno, a receita de recarga funciona como
    #   termo quase constante; as decisoes atuam principalmente na minimizacao do
    #   custo liquido de suprimento e no tamanho otimo dos ativos.
    # A selecao da forma segue use_article_like_objective:
    # 0 -> simplificado: (lucro operacional anualizado - CAPEX unico)
    # 1 -> anualizado: (lucro operacional anualizado - CAPEX anualizado por CRF - O&M anual)
    def objective_rule(m):
        daily_revenue_ev = sum(m.tariff_ev * m.P_ev_load_kw[t] * m.delta_t for t in m.T)
        daily_revenue_export = sum(
            m.export_price_factor * m.grid_price[t] * m.P_grid_export[t] * m.delta_t for t in m.T
        )
        daily_cost_import = sum(m.grid_price[t] * m.P_grid_import[t] * m.delta_t for t in m.T)

        annual_operational_profit = m.operational_days_equivalent * (
            daily_revenue_ev + daily_revenue_export - daily_cost_import
        )

        capex_total = (
            m.capex_pv_kw * m.P_pv_cap
            + m.capex_bess_kwh * m.E_bess_cap
            + m.capex_trafo_kw * m.P_trafo_cap
        )

        annualized_investment = (
            m.crf_pv * m.capex_pv_kw * m.P_pv_cap
            + m.crf_bess * m.capex_bess_kwh * m.E_bess_cap
            + m.crf_trafo * m.capex_trafo_kw * m.P_trafo_cap
        )

        annual_om = (
            m.om_pv_kw_year * m.P_pv_cap
            + m.om_bess_kwh_year * m.E_bess_cap
            + m.om_trafo_kw_year * m.P_trafo_cap
        )

        simplified_objective = annual_operational_profit - capex_total
        article_like_objective = annual_operational_profit - annualized_investment - annual_om

        return (1 - m.use_article_like_objective) * simplified_objective + (
            m.use_article_like_objective * article_like_objective
        )

    model.Obj = Objective(rule=objective_rule, sense=maximize)

    return model


def write_report(instance, report_path: Path) -> None:
    # Pos-processamento economico da solucao.
    # Esta rotina recompõe indicadores financeiros de forma transparente para
    # auditoria: separa receita, custo operacional, CAPEX e metricas anualizadas.
    # Do ponto de vista de pesquisa operacional, favorece interpretabilidade da
    # solucao alem do valor escalar da funcao objetivo.
    objective_value = value(instance.Obj)

    annual_revenue_ev = sum(
        value(instance.tariff_ev) * value(instance.P_ev_load_kw[t]) * value(instance.delta_t)
        for t in instance.T
    ) * value(instance.operational_days_equivalent)
    annual_revenue_export = sum(
        value(instance.export_price_factor)
        * value(instance.grid_price[t])
        * value(instance.P_grid_export[t])
        * value(instance.delta_t)
        for t in instance.T
    ) * value(instance.operational_days_equivalent)
    annual_cost_import = sum(
        value(instance.grid_price[t]) * value(instance.P_grid_import[t]) * value(instance.delta_t)
        for t in instance.T
    ) * value(instance.operational_days_equivalent)
    annual_operational_profit = annual_revenue_ev + annual_revenue_export - annual_cost_import

    capex_total = (
        value(instance.capex_pv_kw) * value(instance.P_pv_cap)
        + value(instance.capex_bess_kwh) * value(instance.E_bess_cap)
        + value(instance.capex_trafo_kw) * value(instance.P_trafo_cap)
    )
    annualized_investment = (
        value(instance.crf_pv) * value(instance.capex_pv_kw) * value(instance.P_pv_cap)
        + value(instance.crf_bess) * value(instance.capex_bess_kwh) * value(instance.E_bess_cap)
        + value(instance.crf_trafo) * value(instance.capex_trafo_kw) * value(instance.P_trafo_cap)
    )
    annual_om = (
        value(instance.om_pv_kw_year) * value(instance.P_pv_cap)
        + value(instance.om_bess_kwh_year) * value(instance.E_bess_cap)
        + value(instance.om_trafo_kw_year) * value(instance.P_trafo_cap)
    )

    objective_simplified = annual_operational_profit - capex_total
    objective_article_like = annual_operational_profit - annualized_investment - annual_om

    with report_path.open("w", encoding="utf-8") as f:
        # Estrutura textual deterministicamente reproduzivel, util para comparacao
        # de cenarios e posterior ingestao por scripts de analise.
        f.write("RELATORIO DE OTIMIZACAO - MICRORREDE RODOVIA\n")
        f.write("=" * 72 + "\n\n")

        f.write("Capacidades otimizadas:\n")
        f.write(f"- PV (kW): {value(instance.P_pv_cap):.3f}\n")
        f.write(f"- BESS (kWh): {value(instance.E_bess_cap):.3f}\n")
        f.write(f"- Transformador (kW): {value(instance.P_trafo_cap):.3f}\n\n")

        f.write(f"Valor da funcao objetivo ativa (BRL): {objective_value:,.2f}\n")
        f.write(f"Modo objetivo (0=simplificado, 1=artigo): {value(instance.use_article_like_objective):.0f}\n\n")

        export_blocked = value(instance.allow_grid_export) < 0.5
        if export_blocked:
            f.write("*** EXPORTACAO BLOQUEADA NO CENARIO ***\n\n")
        else:
            f.write("Exportacao para rede: habilitada no cenario.\n\n")

        f.write("Comparativo lado a lado (avaliado na solucao otimizada):\n")
        f.write(f"- Objetivo simplificado (operacional anual - CAPEX): {objective_simplified:,.2f} BRL\n")
        f.write(
            "- Objetivo artigo-like (operacional anual - CAPEX anualizado CRF - O&M): "
            f"{objective_article_like:,.2f} BRL\n"
        )
        f.write(f"- Lucro operacional anual: {annual_operational_profit:,.2f} BRL\n")
        f.write(f"- CAPEX total (unico): {capex_total:,.2f} BRL\n")
        f.write(f"- CAPEX anualizado (CRF): {annualized_investment:,.2f} BRL/ano\n")
        f.write(f"- O&M anual: {annual_om:,.2f} BRL/ano\n\n")

        f.write("Despacho horario (kW / kWh):\n")
        f.write(
            "h,PV_gen,Grid_import,Grid_export,BESS_charge,BESS_discharge,SOC,EV_load,LoadShedding\n"
        )

        for t in instance.T:
            f.write(
                f"{t},"
                f"{value(instance.P_pv_gen[t]):.4f},"
                f"{value(instance.P_grid_import[t]):.4f},"
                f"{value(instance.P_grid_export[t]):.4f},"
                f"{value(instance.P_bess_charge[t]):.4f},"
                f"{value(instance.P_bess_discharge[t]):.4f},"
                f"{value(instance.SOC[t]):.4f},"
                f"{value(instance.P_ev_load_kw[t]):.4f},"
                f"{value(instance.LoadShedding[t]):.4f}\n"
            )


def generate_figures(instance, output_dir: Path) -> None:
    # Gera figuras pedidas pelo usuario com nomes de parametros consistentes.
    output_dir.mkdir(parents=True, exist_ok=True)

    T = [int(t) for t in instance.T]

    P_ev_load_kw = [value(instance.P_ev_load_kw[t]) for t in instance.T]
    grid_price = [value(instance.grid_price[t]) for t in instance.T]
    irradiance_cf = [value(instance.irradiance_cf[t]) for t in instance.T]

    P_pv_gen = [value(instance.P_pv_gen[t]) for t in instance.T]
    P_grid_import = [value(instance.P_grid_import[t]) for t in instance.T]
    P_bess_charge = [value(instance.P_bess_charge[t]) for t in instance.T]
    P_bess_discharge = [value(instance.P_bess_discharge[t]) for t in instance.T]
    SOC = [value(instance.SOC[t]) for t in instance.T]

    # 1) Demanda eletrica veicular (grafico separado).
    plt.figure(figsize=(12, 6))
    plt.plot(T, P_ev_load_kw, label="Demanda Eletrica Veicular (kW)", color="tab:blue")
    plt.xlabel("Hora")
    plt.ylabel("Potencia (kW)")
    plt.title("Perfil de Demanda Eletrica Veicular")
    plt.xticks(T)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "fig_01_demanda_ev.png", dpi=150)
    plt.show()
    plt.close()

    # 2) Tarifa de eletricidade (grafico separado).
    plt.figure(figsize=(12, 6))
    plt.plot(T, grid_price, label="Tarifa Eletricidade (R$/kWh)", color="tab:orange")
    plt.xlabel("Hora")
    plt.ylabel("Tarifa (R$/kWh)")
    plt.title("Perfil da Tarifa de Eletricidade")
    plt.xticks(T)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "fig_02_tarifa_grid.png", dpi=150)
    plt.show()
    plt.close()

    # 3) Recurso solar FV (grafico separado).
    plt.figure(figsize=(12, 6))
    plt.plot(T, irradiance_cf, label="Recurso Solar FV (p.u.)", color="tab:green")
    plt.xlabel("Hora")
    plt.ylabel("Fator de capacidade (p.u.)")
    plt.title("Perfil de Recurso Solar FV")
    plt.xticks(T)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "fig_03_recurso_solar.png", dpi=150)
    plt.show()
    plt.close()

    # 4) Estado da bateria com series separadas por unidade:
    # colunas em kW (carga/descarga) e linha em kWh (SOC) em eixo secundario.
    fig_bess, ax_kw = plt.subplots(figsize=(12, 6))
    width = 0.4
    ax_kw.bar(
        [t - width / 2 for t in T],
        P_bess_charge,
        width=width,
        label="BESS charge (kW)",
        color="tab:cyan",
    )
    ax_kw.bar(
        [t + width / 2 for t in T],
        P_bess_discharge,
        width=width,
        label="BESS discharge (kW)",
        color="tab:red",
    )
    ax_kw.set_xlabel("Hora")
    ax_kw.set_ylabel("Potencia BESS (kW)")
    ax_kw.set_xticks(T)
    ax_kw.grid(True, axis="y")

    ax_kwh = ax_kw.twinx()
    ax_kwh.plot(T, SOC, label="SOC (kWh)", color="black", linewidth=2.0)
    ax_kwh.set_ylabel("SOC (kWh)")

    ax_kw.set_title("Estado de Carga da Bateria")
    lines1, labels1 = ax_kw.get_legend_handles_labels()
    lines2, labels2 = ax_kwh.get_legend_handles_labels()
    ax_kw.legend(lines1 + lines2, labels1 + labels2, loc="best")

    fig_bess.tight_layout()
    fig_bess.savefig(output_dir / "fig_04_bateria_kw_kwh.png", dpi=150)
    plt.show()
    plt.close(fig_bess)

    # 5) Fluxo energetico horario da microrrede.
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(T, P_pv_gen, label="PV geracao (kW)")
    ax1.plot(T, P_grid_import, label="Grid import (kW)")
    ax1.plot(T, P_ev_load_kw, label="EV load (kW)")
    ax1.set_xlabel("Hora")
    ax1.set_ylabel("Potencia (kW)")
    ax1.set_title("Fluxo Energetico da Microrrede")
    ax1.set_xticks(T)
    ax1.grid(True)

    # SOC e exibido em eixo secundario para manter unidade correta (kWh).
    ax2 = ax1.twinx()
    ax2.plot(T, SOC, color="black", linestyle=":", label="SOC (kWh)")
    ax2.set_ylabel("SOC (kWh)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")

    fig.tight_layout()
    fig.savefig(output_dir / "fig_05_fluxo_energetico.png", dpi=150)
    plt.show()
    plt.close(fig)


def main() -> None:
    # Encapsula fluxo de execucao do experimento: leitura de dados, resolucao da
    # MILP e emissao de relatorio tecnico-economico.
    base_dir = Path(__file__).resolve().parent
    data_file = base_dir / "dados_exemplo.dat"
    report_file = base_dir / "relatorio_saida.txt"
    figures_dir = base_dir / "figuras_saida"

    model = build_model()
    instance = model.create_instance(str(data_file))

    # Observacao de implementacao: o backend "gurobi" usa a interface de solver
    # esperada pelo Pyomo. Validacao explicita evita falhas silenciosas de ambiente.
    solver = SolverFactory("gurobi")
    if not solver.available(False):
        raise RuntimeError(
            "Solver Gurobi indisponivel via 'gurobi'. Verifique instalacao/licenca do Gurobi."
        )

    results = solver.solve(instance, tee=False)

    # Checagem de qualidade de solucao: status e termination condition precisam
    # confirmar resolucao valida (otima global ou local conforme backend).
    status_ok = results.solver.status == SolverStatus.ok
    term_ok = results.solver.termination_condition in {
        TerminationCondition.optimal,
        TerminationCondition.locallyOptimal,
    }

    if not (status_ok and term_ok):
        raise RuntimeError(
            "Falha na otimizacao. "
            f"Status: {results.solver.status}; "
            f"Termination: {results.solver.termination_condition}"
        )

    write_report(instance, report_file)
    generate_figures(instance, figures_dir)
    print(f"Relatorio gerado com sucesso em: {report_file}")
    print(f"Figuras geradas com sucesso em: {figures_dir}")


if __name__ == "__main__":
    main()
