import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para permitir importar o pacote algs4
sys.path.insert(0, str(Path(__file__).parent.parent))

from algs4.graph import Graph

def carregar_projeto():
    """Lê o arquivo de arestas do grafo AS e constrói o objeto Graph."""
    caminho = Path(__file__).parent.parent / 'data' / 'projeto_as.txt'

    with open(caminho, 'r') as f:
        v_total = int(f.readline().strip())  # Número de vértices
        int(f.readline().strip())            # Número de arestas (ignorado, apenas para avançar a linha)
        g = Graph(v_total)
        for linha in f:
            if linha.strip():
                v, w = map(int, linha.split())
                g.add_edge(v, w)

    return g

try:
    grafo_as = carregar_projeto()

    v = grafo_as.V() if callable(grafo_as.V) else grafo_as.V
    e = grafo_as.E() if callable(grafo_as.E) else grafo_as.E

    # Grau médio: soma dos graus / número de vértices = 2E / V
    grau_medio = (2 * e) / v

    # Densidade: fração de arestas existentes sobre o total possível em um grafo simples
    densidade = (2 * e) / (v * (v - 1))

    print(f"Vértices: {v} | Arestas: {e}")
    print(f"Grau médio: {grau_medio:.4f} | Densidade: {densidade:.6f}")

except Exception as erro:
    print(f"Erro ao processar: {erro}")