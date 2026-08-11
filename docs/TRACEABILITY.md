# Rastreabilidade científica do modelo

## Cadeia de reprodução

Fonte/hipótese -> instância de entrada -> formulação matemática -> código -> commit -> execução -> resultado -> interpretação.

## Artefatos principais

- `main.py`: implementação Pyomo do modelo de microrrede PV+BESS+rede+transformador.
- `dados_exemplo.dat`: instância de entrada de 24 h preservada em `instances/`.
- `DictionaryMAIN.md` e `DICIONARIO_REPOSITORIO.md`: documentação de parâmetros/variáveis.
- `results/`: resultados e estrutura para vinculação entre entrada, execução e saída.

## Formulação documentada no código

O modelo contém decisões de investimento para `P_pv_cap`, `E_bess_cap` e `P_trafo_cap` e decisões horárias para geração PV, importação/exportação da rede, carga/descarga do BESS, SOC, load shedding e estado binário do BESS.

As principais restrições documentadas incluem disponibilidade FV, limites do transformador, potência do BESS, capacidade máxima, não simultaneidade carga/descarga, dinâmica do SOC, condição terminal e balanço energético.

## Regra de versionamento

Cada resultado utilizado na dissertação deverá indicar:

1. commit do código;
2. arquivo de entrada;
3. parâmetros econômicos e técnicos;
4. solver e versão;
5. status/critério de terminação;
6. arquivo de saída;
7. figuras geradas;
8. data da execução;
9. interpretação utilizada no texto científico.

## Observação sobre resultados históricos

Resultados encontrados em outros repositórios, notebooks ou chats devem ser tratados como evidência histórica até serem reproduzidos pela versão controlada do modelo. Não substituir resultados históricos sem registrar a razão da alteração.
