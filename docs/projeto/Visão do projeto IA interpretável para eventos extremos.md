# Visão do projeto: IA interpretável para eventos extremos

Oct 20, 2026 · @Pedro

## A ideia

Uma ferramenta aberta, escrita por você, que ajuda pesquisadores a estudar **eventos extremos** em séries e padrões físicos com IA interpretável, de forma reprodutível e testada. É um projeto à parte do mestrado: colabora com ele, mas não é o centro dele, e vira portfólio de software útil para a carreira.

O repositório é independente, com código próprio e licença escolhida por você. O HelioAI serve só de estudo de como obter e validar dados, não de base.

## Público e o que ele precisa

O público inicial é o grupo em que você vai entrar: gente que já usa LSTM, LSTM-Autoencoder e Gradient Pattern Analysis (GPA) em eventos extremos e valida métodos em sistemas sintéticos. As necessidades abaixo são hipóteses a confirmar com o grupo.

| Quem | O que faz | Necessidade provável (hipótese) |
| --- | --- | --- |
| LAMIFE (INPE) | Aprendizado de máquina interpretável em física de eventos extremos: LSTM, LSTM-AE e GPA, validados em p-model, Ginzburg-Landau e CML | Pipeline compartilhado e reproduzível; comparar métodos e explicá-los |
| CAP/INPE (linha IA para Aplicações Espaciais) e LIAREA | Teses e dissertações que refinam protótipos como o AEDeep | Não reescrever preparação de dados, treino e avaliação a cada trabalho |
| Usuários de dados do EMBRACE (MagNet) | Estudam o campo magnético sobre a América do Sul; a dissertação do Chen usou 14 estações | Carregador padronizado com controle de qualidade |
| ITA (dinâmica não linear) | Caos e intermitência em ondas de Alfvén | Sistemas sintéticos com verdade conhecida para testar métodos |

## O que já decidimos

O que está firme hoje, e o que ainda fica em aberto de propósito.

- Construir do zero, em repositório próprio e independente; o HelioAI é só material de estudo.
- É um projeto à parte do mestrado: colabora com ele e ajuda na carreira, sem ser o centro.
- Núcleo geral para séries e padrões espaço-temporais com eventos extremos, com módulos por domínio (clima espacial, plasma de fusão, sintéticos). A especialização está no conhecimento (fichas de método, valores de referência, RAG sobre teses e artigos), não em fine-tuning por enquanto.
- Os métodos do grupo entram como plugins com interface única: integrar o que for aberto; reimplementar com testes de referência o que não for.
- O agente de linguagem natural é uma camada opcional por cima. Os números sempre vêm de código, nunca do modelo.
- Modelo local de cerca de 8B na RTX 4060 de 8 GB; modelos gratuitos maiores só para os passos difíceis.
- **Adiado de propósito:** nome, licença, idioma da documentação principal e se o agente entra no v0.1.

## Brechas encontradas nas teses e nos dados

Seis trabalhos lidos, listados na próxima seção com os links. As fontes citadas por nome têm link na próxima seção. A linha marcada como hipótese é minha, não achado.

