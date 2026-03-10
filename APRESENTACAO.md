# Roteiro de Apresentação — Grafo de Autonomous Systems

**Duração:** 10 minutos | **Equipe:** 3 pessoas  
**Data:** 05/03/2026  
**Roteiro:** Contexto → Método → Evidências → Conclusão  
**Notebook:** `notebooks/apresentacao_grafos_as.ipynb`

---

## Divisão por Pessoa

| Pessoa | Seções | Tempo | Células do Notebook |
|--------|--------|-------|---------------------|
| **1** | Contexto + Modelagem | ~3 min | 1 → 4 |
| **2** | Métricas + Distribuição de Graus | ~4 min | 5 → 10 |
| **3** | Ajuste Power-Law + Conclusão | ~3 min | 11 → 14 |

---

## Pessoa 1 — Contexto e Modelagem (~3 min)
> Células do notebook: 1, 2, 3, 4 — Problema, imports, modelagem, carregamento do grafo.

**Fala sugerida:**

> *"Nosso projeto analisa a topologia da Internet no nível dos Sistemas Autônomos — os ASes. Cada AS é uma rede independente, como a Claro, a AWS ou o Google. Eles se conectam por acordos de peering BGP, e é exatamente essa rede de acordos que modelamos como um grafo."*

> *"Usamos o dataset AS-733 do Stanford SNAP — um snapshot de 1997 com 6.474 ASes e 13.895 conexões. Cada vértice é um AS, cada aresta é um acordo de peering. Como o peering é simétrico, o grafo é não-dirigido."*

> *"Para a implementação, usamos a biblioteca algs4-py, um port do livro do Sedgewick. Aqui carregamos o arquivo e construímos o grafo usando a classe `Graph`."*

**Mostrar:** célula 4 executando → saída com `V = 6474`, `E = 13895`.

---

## Pessoa 2 — Métricas e Distribuição de Graus (~4 min)
> Células do notebook: 5, 6, 7, 8, 9, 10 — Métricas, componentes conexas, BFS, histograma, PMF linear, log-log.

**Fala sugerida:**

> *"Com o grafo carregado, calculamos as métricas básicas. A densidade é de apenas 0,000663 — a rede é extremamente esparsa. Isso faz sentido: acordos de peering têm custo financeiro e técnico, então cada AS se conecta só com quem tem interesse mútuo."*

> *"O grau médio é 4,29 — mas o grau máximo vai a mais de 1.400. Essa diferença enorme já levanta uma hipótese: existem hubs dominantes."*

> *"Verificamos que o grafo tem praticamente uma única componente gigante, com mais de 99% dos vértices. Medindo distâncias via BFS a partir do hub mais conectado, encontramos distância média de poucos saltos — o chamado fenômeno small world."*

> *"A distribuição de graus conta a história: o histograma linear mostra que a esmagadora maioria dos ASes tem grau baixo. Na escala PMF linear vemos o plateau. Mas é no log-log que a estrutura aparece — os pontos formam uma reta, que é a assinatura matemática de uma lei de potência."*

**Mostrar:** células 8, 9 e 10 com os gráficos renderizados inline.

---

## Pessoa 3 — Ajuste Power-Law e Conclusão (~3 min)
> Células do notebook: 11, 12, 13, 14 — MLE, gráfico com fit, painel visual, conclusão.

**Fala sugerida:**

> *"Para medir o expoente da lei de potência com rigor, usamos o método MLE da biblioteca `powerlaw`. O algoritmo encontra automaticamente o ponto de corte xmin = 8, eliminando os outliers de grau baixo que distorcem uma regressão simples."*

> *"O resultado: expoente γ ≈ 2,148, com desvio padrão ±0,056. A reta de ajuste se encaixa na cauda dos dados. A comparação com a distribuição lognormal (R > 0) favorece a hipótese de power-law."*

> *"O painel visual reúne as três visualizações lado a lado para fechar a argumentação."*

> *"Conclusão: o grafo de AS é scale-free com γ ≈ 2,15. Poucos ASes Tier-1 concentram a maioria das conexões. Na prática, isso tem duas implicações opostas: a rede é robusta a falhas aleatórias — se um AS qualquer cair, o impacto é mínimo. Mas é vulnerável a ataques dirigidos — derrubar um hub Tier-1 pode fragmentar a Internet inteira."*

**Mostrar:** célula 14 com a tabela de conclusão e referências.

---

## Tabela de Resultados (para citar durante a fala)

| Métrica | Valor |
|---------|-------|
| Vértices \|V\| | 6.474 |
| Arestas \|E\| | 13.895 |
| Grau médio | 4,2926 |
| Densidade | 0,000663 |
| Grau máximo | ~1.461 |
| Componente gigante | >99% dos vértices |
| Expoente γ (MLE) | 2,148 ± 0,056 |
| xmin (corte KS) | 8 |
| Comparação lognormal | R > 0 → power-law favorecida |

---

## Perguntas Prováveis da Banca

