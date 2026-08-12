# Índice Mestre — Projeto de Mestrado: Eletropostos, Microrredes, MILP e Modelos de Negócio

Atualizado em 12/08/2026.

Este documento consolida, por rastreabilidade, os repositórios de `leticiasdrummond` identificados no GitHub como diretamente, potencialmente ou metodologicamente relacionados ao desenvolvimento do projeto de mestrado. Os repositórios originais permanecem como fontes históricas; não devem ser apagados nem sobrescritos silenciosamente.

## 1. Repositório central de reprodutibilidade

### `EVCS-PV-BESS`

Modelo central de otimização para EVCS/eletroposto com PV+BESS+rede/transformador. Deve funcionar progressivamente como ponto de entrada da pesquisa, preservando formulação, código, instâncias, resultados e documentação.

https://github.com/leticiasdrummond/EVCS-PV-BESS

## 2. Repositórios diretamente relacionados ao modelo de eletroposto

### `Modelo-de-Eletroposto---Casos-Base`

Repositório privado diretamente relacionado à formulação e documentação do eletroposto.

Conteúdos identificados anteriormente:

- `Otimizacao.tex` — formulação/documentação de otimização;
- `Modelagem_pepilane.tex` — modelagem matemática;
- `Caso_2_MIN_Pgrid_t.tex` — formulação de caso;
- `Notas_reuniao.tex` — registro de desenvolvimento;
- `Atividade2_Economia_de_Energia.ipynb`;
- `Anexo 1 - Relatório Q.2.pdf`;
- `main.tex`;
- template acadêmico UNICAMP.

https://github.com/leticiasdrummond/Modelo-de-Eletroposto---Casos-Base

### `cenariosEVCS`

Repositório experimental de cenários, subprogramas, relatórios e resultados.

Conteúdos relevantes:

- `2_3subprogramas.py`;
- mapas e READMEs de subprogramas;
- cenários de rede pura;
- cenários com transformador + PV + BESS;
- cenários com e sem exportação;
- relatórios textuais;
- `resultados.json`;
- figuras de simulação.

https://github.com/leticiasdrummond/cenariosEVCS

### `Artigo-renov-veis-bess-eletroposto`

Repositório associado ao desenvolvimento científico, análise econômica e resultados de integração de renováveis/BESS/eletropostos.

Conteúdos identificados:

- notebooks de otimização;
- análise econômica;
- estudo GN/PV;
- configuração IEEE;
- dados de carregadores;
- séries temporais;
- fluxo da rede;
- SOC;
- operação;
- CSVs de resultados.

https://github.com/leticiasdrummond/Artigo-renov-veis-bess-eletroposto

### `Testes-de-Simula-es--Artigo`

Repositório de testes de simulação associado ao desenvolvimento do artigo/modelo.

https://github.com/leticiasdrummond/Testes-de-Simula-es--Artigo

## 3. Novo repositório identificado — modelos de negócio e MILP

### `modelos-de-neg-cio-com-problema-milp`

Repositório privado identificado no inventário atualizado do GitHub em 12/08/2026. Pelo próprio nome e pelo contexto do projeto, deve ser tratado como candidato prioritário para auditoria e incorporação histórica, pois conecta duas dimensões que se tornaram centrais na dissertação: **modelos de negócio** e **problemas MILP**.

https://github.com/leticiasdrummond/modelos-de-neg-cio-com-problema-milp

Status atual: `identificado — ainda não auditado em profundidade`.

Próxima ação: inventariar arquivos, formulações, instâncias, notebooks, resultados e commits; identificar quais elementos pertencem ao problema de eletropostos/microrredes e quais são apenas exercícios/metodologia.

## 4. Repositórios de apoio à modelagem/otimização

### `Gurobi`

Repositório de apoio relacionado ao solver Gurobi e experimentos de otimização.

https://github.com/leticiasdrummond/Gurobi

### `PyPSA`

Repositório associado ao estudo/uso de PyPSA em sistemas de energia.

https://github.com/leticiasdrummond/PyPSA

### `Gurobi_Exemple_Events`

Repositório de exemplos/experimentação com Gurobi.

https://github.com/leticiasdrummond/Gurobi_Exemple_Events

### `https-github.com-ampl-colab.ampl.com`

Repositório associado à experimentação/documentação AMPL/Colab, potencialmente relevante para o histórico metodológico de otimização.

https://github.com/leticiasdrummond/https-github.com-ampl-colab.ampl.com

## 5. Repositórios de apoio acadêmico/dados

### `epe4md`

Material relacionado à EPE utilizado no contexto acadêmico/pesquisa.

https://github.com/leticiasdrummond/epe4md

### `Modelos-Base`

Repositório de modelos-base. Deve ser auditado antes de classificar conteúdos específicos como parte do modelo principal.

https://github.com/leticiasdrummond/Modelos-Base

### `Notebooks_IT306`

Coleção de notebooks acadêmicos. Deve ser pesquisada por termos, dependências e histórico antes de incorporar conteúdo ao modelo principal.

https://github.com/leticiasdrummond/Notebooks_IT306

## 6. Repositórios identificados, mas sem evidência suficiente para classificação como parte do mestrado

- `Terada`
- `Mario-Levorato-Rosa-Figueiredo-Yuri-Frota`
- `teste1`
- `REGISTROS`

A presença nesta categoria não significa irrelevância; significa apenas que o nome/metadado disponível não é evidência suficiente para misturar seu conteúdo ao acervo científico do mestrado.

## 7. Inventário atual do GitHub

A conta `leticiasdrummond` apresentou, na atualização de 12/08/2026, os seguintes repositórios acessíveis: `teste1`, `epe4md`, `Notebooks_IT306`, `Gurobi_Exemple_Events`, `Terada`, `Modelos-Base`, `Mario-Levorato-Rosa-Figueiredo-Yuri-Frota`, `REGISTROS`, `Gurobi`, `https-github.com-ampl-colab.ampl.com`, `PyPSA`, `Testes-de-Simula-es--Artigo`, `EVCS-PV-BESS`, `cenariosEVCS`, `Modelo-de-Eletroposto---Casos-Base`, `Artigo-renov-veis-bess-eletroposto` e `modelos-de-neg-cio-com-problema-milp`.

A classificação temática acima é deliberadamente mais restritiva que o inventário total.

## 8. Regra de incorporação

Para cada artefato que for efetivamente incorporado ao acervo central, registrar:

1. repositório de origem;
2. caminho original;
3. commit/branch de origem;
4. data de coleta;
5. função no projeto;
6. relação com a formulação;
7. relação com uma instância de entrada;
8. resultado produzido, quando houver;
9. status: `histórico`, `validado`, `reproduzível` ou `descartado`.

## 9. Regra científica

Nenhum resultado histórico deve ser sobrescrito silenciosamente. Se uma nova versão do modelo reproduzir, corrigir ou modificar um resultado antigo, ambas as versões devem permanecer identificáveis, com a diferença documentada.

## 10. Cadeia de rastreabilidade

`referência/hipótese -> parâmetro -> instância -> formulação -> código -> commit -> execução -> resultado -> figura/tabela -> seção da dissertação`.

O objetivo é transformar o GitHub em um **registro científico reprodutível da evolução do mestrado**, e não apenas em um depósito de códigos.
