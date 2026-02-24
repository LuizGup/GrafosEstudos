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



### 3. Análise Estatística (Início do Checkpoint 2)

* **Distribuição de Graus:** Execução da métrica de *Average Degree* no Gephi para análise da **Lei de Potência**.
* **Configuração 3D:** Instalação e teste do plugin **Force Atlas 3D** para análise de volumetria e profundidade da topologia de rede.

##  Estrutura do Repositório

/
├── algs4/              # Classes essenciais da biblioteca algs4-py
├── data/               # Arquivos de dados (.txt do SNAP)
├── main.py             # Script principal de carregamento e métricas
├── GERAR_DOT.PY        # Script de exportação para o Gephi
└── grafo_projeto.dot   # Exportação final para análise visual

```

## Resultados Preliminares

O grafo apresenta uma característica de **Rede Esparsa**, com uma densidade próxima a zero, o que confirma a modelagem real de infraestrutura de internet, onde a conectividade depende de grandes centros de roteamento (Hubs).

---

### Próximo passo para você:

Basta criar um arquivo chamado `README.md` na raiz do seu GitHub e colar esse texto.

**Quer que eu te ajude a escrever a parte específica do "Checkpoint 2" para o seu Notion, focando apenas na explicação da Lei de Potência?**