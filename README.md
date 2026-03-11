# T1 — Grafos de Escala Livre com Dados do SNAP

Análise da topologia de redes de Sistemas Autônomos da Internet utilizando o dataset AS-733 do Stanford SNAP.

**Disciplina:** Resolução de Problemas em Grafos — Universidade de Fortaleza  
**Professor:** Prof. Me. Ricardo Carubbi

**Equipe:**
- Luiz Carlos Monteiro Lopes Neto | 2410410
- Ricardo André Rodrigues Bandeira | 2417200
- João Isaías Ribeiro de Oliveira Alves | 2310283

**Dataset:** [SNAP — AS-733](https://snap.stanford.edu/data/as-733.html)

---

## Como Reproduzir a Análise

### Pré-requisitos
- Python 3.9 ou superior
- Git

### Passos

```bash
# 1. Clonar o repositório
git clone https://github.com/LuizGup/GrafosEstudos.git
cd GrafosEstudos

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Abrir o notebook principal
jupyter notebook notebooks/apresentacao_grafos_as.ipynb
```

> O notebook já inclui o dataset em `data/projeto_as.txt` — nenhum download adicional é necessário.

Para executar os scripts individuais de cada checkpoint:

```bash
python scripts/checkpoint1.py
python scripts/checkpoint2.py
python scripts/checkpoint2_sem_outliers.py
```

---

## Estrutura do Repositório

```
/
├── algs4/                               # Implementação das estruturas algs4-py (Sedgewick & Wayne)
├── data/
│   ├── projeto_as.txt                   # Dataset AS-733 (SNAP): 6.474 vértices, 13.895 arestas
│   └── grafo_projeto.dot                # Exportação para visualização no Gephi
├── notebooks/
│   └── apresentacao_grafos_as.ipynb     # Notebook principal — análise completa
├── scripts/
│   ├── checkpoint1.py                   # Carregamento do grafo e métricas iniciais
│   ├── checkpoint2.py                   # Distribuição de graus com todos os dados
│   ├── checkpoint2_sem_outliers.py      # Distribuição de graus via MLE (powerlaw, xmin=8)
│   └── GERAR_DOT.py                     # Exportação do grafo para Gephi (.dot)
├── distribuicao_graus_linear.png        # Gráfico PMF em escala linear
├── distribuicao_graus_loglog.png        # Gráfico PMF em escala log-log
├── distribuicao_graus_sem_outliers.png  # Gráfico com ajuste MLE (xmin=8)
├── histograma_graus_linear.png          # Histograma de frequências de grau
└── requirements.txt                     # Dependências Python
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
