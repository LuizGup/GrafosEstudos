import sys
from pathlib import Path

# Permite importar o pacote algs4/ da raiz do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np
import powerlaw
from algs4.graph import Graph


# =========================
# 1) Carregar o grafo
# =========================
def carregar_projeto():
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
    V = grafo.V if not callable(grafo.V) else grafo.V()
    return [grafo.degree(v) for v in range(V)]


# =========================
# 3) Ajuste powerlaw (modelo do professor)
# =========================
def ajuste_powerlaw(graus):
    data = np.array(graus, dtype=float)
    data = data[data > 0]

    results = powerlaw.Fit(data, discrete=True, verbose=False)

    alpha = results.power_law.alpha
    xmin = results.power_law.xmin

    R, p = results.distribution_compare("power_law", "lognormal")
    return results, alpha, xmin, R, p


# =========================
# 4) Gráfico log-log com fit
# =========================
def salvar_distribuicao_loglog_com_fit(results, saida_png="distribuicao_graus_sem_outliers.png"):
    """
    Log-log com:
      - PDF dos dados observados
      - PDF do ajuste power-law (apenas na cauda a partir de xmin)
    """
    plt.style.use("seaborn-v0_8-darkgrid")
    plt.figure(figsize=(10, 6))

    results.plot_pdf(marker="o", ls="", alpha=0.7, label="Dados Observados")
    results.power_law.plot_pdf(
        linestyle="--",
        linewidth=2,
        label=f"Power-Law (MLE): α = {results.power_law.alpha:.3f}, xmin = {results.power_law.xmin:.0f}"
    )

    plt.title("Distribuição de Graus — Log-Log (Ajuste MLE / powerlaw)", fontweight="bold")
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

    results, alpha, xmin, R, p = ajuste_powerlaw(graus)
    salvar_distribuicao_loglog_com_fit(results, "distribuicao_graus_sem_outliers.png")

    print("\n☑️ AJUSTE DE LEI DE POTÊNCIA (powerlaw / MLE) — modelo do professor:")
    print(f"  • alpha (expoente): {alpha:.4f}")
    print(f"  • xmin (ponto de corte): {xmin:.1f}")

    print("\n⚖️ COMPARAÇÃO (distribution_compare):")
    print("  • power_law vs lognormal")
    print(f"  • R = {R:.4f}  (R>0 favorece power_law; R<0 favorece lognormal)")
    print(f"  • p = {p:.4f}")

    print("\n📌 Info do grafo:")
    print(f"  • Vértices (V): {V}")
    print(f"  • Arestas (E): {E}")

    print("\n🖼️ PNG gerado:")
    print("  • distribuicao_graus_sem_outliers.png")


if __name__ == "__main__":
    main()