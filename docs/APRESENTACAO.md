# Roteiro de Apresentação — Grafo de Autonomous Systems

**Duração:** 10 minutos | **Equipe:** 3 pessoas  
**Data:** 05/03/2026  
**Roteiro:** Contexto → Métricas → Distribuição de Graus → Ajuste e Conclusão  
**Notebook:** `notebooks/apresentacao_grafos_as.ipynb`

> **Lembrete:** a apresentação é para mostrar o que aprendemos, de forma clara e acessível. As respostas técnicas detalhadas ficam para as perguntas do professor. Não leiam as falas — usem como guia e falem com suas próprias palavras.

---

## Divisão por Pessoa

| Pessoa | Seções | Tempo |
|--------|--------|-------|
| **Ricardo André Rodrigues Bandeira** | 1 — O Problema, 2 — Ambiente, 3 — Modelagem, 4 — Métricas | ~4 min |
| **Luiz Carlos Monteiro Lopes Neto** | 5 — Distribuição de Graus (3 visualizações) | ~3 min |
| **João Isaías Ribeiro de Oliveira Alves** | 6 — Ajuste Power-Law, 7 — Painel Visual, 8 — Conclusão | ~3 min |

---

## Ricardo — Tópicos 1 a 4: Problema, Ambiente, Modelagem e Métricas (~4 min)

**Fala sugerida:**

> *"Nosso trabalho analisa a Internet no nível dos Sistemas Autônomos — os ASes. Pensa assim: cada provedor, como a Claro, a AWS ou o Google, é um AS. Eles precisam conversar entre si para que a Internet funcione, e essa conversa acontece por acordos chamados de peering BGP."*

> *"A pergunta que a gente se fez foi: como é a estrutura dessa rede de acordos? Ela tem alguma forma matemática interessante?"*

> *"Para investigar isso, usamos um dataset do Stanford chamado AS-733 — um retrato da Internet de 1997, com 6.474 ASes e 13.895 conexões. Modelamos isso como um grafo não-dirigido: cada AS é um vértice, cada acordo é uma aresta. Não-dirigido porque peering é mútuo — se A se conecta a B, B também se conecta a A."*

> *"A implementação usou a biblioteca algs4-py, baseada no livro do Sedgewick, que a gente usou na disciplina. Com ela, carregamos o grafo e já calculamos as primeiras métricas."*

**Mostrar:** célula de métricas executando → destacar os números na saída.

> *"Os números já contam uma história. A rede é extremamente esparsa — densidade de 0,000663. Faz sentido: cada acordo de peering tem custo, ninguém se conecta a todo mundo. Mas o ponto mais interessante é a diferença entre o grau médio — 4,29 conexões por AS — e o grau máximo, que passa de 1.400. Isso sugere fortemente que existem alguns ASes gigantes, os chamados hubs."*

---

## Luiz Carlos — Tópico 5: Distribuição de Graus (~3 min)

**Fala sugerida:**

> *"Com as métricas na mão, a gente queria entender melhor como esses graus se distribuem. Para isso, construímos três visualizações, cada uma revelando uma camada diferente da estrutura."*

**Mostrar:** histograma (célula 5.1).

> *"O histograma em escala linear mostra uma coisa clara: a esmagadora maioria dos ASes tem grau baixo, concentrado lá na esquerda. A barra é tão dominante que a cauda direita mal aparece — ela existe, mas é invisível nessa escala."*

**Mostrar:** PMF linear (célula 5.2).

> *"Quando a gente plota a probabilidade de cada grau — a PMF — vemos a mesma coisa, agora ponto a ponto. Quase todos os valores estão acumulados perto do zero. Os pontos isolados lá na direita são os hubs."*

**Mostrar:** log-log (célula 5.3).

> *"O gráfico que faz tudo se encaixar é esse aqui — escala logarítmica nos dois eixos. Quando a distribuição segue uma lei de potência, ela aparece como uma reta nesse espaço. E é exatamente o que a gente vê: os pontos formam uma linha reta na cauda. Isso é a assinatura matemática de uma rede scale-free."*

---

## João Isaías — Tópicos 6, 7 e 8: Ajuste, Painel e Conclusão (~3 min)

**Fala sugerida:**

> *"Ver a reta no gráfico log-log é sugestivo, mas não é prova. Para medir o expoente com rigor, a gente usou o pacote `powerlaw`, que aplica o método MLE — Máxima Verossimilhança."*

**Mostrar:** célula do MLE executando → destacar os valores impressos.

> *"O resultado foi um expoente γ ≈ 2,15. Esse número está dentro do intervalo de 2 a 3, que é justamente o que a literatura descreve como típico de redes reais como a Internet, a Web e redes sociais. A comparação com a distribuição lognormal também favoreceu a power-law."*

**Mostrar:** gráfico com a reta de ajuste sobreposta aos dados.

> *"Aqui dá pra ver a reta de ajuste encaixando na cauda dos dados. O painel ao lado reúne as três visões juntas para fechar o argumento visualmente."*

**Mostrar:** painel (célula 7).

> *"Conclusão: confirmamos que a rede de Sistemas Autônomos é scale-free. Poucos hubs concentram a maioria das conexões. Isso tem duas implicações práticas opostas: a rede é muito resistente a falhas aleatórias — se um AS qualquer cair, quase ninguém sente. Mas é vulnerável a ataques nos hubs — se um Tier-1 sair do ar, o impacto pode ser global."*

