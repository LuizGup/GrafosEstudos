import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para permitir importar o pacote algs4
sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import powerlaw
from algs4.graph import Graph


def carregar_projeto():
    """Lê o arquivo de arestas do grafo AS e constrói o objeto Graph."""
    caminho = Path(__file__).parent.parent / 'data' / 'projeto_as.txt'
    with open(caminho, 'r') as f:
        v_total = int(f.readline().strip())
        int(f.readline().strip())
        g = Graph(v_total)
        for linha in f:
            if linha.strip():
                v, w = map(int, linha.split())
                g.add_edge(v, w)
    return g


def calcular_graus(grafo):
    """Retorna uma lista com o grau de cada vértice do grafo."""
    vertices = grafo.V if not callable(grafo.V) else grafo.V()
    return [grafo.degree(v) for v in range(vertices)]


def gerar_grafico(graus):
    """
    Usa powerlaw (MLE) para encontrar o xmin ideal e remove os outliers abaixo dele.
    Gera dois gráficos: distribuição linear e log-log com ajuste da lei de potência.
    Salva como distribuicao_graus_sem_outliers.png.
    """
    dados = np.array([g for g in graus if g > 0])

    # MLE encontra o xmin ótimo (ponto a partir do qual a lei de potência se aplica)
    fit = powerlaw.Fit(dados, discrete=True, verbose=False)
    xmin = fit.xmin
    gamma = fit.alpha

    # Filtra os outliers: mantém apenas k >= xmin
    dados_filtrados = dados[dados >= xmin]

    # Calcula P(k) empírica para o scatter log-log
    valores, contagens = np.unique(dados_filtrados, return_counts=True)
    pk = contagens / contagens.sum()

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico 1: distribuição linear sem outliers
    axes[0].scatter(valores, pk, alpha=0.6, s=50, color='#2E86AB')
    axes[0].set_xlabel('Grau (k)')
    axes[0].set_ylabel('P(k)')
    axes[0].set_title(f'Distribuição de Graus - Escala Linear (k ≥ {int(xmin)})', fontweight='bold')

    # Gráfico 2: log-log com curva de ajuste
    axes[1].scatter(valores, pk, alpha=0.6, s=50, color='#A23B72', label='Dados')

    # Linha da lei de potência: ancoramos no primeiro ponto empírico
    k_linha = np.linspace(valores[0], valores[-1], 300)
    escala = pk[0] / (valores[0] ** (-gamma))
    axes[1].plot(k_linha, escala * k_linha ** (-gamma),
                 'r--', linewidth=2, label=f'γ = {gamma:.3f}')

    axes[1].set_xscale('log')
    axes[1].set_yscale('log')
    axes[1].set_xlabel('Grau (k) - log')
    axes[1].set_ylabel('P(k) - log')
    axes[1].set_title('Distribuição de Graus - Escala Log-Log', fontweight='bold')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('distribuicao_graus_sem_outliers.png', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    grafo = carregar_projeto()
    graus = calcular_graus(grafo)

    fit = powerlaw.Fit(np.array([g for g in graus if g > 0]), discrete=True, verbose=False)

    gerar_grafico(graus)

    print(f"xmin (corte): {int(fit.xmin)}")
    print(f"γ (MLE): {fit.alpha:.4f} ± {fit.sigma:.4f}")
    print(f"Dados no ajuste: {sum(g >= fit.xmin for g in graus)} / {len(graus)} vértices")
    print("Gráfico salvo: distribuicao_graus_sem_outliers.png")


if __name__ == "__main__":
    main()
