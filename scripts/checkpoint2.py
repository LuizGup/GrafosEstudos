import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para permitir importar o pacote algs4
sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib
matplotlib.use('Agg')  # Backend sem interface gráfica (salva em arquivo)
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
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


def calcular_distribuicao_graus(grafo):
    """Retorna uma lista com o grau de cada vértice do grafo."""
    vertices = grafo.V if not callable(grafo.V) else grafo.V()
    return [grafo.degree(v) for v in range(vertices)]


def preparar_dados_power_law(graus):
    """Conta a frequência de cada grau e calcula P(k): probabilidade de um vértice ter grau k."""
    contador = Counter(graus)
    k_values = sorted(contador.keys())
    total = sum(contador.values())
    probabilidades = [contador[k] / total for k in k_values]
    return k_values, probabilidades


def ajustar_power_law(k_values, probabilidades, k_min=2):
    """
    Ajusta P(k) ~ k^(-γ) via regressão linear no espaço log-log.
    Filtra apenas pontos com k >= k_min para evitar distorções na cauda esquerda.
    """
    dados = [(k, p) for k, p in zip(k_values, probabilidades) if k >= k_min and p > 0]
    if not dados:
        return None, None, None

    k_f, p_f = zip(*dados)
    log_k, log_p = np.log(k_f), np.log(p_f)

    # Coeficientes da reta: log_p = coef[0]*log_k + coef[1]
    coef = np.polyfit(log_k, log_p, 1)
    gamma = -coef[0]       # Expoente da lei de potência (negativo do coeficiente angular)
    intercepto = coef[1]

    # R² mede a qualidade do ajuste linear (quanto mais próximo de 1, melhor)
    p_pred = np.exp(np.polyval(coef, log_k))
    ss_res = np.sum((np.array(p_f) - p_pred) ** 2)
    ss_tot = np.sum((np.array(p_f) - np.mean(p_f)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    return gamma, intercepto, r_squared


def gerar_graficos(k_values, probabilidades, gamma, intercepto):
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico 1: escala linear — mostra a forma geral da distribuição
    axes[0].scatter(k_values, probabilidades, alpha=0.6, s=50, color='#2E86AB')
    axes[0].set_xlabel('Grau (k)')
    axes[0].set_ylabel('P(k)')
    axes[0].set_title('Distribuição de Graus - Escala Linear', fontweight='bold')

    # Gráfico 2: escala log-log — lineariza a lei de potência para fácil visualização
    k_pos = [k for k, p in zip(k_values, probabilidades) if p > 0 and k > 0]
    p_pos = [p for k, p in zip(k_values, probabilidades) if p > 0 and k > 0]
    axes[1].scatter(k_pos, p_pos, alpha=0.6, s=50, color='#A23B72', label='Dados')

    if gamma is not None:
        # Plota a curva ajustada P(k) = e^intercepto * k^(-γ)
        k_linha = np.linspace(min(k_pos), max(k_pos), 100)
        axes[1].plot(k_linha, np.exp(intercepto) * k_linha ** (-gamma),
                     'r--', linewidth=2, label=f'γ = {gamma:.3f}')

    axes[1].set_xscale('log')
    axes[1].set_yscale('log')
    axes[1].set_xlabel('Grau (k) - log')
    axes[1].set_ylabel('P(k) - log')
    axes[1].set_title('Distribuição de Graus - Escala Log-Log', fontweight='bold')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('distribuicao_graus.png', dpi=300, bbox_inches='tight')
    plt.close()


def gerar_histograma_graus(graus):
    """Histograma com bins logarítmicos, adequado para distribuições de cauda longa (scale-free)."""
    bins = np.logspace(0, np.log10(max(graus)), 50)
    plt.figure(figsize=(10, 6))
    plt.hist(graus, bins=bins, color='#F2B04D', edgecolor='black', alpha=0.8)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Grau do Vértice (log)')
    plt.ylabel('Frequência (log)')
    plt.title('Histograma da Distribuição de Graus', fontweight='bold')
    plt.tight_layout()
    plt.savefig('histograma_graus.png', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    grafo = carregar_projeto()
    graus = calcular_distribuicao_graus(grafo)
    k_values, probabilidades = preparar_dados_power_law(graus)
    gamma, intercepto, r_squared = ajustar_power_law(k_values, probabilidades)

    gerar_graficos(k_values, probabilidades, gamma, intercepto)
    gerar_histograma_graus(graus)

    # Métricas e resultado do ajuste
    vertices = grafo.V if not callable(grafo.V) else grafo.V()
    arestas  = grafo.E if not callable(grafo.E) else grafo.E()

    print(f"Vértices: {vertices} | Arestas: {arestas}")
    print(f"Grau — min: {min(graus)}, max: {max(graus)}, médio: {np.mean(graus):.4f}, dp: {np.std(graus):.4f}")
    print(f"Lei de potência — γ: {gamma:.4f}, R²: {r_squared:.4f}")
    print("Gráficos salvos: distribuicao_graus.png, histograma_graus.png")


if __name__ == "__main__":
    main()