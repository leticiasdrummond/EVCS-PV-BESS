# EVCS-PV-BESS
**Microrrede Eletroposto — Otimização (Pyomo + Gurobi)**

Este repositório contém um modelo Pyomo (AbstractModel) para otimização de uma microrrede de eletroposto em rodovia (PV + BESS + transformador) com horizonte diário representativo. O script principal resolve um MILP/MIP, gera um relatório técnico-econômico e salva figuras de despacho.

**Principais arquivos**
- [main.py](main.py): fluxo principal — cria instância a partir de um arquivo `.dat`, resolve com Gurobi, gera relatório e figuras.
- [requirements.txt](requirements.txt): lista de dependências Python recomendadas.
- [dados_exemplo.dat](dados_exemplo.dat): (esperado) arquivo de dados em formato Pyomo `.dat` usado por `main.py`.
- [relatorio_saida.txt](relatorio_saida.txt): arquivo de saída textual gerado pelo script.
- [figuras_saida](figuras_saida/): diretório onde os PNGs são salvos por `main.py`.

**O que o script faz**
- Constrói um modelo Pyomo que otimiza capacidades de PV (kW), BESS (kWh) e transformador (kW) e o despacho horário para atender demanda de recarga de veículos elétricos.
- Objetivo: maximizar lucro operacional anualizado menos custos de investimento (opção entre CAPEX único ou CAPEX anualizado via CRF + O&M).
- Gera `relatorio_saida.txt` com capacidades otimizadas, métricas financeiras e despacho horário.
- Gera figuras (PNG) no diretório `figuras_saida/` com séries temporais (demanda EV, tarifa, geração PV, SOC, etc.).

## Requisitos
A instalação recomendada é um ambiente Python isolado (por exemplo, conda) com as dependências listadas em [requirements.txt](requirements.txt). Principais pacotes:

- `pyomo` (>=6.10.0)
- `gurobipy` (>=13.0.1) — requer Gurobi instalado e licença válida
- `numpy`, `pandas`, `matplotlib`, `pypsa`, `requests`

Instalação rápida (exemplo com conda):

```bash
conda create -n pyomoenv python=3.10 -y
conda activate pyomoenv
python -m pip install -r requirements.txt
```

Observações sobre Gurobi:
- `gurobipy` exige instalação do Gurobi e licença configurada no sistema. No Windows verifique o executável `gurobi_cl.exe` ou a integração com `gurobipy`.
- Se não tiver Gurobi, você pode adaptar `main.py` para outro solver suportado pelo Pyomo (ex.: CBC, GLPK), mas será necessário alterar `SolverFactory("gurobi")` no código.

## Entradas e argumentos
- `main.py` não espera argumentos de linha de comando por padrão: ele procura por `[dados_exemplo.dat](dados_exemplo.dat)` no diretório do script. Para usar outro arquivo de dados, edite `main.py` (variável `data_file`) ou importe/execute as funções no seu workflow.
- Formato do arquivo de entrada: Pyomo `.dat` legível por `model.create_instance(str(data_file))`.

## Como executar
1. Ative o ambiente Python com as dependências instaladas (ver seção `Requisitos`).
2. Coloque o arquivo de dados (`dados_exemplo.dat`) no mesmo diretório de `main.py` ou ajuste o caminho em `main.py`.
3. Execute:

```bash
conda activate pyomoenv
python main.py
```

Saídas esperadas (após execução sem erros):
- `relatorio_saida.txt` — relatório textual com resultados.
- `figuras_saida/` — PNGs de perfil de demanda, tarifa, recurso solar, estado da bateria e fluxo energético.

## Erros comuns e dicas
- Erro: "Solver Gurobi indisponivel via 'gurobi'" — verifique instalação/licença do Gurobi ou modifique `main.py` para usar um solver disponível.
- Se ocorrerem falhas de importação de binários (por ex. `numpy`), reinstale os pacotes no mesmo ambiente Python ativo.
- Para rodar em batch/CI, assegure que `gurobipy` esteja instalado no ambiente do runner e que a licença permita execução não interativa.

## Origem e referências 
- Este programa foi baseado no artigo "Simultaneous capacity configuration and scheduling optimization of an integrated electrical vehicle charging station with photovoltaic and battery energy storage system"

---

