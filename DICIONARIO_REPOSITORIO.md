# Dicionário do Repositório — Microrrede Eletroposto
## Unidades de Medida, Parâmetros e Variáveis

---

## 1. UNIDADES DE MEDIDA FUNDAMENTAIS

| Grandeza | Unidade | Símbolo | Descrição |
|----------|---------|---------|-----------|
| **Potência** | Kilowatt | kW | Fluxo de energia instantâneo (1 kW = 1000 W) |
| **Energia** | Kilowatt-hora | kWh | Quantidade de energia (1 kWh = 3.6 MJ) |
| **Tarifas** | Real por kWh | BRL/kWh | Preço de compra/venda de eletricidade (moeda: Real) |
| **Investimento** | Real | BRL | Custos de capital (CAPEX) e operação (O&M) |
| **Tempo** | Hora | h | Período horário de discretização temporal |
| **Tempo** | Minuto | min | Unidade de tempo para perfil de chegadas VE |
| **Fração** | Adimensional | frac | Percentual expresso como valor 0 a 1 (ex: 0.9 = 90%) |
| **Fator** | Adimensional | CF | Fator de capacidade: razão (geração real / capacidade nominal) |
| **Eficiência** | Adimensional | η | Taxa de conversão (0 a 1); ex: η=0.95 significa 95% de eficiência |
| **Taxa C** | Adimensional | C | Razão entre potência (kW) e energia (kWh); ex: 1-C significa 1 hora até descarregar |
| **Coeficiente de Variação** | Adimensional | CV | Razão entre desvio padrão e média; ex: 0.2358 indica 23.58% de variabilidade relativa |

---

## 2. PARÂMETROS DE DIMENSIONAMENTO (CAPEX)

### 2.1 Custos de Investimento por Unidade

| Parâmetro | Unidade | Descrição | Intervalo Típico | Fonte/Referência |
|-----------|---------|-----------|-----------------|-----------------|
| `capex_pv_kw` | BRL/kW | Custo de instalação de painéis solares por kW | 2,500–4,500 | IRENA, NREL, EPE |
| `capex_bess_kwh` | BRL/kWh | Custo de instalação de bateria por kWh | 400–800 | IRENA, NREL |
| `capex_trafo_kw` | BRL/kW | Custo de transformador + interface de rede por kW | 500–1,500 | Mercado nacional |

### 2.2 Parâmetros de Anualizacao (CRF + O&M)

| Parâmetro | Unidade | Descrição | Intervalo Típico |
|-----------|---------|-----------|-----------------|
| `crf_pv` | BRL/ano | Capital Recovery Factor anualizado para PV | 0.10–0.20 |
| `crf_bess` | BRL/ano | Capital Recovery Factor anualizado para BESS | 0.12–0.25 |
| `crf_trafo` | BRL/ano | Capital Recovery Factor anualizado para transformador | 0.08–0.15 |
| `om_pv_kw_year` | BRL/(kW·ano) | Custo de operação e manutenção anual de PV | 30–100 |
| `om_bess_kwh_year` | BRL/(kWh·ano) | Custo de operação anual de BESS (ex: monitoramento) | 5–20 |
| `om_trafo_kw_year` | BRL/(kW·ano) | Custo de operação anual de transformador | 10–50 |

---

## 3. PARÂMETROS TÉCNICOS DA BATERIA (BESS)

