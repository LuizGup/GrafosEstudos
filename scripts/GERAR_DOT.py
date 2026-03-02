from algs4.graph import Graph

def gerar_projeto_dot():
    caminho_txt = 'data/projeto_as.txt'
    nome_saida = 'grafo_projeto.dot'
    
    # 1. Carregamento dos dados
    with open(caminho_txt, 'r') as f:
        v_total = int(f.readline().strip())
        e_total = int(f.readline().strip())
        g = Graph(v_total)
        
        for linha in f:
            if linha.strip():
                v, w = map(int, linha.split())
                g.add_edge(v, w)

    # 2. Acesso aos dados (Tratando V como atributo)
    num_v = g.V 
    print(f"Grafo carregado com {num_v} vértices.")

    # 3. Escrita do arquivo .dot
    with open(nome_saida, 'w') as out:
        out.write("graph G {\n")
        vistas = set()
        for v in range(num_v):
            # AQUI A MUDANÇA: Usamos [v] em vez de (v)
            for w in g.adj[v]:
                if (min(v, w), max(v, w)) not in vistas:
                    out.write(f"    {v} -- {w};\n")
                    vistas.add((min(v, w), max(v, w)))
        out.write("}\n")
    
    print(f"Sucesso! Arquivo '{nome_saida}' gerado para o Gephi.")

if __name__ == "__main__":
    gerar_projeto_dot()