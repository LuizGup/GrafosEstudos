# GrafosEstudos 
# Projeto de Teoria dos Grafos: Autonomous Systems (AS)

Repositório destinado ao estudo e análise da topologia de redes de Sistemas Autônomos da Internet, utilizando a biblioteca `algs4-py`.

link SNAP utilizado: https://snap.stanford.edu/data/as-733.html

link NOTION: https://www.notion.so/PROJETO-GRAFOS-31111813a50e80e39d29fa0041dba56f?source=copy_link

### 1. Modelagem e Processamento de Dados

* **Integração com algs4-py:** Configuração do ambiente no VS Code utilizando as classes `Graph` e `Bag` para manipulação programática do dataset.
* **Carregamento do Dataset:** Implementação de script Python para leitura do arquivo `projeto_as.txt`, contendo **6.474 vértices** e **13.895 arestas**.
* **Cálculo de Métricas:** Geração automática das métricas base do Checkpoint 1:
* **Grau Médio:** 4,2926
* **Densidade:** 0,000663



### 2. Interoperabilidade e Visualização

* **Geração de Arquivo DOT:** Criação de um script exportador (`GERAR_DOT.PY`) que converte a estrutura de dados do Python para o formato `.dot`, permitindo a migração para ferramentas de análise visual.
* **Ambiente Gephi 0.10.1:**
* Importação bem-sucedida do grafo de Autonomous Systems.
* Aplicação do algoritmo de layout **ForceAtlas 2** para organização espacial da rede.
* Execução de filtros de **Ranking por Grau** (Degree) para identificação visual de Hubs através de cores e tamanhos variados.



### 3. Análise Estatística e Distribuição de Graus (Checkpoint 2)

* **Ajuste de Lei de Potência:** Implementação de análise estatística completa com ajuste P(k) ~ k^(-γ)
* **Expoente Calculado:** γ = **1.180** (rede ultra scale-free)
* **Visualizações Geradas:**
  * Gráfico de distribuição em escala linear
  * Gráfico de distribuição em escala log-log com linha de ajuste
  * Histograma de frequências de grau
* **Interpretação:** O valor γ < 2.0 confirma uma rede com concentração extrema em hubs, característica da topologia real da Internet, onde poucos AS Tier-1 dominam a conectividade global.

##  Estrutura do Repositório

```
/
├── algs4/                      # Classes essenciais da biblioteca algs4-py
├── data/                       # Arquivos de dados (.txt do SNAP)
├── main.py                     # Script principal de carregamento e métricas (Checkpoint 1)
├── checkpoint2.py              # Script de análise de distribuição de graus (Checkpoint 2)
├── GERAR_DOT.PY                # Script de exportação para o Gephi
├── grafo_projeto.dot           # Exportação final para análise visual
├── distribuicao_graus.png      # Gráficos de distribuição (linear e log-log)
├── histograma_graus.png        # Histograma de frequências de grau
└── CHECKPOINT2_INTERPRETACAO.md # Análise detalhada e interpretação dos resultados
```

## Resultados

### Checkpoint 1 — Modelagem e Métricas Iniciais ✅
O grafo apresenta uma característica de **Rede Esparsa**, com uma densidade próxima a zero (0.000663), o que confirma a modelagem real de infraestrutura de internet, onde a conectividade depende de grandes centros de roteamento (Hubs).

**Métricas:**
- Vértices: 6.474
- Arestas: 13.895 (nota: discrepância no arquivo - linha 2 indica 13.233)
- Grau Médio: 4.2926
- Densidade: 0.000663

### Checkpoint 2 — Distribuição de Graus e Lei de Potência ✅
A análise confirma que o grafo segue uma **lei de potência com expoente γ = 1.180**, caracterizando uma **rede ultra scale-free**. 

**Principais descobertas:**
1. **Concentração extrema em hubs:** Poucos AS (Tier-1) concentram a maioria das conexões
2. **Ajuste excelente:** O gráfico log-log mostra clara aderência à linha de tendência
3. **Comportamento realista:** O valor de γ está alinhado com estudos da topologia real da Internet (γ típico entre 1.1 e 1.3)
4. **Implicação prática:** A rede é robusta contra falhas aleatórias mas vulnerável a ataques direcionados aos hubs principais

**Interpretação em 3 linhas (conforme requisito):**
O gráfico log-log revela que o grafo de AS segue uma lei de potência com γ=1.18, indicando uma rede ultra scale-free onde pouquíssimos hubs concentram a vasta maioria das conexões. Este padrão reflete fielmente a arquitetura hierárquica da Internet real, com clara distinção entre AS Tier-1 (backbones globais) e ASes periféricos. A topologia demonstra robustez a falhas aleatórias mas vulnerabilidade crítica à remoção dos principais conectores.