| Parâmetro | Unidade | Símbolo | Descrição | Intervalo Típico |
|-----------|---------|---------|-----------|-----------------|
| **Eficiência de Carga** | Fração | `eta_charge` | Percentual de energia que entra na bateria vs. demandada do inversor | 0.90–0.98 |
| **Eficiência de Descarga** | Fração | `eta_discharge` | Percentual de energia que sai da bateria vs. armazenada | 0.90–0.98 |
| **Taxa de Carga (C-Rate)** | Adimensional | `c_rate_charge` | Razão P_max_carga / E_bess; ex: 1-C = carga em 1h | 0.5–2.0 |
| **Taxa de Descarga (C-Rate)** | Adimensional | `c_rate_discharge` | Razão P_max_descarga / E_bess; ex: 1-C = descarga em 1h | 0.5–2.0 |
| **SOC Mínimo** | Fração | `soc_min_frac` | Limite inferior de estado de carga (evita descarga profunda) | 0.05–0.20 |
| **SOC Máximo** | Fração | `soc_max_frac` | Limite superior de estado de carga (evita sobrecarga) | 0.80–0.95 |
| **SOC Inicial** | Fração | `soc_initial_frac` | Estado de carga no início do dia representativo | 0.50–0.70 |
| **Capacidade Máxima (limite segurança)** | kWh | `E_bess_cap_max` | Limite superior exógeno para dimensionamento (Big-M) | 2,000–5,000 |

**Notas:**
- Eficiência *round-trip* ≈ η_charge × η_discharge (energia que retorna ao uso / energia original)
- C-rate maior permite arbitragem mais rápida, mas aumenta desgaste
- SOC operacional = intervalo entre min e max; ex: [0.2, 0.9] = 70% de capacidade usável

---

## 4. PARÂMETROS TÉCNICOS DO PAINEL SOLAR (PV)

| Parâmetro | Unidade | Descrição | Intervalo Típico |
|-----------|---------|-----------|-----------------|
| **Fator de Capacidade Horário** | Fração | `irradiance_cf[t]` | Irradiância disponível em cada hora *t* como fração da potência nominal (0 em noite, ~1.0 ao meio-dia) | 0.0–1.0 |
| **Capacidade Máxima (limite segurança)** | kW | `P_pv_cap_max` | Limite superior exógeno para dimensionamento | 500–1,500 |

**Notas:**
- Fator de capacidade diário típico (Brasil): 0.15–0.20 (anual); curva diária é aproximada por sino com pico solar
- Dados horários de irradiância são obtidos de CRESESB, INPE/CPTEC ou simulação

---

## 5. PARÂMETROS TÉCNICOS DO TRANSFORMADOR

| Parâmetro | Unidade | Descrição | Intervalo Típico |
|-----------|---------|-----------|-----------------|
| **Capacidade Máxima (limite segurança)** | kW | `P_trafo_cap_max` | Limite superior exógeno para dimensionamento (em geral = limite da subestação) | 200–600 |
| **Permissão de Exportação** | Booleano | `allow_grid_export` | Indica se a conexão permite exportação reversa (1 = sim, 0 = não) | 0 ou 1 |

---

## 6. PARÂMETROS ECONÔMICOS

### 6.1 Tarifas Horárias

| Parâmetro | Unidade | Descrição | Intervalo Típico | Fonte |
|-----------|---------|-----------|-----------------|--------|
| **Tarifa de Compra (Grid)** | BRL/kWh | `grid_price[t]` | Preço de compra de eletricidade da rede em cada hora *t* (pode variar por período tarifário: ponta, intermediário, fora de ponta) | 0.5–2.5 |
| **Tarifa de Venda (EV)** | BRL/kWh | `tariff_ev` | Preço de venda do serviço de recarga ao usuário final | 1.5–4.0 |
| **Fator de Preço de Exportação** | Fração | `export_price_factor` | Redução aplicada ao preço de compra quando há exportação reversa à rede (ex: 0.7 = recebe 70% do grid_price) | 0.5–1.0 |

**Fontes brasileiras:**
- ANEEL: Banco de tarifas e estrutura TOU
- MME/ANEEL: Documentos de Tarifa Branca e sinal horário

### 6.2 Parâmetros de Tempo

| Parâmetro | Unidade | Descrição | Valor Padrão |
|-----------|---------|-----------|-------------|
| **Intervalo Temporal** | h | `delta_t` | 1.0 (discretização em 1 hora) |
| **Dias Operacionais Equivalentes Anuais** | dias/ano | `operational_days_equivalent` | 365 (para anualização de resultado diário) |