| Brecha | Evidência | Fonte |
| --- | --- | --- |
| Sem comparação da GPA com outras medidas; uso como atributo em aprendizado de máquina só esboçado | O autor diz que dispensou o benchmark apoiando-se em trabalhos anteriores e propõe a GPA para deep learning no Apêndice D | [Sautter 2023](http://mtc-m21d.sid.inpe.br/col/sid.inpe.br/mtc-m21d/2023/08.22.19.06/doc/publicacao.pdf) |
| Limitações da GPA | G3 dá o mesmo valor (0,75) para padrão laminar e aleatório; G1 tende a 2 em matrizes grandes e fica indistinguível; custo alto em matrizes grandes; métricas zeram com poucos elementos | [Sautter 2023](http://mtc-m21d.sid.inpe.br/col/sid.inpe.br/mtc-m21d/2023/08.22.19.06/doc/publicacao.pdf) |
| Seleção manual e poucos casos | Oito séries escolhidas à mão por experimento; q limitado a −5 a +5 pelo tamanho curto; trechos de rádio solar escolhidos por intensidade e relatório da NOAA; a autora pede dados de outras latitudes e altitudes | [Joshi 2020](http://mtc-m21c.sid.inpe.br/col/sid.inpe.br/mtc-m21c/2020/04.17.16.01/doc/publicacao.pdf) |
| Dados que não são públicos | As séries de dessincronização de Lorenz foram cedidas pelo professor Valdivia (Universidade do Chile) | [Sautter 2023](http://mtc-m21d.sid.inpe.br/col/sid.inpe.br/mtc-m21d/2023/08.22.19.06/doc/publicacao.pdf) |
| Formato e acesso aos dados do EMBRACE | Arquivos diários fora do padrão IAGA-2002, em três estruturas (1 s em ASCII, 1 min em mV, 1 min em unidades magnéticas); download com cadastro | [Chen 2019](https://www.gov.br/inpe/pt-br/area-conhecimento/posgraduacao/ges/repositorio-de-arquivos/dissertacoes/dissertacao_sony_su_chen_2019.pdf) |
| Qualidade dos dados magnéticos | Estações sem medida absoluta, com linha de base vinda do IGRF; Tucumán com flutuação de cerca de 200 nT; lacunas por datas de instalação e manutenção | [Chen 2019](https://www.gov.br/inpe/pt-br/area-conhecimento/posgraduacao/ges/repositorio-de-arquivos/dissertacoes/dissertacao_sony_su_chen_2019.pdf) |
| Dependência de lista externa de dias calmos | Os 5 dias mais calmos vêm da lista do GFZ via WDC Kyoto; em alguns meses nem todos estão disponíveis | [Chen 2019](https://www.gov.br/inpe/pt-br/area-conhecimento/posgraduacao/ges/repositorio-de-arquivos/dissertacoes/dissertacao_sony_su_chen_2019.pdf) |
| Painel da GPA é protótipo | O GPA-Dash é um painel em matplotlib dentro da tese, não uma ferramenta compartilhada | [Sautter 2023](http://mtc-m21d.sid.inpe.br/col/sid.inpe.br/mtc-m21d/2023/08.22.19.06/doc/publicacao.pdf) |
| Cada trabalho reimplementa os métodos (hipótese) | As teses trazem fluxogramas e código próprios de DFA, MFDFA, p-model, solver de Ginzburg-Landau e GPA | [Joshi 2020](http://mtc-m21c.sid.inpe.br/col/sid.inpe.br/mtc-m21c/2020/04.17.16.01/doc/publicacao.pdf) |
| Validação com vazamento infla os resultados | No trabalho do INPE sobre cintilação, o k-fold com intervalo de 30 dias deu F1 de 0,91 a 0,97 em 30 min nos blocos I a IV; o walk-forward, que só usa o passado, ficou menor. Os autores dizem que o k-fold deixa o treino ver o "futuro" e que o walk-forward serve melhor à operação | dos Santos, Stephany e de Paula 2022 |
| Desempenho muda entre fases do ciclo solar | O último bloco (2017–2018, mínimo solar), testado com modelo treinado em 2011–2017 (máximo), teve F1 de 0,79 em 30 min e cerca de 0,5 de 90 min em diante | dos Santos, Stephany e de Paula 2022 |
| Bases pequenas, curtas e com lacunas | A regressão usou 4.374 exemplos de Cachoeira Paulista (out–nov de 2014) e a classificação 40.125 de São Luís; os limites declarados são lacunas por fontes sem dados, só duas cidades, período curto e possível sobreajuste | Carvalho 2021 |
| Pipeline manual com muitas fontes | Magnetômetro e ionossonda do portal Space Weather Data Share (a ionossonda exige o SAO Explorer), OMNIWeb e GNSS pelo ISMR Query Tool, com filtros como C-score acima de 40 e satélite acima de 30° de elevação | Carvalho 2021 |
| Explicação só por rankings de importância | A seleção de atributos usa correlação, informação mútua e importância do Random Forest, que ignoram a relação entre atributos e podem manter redundância; o texto não usa SHAP nem oclusão | Carvalho 2021 |
| Qualidade dos sensores varia no tempo | Nos primeiros anos do ciclo 24 havia menos estações GNSS; os mapas de S4 e TEC têm qualidade e periodicidade variáveis e estações fora de serviço | dos Santos, Stephany e de Paula 2022 |
| Previsão de séries do p-model só preliminar | O resumo estendido mostra previsões com Keras para séries de 2.048 pontos e deixa a análise de desempenho para depois; não traz métricas | Ibanez et al. 2020 |
| Multicaminho confundido com cintilação | Trabalho futuro citado: modelos que diferenciem multicaminho de cintilação | Carvalho 2021 |

## Teses, dissertações e artigos: lidos e candidatos

Seis trabalhos foram lidos e dez são candidatos. Dos candidatos só vi resumo ou título; nada foi concluído sobre eles além da coluna Situação.

| Trabalho | Tipo e instituição | Por que importa | Situação |
| --- | --- | --- | --- |
| [Joshi (2020)](http://mtc-m21c.sid.inpe.br/col/sid.inpe.br/mtc-m21c/2020/04.17.16.01/doc/publicacao.pdf) | Tese, CAP/INPE | MFDFA e p-model em dados de foguete e de rádio solar | Lida até o capítulo 5; conclusão não alcançada |
| [Sautter (2023)](http://mtc-m21d.sid.inpe.br/col/sid.inpe.br/mtc-m21d/2023/08.22.19.06/doc/publicacao.pdf) | Tese, CAP/INPE | GPA, Ginzburg-Landau com ruído e painel | Lida inteira |
| [Chen (2019)](https://www.gov.br/inpe/pt-br/area-conhecimento/posgraduacao/ges/repositorio-de-arquivos/dissertacoes/dissertacao_sony_su_chen_2019.pdf) | Dissertação, GES/INPE | Rede MagNet do EMBRACE e curva do dia calmo | Lida até o capítulo 6; conclusão não alcançada |
| [Carvalho (2021)](https://tedebc.ufma.br/jspui/bitstream/tede/3650/2/Ot%c3%a1vio_Carvalho.pdf) | Dissertação, PPGAero/UFMA | Previsão de S4 com dados do EMBRACE, validação em blocos e Random Forest | Lida inteira, com conclusão e trabalhos futuros |
| [dos Santos, Stephany e de Paula (2022)](https://www.sbgf.org.br/revista/index.php/rbgf/article/download/2187/1434) | Artigo, INPE (COPDT e DIHPA) | Gradient boosting, k-fold e walk-forward com intervalo, vazamento e fase do ciclo solar | Lido inteiro |
| [Ibanez et al. (2020)](https://proceedings.sbmac.org.br/sbmac/article/download/2874/2905/5760) | Resumo estendido, CAP/INPE e IEAv/DCTA | Previsão de séries do p-model com Keras | Lido inteiro (2 páginas) |
| [Previsão do índice Dst com redes neurais e árvore de decisão (2009)](https://brcris.ibict.br/vivo/display/publ_190cd4bf-807f-4697-bb3b-cef1887fb37a) | Mestrado; instituição não confirmada | MLP, mapa de Kohonen e J48 para prever Dst | Só resumo |
| [Vani (2018)](http://hdl.handle.net/11449/153701) | Tese, UNESP Presidente Prudente | Modelagem, mitigação e previsão de cintilação na região brasileira; citada por dos Santos 2022 | Não aberta |
| [de Sousa do Carmo (2018)](http://urlib.net/8JMKD3MGP3W34P/3QJNJHE) | Dissertação, GES/INPE | TEC absoluto, método usado pelo EMBRACE; citada por dos Santos 2022 | Não aberta |
| Sautter (2018) | Dissertação, INPE | GPA em redes de mapas acoplados (CML); citada na tese de 2023 | Não localizada online |
| [Tese do MIT sobre disrupções](https://dspace.mit.edu/handle/1721.1/142684) | Doutorado, MIT | Random forest com contribuições de variáveis, usado em tempo real no DIII-D; previsibilidade limitada na Alcator C-Mod | Só resumo |
| [Martins](https://fenix.tecnico.ulisboa.pt/downloadFile/563345090420758/ist97169_Tiago_Martins_Thesis.pdf) | Mestrado, IST Lisboa | CNN em espectrogramas de atividade MHD com ferramenta de interpretação | Só índice e resumo |
| [Chierichini (2025)](https://etheses.whiterose.ac.uk/id/eprint/36902/) | Doutorado, Sheffield | Aprendizado de máquina e inferência bayesiana para CMEs, com SHAP | Só resumo |
| [Plava (2026)](https://amslaurea.unibo.it/id/eprint/38687/) | Mestrado, Bologna | Confiança em autoencoder para anomalias em telemetria de satélite | Texto integral indisponível |
| [Dissertação da UFC (2021)](https://bdtd.ibict.br/vufind/Record/UFC-7_f584bf0e67b52de10551ad4a0e4bcefb) | Mestrado, UFC | Detecção de anomalias em séries multivariadas; relata até 25% mais F1 que outro autoencoder | Só resumo |
| [Souza (UNESP)](https://repositorio.unesp.br/bitstreams/9c5de663-15ac-4b76-9f42-28cbd458ec08/download) | Tese, UNESP Presidente Prudente | Detecção de bolhas de plasma na região brasileira com GNSS de frequência simples | Só resumo |

XAI em clima espacial e fusão já existe: SHAP e PDP para o índice Kp ([Singampalli et al. 2026](https://journals.flvc.org/FLAIRS/article/view/141518)), SHAP e LIME em LSTM para tempestades solares ([Rawashdeh et al. 2025](https://arxiv.org/html/2508.16543v1)), SHAP em perturbações ionosféricas ([Ventriglia et al. 2025](https://www.swsc-journal.org/articles/swsc/abs/2025/01/swsc240048/swsc240048.html)) e oclusão e saliência em disrupções ([Bonalumi et al. 2024](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2024.1359656/full)). A novidade possível não está em aplicar SHAP, e sim em medir a fidelidade da explicação contra verdade conhecida e em dados brasileiros.

Dois pontos de avaliação, vistos só em resumos: [Wintoft e Wik (2021)](https://www.frontiersin.org/journals/astronomy-and-space-sciences/articles/10.3389/fspas.2021.664483/full) não acharam diferença significativa entre GRU e LSTM para o Dst, e a incerteza cresce com a magnitude do Dst; o artigo do Scientific Reports sobre [preparação de dados](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9091271/) mostra como separar validação e teste pelas metades do ciclo solar muda a distribuição do Dst.

## Métodos do grupo: usar, integrar ou reimplementar

Nenhum dos três é um pipeline de ponta a ponta: são métodos e protótipos. O sistema seria a casca que falta, e os métodos entram como plugins.

| Item | O que é | Estado | Papel proposto |
| --- | --- | --- | --- |
| GPA | Método de 1999 (Rosa, Sharma, Valdivia) que mede a quebra de simetria no padrão de gradiente; a tese de 2023 traz G1, G2, G3, a versão para séries via curva de Hilbert, o caso 3D e tabelas de valores de referência | Código da tese não localizado publicamente; a G2 existe no CyMorph | Plugin de atributos: integrar se o grupo liberar o código, senão reimplementar com as tabelas da tese como testes |
| CyMorph | Pacote Python/Cython de morfologia de galáxias (inclui a G2 da GPA), licença MIT, `pip install cymorph` | Aberto, com documentação (visto em resultado de busca, página não aberta) | Referência de empacotamento; dependência possível só para imagens 2D |
| AEDeep | Protótipo do grupo para exploração de anomalias com deep learning, citado na página do LAMIFE | Nenhum repositório público encontrado | Perguntar ao grupo; reproduzir seus resultados como teste de aceitação |

Regra proposta: integrar onde houver código aberto e mantido; reimplementar a partir da tese quando não houver; nunca copiar sem licença. As duas teses são CC BY-NC 3.0, então servem de corpus de pesquisa não comercial, com atribuição.

## Funcionalidades e fluxo de ponta a ponta

O fluxo abaixo é uma proposta, não uma decisão fechada.

1. **Sistema:** sintético (p-model, Ginzburg-Landau, CML, Lorenz acoplado) ou real (EMBRACE, OMNI, e-CALLISTO, tokamak).
2. **Dados:** baixar, guardar em cache e gerar relatório de qualidade com proveniência (fonte, versão, citação).
3. **Preparar:** valores de preenchimento viram NaN, tratar lacunas, reamostrar, corrigir linha de base quando houver.
4. **Dividir no tempo:** blocos com intervalo de segurança, com baselines obrigatórios (persistência e climatologia).
5. **Atributos (plugins, opcionais):** GPA, MFDFA e outros métodos do grupo.
6. **Modelos:** LSTM para previsão e LSTM-Autoencoder para anomalias.
7. **Avaliar:** métricas de evento raro, com intervalos de confiança.
8. **Explicar:** SHAP, oclusão e atenção; no sintético, medir se a explicação aponta a causa conhecida (fidelidade).
9. **Relatório reprodutível:** dados, versões, parâmetros e citações. Opcionalmente, um agente em linguagem natural que só escolhe ferramentas e narra, sem calcular.

Princípios de usabilidade:

- Notebook primeiro, linha de comando com arquivo de configuração para repetir execuções, agente por cima.
- Seguro por padrão: divisão temporal correta e baselines ligados, e o usuário precisa pedir para desligar.
- Primeiro resultado em minutos, em CPU ou numa GPU de 8 GB.
- Interoperar com pandas e xarray; saída em IAGA-2002 para dados magnéticos.
- Credibilidade: reproduzir resultados publicados do grupo como testes de aceitação.

## Escopo do v0.1

O v0.1 roda sem nenhum dado externo e cabe numa RTX 4060 de 8 GB: só o essencial para provar a ideia do banco de provas com verdade conhecida.

- **Dentro:** p-model (endógeno e exógeno), divisão temporal sem vazamento (walk-forward com intervalo), relatório por fase do ciclo solar, baselines, LSTM, oclusão e SHAP, métrica de fidelidade da explicação, relatório reprodutível e testes.
- **v0.2 (proposta):** dados reais (OMNI e e-CALLISTO), plugin GPA, LSTM-Autoencoder.
- **v0.3 (proposta):** carregador do EMBRACE com controle de qualidade e saída IAGA-2002; calibração e abstenção.
- **Depois:** plasma de laboratório (MAST) e o agente em linguagem natural.
- **Fora do v0.1:** interface web, agente, qualquer dado que exija cadastro ou permissão.

## Interface do MVP: terminal primeiro

**Decisão:** o MVP é uma aplicação de linha de comando, sem site nem interface gráfica no começo. A biblioteca Python é o núcleo e a linha de comando é uma camada fina por cima, chamando as mesmas funções da referência da API. O mesmo trabalho serve ao terminal, ao Jupyter e, depois, ao agente.

Por que combina com o projeto:

- É rápido de construir e de rodar, porque não há front-end.
- O público do grupo (Linux, scripts, máquinas remotas) já vive no terminal.
- É reprodutível: um comando, ou um arquivo de configuração, refaz um resultado.
- É fácil de instalar com pip ou uv, sem servidor.
- O agente do v0.4 cabe aqui como no Claude Code: a pessoa escreve em linguagem natural e o agente chama os mesmos comandos.

### Desenho dos comandos

Comandos no estilo do git (verbo e objeto), com saída bonita por padrão e uma opção para JSON ou Parquet quando for usar em script. Exemplo provisório:

```text
xai synth pmodel --n 4096 --p 0.3 --seed 1 --out serie.parquet
xai train lstm serie.parquet --horizon 32
xai explain occlusion run-01
xai eval fidelity run-01
xai report run-01 --out relatorio.html
xai sql "SELECT run, method, fidelity FROM runs ORDER BY fidelity DESC"
```

O SQL entra sem inventar linguagem nova: cada execução grava seus resultados em arquivos (pasta runs/), e o comando sql consulta esses arquivos com SQL de verdade pelo DuckDB, além dos Parquet e CSV das séries. Comparar experimentos vira uma consulta.

### Pilha sugerida

Python 3.12 ou mais novo; Typer para os comandos; Rich para tabelas, cores e barras de progresso; DuckDB para o SQL; uv para instalar (uv tool install). Textual, para uma interface interativa dentro do terminal, só depois do v0.2 e se fizer falta.

### Cuidados

- Não criar uma linguagem de consulta própria no MVP: subcomandos mais SQL padrão do DuckDB.
- Dividir a instalação em núcleo leve (NumPy, SciPy, DuckDB, Rich) e um extra ml com PyTorch e SHAP. O PyTorch com CUDA é grande e é o que mais atrapalha o fácil de baixar.
- O terminal não substitui os gráficos: tabelas e sparklines no terminal, figuras no relatório em HTML e em PNG.
- A API em Python continua sendo a entrada oficial para quem usa Jupyter; a linha de comando não pode virar a única porta.
- Testar no Windows Terminal e no Linux, porque o grupo pode usar os dois.

### Efeito na documentação

Os tutoriais mostram o comando e o equivalente em Python lado a lado, em abas. A referência da linha de comando é gerada dos próprios comandos, e o início rápido vira instalar e rodar três comandos.

## Especificação técnica do v0.1

Esta seção diz o que construir e com o quê. É proposta, para ser validada com código pequeno na primeira semana; o que for decidido vira cartão de método ou registro de decisão.

### Onde o projeto se encaixa

Benchmarks de explicação com verdade conhecida em séries temporais já existem, então a novidade não é essa. Pelo que vi em resumos:

| Trabalho | O que faz | O que o nosso projeto muda |
| --- | --- | --- |
| [Ismail et al. (NeurIPS 2020)](https://arxiv.org/abs/2010.13924) | Séries sintéticas para comparar métodos de saliência em RNN, TCN e Transformer; mostra que falham em separar tempo e atributo | A verdade vem de uma dinâmica física, não de um sinal injetado |
| [Time Interpret](https://arxiv.org/abs/2306.02968) | Extensão do Captum com métodos, datasets sintéticos e métricas para séries | Reaproveitar o Captum em vez de reescrever os explicadores |
| [xaitimesynth (2026)](https://arxiv.org/abs/2603.06781) | Gera séries com máscara de verdade e mede RMA, pointing game e NAC | Verdade vinda de acoplamento com defasagem, com eventos extremos |
| [OpenXAI](https://arxiv.org/abs/2206.11104) | Gerador sintético, 22 métricas e rankings públicos, para dados tabulares | Séries temporais físicas |
| [Synthetic Benchmarks for Scientific Research in Explainable ML](https://arxiv.org/abs/2106.12543) | Datasets sintéticos com distribuição conhecida para métricas de atribuição | Mesma ideia, em séries físicas com extremos |

O que não achei em nenhum deles: a verdade conhecida vir da física do sistema (acoplamento com defasagem, intermitência do p-model, Ginzburg-Landau), com eventos extremos e com os métodos do grupo (GPA, MFDFA) como atributos. Só vi resumos e busquei em inglês; se isso for a contribuição central, vale uma busca mais funda antes de afirmar em artigo.

### Experimento central do v0.1

O caso mais parecido com o clima espacial é um sistema de duas séries: um driver e uma resposta, como o vento solar e um índice geomagnético.

1. O driver é uma série do p-model, com β e p escolhidos para ser endógeno (fortemente autocorrelacionado) ou exógeno (fracamente), como no resumo de Ibanez et al.
2. A resposta segue uma dinâmica própria mais o acoplamento: y(t+1) = f(y(t)) + c · g(x(t − τ)) + ruído, com defasagem τ e força c conhecidas.
3. Evento extremo: a resposta passa de um limiar, por exemplo o percentil 99.
4. Verdade conhecida: as amostras do driver em torno de t − τ, nos instantes em que o acoplamento causa o evento. Isso vira uma máscara com a mesma forma da entrada.
5. O que varia: τ, c, ruído, tamanho da janela, tipo do driver e a presença de um canal isca, correlacionado com o driver mas sem efeito sobre a resposta.

**Controle obrigatório:** um modelo pode acertar sem usar a causa verdadeira, e o OpenXAI já aponta que modelos treinados em dados sintéticos podem não seguir a explicação verdadeira. Antes de avaliar um explicador, remover a causa da entrada (embaralhar o driver em torno de t − τ) e conferir que o desempenho cai. Só entram na avaliação os modelos que dependem dela.

No v0.2 em diante: redes de mapas acoplados, Lorenz acoplado (dessincronização) e Ginzburg-Landau, com a GPA como atributo extraído.

### Métricas

| Métrica | Pergunta | Origem |
| --- | --- | --- |
| Massa de relevância (RMA) | Que fração da atribuição cai dentro da máscara de verdade? | xaitimesynth |
| Pointing game | O ponto de maior atribuição cai dentro da máscara? | xaitimesynth |
| Deletion e insertion (AUC) | Mascarar o que o explicador aponta derruba a previsão mais rápido do que mascarar ao acaso? | Protocolo de Petsiuk et al. 2018, adaptado a séries |
| Estabilidade | A atribuição muda pouco entre sementes de treino e com ruído pequeno? | Categoria de robustez do OpenXAI |
| Uso da causa | O desempenho cai quando a causa é removida? | Controle do projeto |

RMA e pointing game medem o acerto contra a verdade; deletion e insertion medem a fidelidade ao modelo. São duas perguntas diferentes e o relatório mostra as duas.

### Conferência com repositórios de referência

Comparei a organização e a pilha com quatro repositórios conhecidos. Nenhum é de XAI em física espacial; o que interessa é o formato: biblioteca com linha de comando, módulos trocáveis, avaliação e resultados.

| Repositório | Por que serve de referência | O que adotamos |
| --- | --- | --- |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | Sistema de avaliação com linha de comando, tarefas em YAML e vários backends | Subcomandos run, ls e validate com configuração em YAML; instalação base leve e extras para o que é pesado; plugins por entry points; resultados em arquivos |
| [PlasmaPy](https://github.com/PlasmaPy/PlasmaPy) | Biblioteca de plasma da mesma comunidade científica | Layout src/ com tests/ fora do pacote, noxfile, uv.lock, grupos de dependências, versão pelas tags do git, testes com pytest-regressions e hypothesis, avisos tratados como erro |
| [Darts](https://github.com/unit8co/darts) | Séries temporais com modelos, detecção de anomalias, explicação com SHAP e métricas | Mesma interface fit e predict para todos os modelos; PyTorch em extra separado e versão CPU no CI; documentação com Sphinx, pydata-sphinx-theme, MyST e sphinx-design; MLflow como opcional |
| [Captum](https://github.com/meta-pytorch/captum) | Atribuição para PyTorch, com métricas de infidelidade e sensibilidade | Usar o Captum nos explicadores e nessas métricas; site (website/) separado da referência (sphinx/), como nas nossas duas frentes; a interface gráfica do Captum (Insights) foi aposentada depois da v0.8.0, o que reforça começar pelo terminal |

O que mudou na nossa proposta por causa disso:

- Resultados em arquivos (pasta runs/) são a fonte de verdade, e o DuckDB só consulta. Nenhum dos repositórios que vi mantém um registro próprio de execuções: o lm-evaluation-harness grava arquivos e integra com W&B e Zeno, e o Darts integra com MLflow.
- Python 3.12 ou mais novo, seguindo a política SPEC 0 como o PlasmaPy (o Darts aceita 3.11).
- Grupos de dependências (PEP 735) para teste, docs e lint; extras só para o que o usuário instala (ml, shap, data).
- Verificador de tipos ty no lugar do mypy: PlasmaPy e Darts já usam, mas as versões ainda são 0.0.x.
- Docstrings no estilo numpy, como o PlasmaPy; o lm-evaluation-harness e o Darts usam o estilo Google. O importante é padronizar.
- Plugins por entry points para métodos (GPA, MFDFA), explicadores e geradores, para o grupo adicionar peças sem mexer no núcleo.
- Cenários em arquivos YAML, como as tarefas do lm-evaluation-harness, e os subcomandos run, ls e validate.
- Testes com pytest-regressions para os valores de referência das teses e hypothesis para as propriedades dos geradores.
- Sem respaldo nesses repositórios: Typer, Rich e DuckDB são escolhas minhas, porque não aparecem nas dependências do lm-evaluation-harness, do PlasmaPy nem do Darts. São populares, mas se você quiser seguir só o padrão deles, o caminho é argparse e arquivos.

### Pilha técnica

| Camada | Escolha | Observação |
| --- | --- | --- |
| Linguagem | Python 3.12 ou mais novo | Política SPEC 0, como o PlasmaPy |
| Empacotamento | pyproject.toml, setuptools com setuptools-scm, layout src/ | A versão vem das tags do git |
| Números | NumPy e SciPy | Geradores e métodos (DFA, MFDFA, GPA) sem dependência pesada |
| Modelos | PyTorch | LSTM e LSTM-Autoencoder simples, com laço de treino próprio. O resumo de Ibanez et al. usa Keras, mas o Captum é de PyTorch |
| Explicação | Captum (oclusão, GradientShap, Integrated Gradients, infidelidade e sensibilidade); SHAP opcional | Reaproveita implementações e, quando servir, o Time Interpret |
| Dados e resultados | Parquet e JSON em runs/ID/; DuckDB para consultar | Os arquivos são a fonte de verdade |
| Linha de comando | Typer e Rich | Escolha minha, sem respaldo nos repositórios de referência |
| Configuração | YAML validado com Pydantic | Cada execução guarda o YAML |
| Plugins | Entry points do Python | Como o lm-evaluation-harness; métodos, explicadores e geradores |
| Testes | pytest, pytest-regressions, hypothesis, pytest-cov, pytest-xdist | Avisos tratados como erro; marcador slow |
| Qualidade | ruff, ty e pre-commit; nox para as tarefas | Docstrings no estilo numpy |
| Ambiente | uv com uv.lock no repositório; grupos de dependências test, docs e lint; extras ml, shap e data | Núcleo sem PyTorch; versão CPU do PyTorch no CI |
| Documentação | Sphinx com MyST e numpydoc | Seção Documentação e site |

### Contratos entre módulos

Cada peça troca arrays NumPy com a mesma forma, para que geradores, modelos, explicadores e métricas sejam trocáveis. O código abaixo é um esboço das interfaces, não uma implementação.

```python
@dataclass
class Sample:
    x: np.ndarray             # (T, C) entrada: driver, resposta, canal isca
    y: np.ndarray             # alvo de previsão ou rótulo de evento extremo
    truth: np.ndarray | None  # (T, C) máscara 0/1 da causa conhecida
    meta: dict                # semente, tau, c, tipo do driver, ruído

class Generator(Protocol):
    def generate(self, seed: int, **params) -> list[Sample]: ...

class Model(Protocol):
    def fit(self, train, val) -> None: ...
    def predict(self, x: np.ndarray) -> np.ndarray: ...

class Explainer(Protocol):
    def explain(self, model: Model, x: np.ndarray) -> np.ndarray: ...  # (T, C)

class Method(Protocol):           # GPA, MFDFA, DFA como atributos
    def compute(self, window: np.ndarray) -> dict[str, float]: ...

def score(attr: np.ndarray, truth: np.ndarray) -> dict[str, float]: ...
```

Resultados em arquivos, como o lm-evaluation-harness faz, com o DuckDB só como camada de consulta:

| Arquivo em runs/ID/ | Conteúdo |
| --- | --- |
| config.yaml | Configuração completa: cenário, modelo, explicador e sementes |
| meta.json | Commit do git, versão, data e ambiente |
| metrics.json | Métricas por bloco e por regime |
| attributions.parquet | Atribuições (T, C) por amostra e explicador |

O comando sql abre o DuckDB e lê runs/\*\*/metrics.json e os arquivos Parquet; o catálogo pode ser reconstruído a qualquer momento. O MLflow entra depois, como extra, se o grupo quiser um painel.

### Esqueleto do pyproject.toml

Esboço: nomes e versões mínimas se decidem quando o repositório for criado. O grupo ml fica fora do núcleo para a instalação padrão ser leve.

```toml
[build-system]
requires = ["setuptools>=77", "setuptools-scm>=8.1"]
build-backend = "setuptools.build_meta"

[project]
name = "xai-extremos"            # provisório
dynamic = ["version"]            # vem das tags do git
requires-python = ">=3.12"
dependencies = ["numpy", "scipy", "duckdb", "pyarrow", "typer", "rich", "pydantic", "pyyaml"]

[project.optional-dependencies]
ml = ["torch", "captum"]         # instalação pesada, separada do núcleo
shap = ["shap"]
data = ["astropy", "requests"]   # carregadores de dados reais, a partir do v0.2

[project.scripts]
xai = "xai_extremos.cli:app"

[project.entry-points."xai.methods"]   # plugins: GPA, MFDFA e outros
gpa = "xai_extremos.methods.gpa:GPA"

[dependency-groups]
test = ["pytest", "pytest-cov", "pytest-xdist", "pytest-regressions", "hypothesis"]
docs = ["sphinx", "myst-nb", "pydata-sphinx-theme", "sphinx-design", "sphinx-copybutton", "sphinxcontrib-bibtex", "numpydoc"]
lint = ["ruff", "ty", "pre-commit"]
dev = [{include-group = "test"}, {include-group = "docs"}, {include-group = "lint"}]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
filterwarnings = ["error"]
markers = ["slow: testes lentos"]

[tool.ruff.lint.pydocstyle]
convention = "numpy"
```

### Protocolo de avaliação

- Divisão temporal em blocos contíguos (treino, validação, teste), com intervalo maior que janela mais horizonte entre eles, sem embaralhar. É a lição do artigo do INPE sobre cintilação, em que o k-fold deixou o treino ver o futuro.
- Baselines: persistência, regressão linear autorregressiva e um limiar simples.
- Métricas de previsão: MAE e RMSE. Para o evento extremo: PR-AUC e F1 no limiar, e Brier se houver probabilidade.
- Pelo menos 10 sementes por configuração, com média e desvio, e teste de Wilcoxon pareado entre métodos (a dissertação da UFMA usa o mesmo teste).
- Resultados separados por regime (endógeno e exógeno) e, nos dados reais, por fase do ciclo solar.

### Hardware e desempenho

Séries de alguns milhares a dezenas de milhares de pontos e uma LSTM pequena cabem em CPU. A GPU de 8 GB serve para varrer muitas sementes e configurações, não para caber o modelo. Meta a calibrar: o início rápido roda em poucos minutos em CPU.

### Pronto quando (v0.1)

- [ ] O comando synth gera o sistema driver e resposta com máscara de verdade, de forma determinística por semente, com testes de propriedades do p-model (por exemplo, p = 0,5 dá série homogênea) e comparação com valores publicados na tese da Joshi (a extrair).
- [ ] A LSTM vence os três baselines no bloco de teste nos dois regimes, ou o relatório explica quando não vence.
- [ ] O controle de uso da causa passa: remover a causa derruba o desempenho.
- [ ] Oclusão e GradientShap geram atribuições (T, C), e o relatório mostra RMA, pointing game, deletion e insertion contra o acaso.
- [ ] Cada execução grava runs/ID/ (config, meta, métricas e atribuições), e uma consulta SQL pelo DuckDB compara os métodos.
- [ ] Os comandos run, ls e validate funcionam com um cenário em YAML.
- [ ] O comando report gera um HTML com tabela e figuras por regime.
- [ ] Instalação limpa com uv tool install e início rápido funcionando em Linux e Windows.
- [ ] Publicados: início rápido, tutorial 1 e cartões do p-model e das métricas.

### Riscos científicos

- A verdade conhecida é do sistema, não do modelo; por isso o controle de uso da causa.
- Conclusões em séries sintéticas podem não valer nos dados reais. O banco de provas serve para falhar cedo, não para provar que um explicador funciona no vento solar; o v0.2, com OMNI, testa essa transferência.
- A escolha de f, g e τ pode ser arbitrária. Documentar em cartão, variar os parâmetros e pedir a alguém do grupo que confira se o desenho lembra o acoplamento físico.
- A novidade depende da busca mais funda indicada na primeira subseção.

## Documentação e site

A documentação é parte do produto: o grupo só vai usar o que conseguir entender dela. A proposta é um site de documentação como o do HelioAI e o do PlasmaPy, escrito em Markdown, gerado a partir do repositório e versionado junto com o código. Um wiki do GitHub não serve para isso, porque fica em um repositório separado, não passa por pull request e não gera a referência da API.

São duas frentes separadas, ligadas por links:

- **Documentação do sistema** (este plano): instalar, usar, entender os métodos e os dados, referência da API e como contribuir.
- **Site educacional de XAI em português** (a ideia já existente, em TypeScript, com simulações e as calculadoras do mestrado): ensina os conceitos. As páginas de método da documentação apontam para as simulações, e o site aponta de volta para a referência.

Separar evita misturar dois públicos e duas tecnologias: a documentação é gerada de código Python e notebooks, enquanto o site educacional é uma aplicação web feita à mão. A estrutura segue o [Diátaxis](https://diataxis.fr), que divide a documentação em tutoriais, guias práticos, explicação e referência, e pede que cada página seja de um tipo só.

### Mapa do site

O menu do HelioAI tem quatro blocos: começo, guia do usuário, guia do desenvolvedor e referência da API. Aqui entram também Explicação, Métodos e Dados, que é o que uma ferramenta de pesquisa precisa. Uma página só entra no menu quando existe; seção vazia desanima.

| Seção | Tipo | O que tem | Entra em |
| --- | --- | --- | --- |
| Início | Porta de entrada | O que é, para quem, e três caminhos: rodar, entender, contribuir | v0.1 |
| Primeiros passos | Tutorial | Instalação, início rápido de 10 minutos (série sintética, previsão, explicação, fidelidade), configuração para GPU de 8 GB e modelo local, problemas comuns | v0.1 |
| Tutoriais | Tutorial | Passo a passo que sempre funciona: série com causa conhecida, treinar um previsor, explicar e medir a fidelidade, comparar métodos. São notebooks executados na geração do site | v0.1, e cresce |
| Guias práticos | Como fazer | Dividir a série sem vazamento, relatar por fase do ciclo solar, adicionar um dado, adicionar um método como plugin, rodar com modelo local, reproduzir um resultado, exportar o relatório | v0.1 a v0.3 |
| Explicação | Entendimento | Por que verdade conhecida, endógeno e exógeno, vazamento e validação temporal, limites de cada explicador, calibração e abstenção, o que o agente faz e não faz | v0.1 em diante |
| Métodos | Cartões | Um cartão por método: p-model, Ginzburg-Landau, CML, DFA e MFDFA, GPA, LSTM, LSTM-Autoencoder, SHAP e oclusão | p-model, oclusão e SHAP no v0.1; GPA e MFDFA no v0.2 |
| Dados | Cartões | Um cartão por fonte: OMNI, e-CALLISTO, EMBRACE (MagNet) e MAST | v0.2 e v0.3 |
| Modelos | Cartões | Um cartão por modelo treinado | v0.2 em diante |
| Referência da API | Referência | Gerada das docstrings: synthetic, data, methods, models, explain, evaluate, report e a linha de comando | v0.1 |
| Galeria | Exemplos | Notebooks executados com figuras, organizados por tarefa | v0.2 |
| Contribuir | Como fazer | Primeiros passos, estilo, testes, como documentar e política de dependências (o HelioAI tem uma página assim) | v0.1 |
| Projeto | Explicação | Visão, decisões datadas, roteiro, changelog, como citar, créditos ao grupo, glossário e bibliografia | v0.1 |

Os cartões seguem a ideia dos [model cards](https://arxiv.org/abs/1810.03993) e dos [datasheets for datasets](https://arxiv.org/abs/1803.09010), adaptada: todo cartão tem uma seção fixa de limitações documentadas, porque é lá que estão as brechas que achamos (o G3 da GPA, as lacunas do EMBRACE). O cartão de método traz o que mede, entradas e saídas, parâmetros, valores de referência, limitações, referências e onde está no pacote. O cartão de dado traz origem, como acessar, formato, cobertura, lacunas e qualidade, licença de uso e o carregador no pacote.

### Árvore do repositório

Os nomes são provisórios. A regra é que cada pasta de código tem uma página de método, de dado ou de referência correspondente em docs/.

```text
projeto/
├─ README.md             vitrine curta, com link para o site
├─ pyproject.toml        pacote, extras, grupos de dependências e plugins
├─ uv.lock               versões travadas, para reprodutibilidade
├─ noxfile.py            tarefas: testes, lint, tipos e docs
├─ CITATION.cff  CHANGELOG.md  LICENSE  CONTRIBUTING.md
├─ .readthedocs.yaml  .pre-commit-config.yaml
├─ src/pacote/
│  ├─ cli/               comandos: run, ls, validate, synth, train, explain, eval, report, sql
│  ├─ synthetic/         p-model, Ginzburg-Landau, CML, Lorenz acoplado
│  ├─ data/              carregadores e controle de qualidade
│  ├─ methods/           GPA, MFDFA e outros, com interface única
│  ├─ models/            baselines, LSTM, LSTM-Autoencoder
│  ├─ explain/           oclusão, GradientShap, SHAP (via Captum)
│  ├─ evaluate/          divisão temporal, backtest, métricas, fidelidade
│  ├─ report/            relatório reprodutível
│  ├─ registry.py        descoberta de plugins por entry points
│  └─ agent/             só a partir do v0.4
├─ scenarios/            cenários em YAML (driver, resposta, ruído, defasagem)
├─ templates/            modelos para novo cenário, método e cartão
├─ tests/                inclui valores de referência das teses (pytest-regressions)
├─ examples/             notebooks, um por tutorial e por tarefa
├─ scripts/              utilitários: baixar dados, gerar figuras
├─ docs/
│  ├─ conf.py  index.md  bibliografia.bib
│  ├─ primeiros-passos/  tutoriais/  guias/  explicacao/
│  ├─ metodos/  dados/  modelos/  referencia/  galeria/
│  └─ contribuir/  projeto/
├─ runs/                 resultados locais, fora do git
└─ .github/workflows/    testes, geração do site e publicação
```

### Ferramentas e hospedagem

| Peça | Escolha | Por quê |
| --- | --- | --- |
| Gerador | Sphinx com MyST (Markdown) | O Material for MkDocs, que o HelioAI usa, chega ao fim de vida em 5 de novembro de 2026, e o sucessor (Zensical) é novo. O Sphinx é o que o PlasmaPy usa e o que o guia do Scientific Python aponta como mais comum em bibliotecas científicas |
| Notebooks | myst-nb | Executa os notebooks na geração do site e guarda cache; se um tutorial parar de funcionar, a geração falha |
| API | autodoc e napoleon | Geram a referência a partir das docstrings; o intersphinx liga para as docs de NumPy, SciPy e PyTorch |
| Tema | pydata-sphinx-theme com cores próprias | Usado por projetos científicos; dá para aplicar a paleta marrom e verde escuro opaco do site educacional, e os dois parecem da mesma família |
| Bibliografia | sphinxcontrib-bibtex com um .bib exportado do Zotero | Uma fonte só; as citações das páginas de método viram links |
| Fórmulas | MathJax | Equações da GPA, do MFDFA e do p-model |
| Hospedagem da documentação | Read the Docs Community | Grátis para código aberto (com anúncios), versões por tag, prévia de cada pull request e PDF |
| Hospedagem do site educacional | Cloudflare Pages | Grátis, com a geração rodando no GitHub Actions |
| Citação | CITATION.cff e Zenodo | Cada versão publicada ganha um DOI |

Base da escolha: [guia de documentação do Scientific Python](https://learn.scientific-python.org/development/guides/docs/), [notas da versão 9.7.7 do Material for MkDocs](https://github.com/cms-cat/mkdocs-material/pull/229), [configuração do PlasmaPy](https://github.com/PlasmaPy/PlasmaPy/blob/v2024.2.x/docs/conf.py), [mkdocs.yml do HelioAI](https://github.com/erdoganfurkan/HelioAI/blob/main/mkdocs.yml), [Read the Docs](https://docs.readthedocs.io/) e [MyST-NB](https://myst-nb.readthedocs.io/).

### Como o site é gerado e mantido

- Fonte única: docstrings, páginas em Markdown, notebooks e o .bib. Nada é copiado à mão para o site.
- A cada pull request, a automação roda os testes, executa os notebooks, confere os links e trata aviso como erro; a Read the Docs publica uma prévia.
- A branch principal publica a versão latest, uma tag publica a stable, e o Zenodo gera o DOI da versão.
- Os valores de referência das teses (como o G2 de 0,5 do padrão laminar na tese do Sautter) ficam em um arquivo que os testes e a página do método leem. Se o código mudar o resultado, o teste quebra e a página não mente. Isso entra no v0.2.
- Cada limitação documentada em um cartão vira, quando der, um teste ou uma issue.
- Quem do grupo quiser corrigir uma página usa o botão de editar do tema, que abre o arquivo no GitHub; páginas em Markdown não exigem saber Python.

### Ordem de construção

1. Antes de codar (1 a 2 dias): repositório, pyproject, docs/ com Início, Projeto (Visão, Decisões, Roteiro) e Como citar, e a Read the Docs conectada. Este documento vira a página Visão.
2. Escrever antes de implementar: o cartão do p-model e o esboço do tutorial 1. Se o tutorial não couber em uma página, a interface do código está complicada.
3. v0.1: início rápido, tutoriais 1 a 3, guia da divisão sem vazamento, cartões de p-model, oclusão, SHAP e fidelidade, e a referência da API.
4. v0.2: cartões de GPA, MFDFA, OMNI e e-CALLISTO, galeria e valores de referência lidos pelos testes.
5. v0.3: cartão do EMBRACE com o guia do carregador e do controle de qualidade, e a explicação de calibração e abstenção.
6. v0.4: guia do agente.

### A decidir

- Idioma. Proposta: páginas em português; código, docstrings e referência da API em inglês; o essencial traduzido depois (o Sphinx traduz com gettext). Parte das teses do grupo é em inglês, então vale ouvir o Reinaldo antes de fechar.
- Nome do pacote e endereço do site, que mudam os caminhos das páginas e o nome no Zenodo.
- Licença do código e do texto (por exemplo, uma para o código e CC BY 4.0 para a documentação), que depende da regra do INPE sobre código de pesquisa já listada nas perguntas abertas.
- Read the Docs (recomendado, tem versões e prévia) ou Cloudflare Pages com a geração no GitHub Actions (um provedor só e sem anúncios).

## Perguntas abertas e hipóteses a validar

Nada abaixo foi confirmado com o grupo ainda. Duas hipóteses sustentam o projeto: cada trabalho reimplementa os métodos, e o acesso aos dados é o maior gargalo dos alunos.

- [ ] O grupo tem código do AEDeep, da GPA e dos geradores sintéticos? Em que linguagem e com que licença?
- [ ] Como os alunos pegam os dados do EMBRACE hoje (portal Space Weather Data Share, cadastro, arquivos diários, formato, lacunas)?
- [ ] Quais são os gargalos reais dos alunos: dados, reprodutibilidade, GPU?
- [ ] Os dados do EMBRACE podem entrar em exemplos públicos do repositório? Qual é a licença de uso e de redistribuição?
- [ ] O Reinaldo e o Elcio apoiam isso como projeto à parte? Há regra do INPE sobre código de pesquisa e propriedade?
- [ ] Já existe benchmark de fidelidade de XAI em séries sintéticas? Sim, genéricos (veja a especificação técnica). Em p-model ou Ginzburg-Landau não achei nenhum, mas só vi resumos.
- [ ] Como o grupo quer ser creditado (autoria, citação, agradecimentos)?
- [ ] Ler as candidatas da tabela de trabalhos, começando por Vani (2018), de Sousa do Carmo (2018) e Sautter (2018), mais a conclusão do Chen e a do Joshi. O Fornari não foi achado.
- [ ] O primeiro caso do v0.1 deve ser previsão (LSTM) ou detecção de anomalias (LSTM-Autoencoder)?
- [ ] Decidir idioma da documentação, nome do pacote, endereço do site, licenças e hospedagem (seção Documentação e site).

## Histórico de como a ideia mudou

Da mais recente para a mais antiga; todas as mudanças ocorreram em 2026-10-20.

| Mudança | O que passou a valer |
| --- | --- |
| 10 | Conferência com lm-evaluation-harness, PlasmaPy, Darts e Captum: resultados em arquivos com DuckDB só para consulta, Python 3.12, grupos de dependências e uv.lock, plugins por entry points, cenários em YAML, comandos run, ls e validate, testes de regressão e propriedades, ty no lugar do mypy |
| 9 | Especificação técnica do v0.1: experimento driver e resposta com verdade conhecida, métricas, pilha, contratos entre módulos, protocolo de avaliação e critérios de pronto. Benchmarks genéricos já existem, então a novidade passa a ser a verdade vinda da física do sistema |
| 8 | MVP como aplicação de terminal (comandos no estilo git, resultados em DuckDB consultáveis com SQL, saída bonita com Rich); biblioteca Python continua sendo o núcleo |
| 7 | Documentação e site: duas frentes (documentação do sistema e site educacional), Sphinx com MyST no lugar do MkDocs, estrutura Diátaxis com cartões de método, dado e modelo, e ordem de construção por versão |
| 6 | Pesquisa ampliada: seis trabalhos lidos e dez candidatos; novas brechas de validação, de dados e de explicação; v0.1 passa a exigir divisão sem vazamento e relatório por fase do ciclo solar |
| 5 | Projeto à parte do mestrado, para colaborar com ele e ajudar na carreira |
| 4 | Ideia central: banco de provas com verdade conhecida para IA interpretável em eventos extremos |
| 3 | Alvo: o grupo do mestrado (LAMIFE, CAP, EMBRACE, ITA), não a comunidade de heliofísica em geral |
| 2 | Construir do zero, em repositório independente, com o HelioAI só para estudo |
| 1 | Ponto de partida: um agente de IA especialista em clima espacial e plasma |

## Fontes

Páginas abertas e lidas: [Joshi 2020](http://mtc-m21c.sid.inpe.br/col/sid.inpe.br/mtc-m21c/2020/04.17.16.01/doc/publicacao.pdf), [Sautter 2023](http://mtc-m21d.sid.inpe.br/col/sid.inpe.br/mtc-m21d/2023/08.22.19.06/doc/publicacao.pdf), [Chen 2019](https://www.gov.br/inpe/pt-br/area-conhecimento/posgraduacao/ges/repositorio-de-arquivos/dissertacoes/dissertacao_sony_su_chen_2019.pdf) (lida até o capítulo 6), [HelioAI (GitHub)](https://github.com/erdoganfurkan/HelioAI), [CONTRIBUTING do HelioAI](https://github.com/erdoganfurkan/HelioAI/blob/main/CONTRIBUTING.md).

Apenas em resultados de busca, não abertas: [LAMIFE (INPE)](https://www.gov.br/inpe/pt-br/area-conhecimento/pesquisa-aplicada-e-desenvolvimento-tecnologico/laboratorios-banco-de-testes-grupos-p-d/laboratorio-de-aprendizagem-de-maquina-interpretavel-em-fisica-de-eventos-extremos-lamife) e [CyMorph (documentação)](https://cymorph.readthedocs.io/).

Segunda rodada, páginas abertas e lidas: [Carvalho 2021](https://tedebc.ufma.br/jspui/bitstream/tede/3650/2/Ot%c3%a1vio_Carvalho.pdf), [dos Santos, Stephany e de Paula 2022](https://www.sbgf.org.br/revista/index.php/rbgf/article/download/2187/1434), [Ibanez et al. 2020](https://proceedings.sbmac.org.br/sbmac/article/download/2874/2905/5760) e o [registro do mestrado sobre o Dst (2009)](https://brcris.ibict.br/vivo/display/publ_190cd4bf-807f-4697-bb3b-cef1887fb37a).

Segunda rodada, apenas resultados de busca, não abertas: os candidatos e os artigos de XAI linkados na seção de teses e dissertações.
