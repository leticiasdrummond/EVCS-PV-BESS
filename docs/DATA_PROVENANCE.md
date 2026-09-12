# Proveniência dos dados e auditoria de nomenclatura

**Projeto:** Alternativas de Fornecimento de Energia para Eletropostos — microrredes em rodovias de grande tráfego  
**Repositório:** `EVCS-PV-BESS`  
**Objetivo:** estabelecer um padrão mínimo para identificar a origem, natureza, transformação e versão de cada dado/parâmetro utilizado em estudos computacionais.

## 1. Princípio de proveniência

Nenhum valor utilizado em resultado científico deve ser apresentado apenas como "dado de entrada". Deve ser possível distinguir:

- **Dado observado:** obtido de medição, levantamento operacional ou base institucional.
- **Dado secundário:** extraído de publicação, relatório técnico, norma ou base pública.
- **Hipótese econômica:** valor adotado para representar uma condição de mercado ou modelo de negócio, sem alegação de que seja preço observado.
- **Perfil sintético:** série construída matematicamente a partir de estatísticas, padrões horários ou hipóteses.
- **Parâmetro de modelagem:** valor definido para fechar a formulação ou controlar o experimento numérico.
- **Valor derivado:** calculado a partir de outros dados, com fórmula ou transformação documentada.

Essas categorias não devem ser tratadas como equivalentes. Em particular, um perfil sintético calibrado com dados observados continua sendo um **perfil sintético**, e não uma medição.

## 2. Registro mínimo por parâmetro

Cada entrada que possa afetar um resultado deve possuir, preferencialmente em uma tabela versionada, os seguintes campos:

| Campo | Conteúdo |
|---|---|
| `parameter_id` | identificador estável do parâmetro |
| `nome_codigo` | nome exato utilizado no código |
| `nome_cientifico` | nomenclatura usada na dissertação |
| `unidade` | unidade física/econômica |
| `valor` | valor ou referência à série |
| `tipo_proveniencia` | observado / secundário / hipótese / sintético / modelagem / derivado |
| `fonte` | instituição, artigo, relatório ou conjunto de dados |
| `referencia` | DOI, URL, documento ou identificador interno, quando aplicável |
| `localizacao_original` | arquivo, tabela, página, variável ou caminho de origem |
| `transformacao` | cálculo, normalização, agregação ou conversão aplicada |
| `data_coleta` | data de obtenção |
| `data_acesso` | data de acesso quando aplicável |
| `versao_fonte` | versão, edição, período ou commit da fonte |
| `arquivo_entrada` | instância `.dat`, CSV ou outro arquivo usado pelo modelo |
| `commit_modelo` | commit do código que utilizou o valor |
| `status` | histórico / em validação / validado / reproduzível / descartado |
| `observacao` | limitações, ressalvas e decisões metodológicas |

## 3. Regra específica para séries temporais

Para `P_ev_load_kw[t]`, `irradiance_cf[t]` e `grid_price[t]`, registrar separadamente:

1. origem da série bruta;
2. período de observação;
3. resolução temporal original;
4. tratamento de dados ausentes/outliers;
5. agregação ou interpolação;
6. normalização, se houver;
7. unidade antes e depois da transformação;
8. método de construção do perfil representativo;
9. parâmetros estatísticos usados;
10. arquivo final efetivamente consumido pelo modelo.

Um perfil de demanda construído a partir de estatísticas de tráfego deve ser denominado, por exemplo, `perfil_sintetico_demanda_calibrado`, e não `demanda_real`, salvo quando cada observação corresponder efetivamente ao período modelado.

## 4. Nomenclatura recomendada

### 4.1 PV

Preferir **fator de disponibilidade fotovoltaica** (`irradiance_cf[t]`) quando a série representa apenas a fração disponível da capacidade instalada. Evitar chamar automaticamente essa variável de "irradiância" em W/m², pois no modelo ela é adimensional.

### 4.2 Demanda de recarga

`P_ev_load_kw[t]` deve ser descrita como **potência elétrica demandada pelo serviço de recarga no intervalo t** quando for uma carga agregada inelástica. Não confundir com fluxo de veículos, número de sessões ou energia por sessão.

### 4.3 Tarifa e preço de venda