**Notas:**
- delta_t = 1 h significa que variáveis de potência são integradas em 1 h para obter energia
- Exemplo: P_pv_gen[t] (kW) × delta_t (1 h) = energia em kWh

---

## 7. VARIÁVEIS DE DECISÃO — INVESTIMENTO

| Variável | Unidade | Tipo | Descrição | Intervalo |
|----------|---------|------|-----------|-----------|
| **Capacidade PV** | kW | Contínua ≥ 0 | Potência nominal de painéis solares instalados | [0, P_pv_cap_max] |
| **Capacidade BESS** | kWh | Contínua ≥ 0 | Energia armazenável da bateria | [0, E_bess_cap_max] |
| **Capacidade Transformador** | kW | Contínua ≥ 0 | Capacidade de interface com rede | [0, P_trafo_cap_max] |

**Notação em código:** `P_pv_cap`, `E_bess_cap`, `P_trafo_cap`

---

## 8. VARIÁVEIS DE DESPACHO — OPERAÇÃO HORÁRIA

Todas as variáveis operacionais são indexadas por hora *t* ∈ {1, 2, ..., 24}.

### 8.1 Fluxos de Potência

| Variável | Unidade | Tipo | Descrição |
|----------|---------|------|-----------|
| **Geração PV** | kW | Contínua ≥ 0 | Potência ativa injetada pelo painel solar na hora *t* |
| **Importação da Rede** | kW | Contínua ≥ 0 | Potência comprada da rede na hora *t* |
| **Exportação para Rede** | kW | Contínua ≥ 0 | Potência vendida à rede na hora *t* (requer `allow_grid_export=1`) |
| **Carga de BESS** | kW | Contínua ≥ 0 | Potência ativa de carga da bateria na hora *t* |
| **Descarga de BESS** | kW | Contínua ≥ 0 | Potência ativa de descarga da bateria na hora *t* |
| **Corte de Carga** | kW | Contínua ≥ 0 | Potência não suprida (load shedding); modelada mas forçada a zero |

**Notação em código:** `P_pv_gen[t]`, `P_grid_import[t]`, `P_grid_export[t]`, `P_bess_charge[t]`, `P_bess_discharge[t]`, `LoadShedding[t]`

### 8.2 Estado Energético

| Variável | Unidade | Tipo | Descrição |
|----------|---------|------|-----------|
| **Estado de Carga (SOC)** | kWh | Contínua ≥ 0 | Energia armazenada na bateria ao final da hora *t* |
| **Indicador Binário de Operação** | {0, 1} | Binária | Se 1, bateria está em descarga; se 0, em carga (Big-M linearization) |

**Notação em código:** `SOC[t]`, `y_bess[t]`

**Equação de Dinâmica SOC:**
```
SOC[t] = SOC[t-1] 
         + P_bess_charge[t] × eta_charge × delta_t 
         - P_bess_discharge[t] × delta_t / eta_discharge
```

---

## 9. SÉRIE HORÁRIA DE ENTRADA — DEMANDA E RECURSO

| Série | Unidade | Descrição | Fonte | Intervalo |
|-------|---------|-----------|--------|-----------|
| **Demanda de VE** | kW | `P_ev_load_kw[t]` | Perfil horário de potência demandada para recarga (inelástica) | 0–200+ |
| **Fator de Capacidade Solar** | Fração | `irradiance_cf[t]` | Perfil de irradiância normalizado (0 à noite, ~1.0 ao meio-dia) | 0.0–1.0 |
| **Tarifa Horária** | BRL/kWh | `grid_price[t]` | Preço de compra de eletricidade por hora (TOU: ponta, intermediário, fora de ponta) | 0.5–2.5 |