**Mostrar:** célula de conclusão com a tabela de resultados.

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
| O que é um Sistema Autônomo? | Ricardo | Rede independente sob controle de uma única organização, identificada por um ASN. | Na Internet, nenhuma entidade única controla tudo. Cada provedor (Claro, AWS, Google) opera seu próprio bloco de IPs e roteadores. O protocolo BGP é o "idioma" que permite que esses blocos troquem informações de roteamento entre si — cada acordo de troca é uma aresta no nosso grafo. |
| Por que grafo não-dirigido? | Ricardo | Peering BGP é acordo mútuo e simétrico. | Para dois ASes fazerem peering, ambos precisam concordar: A anuncia rotas para B e B anuncia para A. Não existe peering unilateral. Portanto, a relação é simétrica e representada corretamente por uma aresta sem direção. |
| O que é densidade e por que é baixa? | Ricardo | Fração das arestas possíveis que existem; d ≈ 0,000663 porque acordos de peering têm custo. | A fórmula é d = 2\|E\| / (\|V\| · (\|V\|−1)). Em um grafo completo com 6.474 nós existiriam ~20 milhões de arestas — temos apenas 13.895. Cada acordo de peering envolve negociação, infraestrutura física e custos operacionais, então cada AS se conecta seletivamente apenas a quem tem interesse mútuo. |
| O que é o fenômeno small world? | Ricardo | Distância média baixa apesar da rede ser grande e esparsa. | Em redes scale-free, os hubs funcionam como "atalhos": qualquer AS consegue alcançar qualquer outro em poucos saltos passando pelos Tier-1. No nosso resultado, a distância média a partir do hub mais conectado foi de poucos saltos para mais de 99% da rede — consistente com o que a literatura chama de "6 graus de separação" aplicado à Internet. |
| Por que o histograma linear não é suficiente? | Luiz | Ele esconde a cauda — os hubs somem perto do eixo. | A escala linear comprime tudo para baixo quando há valores extremos. Como a maioria dos ASes tem grau 1–5, a barra desse intervalo domina o gráfico e os hubs com grau >100 ficam irrelevantes visualmente. A escala log-log redistribui o espaço e revela a estrutura da cauda. |
| O que é uma rede scale-free? | Luiz | Rede onde a distribuição de graus segue uma lei de potência P(k) ∝ k^(−γ). | Em redes aleatórias, os graus se concentram em torno da média (distribuição de Poisson). Em redes scale-free, não há escala característica — existem hubs com grau ordens de magnitude acima da média. Isso emerge de um processo de crescimento preferencial: nós novos preferem se conectar a quem já tem mais conexões. |
| Por que MLE e não regressão linear? | João | Regressão em log-log é enviesada para dados discretos; MLE é o estimador ótimo. | Ao fazer log(P(k)) vs log(k), transformamos os dados antes de regredir — isso introduz viés sistemático porque o erro não é gaussiano após a transformação. O MLE maximiza diretamente a função de verossimilhança P(dados \| γ, xmin) sem transformar os dados, produzindo o estimador não-enviesado de mínima variância. Para distribuições de cauda pesada com dados discretos, a diferença no expoente estimado pode ser grande. |
| O xmin = 8 foi escolhido como? | João | Minimização da estatística KS entre os dados e o ajuste. | O pacote `powerlaw` testa cada valor possível de xmin, ajusta a power-law para os dados acima desse corte via MLE, e calcula a distância de Kolmogorov-Smirnov (KS) entre a CDF empírica e a CDF teórica. O xmin que produz o menor KS é escolhido — é o ponto a partir do qual a cauda dos dados mais se parece com uma power-law pura, descartando o "corpo" da distribuição onde outros mecanismos dominam. |
| O que significa γ ∈ [2, 3]? | João | Segundo momento finito; hubs existem mas não dominam completamente. | Para uma power-law P(k) ∝ k^(−γ), o segundo momento (variância) diverge se γ ≤ 3 e o primeiro momento (média) diverge se γ ≤ 2. Com γ ≈ 2,15: a média é finita (rede tem grau médio definido), mas a variância é teoricamente infinita — o que explica a enorme diferença entre grau médio (4,29) e grau máximo (>1.400). É a faixa típica de redes scale-free reais como a Internet, a Web e redes de co-autoria científica. |
| Como vocês validaram o resultado? | Qualquer | Comparação power_law vs lognormal com R > 0 favorece a hipótese de power-law. | O método `distribution_compare` do `powerlaw` calcula a razão de log-verossimilhança (Log-Likelihood Ratio, LLR) entre dois modelos. R > 0 significa que a power-law explica os dados melhor que a lognormal; p < 0,05 indica que essa diferença é estatisticamente significativa e não fruto do acaso. É o teste padrão da literatura para distinguir power-law de distribuições alternativas de cauda pesada (Clauset et al., 2009). |
| Quais são as limitações do modelo? | Qualquer | Snapshot único de 1997; grafo simples sem pesos; BFS parcial. | Três limitações principais: (1) é um snapshot estático — a Internet de 1997 era menor e menos hierárquica que a atual; (2) tratamos todas as arestas como iguais, mas acordos de peering têm capacidades e custos muito diferentes; (3) a distância média foi estimada a partir de um único nó, não calculada globalmente. Essas limitações não invalidam as conclusões qualitativas, mas circunscrevem o alcance quantitativo dos resultados. |

---

## Referências

- Leskovec, J., Kleinberg, J., & Faloutsos, C. (2005). *Graphs over time: densification laws, shrinking diameters.* [SNAP AS-733](https://snap.stanford.edu/data/as-733.html)
- Barabási, A. L., & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509–512.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms, 4th Edition.* Addison-Wesley.
- Alstott, J., Bullmore, E., & Plenz, D. (2014). powerlaw: A Python Package for Analysis of Heavy-Tailed Distributions. *PLOS ONE*.
