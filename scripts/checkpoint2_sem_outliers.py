import sys
from pathlib import Path

# --- IMPORTANTE: permite importar algs4/ quando rodamos o script dentro de scripts/
# Ex.: python scripts/checkpoint2_powerlaw_final.py
sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib
matplotlib.use("Agg")  # backend sem interface gráfica (salva imagens)
import matplotlib.pyplot as plt

import numpy as np
import powerlaw
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
# 3) PMF P(k) (escala linear)
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
# 4) Gráficos (PNGs separados)
# =========================
def salvar_histograma_linear(graus, saida_png="histograma_graus_linear.png"):
    """
    Histograma SEM escala log (como o professor pediu).
    """
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
    """
    Distribuição de graus em escala linear (PMF P(k)).
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(k_values, p_values, s=35, alpha=0.75)
    plt.title("Distribuição de Graus (PMF) — Escala Linear", fontweight="bold")
    plt.xlabel("Grau (k)")
    plt.ylabel("P(k)")
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()
    plt.savefig(saida_png, dpi=300, bbox_inches="tight")
    plt.close()


def salvar_distribuicao_loglog(results, saida_png="distribuicao_graus_loglog.png"):
    """
    Distribuição em log-log usando o powerlaw:
      - plota a PDF (discreta) dos dados
      - plota a PDF do ajuste power-law
    """
    plt.style.use("seaborn-v0_8-darkgrid")
    plt.figure(figsize=(10, 6))

    # Dados observados (PDF)
    results.plot_pdf(marker="o", ls="", alpha=0.7, label="Dados Observados")

    # Ajuste power-law (PDF do modelo ajustado)
    results.power_law.plot_pdf(
        linestyle="--",
        linewidth=2,
        label=f"Ajuste Power-Law (MLE): α = {results.power_law.alpha:.3f}"
    )

    plt.title("Distribuição de Graus — Escala Log-Log (Ajuste MLE)", fontweight="bold")
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
# 5) Função no formato do professor
# =========================
def ajuste_powerlaw(graus):
    """
    Implementa o modelo indicado pelo professor:

        data = array([...])
        results = powerlaw.Fit(data)
        print(results.power_law.alpha)
        print(results.power_law.xmin)
        R, p = results.distribution_compare('power_law', 'lognormal')

    Aqui, data = lista/array de graus.
    """
    data = np.array(graus, dtype=float)
    data = data[data > 0]  # segurança

    # discrete=True pois graus são inteiros
    results = powerlaw.Fit(data, discrete=True, verbose=False)

    alpha = results.power_law.alpha
    xmin = results.power_law.xmin

    R, p = results.distribution_compare("power_law", "lognormal")

    return results, alpha, xmin, R, p


# =========================
# 6) Main
# =========================
def main():
    # --- Carrega o grafo e calcula graus
    grafo = carregar_projeto()
    graus = calcular_graus(grafo)

    V = grafo.V if not callable(grafo.V) else grafo.V()
    E = grafo.E if not callable(grafo.E) else grafo.E()

    # --- Gera imagens solicitadas (separadas)
    salvar_histograma_linear(graus, "histograma_graus_linear.png")

    k_values, p_values = pmf_graus(graus)
    salvar_distribuicao_linear(k_values, p_values, "distribuicao_graus_linear.png")

    # --- Ajuste powerlaw conforme o professor
    results, alpha, xmin, R, p = ajuste_powerlaw(graus)

    # --- Log-log em PNG separado
    salvar_distribuicao_loglog(results, "distribuicao_graus_loglog.png")

    # --- Saída no terminal
    data = np.array(graus, dtype=float)
    data = data[data > 0]

    print("\n📊 MÉTRICAS BÁSICAS:")
    print(f"  • Vértices (V): {V}")
    print(f"  • Arestas (E): {E}")
    print(f"  • Grau mínimo: {int(np.min(data))}")
    print(f"  • Grau máximo: {int(np.max(data))}")
    print(f"  • Grau médio: {np.mean(data):.4f}")
    print(f"  • Desvio padrão: {np.std(data):.4f}")
    print(f"  • Mediana: {np.median(data):.1f}")

    print("\n☑️ AJUSTE DE LEI DE POTÊNCIA (powerlaw / MLE) — modelo do professor:")
    print(f"  • alpha (expoente): {alpha:.4f}")
    print(f"  • xmin (ponto de corte): {xmin:.1f}")

    print("\n⚖️ COMPARAÇÃO (distribution_compare):")
    print("  • power_law vs lognormal")
    print(f"  • R = {R:.4f}  (R>0 favorece power_law; R<0 favorece lognormal)")
    print(f"  • p = {p:.4f}")

    print("\n🖼️ PNGs gerados:")
    print("  • histograma_graus_linear.png")
    print("  • distribuicao_graus_linear.png")
    print("  • distribuicao_graus_loglog.png")


if __name__ == "__main__":
    main()