**Exemplo de padrão horário típico:**
- Horas 6–9: `irradiance_cf` sobe (0.0 → 0.5)
- Horas 9–14: `irradiance_cf` máximo (~0.9)
- Horas 14–18: `irradiance_cf` desce (0.5 → 0.0)
- Horas 18–6: `irradiance_cf` = 0.0 (noite)

---

## 10. PARÂMETROS DE DEMANDA — ELETROPOSTO RODOVIA (Calibração Dutra)

### 10.1 Recorte Empírico

| Parâmetro | Unidade | Valor | Descrição |
|-----------|---------|-------|-----------|
| **Chegadas Médias Diárias** | veículos/dia | 246 | Número médio de VE chegando ao eletroposto por dia |
| **Desvio Padrão Diário** | veículos/dia | 58 | Variabilidade dia a dia (σ) |
| **Percentil 90** | veículos/dia | 312 | Cenário de dia típico "pesado" |
| **Coeficiente de Variação** | Fração | 0.2358 | CV = σ / μ = 58 / 246 |
| **Energia Média por Sessão** | kWh | 31.80 | Quantidade demandada por sessão de recarga |
| **Participação Noturna** | % | 24.0 | Percentual de chegadas nas horas 22h–6h |
| **Janela de Observação** | período | 2025-01 a 2026-02 | Intervalo de coleta de dados |
| **Dias Observados** | dias | 182 | Total de dias com registro completo |

**Fonte:** Levantamento operacional do corredor Dutra

### 10.2 Parâmetros Derivados para Cenários

| Parâmetro | Unidade | Valor | Descrição |
|-----------|---------|-------|-----------|
| **Perturbação Estocástica Calibrada** | Fração | 0.2593 | Fator de variação usado em simulações Monte Carlo |
| **Ajuste Energético (Viagem Longa)** | kWh | 4.770 | Acréscimo de SOC inicial (rodovia vs. urbano) |

### 10.3 Projeção de Demanda Multi-Ano

| Ano | Chegadas Médias | Fator de Crescimento | Justificativa |
|-----|-----------------|---------------------|---------------|
| 2026 | 246 | 1.00 | Base empírica (observado) |
| 2030 | 310 | 1.26 | Crescimento da frota EV (~6% a.a.) |
| 2035 | 381 | 1.55 | Continuação da tendência |

**Fonte:** EPE (Plano Decenal 2035), ABVE (Relatório Anual), tendências regionais

---

## 11. VARIÁVEIS DE SIMULAÇÃO ESTOCÁSTICA — ELETROPOSTO VE

*[Quando simulacao_eletroposto_ve.py é usado em modo estocástico]*

### 11.1 Classes de Tecnologia de Veículos

| Atributo | Unidade | Descrição |
|----------|---------|-----------|
| `battery_kwh` | kWh | Capacidade da bateria do veículo |
| `ac_limit_kw` | kW | Potência máxima de carregador AC (monofásico/trifásico) |
| `dc_limit_kw` | kW | Potência máxima de carregador DC (recarga rápida) |
| `target_soc` | Fração | Estado de carga desejado ao fim da sessão |

**Exemplos brasileiros (2025–2026):**
- Chevrolet Bolt EV: ~66 kWh, AC=11 kW, DC=150 kW
- Volkswagen ID.4: ~62–82 kWh, AC=11 kW, DC=125 kW
- Tesla Model 3/Y: ~54–80 kWh, AC=11 kW, DC=250 kW
- BYD Song Plus DM-i: ~18.3 kWh, AC=6.6 kW, DC=30 kW

### 11.2 Classes de Tecnologia de Carregador

| Atributo | Unidade | Descrição |
|----------|---------|-----------|
| `power_kw` | kW | Potência nominal do carregador |
| `is_dc` | Booleano | 1 = carregador DC (rápido); 0 = carregador AC (lento) |

**Exemplos brasileiros:**
- Carregador AC trifásico: 11–22 kW
- Carregador DC (recarga rápida): 50–350 kW

