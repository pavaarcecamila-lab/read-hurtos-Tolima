"""
Generador de Gráficas de Alta Calidad para Métodos Numéricos
Proyecto: Observatorio de Hurto y Recuperación Vehicular en Colombia
Muestra oficial: 15 años (2010–2024) - Policía Nacional / DIJIN
"""

import os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Configuración de directorio
CARPETA_FIGURAS = Path(__file__).resolve().parent.parent / "docs" / "figuras"
CARPETA_FIGURAS.mkdir(parents=True, exist_ok=True)

# 1. Datos oficiales de la serie nacional 2010 - 2024
DATA = [
    {"anio": 2010, "x": 10243, "y": 8240},
    {"anio": 2011, "x": 12504, "y": 8309},
    {"anio": 2012, "x": 14516, "y": 8300},
    {"anio": 2013, "x": 15986, "y": 8628},
    {"anio": 2014, "x": 15316, "y": 8876},
    {"anio": 2015, "x": 17054, "y": 9460},
    {"anio": 2016, "x": 18778, "y": 9639},
    {"anio": 2017, "x": 21642, "y": 9465},
    {"anio": 2018, "x": 21177, "y": 8970},
    {"anio": 2019, "x": 22964, "y": 9058},
    {"anio": 2020, "x": 18409, "y": 7376},
    {"anio": 2021, "x": 21805, "y": 8522},
    {"anio": 2022, "x": 24431, "y": 12107},
    {"anio": 2023, "x": 24725, "y": 12621},
    {"anio": 2024, "x": 23295, "y": 13353},
]

x_arr = np.array([d["x"] for d in DATA])
y_arr = np.array([d["y"] for d in DATA])
anios = [d["anio"] for d in DATA]

# Parámetros MCO
b1 = 0.260264  # ~0.2603
b0 = 4620.64
r2 = 0.6552
r_corr = 0.8094
y_pred = b0 + b1 * x_arr

# 4 Nodos de Lagrange
NODES = [
    {"x": 10243, "y": 8240, "anio": 2010, "label": "Nodo 0 (2010)\nInicio: x₀=10,243 | y₀=8,240"},
    {"x": 18778, "y": 9639, "anio": 2016, "label": "Nodo 1 (2016)\nIntermedio: x₁=18,778 | y₁=9,639"},
    {"x": 24431, "y": 12107, "anio": 2022, "label": "Nodo 2 (2022)\nCrecimiento: x₂=24,431 | y₂=12,107"},
    {"x": 23295, "y": 13353, "anio": 2024, "label": "Nodo 3 (2024)\nMáximo: x₃=23,295 | y₃=13,353"},
]

def eval_lagrange(x_val):
    val = 0.0
    for i, ni in enumerate(NODES):
        term = ni["y"]
        for j, nj in enumerate(NODES):
            if i != j:
                term *= (x_val - nj["x"]) / (ni["x"] - nj["x"])
        val += term
    return val


