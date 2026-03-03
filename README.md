# GrafosEstudos
# Projeto de Teoria dos Grafos: Autonomous Systems (AS)

Repositório destinado ao estudo e análise da topologia de redes de Sistemas Autônomos da Internet, utilizando a biblioteca `algs4-py`.

- **Dataset:** [SNAP — AS-733](https://snap.stanford.edu/data/as-733.html)
- **Notion:** [Página do Projeto](https://www.notion.so/PROJETO-GRAFOS-31111813a50e80e39d29fa0041dba56f?source=copy_link)

---

## Estrutura do Repositório

```
/
├── algs4/                          # Classes essenciais da biblioteca algs4-py
├── data/                           # Arquivos de dados (.txt do SNAP, .dot para Gephi)├── notebooks/
│   └── apresentacao_grafos_as.ipynb # Notebook único de apresentação (Checkpoint 3)├── scripts/
│   ├── checkpoint1.py              # Carregamento do grafo e métricas iniciais
│   ├── checkpoint2.py              # Distribuição de graus com todos os dados
│   ├── checkpoint2_sem_outliers.py # Distribuição de graus com corte via MLE (powerlaw)
│   └── GERAR_DOT.py               # Exportação para Gephi (.dot)
├── distribuicao_graus.png          # Gráfico de distribuição (linear + log-log, com outliers)
├── distribuicao_graus_sem_outliers.png  # Gráfico de distribuição sem outliers (MLE, xmin=8)
└── histograma_graus.png            # Histograma de frequências de grau
```

---

## Resultados por Checkpoint

### Checkpoint 1 — Modelagem e Métricas Iniciais ✅
> Desenvolvimento: 19/02 | Entrega: modelagem inicial do grafo e métricas básicas.

O grafo de Autonomous Systems é uma **rede esparsa**, com densidade próxima a zero, refletindo a arquitetura real da Internet onde a conectividade se concentra em grandes centros de roteamento (hubs).

| Métrica | Valor |
|---|---|
| Vértices (V) | 6.474 |
| Arestas (E) | 13.895 |
| Grau médio | 4,2926 |
| Densidade | 0,000663 |

---

### Checkpoint 2 — Distribuição de Graus e Lei de Potência ✅
> Desenvolvimento: 24/02 | Entrega: ajuste de lei de potência, interpretação do expoente e resultados parciais.

Foram gerados dois gráficos complementares:

**Com todos os dados (`checkpoint2.py`):**
- Ajuste via regressão log-log: γ = 1.180
- Inclui outliers de baixo grau (k=1, k=2) que distorcem o expoente

**Sem outliers via MLE (`checkpoint2_sem_outliers.py`):**
- Corte automático via KS-minimization: xmin = 8
- Ajuste via Maximum Likelihood Estimation: **γ = 2.148 ± 0.056**
- 413 / 6.474 vértices usados no ajuste (acima do xmin)

**Interpretação:**
O gráfico log-log revela que o grafo de AS segue uma lei de potência com γ ≈ 2.15 (após remoção dos outliers via MLE), situando-se no intervalo [2, 3] típico de redes scale-free reais. Isso indica que poucos ASes (Tier-1) concentram a maioria das conexões, enquanto a maioria possui grau baixo. O plateau observado na cauda direita corresponde a hubs de grande porte como backbones globais, estrutura esperada e documentada na topologia da Internet.

---

### Checkpoint 3 — Notebooks para Apresentação ✅
> Desenvolvimento: 26/02 | Entrega: notebooks revisados, com metodologia e resultados consolidados.

Notebook único em `notebooks/apresentacao_grafos_as.ipynb` seguindo o roteiro:

**problema → modelagem → métricas → resultados → conclusão**

| Seção | Conteúdo |
|---|---|
| O Problema | Contexto da rede de AS, dataset SNAP AS-733 |
| Modelagem | Estrutura do arquivo, grafo não-dirigido, biblioteca algs4 |
| Métricas Iniciais | V, E, grau médio, densidade, grau máximo/mínimo |
| Componentes Conexas | DFS via CC, BFS manual para distâncias |
| Distribuição de Graus | Histograma, PMF linear, PMF log-log sem ajuste |
| Ajuste Power-Law | MLE via `powerlaw`, xmin=8, γ≈2.148, comparação com lognormal |
| Painel Visual | Subplots com as 3 visualizações lado a lado |
| Conclusão | Tabela de resultados, implicações práticas, referências |

---

### Apresentação Final — Defesa dos Resultados 📅
> Desenvolvimento: 05/03 | Entrega: apresentação de 10 minutos com síntese de metodologia, resultados e conclusão.

> Roteiro da fala: **contexto → método → evidências → conclusão**