### 11.3 Métricas de Desempenho (Output)

| Métrica | Unidade | Descrição |
|---------|---------|-----------|
| `total_arrivals` | veículos | Total de chegadas simuladas no horizonte |
| `served` | veículos | Número de chegadas com recarga completa |
| `total_energy_kwh` | kWh | Energia total entregue |
| `mean_wait_min` | min | Tempo médio de espera na fila |
| `p95_wait_min` | min | 95º percentil de tempo de espera |
| `peak_kw` | kW | Pico de demanda simultânea |
| `load_factor` | Fração | Razão entre demanda média e demanda máxima |
| `utilization` | Fração | Taxa de ocupação dos carregadores |

---

## 12. SÍMBOLOS E NOTAÇÕES MATEMÁTICAS

| Símbolo | Significado | Exemplo/Contexto |
|---------|-----------|------------------|
| **t** | Índice de período horário | t ∈ {1, 2, ..., 24} |
| **P** | Potência ativa | P_pv_gen, P_bess_charge [kW] |
| **E** | Energia | E_bess_cap, total_energy_kwh [kWh] |
| **η** (eta) | Eficiência | η_charge = 0.95 (95% eficaz) |
| **C** | Taxa (C-rate) | 1-C = descarga em 1 hora |
| **ΔT** ou **Δt** | Intervalo de tempo | delta_t = 1 h |
| **CF** | Fator de capacidade | irradiance_cf[t] ∈ [0, 1] |
| **SOC** | State of Charge (Estado de Carga) | SOC[t] em kWh ou fração |
| **CRF** | Capital Recovery Factor | Converte CAPEX em fluxo anual |
| **O&M** | Operation & Maintenance | Custos operacionais anuais |
| **CAPEX** | Capital Expenditure | Investimento inicial |
| **OPEX** | Operational Expenditure | Custos operacionais |
| **μ** (mu) | Média | Ex: 246 chegadas/dia |
| **σ** (sigma) | Desvio padrão | Ex: 58 chegadas/dia |
| **CV** | Coeficiente de Variação | CV = σ/μ = 0.2358 |
| **TOU** | Time-of-Use | Tarifa por período (ponta, inter, fora) |
| **MILP/MIP** | Mixed Integer Linear Programming | Tipo de problema de otimização |
| **Big-M** | Técnica de linearização | Converte lógica disjuntiva em linear |

---

## 13. CONVENÇÕES DE ARQUIVO DE DADOS (.dat)

Arquivos de entrada no formato Pyomo `.dat` seguem estrutura declarativa:

```
# Parâmetros escalares
param delta_t := 1.0 ;
param tariff_ev := 2.50 ;  # BRL/kWh
param operational_days_equivalent := 365 ;

# Séries horárias (exemplo para 3 horas)
param irradiance_cf :=
  1   0.00
  2   0.10
  3   0.25
;

param grid_price :=
  1   1.20
  2   1.15
  3   1.10
;

# Capacidades máximas
param P_pv_cap_max := 1000 ;  # kW
param E_bess_cap_max := 2000 ;  # kWh
```

---

## 14. REFERÊNCIAS DE CALIBRAÇÃO

