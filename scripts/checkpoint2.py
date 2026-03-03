import sys
from pathlib import Path

# Permite importar o pacote algs4/ da raiz do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np
from collections import Counter
from algs4.graph import Graph


# =========================
# 1) Carregar o grafo
# =========================
def carregar_projeto():
    """
    Lê o arquivo data/projeto_as.txt no formato:
      1ª linha: V (número de vértices)
      2ª linha: E (número de arestas) [não é necessário para montar o Graph]
      demais linhas: pares v w (arestas)
    """
    caminho = Path(__file__).parent.parent / "data" / "projeto_as.txt"

    with open(caminho, "r", encoding="utf-8") as f:
        v_total = int(f.readline().strip())
        _ = f.readline().strip()  # E_total (ignorado)
        g = Graph(v_total)

        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            v, w = map(int, linha.split())
            g.add_edge(v, w)

    return g


# =========================
# 2) Calcular graus
# =========================
def calcular_graus(grafo):
    """Retorna uma lista com o grau de cada vértice."""
    V = grafo.V if not callable(grafo.V) else grafo.V()
    return [grafo.degree(v) for v in range(V)]


# =========================
# 3) PMF P(k)
# =========================
def pmf_graus(graus):
    """
    Constrói P(k) = freq(k)/N para cada grau k observado.
    Retorna arrays:
      k_values (ordenado)
      p_values
    """
    contador = Counter(graus)
    k_values = np.array(sorted(contador.keys()), dtype=int)
    total = sum(contador.values())
    p_values = np.array([contador[k] / total for k in k_values], dtype=float)
    return k_values, p_values


# =========================
# 4) Gráficos (sem powerlaw)
# =========================
def salvar_histograma_linear(graus, saida_png="histograma_graus_linear.png"):
    """Histograma SEM escala log."""
    plt.figure(figsize=(10, 6))
    plt.hist(graus, bins=50, edgecolor="black", alpha=0.85)
    plt.title("Histograma da Distribuição de Graus (Escala Linear)", fontweight="bold")
    plt.xlabel("Grau (k)")
    plt.ylabel("Frequência")
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()
    plt.savefig(saida_png, dpi=300, bbox_inches="tight")
    plt.close()


def salvar_distribuicao_linear(k_values, p_values, saida_png="distribuicao_graus_linear.png"):
    """Distribuição de graus em escala linear (PMF P(k))."""
    plt.figure(figsize=(10, 6))
    plt.scatter(k_values, p_values, s=35, alpha=0.75)
    plt.title("Distribuição de Graus (PMF) — Escala Linear", fontweight="bold")
    plt.xlabel("Grau (k)")
    plt.ylabel("P(k)")
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()
    plt.savefig(saida_png, dpi=300, bbox_inches="tight")
    plt.close()


def salvar_distribuicao_loglog_sem_fit(k_values, p_values, saida_png="distribuicao_graus_loglog.png"):
    """
    Distribuição em log-log SEM ajuste powerlaw.
    Aqui a gente plota apenas os pontos (k, P(k)) em escala log-log.
    """
    # filtra pontos válidos para log
    mask = (k_values > 0) & (p_values > 0)
    k_pos = k_values[mask]
    p_pos = p_values[mask]

    plt.style.use("seaborn-v0_8-darkgrid")
    plt.figure(figsize=(10, 6))
    plt.scatter(k_pos, p_pos, s=35, alpha=0.75, label="Dados Observados")

    plt.title("Distribuição de Graus — Escala Log-Log (Sem Ajuste)", fontweight="bold")
    plt.xlabel("Grau (k) — escala log")
    plt.ylabel("P(k) — escala log")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(saida_png, dpi=300, bbox_inches="tight")
    plt.close()


# =========================
# 5) Main
# =========================
def main():
    grafo = carregar_projeto()
    graus = calcular_graus(grafo)

    V = grafo.V if not callable(grafo.V) else grafo.V()
    E = grafo.E if not callable(grafo.E) else grafo.E()

    # Gera imagens do checkpoint 2 (SEM powerlaw)
    salvar_histograma_linear(graus, "histograma_graus_linear.png")

    k_values, p_values = pmf_graus(graus)
    salvar_distribuicao_linear(k_values, p_values, "distribuicao_graus_linear.png")
    salvar_distribuicao_loglog_sem_fit(k_values, p_values, "distribuicao_graus_loglog.png")

    # Saída de métricas básicas (útil para o checkpoint 2 também)
    dados = np.array(graus, dtype=float)
    dados = dados[dados > 0]

    print("\n📊 MÉTRICAS BÁSICAS (Checkpoint 2 - sem powerlaw):")
    print(f"  • Vértices (V): {V}")
    print(f"  • Arestas (E): {E}")
    print(f"  • Grau mínimo: {int(np.min(dados))}")
    print(f"  • Grau máximo: {int(np.max(dados))}")
    print(f"  • Grau médio: {np.mean(dados):.4f}")
    print(f"  • Desvio padrão: {np.std(dados):.4f}")
    print(f"  • Mediana: {np.median(dados):.1f}")

    print("\n🖼️ PNGs gerados:")
    print("  • histograma_graus_linear.png")
    print("  • distribuicao_graus_linear.png")
    print("  • distribuicao_graus_loglog.png")


if __name__ == "__main__":
    main()