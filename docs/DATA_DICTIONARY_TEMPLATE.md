# Registro de parâmetros e dados — modelo de proveniência

Use esta tabela como registro mestre. Uma linha corresponde a um parâmetro, série ou dado derivado que possa influenciar uma execução.

| ID | Nome no código | Nome científico | Unidade | Valor/arquivo | Proveniência | Fonte | Referência/DOI/URL | Localização na fonte | Transformação | Data | Versão fonte | Instância | Commit | Status | Observação |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `PV-001` | `irradiance_cf[t]` | Fator de disponibilidade FV | frac | — | sintético / a validar | — | — | — | — | — | — | — | — | em validação | Não chamar de irradiância em W/m² sem conversão documentada. |
| `LOAD-001` | `P_ev_load_kw[t]` | Potência de demanda de recarga | kW | — | sintético calibrado / a validar | — | — | — | — | — | — | — | — | em validação | Separar fluxo de veículos, sessões e potência. |
| `GRID-001` | `grid_price[t]` | Custo unitário da energia importada | BRL/kWh | — | secundário / hipótese | — | — | — | — | — | — | — | — | em validação | Identificar se é tarifa regulada, componente tarifário ou preço modelado. |
| `EV-001` | `tariff_ev` | Preço de venda do serviço de recarga | BRL/kWh | — | hipótese econômica / observado | — | — | — | — | — | — | — | — | em validação | Não tratar como tarifa regulada sem evidência. |
| `BESS-001` | `eta_charge` | Eficiência de carga do BESS | frac | — | secundário / hipótese | — | — | — | — | — | — | — | — | em validação | Registrar se é eficiência do conjunto ou de componente. |
| `BESS-002` | `eta_discharge` | Eficiência de descarga do BESS | frac | — | secundário / hipótese | — | — | — | — | — | — | — | — | em validação | Registrar escopo físico. |
| `CAPEX-001` | `capex_pv_kw` | Custo de investimento FV | BRL/kW | — | secundário / hipótese | — | — | — | — | — | — | — | — | em validação | Informar data-base e escopo do CAPEX. |
| `CAPEX-002` | `capex_bess_kwh` | Custo de investimento BESS | BRL/kWh | — | secundário / hipótese | — | — | — | — | — | — | — | — | em validação | Informar se inclui PCS, instalação, integração etc. |
| `CAPEX-003` | `capex_trafo_kw` | Custo da interface/transformador | BRL/kW | — | secundário / hipótese | — | — | — | — | — | — | — | — | em validação | Verificar unidade original, frequentemente kVA. |
| `FIN-001` | `crf_pv` | Fator de recuperação de capital FV | 1/ano | — | derivado | — | — | — | fórmula documentada | — | — | — | — | em validação | Registrar vida útil e taxa de desconto. |
| `FIN-002` | `crf_bess` | Fator de recuperação de capital BESS | 1/ano | — | derivado | — | — | — | fórmula documentada | — | — | — | — | em validação | Registrar vida útil compatível com a hipótese de substituição. |
| `FIN-003` | `crf_trafo` | Fator de recuperação de capital do transformador | 1/ano | — | derivado | — | — | — | fórmula documentada | — | — | — | — | em validação | Registrar vida útil e taxa de desconto. |
