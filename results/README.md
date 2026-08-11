# Resultados e rastreabilidade das simulações

Este diretório deve preservar resultados gerados por execuções do modelo, sempre vinculados a uma instância de entrada e à versão do código utilizada.

## Estrutura recomendada

- `YYYY-MM-DD_<cenario>/input/` — cópia exata da instância `.dat` utilizada.
- `YYYY-MM-DD_<cenario>/output/relatorio_saida.txt` — saída textual do solver/modelo.
- `YYYY-MM-DD_<cenario>/figures/` — figuras geradas automaticamente.
- `YYYY-MM-DD_<cenario>/metadata.md` — solver, versão do Python/Pyomo/Gurobi, commit do código, parâmetros e observações.

## Resultado já rastreado no histórico do projeto

Uma execução preservada no repositório `cenariosEVCS` em `CAPEX SIMPLES e sem exportação/v1_2026-05-12/relatorio_microrrede.txt` registrou:

- PV: 118,18 kW
- BESS: 23,42 kWh
- Transformador: 116,00 kW
- Receita anual com recarga: R$ 1.132.960,00
- Custo anual de importação: R$ 251.206,25
- Lucro operacional anual: R$ 881.753,75
- CAPEX: R$ 274.209,23
- Função objetivo: R$ 607.544,52
- Resíduo máximo do balanço energético: 0 kW
- Horas com importação no limite do transformador: 3
- Sobreposição carga/descarga do BESS: 0 kW

Este registro é evidência histórica e não deve ser tratado automaticamente como resultado definitivo da dissertação sem identificar a instância, versão do modelo e hipóteses correspondentes.
