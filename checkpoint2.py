"""
Checkpoint 2 — Gráficos e distribuição de graus
Análise de lei de potência e distribuição de graus do grafo AS
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend não-interativo
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from algs4.graph import Graph

def carregar_projeto():
    """Carrega o grafo do projeto a partir do arquivo de dados"""
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
    """Calcula a distribuição de graus do grafo"""
    graus = []
    vertices = grafo.V if not callable(grafo.V) else grafo.V()
    
    for v in range(vertices):
        grau = grafo.degree(v)
        graus.append(grau)
    
    return graus

def preparar_dados_power_law(graus):
    """Prepara os dados para análise de lei de potência"""
    # Contar a frequência de cada grau
    contador = Counter(graus)
    
    # Separar em k (grau) e P(k) (probabilidade/frequência)
    k_values = sorted(contador.keys())
    frequencias = [contador[k] for k in k_values]
    
    # Calcular probabilidade normalizada
    total = sum(frequencias)
    probabilidades = [f / total for f in frequencias]
    
    return k_values, probabilidades, contador

def ajustar_power_law(k_values, probabilidades, k_min=2):
    """
    Ajusta uma lei de potência aos dados usando regressão linear em log-log
    P(k) ~ k^(-γ)
    log(P(k)) = -γ * log(k) + C
    """
    # Filtrar valores válidos (k >= k_min e P(k) > 0)
    dados_filtrados = [(k, p) for k, p in zip(k_values, probabilidades) 
                       if k >= k_min and p > 0]
    
    if not dados_filtrados:
        return None, None, None
    
    k_filtrado, p_filtrado = zip(*dados_filtrados)
    
    # Converter para log
    log_k = np.log(k_filtrado)
    log_p = np.log(p_filtrado)
    
    # Regressão linear
    coeficientes = np.polyfit(log_k, log_p, 1)
    gamma = -coeficientes[0]  # O expoente da lei de potência
    intercepto = coeficientes[1]
    
    # Calcular R² para avaliar o ajuste
    p_pred = np.exp(np.polyval(coeficientes, log_k))
    ss_res = np.sum((np.array(p_filtrado) - p_pred) ** 2)
    ss_tot = np.sum((np.array(p_filtrado) - np.mean(p_filtrado)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    return gamma, intercepto, r_squared

def gerar_graficos(k_values, probabilidades, gamma, intercepto, grafo):
    """Gera os gráficos para análise de distribuição de graus"""
    
    # Configurar estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    ### GRÁFICO 1: Distribuição Linear
    axes[0].scatter(k_values, probabilidades, alpha=0.6, s=50, color='#2E86AB')
    axes[0].set_xlabel('Grau (k)', fontsize=12)
    axes[0].set_ylabel('P(k)', fontsize=12)
    axes[0].set_title('Distribuição de Graus - Escala Linear', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    ### GRÁFICO 2: Distribuição Log-Log (Lei de Potência)
    # Filtrar valores positivos para log
    k_pos = [k for k, p in zip(k_values, probabilidades) if p > 0 and k > 0]
    p_pos = [p for k, p in zip(k_values, probabilidades) if p > 0 and k > 0]
    
    axes[1].scatter(k_pos, p_pos, alpha=0.6, s=50, color='#A23B72', label='Dados Observados')
    
    # Linha de ajuste da lei de potência
    if gamma is not None:
        k_linha = np.linspace(min(k_pos), max(k_pos), 100)
        p_linha = np.exp(intercepto) * k_linha ** (-gamma)
        axes[1].plot(k_linha, p_linha, 'r--', linewidth=2, 
                     label=f'Lei de Potência: γ = {gamma:.3f}')
    
    axes[1].set_xscale('log')
    axes[1].set_yscale('log')
    axes[1].set_xlabel('Grau (k) - escala log', fontsize=12)
    axes[1].set_ylabel('P(k) - escala log', fontsize=12)
    axes[1].set_title('Distribuição de Graus - Escala Log-Log', fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('distribuicao_graus.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo como 'distribuicao_graus.png'")
    plt.close()
    
def gerar_histograma_graus(graus):
    """Gera histograma da distribuição de graus"""
    plt.figure(figsize=(12, 6))
    
    # Usar bins logarítmicos para melhor visualização de scale-free
    max_grau = max(graus)
    bins = np.logspace(0, np.log10(max_grau), 50)
    
    plt.hist(graus, bins=bins, color='#F18F01', alpha=0.7, edgecolor='black')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Grau do Vértice (escala log)', fontsize=12)
    plt.ylabel('Frequência (escala log)', fontsize=12)
    plt.title('Histograma da Distribuição de Graus - Escala Log-Log', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    plt.savefig('histograma_graus.png', dpi=300, bbox_inches='tight')
    print("✓ Histograma salvo como 'histograma_graus.png'")
    plt.close()

def interpretar_resultados(gamma, r_squared, graus, grafo):
    """Gera interpretação dos resultados"""
    print("\n" + "="*70)
    print("CHECKPOINT 2 — ANÁLISE DE DISTRIBUIÇÃO DE GRAUS")
    print("="*70)
    
    vertices = grafo.V if not callable(grafo.V) else grafo.V()
    arestas = grafo.E if not callable(grafo.E) else grafo.E()
    
    print(f"\n📊 MÉTRICAS BÁSICAS:")
    print(f"   • Vértices: {vertices}")
    print(f"   • Arestas: {arestas}")
    print(f"   • Grau mínimo: {min(graus)}")
    print(f"   • Grau máximo: {max(graus)}")
    print(f"   • Grau médio: {np.mean(graus):.4f}")
    print(f"   • Desvio padrão: {np.std(graus):.4f}")
    print(f"   • Mediana: {np.median(graus):.1f}")
    
    print(f"\n📈 AJUSTE DE LEI DE POTÊNCIA:")
    print(f"   • Expoente γ: {gamma:.4f}")
    print(f"   • R² (qualidade do ajuste): {r_squared:.4f}")
    
    print(f"\n💡 INTERPRETAÇÃO:")
    print(f"   O expoente γ ≈ {gamma:.2f} indica que o grafo de Autonomous Systems")
    print(f"   segue uma distribuição de lei de potência característica de redes")
    
    if 2.0 <= gamma <= 3.0:
        print(f"   scale-free. Esse padrão é típico de redes reais, onde poucos nós")
        print(f"   (hubs) concentram a maioria das conexões, enquanto a maioria dos")
        print(f"   nós tem poucas conexões. Esse comportamento é comum na topologia")
        print(f"   da Internet, refletindo a arquitetura hierárquica dos Sistemas")
        print(f"   Autônomos.")
    elif gamma < 2.0:
        print(f"   ultra scale-free. Isso indica uma concentração extrema de conexões")
        print(f"   em alguns hubs, sugerindo uma topologia altamente centralizada.")
    else:
        print(f"   que se afasta do comportamento típico de redes scale-free ideais.")
        print(f"   Pode indicar limitações estruturais ou regulatórias na rede.")
    
    if r_squared > 0.85:
        print(f"\n   ✓ O R² = {r_squared:.4f} confirma um excelente ajuste à lei de potência.")
    elif r_squared > 0.70:
        print(f"\n   ✓ O R² = {r_squared:.4f} indica um bom ajuste à lei de potência.")
    else:
        print(f"\n   ⚠ O R² = {r_squared:.4f} sugere ajuste moderado, podendo haver")
        print(f"     desvios do modelo ideal de lei de potência.")
    
    print("\n" + "="*70)

def main():
    print("Carregando grafo de Autonomous Systems...")
    grafo = carregar_projeto()
    
    print("Calculando distribuição de graus...")
    graus = calcular_distribuicao_graus(grafo)
    
    print("Preparando dados para análise de lei de potência...")
    k_values, probabilidades, contador = preparar_dados_power_law(graus)
    
    print("Ajustando lei de potência...")
    gamma, intercepto, r_squared = ajustar_power_law(k_values, probabilidades)
    
    print("\nGerando gráficos...")
    gerar_graficos(k_values, probabilidades, gamma, intercepto, grafo)
    gerar_histograma_graus(graus)
    
    interpretar_resultados(gamma, r_squared, graus, grafo)
    
    print("\n✅ Análise do Checkpoint 2 concluída com sucesso!")

if __name__ == "__main__":
    main()