### Energia e Recursos Solares
- **CRESESB:** Atlas Solarimétrico do Brasil (http://www.cresesb.cepel.br/)
- **INPE/CPTEC:** Dados de irradiância e previsão solar
- **ONS/EPE:** Série histórica de geração renovável e oferta de energia

### Custos e Economicidade
- **IRENA:** "Renewable Power Generation Costs in 2024" (https://www.irena.org/)
- **NREL:** Annual Technology Baseline (ATB) e SAM (System Advisor Model)
- **EPE:** Plano Decenal de Expansão de Energia 2035 — Caderno de Eletromobilidade

### Regulação e Tarifação (Brasil)
- **ANEEL:** Banco de Tarifas e Estruturas de Compensação Fixa (http://www2.aneel.gov.br/)
- **MME:** Sinal Horário e Tarifa Branca
- **Concessionárias:** EDP Brasil, Light, Cemig (dados operacionais públicos)

### Veículos Elétricos e Mobilidade
- **ABVE:** Associação Brasileira do Veículo Elétrico — Relatório Anual
- **Xi et al. (2013):** "Simulation-optimization model for a station-level electric vehicle charging infrastructure operation problem" — Transportation Research Part D, 22, 60–69.
- **Zhao et al. (2016):** "A review of electric vehicle charging station capacity planning..." — IEEE Access, 4, 8635–8648.

---

## 15. GLOSSÁRIO RÁPIDO

| Termo | Significado | Contexto |
|-------|-----------|---------|
| **Eletroposto** | Estação de carregamento de VE | Localização: rodovia, estacionamento, comercial |
| **Microrrede** | Rede local integrada com geração distribuída (PV), armazenamento (BESS) e carga | Modelo AbstractModel do repositório |
| **Recarga Rápida** | Carregamento DC de alta potência (50–350 kW) | ~30 min para 80% SOC |
| **Recarga Lenta** | Carregamento AC de menor potência (11–22 kW) | 4–8 horas para carga completa |
| **SOC (State of Charge)** | Nível de carga da bateria, expresso em kWh ou % | Range operacional: 20%–90% em geral |
| **C-rate** | Taxa de carga/descarga da bateria em relação à capacidade | 1-C = 1 h; 2-C = 30 min |
| **Fator de Capacidade** | Razão entre geração real e capacidade nominal | PV Brasil: 15–20% anual; 0–90% horário |
| **Arbitragem Temporal** | Compra de energia barata, armazenamento e venda em período mais caro | Função do BESS + sinal TOU |
| **TOU (Time-of-Use)** | Tarifação que varia por período do dia | Ponta (mais cara), intermediário, fora de ponta |
| **CRF (Capital Recovery Factor)** | Fator que converte CAPEX em parcelas anuais equivalentes | CRF = [r(1+r)^n] / [(1+r)^n–1], onde r=taxa de juros, n=anos |
| **Big-M** | Técnica de linearização usando variável binária e constante grande | Força exclusividade: carga OU descarga |
| **MILP** | Mixed Integer Linear Programming | Tipo de problema de otimização com variáveis inteiras e contínuas |

---

## 16. ESTRUTURA DE DIRETÓRIOS ASSOCIADOS

```
c:\Users\letic\OneDrive\FAPESP PROJETO\4- Versão Guilherme\Teste\
├── main.py                          (script principal de otimização Pyomo)
├── simulacao_eletroposto_ve.py      (simulação estocástica de carregamento)
├── referencias_parametros_dutra.md  (fontes de calibração)
├── hipoteses_metodologia_calibracao_dutra.md  (metodologia)
├── recorte_empirico_dutra.json      (dados empíricos do corredor Dutra)
├── requirements.txt                 (dependências Python)
├── DICIONARIO_REPOSITORIO.md        (este arquivo)
├── figuras_saida/                   (gráficos de saída: PNG)
│   ├── analise_grafica.html
│   └── [outros gráficos]
├── CALIBRAÇÃO BRASIL/               (validação contra mercado/MMMs)
│   ├── validacao_eletroposto_brasil_sem_viz.py
│   ├── RELATORIO_CONSOLIDADO_COMPLETO_ELETROPOSTO_BRASIL.md
│   └── [outros arquivos]
├── saida_fronteira_viabilidade/     (análise de sensibilidade)
│   ├── fronteira_viabilidade.csv
│   ├── sensibilidade_resultados.csv
│   └── graficos/
└── [outros arquivos de entrada/saída]
```

---

**Última atualização:** 1 de maio de 2026  
**Responsável:** Análise de Microrrede de Eletroposto — Projeto FAPESP
