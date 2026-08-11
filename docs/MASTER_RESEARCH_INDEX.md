# Índice Mestre — Projeto de Mestrado: Eletropostos, Microrredes e Otimização

Este documento consolida, por rastreabilidade, os repositórios de `leticiasdrummond` identificados como diretamente ou potencialmente relacionados ao desenvolvimento do projeto de mestrado. A consolidação preserva a origem de cada artefato: os repositórios originais não são apagados nem substituídos.

## 1. Repositório central

- `EVCS-PV-BESS` — modelo MILP/Pyomo para EVCS + PV + BESS + rede/transformador; código funcional, instâncias, dicionários, notebook e protocolo de rastreabilidade.
- https://github.com/leticiasdrummond/EVCS-PV-BESS

## 2. Repositórios diretamente relacionados ao modelo de eletroposto

### 2.1 `Modelo-de-Eletroposto---Casos-Base`

Repositório privado identificado como diretamente relacionado à modelagem e documentação do eletroposto.

Conteúdos identificados:

- `Otimizacao.tex` — formulação/documentação de otimização;
- `Modelagem_pepilane.tex` — modelagem matemática;
- `Caso_2_MIN_Pgrid_t.tex` — rascunho de formulação;
- `Notas_reuniao.tex` — registro de desenvolvimento;
- `Atividade2_Economia_de_Energia.ipynb`;
- `Anexo 1 - Relatório Q.2.pdf`;
- `main.tex`;
- template de dissertação/trabalho acadêmico da UNICAMP.

Origem: https://github.com/leticiasdrummond/Modelo-de-Eletroposto---Casos-Base

### 2.2 `cenariosEVCS`

Repositório de cenários, subprogramas, relatórios e resultados de simulações.

Conteúdos relevantes identificados:

- `2_3subprogramas.py`;
- `2.2 MAPA_SUBPROGRAMAS.md`;
- `2.README_subprogramas.md`;
- cenários de rede pura;
- cenários com transformador + PV + BESS;
- cenários com e sem exportação;
- relatórios textuais;
- arquivos `resultados.json`;
- figuras de simulação.

Origem: https://github.com/leticiasdrummond/cenariosEVCS

### 2.3 `Artigo-renov-veis-bess-eletroposto`

Repositório associado ao desenvolvimento científico, análise econômica e resultados para integração de renováveis/BESS/eletropostos.

Conteúdos identificados:

- notebooks de otimização;
- análise econômica;
- análise de usinas GN/PV;
- configuração IEEE;
- dados de carregadores;
- séries temporais de solução;
- fluxo da rede;
- SOC;
- operação;
- arquivos CSV de resultados.

Origem: https://github.com/leticiasdrummond/Artigo-renov-veis-bess-eletroposto

### 2.4 `Testes-de-Simula-es--Artigo`

Repositório identificado como parte do conjunto de testes de simulação utilizado no desenvolvimento do artigo/modelo.

Origem: https://github.com/leticiasdrummond/Testes-de-Simula-es--Artigo

## 3. Repositórios de apoio à modelagem/otimização

### 3.1 `Gurobi`

Repositório de apoio relacionado ao solver Gurobi e experimentos/integrações de otimização.

Origem: https://github.com/leticiasdrummond/Gurobi

### 3.2 `PyPSA`

Repositório associado ao estudo/uso da plataforma PyPSA para sistemas de energia.

Origem: https://github.com/leticiasdrummond/PyPSA

### 3.3 `Gurobi_Exemple_Events`

Repositório de exemplos de eventos/uso do Gurobi.

Origem: https://github.com/leticiasdrummond/Gurobi_Exemple_Events

### 3.4 `https-github.com-ampl-colab.ampl.com`

Repositório associado a experimentação/documentação com AMPL/Colab, potencialmente relevante para histórico de métodos de otimização.

Origem: https://github.com/leticiasdrummond/https-github.com-ampl-colab.ampl.com

## 4. Repositórios de apoio acadêmico/dados

### 4.1 `epe4md`

Repositório relacionado ao material EPE utilizado no contexto acadêmico e de pesquisa.

Origem: https://github.com/leticiasdrummond/epe4md

### 4.2 `Modelos-Base`

Repositório de modelos-base. Deve ser mantido como fonte histórica e auditado antes de qualquer classificação definitiva como parte do modelo principal.

Origem: https://github.com/leticiasdrummond/Modelos-Base

### 4.3 `Notebooks_IT306`

Coleção de notebooks acadêmicos. Deve ser pesquisada por termos e dependências antes de incorporar qualquer conteúdo ao modelo principal.

Origem: https://github.com/leticiasdrummond/Notebooks_IT306

## 5. Repositórios não incorporados automaticamente ao modelo principal

`Terada`, `Mario-Levorato-Rosa-Figueiredo-Yuri-Frota`, `teste1` e outros repositórios pessoais não foram classificados automaticamente como parte do mestrado apenas pelo nome. A ausência nesta seção de classificação principal não significa que sejam irrelevantes; significa apenas que não há evidência suficiente, nesta etapa, para misturar seu conteúdo ao modelo científico.

## 6. Regra de incorporação

O repositório central `EVCS-PV-BESS` deve funcionar como índice e, progressivamente, como arquivo de reprodução. Para cada artefato incorporado, registrar:

1. repositório de origem;
2. caminho original;
3. commit/branch de origem;
4. data de coleta;
5. função no projeto;
6. relação com a formulação;
7. relação com uma instância de entrada;
8. resultado produzido, quando houver;
9. status: `histórico`, `validado`, `reproduzível` ou `descartado`.

## 7. Regra científica

Nenhum resultado histórico deve ser sobrescrito silenciosamente. Se uma nova versão do modelo reproduzir ou modificar um resultado antigo, ambos devem permanecer identificáveis, com a diferença documentada.

## 8. Cadeia de rastreabilidade

`referência/hipótese -> parâmetro -> instância -> formulação -> código -> commit -> execução -> resultado -> figura/tabela -> seção da dissertação`.

Esta estrutura permite que os repositórios originais continuem sendo a fonte histórica, enquanto `EVCS-PV-BESS` passa a funcionar como ponto de entrada organizado para a reprodução do projeto.