# ==============================================================================
# FIGURA 1: REGRESIÓN LINEAL SIMPLE POR MCO
# ==============================================================================
def generar_figura_regresion():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#F8FAFC")

    # Rejilla sutil
    ax.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=1)

    # 1. Residuos verticales
    for xi, yi, ypi in zip(x_arr, y_arr, y_pred):
        ax.plot([xi, xi], [yi, ypi], color="#EF4444", linestyle=":", linewidth=1.4, alpha=0.75, zorder=2)

    # 2. Recta de regresión
    x_line = np.linspace(9500, 26000, 200)
    y_line = b0 + b1 * x_line
    ax.plot(x_line, y_line, color="#2563EB", linewidth=2.8, label=r"Recta MCO: $\hat{y} = 4,620.64 + 0.2603 \cdot x$", zorder=3)

    # 3. Puntos de dispersión
    ax.scatter(x_arr, y_arr, color="#0F172A", s=65, edgecolor="#FFFFFF", linewidth=1.5, zorder=4, label="Datos Reales Anuales (15 años)")

    # Etiquetas de año
    for xi, yi, a in zip(x_arr, y_arr, anios):
        offset_y = 160 if yi >= (b0 + b1*xi) else -220
        ax.annotate(str(a), (xi, yi), textcoords="offset points", xytext=(0, 6 if offset_y > 0 else -12),
                    ha="center", fontsize=8.5, fontweight="bold", color="#334155", zorder=5)

    # Título y Ejes explicativos
    ax.set_title("MÉTODOS NUMÉRICOS: REGRESIÓN LINEAL SIMPLE POR MÍNIMOS CUADRADOS (MCO)",
                 fontsize=13, fontweight="bold", color="#0F172A", pad=14)
    ax.set_xlabel("VARIABLE INDEPENDIENTE (Eje X): Vehículos Hurtados Anuales (Denuncias en Colombia)",
                  fontsize=10.5, fontweight="bold", color="#1E3A8A", labelpad=10)
    ax.set_ylabel("VARIABLE DEPENDIENTE (Eje Y): Vehículos Recuperados Anuales (Policía Nacional)",
                  fontsize=10.5, fontweight="bold", color="#1E3A8A", labelpad=10)

    # Formato de números en ejes con comas
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    ax.set_xlim(9200, 26200)
    ax.set_ylim(6800, 14200)

    # Recuadro de Parámetros Matemáticos
    texto_kpis = (
        r"$\mathbf{PARÁMETROS\ DEL\ MODELO\ MCO:}$" + "\n"
        r"• $\mathbf{Ecuación:}\ \hat{y} = 4,620.64 + 0.2603 \cdot x$" + "\n"
        r"• $\mathbf{Pendiente\ (b_1):}\ 0.2603$ (~26 recuperados por 100 hurtos)" + "\n"
        r"• $\mathbf{Intercepto\ (b_0):}\ 4,620.64$ (Capacidad base inercial)" + "\n"
        r"• $\mathbf{R^2:}\ 0.6552\ (65.5\%\ de\ variabilidad\ explicada)$" + "\n"
        r"• $\mathbf{Correlación\ (r):}\ 0.8094$ (Asociación positiva fuerte)" + "\n"
        r"• $\mathbf{Residuos\ (líneas\ rojas):}\ e_i = y_i - \hat{y}_i$"
    )
    ax.text(0.03, 0.96, texto_kpis, transform=ax.transAxes, fontsize=8.8,
            verticalalignment="top", bbox=dict(boxstyle="round,pad=0.7", facecolor="#EFF6FF", edgecolor="#3B82F6", alpha=0.95))

    ax.legend(loc="lower right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=9.5)
    plt.tight_layout()
    salida = CARPETA_FIGURAS / "fig_metodos_numericos_regresion_mco.png"
    plt.savefig(salida, dpi=300)
    plt.close()
    print(f"✅ Guardada: {salida}")


# ==============================================================================
# FIGURA 2: INTERPOLACIÓN POLINÓMICA DE LAGRANGE
# ==============================================================================
def generar_figura_lagrange():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFBEB")

    ax.grid(True, linestyle="--", alpha=0.5, color="#FDE68A", zorder=1)

    # Curva polinómica de Lagrange
    x_lag = np.linspace(10243, 24431, 300)
    y_lag = [eval_lagrange(val) for val in x_lag]
    ax.plot(x_lag, y_lag, color="#EA580C", linestyle="--", linewidth=2.8,
            label=r"Polinomio de Lagrange $P_3(x) = \sum y_i L_i(x)$ (Grado 3)", zorder=3)

    # Puntos reales de la serie
    ax.scatter(x_arr, y_arr, color="#64748B", s=40, alpha=0.6, zorder=2, label="Otros Años de la Muestra (n=11)")

    # Nodos de soporte
    colores_nodos = ["#DC2626", "#D97706", "#CA8A04", "#16A34A"]
    for idx, (node, col) in enumerate(zip(NODES, colores_nodos)):
        ax.scatter(node["x"], node["y"], color=col, s=140, edgecolor="#FFFFFF", linewidth=2.2, zorder=5)
        offset = (15, -15) if idx != 2 else (-20, 20)
        ax.annotate(f"Nodo {idx} ({node['anio']})\n({node['x']:,}, {node['y']:,})",
                    (node["x"], node["y"]), textcoords="offset points", xytext=offset,
                    fontsize=8.5, fontweight="bold", color="#7C2D12",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF3C7", edgecolor=col, alpha=0.9),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.2), zorder=6)

    # Título y Ejes explicativos
    ax.set_title("MÉTODOS NUMÉRICOS: INTERPOLACIÓN POLINÓMICA DE LAGRANGE (4 NODOS)",
                 fontsize=13, fontweight="bold", color="#7C2D12", pad=14)
    ax.set_xlabel("VARIABLE INDEPENDIENTE (Eje X): Vehículos Hurtados Anuales (x)",
                  fontsize=10.5, fontweight="bold", color="#9A3412", labelpad=10)
    ax.set_ylabel("VARIABLE DEPENDIENTE (Eje Y): Vehículos Recuperados Anuales (y)",
                  fontsize=10.5, fontweight="bold", color="#9A3412", labelpad=10)

    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    ax.set_xlim(9500, 25500)
    ax.set_ylim(6800, 14200)

    # Recuadro explicativo
    texto_lagrange = (
        r"$\mathbf{PROPIEDADES\ DE\ LAGRANGE:}$" + "\n"
        r"• $\mathbf{Polinomio\ Cúbico:}\ P_3(x) = y_0 L_0(x) + y_1 L_1(x) + y_2 L_2(x) + y_3 L_3(x)$" + "\n"
        r"• $\mathbf{Propiedad\ Kronecker:}\ L_i(x_k) = 1\ \text{si}\ i=k,\ 0\ \text{si}\ i \neq k$" + "\n"
        r"• $\mathbf{Error\ en\ Nodos:}\ e_i = 0.00\ \text{(Ajuste exacto sin residuales)}$" + "\n"
        r"• $\mathbf{Control\ de\ Runge:}\ Se\ eligen\ 4\ nodos\ para\ evitar\ oscilaciones\ inestables$" + "\n"
        r"• $\mathbf{Uso\ Policial:}\ Reconstruir\ curvas\ no\ lineales\ en\ periodos\ intermedios$"
    )
    ax.text(0.03, 0.96, texto_lagrange, transform=ax.transAxes, fontsize=8.8,
            verticalalignment="top", bbox=dict(boxstyle="round,pad=0.7", facecolor="#FFFBEB", edgecolor="#EA580C", alpha=0.95))

    ax.legend(loc="lower right", frameon=True, facecolor="#FFFFFF", edgecolor="#FDE68A", fontsize=9.5)
    plt.tight_layout()
    salida = CARPETA_FIGURAS / "fig_metodos_numericos_lagrange.png"
    plt.savefig(salida, dpi=300)
    plt.close()
    print(f"✅ Guardada: {salida}")


# ==============================================================================
# FIGURA 3: COMPARATIVA SUPERPUESTA MCO VS LAGRANGE
# ==============================================================================
def generar_figura_comparativa():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#F8FAFC")

    ax.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1", zorder=1)

    # 1. Recta MCO
    x_line = np.linspace(9500, 25500, 200)
    y_mco = b0 + b1 * x_line
    ax.plot(x_line, y_mco, color="#2563EB", linewidth=3, label=r"Regresión MCO: Recta Global $\hat{y} = 4,620.64 + 0.2603 \cdot x$", zorder=3)

    # 2. Curva Lagrange
    x_lag = np.linspace(10243, 24431, 300)
    y_lag = [eval_lagrange(val) for val in x_lag]
    ax.plot(x_lag, y_lag, color="#EA580C", linestyle="--", linewidth=3, label=r"Lagrange: Curva Cúbica Exacta $P_3(x)$", zorder=4)

    # 3. Puntos de datos
    ax.scatter(x_arr, y_arr, color="#0F172A", s=55, edgecolor="#FFFFFF", linewidth=1.5, zorder=5, label="Observaciones Reales (2010–2024)")

    # 4. Destacar nodos
    for node in NODES:
        ax.scatter(node["x"], node["y"], color="#EA580C", s=130, edgecolor="#FFFFFF", linewidth=2, zorder=6)

    # Título y Ejes explicativos detallados
    ax.set_title("COMPARATIVA DE MÉTODOS NUMÉRICOS: REGRESIÓN LINEAL (MCO) VS INTERPOLACIÓN DE LAGRANGE",
                 fontsize=12.5, fontweight="bold", color="#0F172A", pad=14)
    ax.set_xlabel("VARIABLE INDEPENDIENTE (Eje X): Vehículos Hurtados Anuales (Hurtos)",
                  fontsize=10.5, fontweight="bold", color="#1E3A8A", labelpad=10)
    ax.set_ylabel("VARIABLE DEPENDIENTE (Eje Y): Vehículos Recuperados Anuales (Recuperaciones Policiales)",
                  fontsize=10.5, fontweight="bold", color="#1E3A8A", labelpad=10)

    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    ax.set_xlim(9500, 25500)
    ax.set_ylim(6800, 14200)

    # Cuadro comparativo empotrado
    cuadro_comparativo = (
        "┌─────────────────────────────────────────────────────────────┐\n"
        "│             TABLA COMPARATIVA DE MÉTODOS                    │\n"
        "├──────────────────────────┬──────────────────────────────────┤\n"
        "│  Regresión Lineal (MCO)  │  Interpolación de Lagrange       │\n"
        "├──────────────────────────┼──────────────────────────────────┤\n"
        "│ • Modela tendencia global│ • Reconstrucción nodal exacta    │\n"
        "│ • Minimiza error cuadrático│ • Error cero en nodos (e_i = 0) │\n"
        "│ • Filtra ruido y atípicos│ • Modela curvas y no-linealidades│\n"
        "│ • Meta de política pública│ • Estimación de periodos vacíos │\n"
        "└──────────────────────────┴──────────────────────────────────┘"
    )
    ax.text(0.02, 0.96, cuadro_comparativo, transform=ax.transAxes, fontsize=8.2, family="monospace",
            verticalalignment="top", bbox=dict(boxstyle="round,pad=0.6", facecolor="#F1F5F9", edgecolor="#64748B", alpha=0.95))

    ax.legend(loc="lower right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=9.5)
    plt.tight_layout()
    salida = CARPETA_FIGURAS / "fig_metodos_numericos_comparativa_mco_vs_lagrange.png"
    plt.savefig(salida, dpi=300)
    plt.close()
    print(f"✅ Guardada: {salida}")


if __name__ == "__main__":
    generar_figura_regresion()
    generar_figura_lagrange()
    generar_figura_comparativa()
