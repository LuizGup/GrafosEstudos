import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import powerlaw
from collections import Counter
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

def calcular_distribuicao_graus(grafo):
    graus = []
    vertices = grafo.V if not callable(grafo.V) else grafo.V()
    for v in range(vertices):
        grau = grafo.degree(v)
        graus.append(grau)
    return graus

def gerar_histograma_laranja(graus):
    """Gera o histograma laranja conforme o modelo enviado"""
    plt.figure(figsize=(10, 6))
    plt.hist(graus, bins=50, color='#F2B04D', edgecolor='black', alpha=0.8)
    plt.title('Histograma da Distribuição de Graus', fontsize=14, fontweight='bold')
    plt.xlabel('Grau do Vértice', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig('histograma_graus.png', dpi=300)
    plt.close()

def gerar_grafico_loglog_mle(graus):
    """Gera o gráfico Log-Log tratando outliers via MLE"""
    dados = np.array(graus)
    dados = dados[dados > 0]
    fit = powerlaw.Fit(dados, discrete=True, verbose=False)
    
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-darkgrid')
    fit.plot_pdf(color='#A23B72', marker='o', ls='', alpha=0.6, label='Dados Observados')
    fit.power_law.plot_pdf(color='red', linestyle='--', linewidth=2, 
                           label=f'Lei de Potência: γ = {fit.alpha:.3f}')
    
    plt.title('Distribuição de Graus - Escala Log-Log (Ajuste MLE)', fontsize=14, fontweight='bold')
    plt.xlabel('Grau (k) - escala log', fontsize=12)
    plt.ylabel('P(k) - escala log', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig('distribuicao_loglog_mle.png', dpi=300)
    plt.close()
    return fit

def main():
    # Carregamento e Cálculos
    grafo = carregar_projeto()
    graus = calcular_distribuicao_graus(grafo)
    vertices = grafo.V if not callable(grafo.V) else grafo.V()
    arestas = grafo.E if not callable(grafo.E) else grafo.E()
    
    # Geração de Imagens
    gerar_histograma_laranja(graus)
    fit = gerar_grafico_loglog_mle(graus)

    # SAÍDA DO TERMINAL (Formatada conforme as imagens enviadas)
    print("\n📊 MÉTRICAS BÁSICAS:")
    print(f"  • Vértices: {vertices}")
    print(f"  • Arestas: {arestas}")
    print(f"  • Grau mínimo: {min(graus)}")
    print(f"  • Grau máximo: {max(graus)}")
    print(f"  • Grau médio: {np.mean(graus):.4f}")
    print(f"  • Desvio padrão: {np.std(graus):.4f}")
    print(f"  • Mediana: {np.median(graus):.1f}")
    
    print("\n☑️ AJUSTE DE LEI DE POTÊNCIA:")
    print(f"  • Expoente γ: {fit.alpha:.4f}")
    # Nota: R² não é uma métrica padrão do MLE, mas k_min é o indicador de qualidade do corte
    print(f"  • Ponto de corte (k_min): {fit.xmin}")
    
    print("\n✅ Análise do Checkpoint 2 concluída com sucesso!")

if __name__ == "__main__":
    main()