`grid_price[t]`: **preço/custo unitário da energia importada da rede**, deixando explícito se representa tarifa regulada, componente tarifário, preço efetivo modelado ou composição econômica.  
`tariff_ev`: **preço de venda do serviço de recarga ao usuário final**, caso seja uma hipótese econômica do modelo. Não denominar esse valor simplesmente de "tarifa de energia" se ele inclui serviço, margem ou outros componentes.

### 4.4 BESS

`SOC[t]` deve indicar claramente se representa energia armazenada (kWh) ou estado de carga normalizado (% ou fração). No modelo atual, a variável é declarada em kWh; portanto, **estado de energia armazenada** pode ser mais preciso que "SOC" em sentido estrito. Se a nomenclatura SOC for mantida por aderência à literatura, registrar essa convenção explicitamente.

### 4.5 Transformador

`P_trafo_cap` é capacidade de potência da interface/transformador em kW no modelo. Quando o equipamento real for especificado em kVA, não misturar kW e kVA sem documentar fator de potência e critério de conversão.

### 4.6 Load shedding

`LoadShedding[t]` deve ser denominado **corte de carga não atendida** ou **potência de carga não suprida**. Se a restrição força essa variável a zero, isso deve ser apresentado como requisito de continuidade imposto pelo modelo, e não como indicador de confiabilidade empiricamente medido.

## 5. Valores econômicos e técnicos ainda não validados

Intervalos genéricos de mercado presentes em dicionários de parâmetros não devem ser citados na dissertação como "valores típicos do Brasil" sem fonte identificável e data de referência. Quando um valor é apenas uma premissa para teste, classificá-lo como **hipótese econômica** ou **parâmetro de modelagem**.

Exemplo de distinção:

- `capex_pv_kw = X`: hipótese/valor secundário somente se houver fonte identificada, unidade, data e escopo.
- `tariff_ev = X`: hipótese econômica se não representar preço observado de um CPO específico.
- `irradiance_cf[t]`: perfil sintético se construído matematicamente.
- `P_ev_load_kw[t]`: dado observado somente se derivado diretamente de registros de operação; caso contrário, perfil sintético calibrado.

## 6. Regra de versionamento

Toda alteração que possa modificar resultados deve ser feita em branch própria e registrada por commit. O resultado final deve apontar para:

`fonte -> transformação -> arquivo de entrada -> commit do código -> configuração do solver -> execução -> resultado -> figura/tabela -> seção da dissertação`.

Não substituir arquivos históricos silenciosamente. Quando um dado for corrigido ou substituído, preservar a versão anterior ou registrar seu identificador/commit e a justificativa da mudança.

## 7. Critério para uso na dissertação

Um resultado deve ser considerado **apto para sustentar uma afirmação quantitativa da dissertação** somente depois de verificados, no mínimo:

- proveniência dos dados;
- unidade e definição da variável;
- transformação aplicada;
- consistência com a formulação;
- arquivo de entrada versionado;
- commit do código;
- versão/configuração do solver;
- execução reproduzível;
- coerência dimensional e econômica;
- interpretação compatível com o tipo de dado.

## 8. Auditoria pendente

Antes de consolidar os resultados do mestrado, auditar especialmente:

1. parâmetros econômicos do `dados_exemplo.dat` e das demais instâncias;
2. origem efetiva da curva `irradiance_cf[t]`;
3. origem e natureza de `P_ev_load_kw[t]`;
4. distinção entre tarifa regulada, custo de energia e preço de recarga;
5. custos de PV, BESS e transformador e sua data-base;
6. CRF e O&M, verificando se são derivados de premissas financeiras explícitas;
7. coerência entre potência do transformador, demanda e eventual fator de potência;
8. tratamento do requisito de continuidade e da variável `LoadShedding`;
9. relação entre dados Dutra/Scania e perfis efetivamente usados nas simulações;
10. correspondência entre resultados históricos de outros repositórios e a versão central reproduzível.

## 9. Regra de redação científica

Não usar expressões como "dado real", "valor de mercado", "valor típico", "tarifa vigente" ou "perfil real" sem evidência documental suficiente. Preferir formulações que revelem a proveniência: **dado observado**, **dado secundário**, **hipótese econômica**, **perfil sintético calibrado**, **parâmetro de modelagem** ou **valor derivado**.
