from algs4.graph import Graph

def carregar_projeto():
    caminho = 'data/projeto_as.txt'
    
    with open(caminho, 'r') as f:
        v_total = int(f.readline().strip())
        e_total = int(f.readline().strip())
        g = Graph(v_total)
        for linha in f:
            if linha.strip():
                v, w = map(int, linha.split())
                g.add_edge(v, w)
                
    return g

try:
    grafo_as = carregar_projeto()
    print("--- Checkpoint 1: Autonomous Systems ---")
    v = grafo_as.V() if callable(grafo_as.V) else grafo_as.V
    e = grafo_as.E() if callable(grafo_as.E) else grafo_as.E
    
    print(f"Vértices carregados: {v}")
    print(f"Arestas carregadas: {e}")
    
    grau_medio = (2 * e) / v
    densidade = (2 * e) / (v * (v - 1))
    
    print(f"Grau Médio: {grau_medio:.4f}")
    print(f"Densidade: {densidade:.6f}")

except Exception as erro:
    print(f"Erro ao processar: {erro}")