| Pergunta | Quem responde | Resposta curta | Por que / Como funciona (resposta detalhada) |
|----------|---------------|----------------|----------------------------------------------|
| O que é um Sistema Autônomo? | Pessoa 1 | Rede independente sob controle de uma única organização, identificada por um ASN. | Na Internet, nenhuma entidade única controla tudo. Cada provedor (Claro, AWS, Google) opera seu próprio bloco de IPs e roteadores. O protocolo BGP é o "idioma" que permite que esses blocos troquem informações de roteamento entre si — cada acordo de troca é uma aresta no nosso grafo. |
| Por que grafo não-dirigido? | Pessoa 1 | Peering BGP é acordo mútuo e simétrico. | Para dois ASes fazerem peering, ambos precisam concordar: A anuncia rotas para B e B anuncia para A. Não existe peering unilateral. Portanto, a relação é simétrica e representada corretamente por uma aresta sem direção. |
| O que é densidade e por que é baixa? | Pessoa 2 | Fração das arestas possíveis que existem; d ≈ 0,000663 porque acordos de peering têm custo. | A fórmula é d = 2\|E\| / (\|V\| · (\|V\|−1)). Em um grafo completo com 6.474 nós existiriam ~20 milhões de arestas — temos apenas 13.895. Cada acordo de peering envolve negociação, infraestrutura física e custos operacionais, então cada AS se conecta seletivamente apenas a quem tem interesse mútuo. |
| O que é o fenômeno small world? | Pessoa 2 | Distância média baixa apesar da rede ser grande e esparsa. | Em redes scale-free, os hubs funcionam como "atalhos": qualquer AS consegue alcançar qualquer outro em poucos saltos passando pelos Tier-1. No nosso resultado, a distância média a partir do hub mais conectado foi de poucos saltos para mais de 99% da rede — consistente com o que a literatura chama de "6 graus de separação" aplicado à Internet. |
| Como vocês calcularam a distância média? | Pessoa 2 | BFS a partir do hub mais conectado como estimativa. | Calcular a distância média exata exigiria rodar BFS a partir de todos os 6.474 vértices — custo O(V · (V+E)), inviável sem paralelização. Usamos o hub de maior grau como ponto de origem para obter uma estimativa conservadora: como ele é o nó mais central, as distâncias tendem a ser mínimas, fornecendo um limite inferior para o diâmetro da rede. |
| Por que MLE e não regressão linear? | Pessoa 3 | Regressão em log-log é enviesada para dados discretos; MLE é o estimador ótimo. | Ao fazer log(P(k)) vs log(k), transformamos os dados antes de regredir — isso introduz viés sistemático porque o erro não é gaussiano após a transformação. O MLE maximiza diretamente a função de verossimilhança P(dados \| γ, xmin) sem transformar os dados, produzindo o estimador não-enviesado de mínima variância. Para distribuições de cauda pesada com dados discretos, a diferença no expoente estimado pode ser grande. |
| O xmin = 8 foi escolhido como? | Pessoa 3 | Minimização da estatística KS entre os dados e o ajuste. | O pacote `powerlaw` testa cada valor possível de xmin, ajusta a power-law para os dados acima desse corte via MLE, e calcula a distância de Kolmogorov-Smirnov (KS) entre a CDF empírica e a CDF teórica. O xmin que produz o menor KS é escolhido — é o ponto a partir do qual a cauda dos dados mais se parece com uma power-law pura, descartando o "corpo" da distribuição onde outros mecanismos dominam. |
| O que significa γ ∈ [2, 3]? | Pessoa 3 | Segundo momento finito; hubs existem mas não dominam completamente. | Para uma power-law P(k) ∝ k^(−γ), o segundo momento (variância) diverge se γ ≤ 3 e o primeiro momento (média) diverge se γ ≤ 2. Com γ ≈ 2,15: a média é finita (rede tem grau médio definido), mas a variância é teoricamente infinita — o que explica a enorme diferença entre grau médio (4,29) e grau máximo (>1.400). É a faixa típica de redes scale-free reais como a Internet, a Web e redes de co-autoria científica. |
| Como vocês validaram o resultado? | Qualquer | Comparação power_law vs lognormal com R > 0 favorece a hipótese de power-law. | O método `distribution_compare` do `powerlaw` calcula a razão de log-verossimilhança (Log-Likelihood Ratio, LLR) entre dois modelos. R > 0 significa que a power-law explica os dados melhor que a lognormal; p < 0,05 indica que essa diferença é estatisticamente significativa e não fruto do acaso. É o teste padrão da literatura para distinguir power-law de distribuições alternativas de cauda pesada (Clauset et al., 2009). |
| Quais são as limitações do modelo? | Qualquer | Snapshot único de 1997; grafo simples sem pesos; BFS parcial. | Três limitações principais: (1) é um snapshot estático — a Internet de 1997 era menor e menos hierárquica que a atual; (2) tratamos todas as arestas como iguais, mas acordos de peering têm capacidades e custos muito diferentes; (3) a distância média foi estimada a partir de um único nó, não calculada globalmente. Essas limitações não invalidam as conclusões qualitativas, mas circunscrevem o alcance quantitativo dos resultados. |

---

## Referências

- Leskovec, J., Kleinberg, J., & Faloutsos, C. (2005). *Graphs over time: densification laws, shrinking diameters.* [SNAP AS-733](https://snap.stanford.edu/data/as-733.html)
- Barabási, A. L., & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509–512.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms, 4th Edition.* Addison-Wesley.
- Alstott, J., Bullmore, E., & Plenz, D. (2014). powerlaw: A Python Package for Analysis of Heavy-Tailed Distributions. *PLOS ONE*.
