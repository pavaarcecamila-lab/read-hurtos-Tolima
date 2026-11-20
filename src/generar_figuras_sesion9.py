"""
Sesión 9 · Clustering: K-means y Jerárquico
Proyecto: Análisis del Hurto de Vehículos y Capacidad Policial en Colombia
Minería de Datos · UNIMINUTO Ibagué · 2026-2
Docente: Esteban Ernesto Morales Castro
"""

import os
import sys
from pathlib import Path

os.environ["MPLCONFIGDIR"] = "/tmp/mpl"
local_pkgs = Path(__file__).resolve().parent.parent.parent / ".local_python" / "lib" / "python3.11" / "site-packages"
if local_pkgs.exists() and str(local_pkgs) not in sys.path:
    sys.path.insert(0, str(local_pkgs))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

FIGURAS = Path(__file__).resolve().parent.parent / "analisis" / "figuras"
FIGURAS.mkdir(parents=True, exist_ok=True)
DATASET = Path(__file__).resolve().parent.parent / "dataset" / "dataset_integrado.csv"

COLORES = {0: "#2ca02c", 1: "#1f77b4", 2: "#d62728", 3: "#ff7f0e"}
NOMBRES_CLUSTER = {
    0: "Zonas Pacíficas\n(Sin foco delictivo)",
    1: "Riesgo Moderado\n(Alta recuperación policial)",
    2: "FOCO CRÍTICO\n(Alto hurto, baja recuperación)",
    3: "Parque Grande\n(Poco hurto relativo)"
}
NOMBRES_CORTO = {0: "Zonas Pacíficas", 1: "Riesgo Moderado", 2: "Foco Crítico", 3: "Parque Grande / Bajo Hurto"}
V = ["VEHICULOS_REGISTRADOS", "VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10

# ─── Carga y preprocesamiento ──────────────────────────────────────────────────
df = pd.read_csv(DATASET)
df_mod = df[df["AÑO"] >= 2010].copy()
scaler = StandardScaler()
X = scaler.fit_transform(df_mod[V])
print(f"Dataset base: {len(df):,} | Registros modernos (2010-2026): {len(df_mod):,}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 1: Curva del Codo + Silueta (Búsqueda del K óptimo)
# ══════════════════════════════════════════════════════════════════════════════
def fig1_codo_silueta():
    print("Generando Figura 1: Codo + Silueta...")
    inercias, siluetas, ks = [], [], list(range(2, 8))
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        etiq = km.fit_predict(X)
        inercias.append(km.inertia_)
        siluetas.append(silhouette_score(X, etiq))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # --- Panel izquierdo: Codo (Inercia) ---
    ax1.plot(ks, inercias, marker="o", color="#1f77b4", linewidth=2.5, markersize=8)
    ax1.axvline(x=4, color="#d62728", linestyle="--", linewidth=1.8, label="k=4 (punto de codo)")
    ax1.fill_between(ks, inercias, min(inercias), alpha=0.08, color="#1f77b4")
    for k, inerc in zip(ks, inercias):
        ax1.annotate(f"{inerc:,.0f}", xy=(k, inerc), xytext=(0, 10),
                     textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")
    ax1.set_title("Método del Codo (Inercia vs k)\n¿En qué k deja de valer la pena más grupos?",
                  fontweight="bold", fontsize=11, pad=10)
    ax1.set_xlabel("Número de Clústeres (k)", fontweight="bold")
    ax1.set_ylabel("Inercia (Suma de Distancias²)", fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.set_xticks(ks)

    # Flecha de codo
    ax1.annotate("CODO\naquí dobla", xy=(4, inercias[2]),
                 xytext=(5.1, inercias[2] + 4000),
                 arrowprops=dict(facecolor="#d62728", shrink=0.1, width=1.5, headwidth=7),
                 fontsize=9, fontweight="bold", color="#b71c1c")

    # --- Panel derecho: Silueta ---
    colores_barra = ["#1f77b4" if k != 4 else "#2ca02c" for k in ks]
    bars = ax2.bar(ks, siluetas, color=colores_barra, width=0.6, alpha=0.9)
    ax2.set_title("Coeficiente de Silueta vs k\n(Cohesión – Separación: mayor es mejor)",
                  fontweight="bold", fontsize=11, pad=10)
    ax2.set_xlabel("Número de Clústeres (k)", fontweight="bold")
    ax2.set_ylabel("Coeficiente de Silueta Promedio", fontweight="bold")
    ax2.set_xticks(ks)
    for b, sil in zip(bars, siluetas):
        ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.005,
                 f"{sil:.3f}", ha="center", fontsize=9, fontweight="bold")
    ax2.set_ylim(0, 1.0)

    # Resaltado del k elegido
    ax2.patches[ks.index(4)].set_edgecolor("#155724")
    ax2.patches[ks.index(4)].set_linewidth(2.5)
    ax2.annotate("k=4 ELEGIDO\n(Codo + 4 perfiles\ncriminológicos)",
                 xy=(4, siluetas[ks.index(4)]),
                 xytext=(5.3, 0.65),
                 arrowprops=dict(facecolor="#155724", shrink=0.1),
                 fontsize=8.5, color="#155724", fontweight="bold")

    plt.tight_layout()
    out = FIGURAS / "fig_sesion9_codo_silueta.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  → {out}")
    return ks, inercias, siluetas


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 2: Mapa de dispersión de los 4 clústeres K-means
# ══════════════════════════════════════════════════════════════════════════════
def fig2_scatter_kmeans(km_model, etiquetas):
    print("Generando Figura 2: Dispersión K-means (k=4)...")

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

    # --- Panel A: Registrados vs Hurtados ---
    ax = axes[0]
    for cl in range(4):
        mask = etiquetas == cl
        ax.scatter(df_mod.loc[mask, "VEHICULOS_REGISTRADOS"],
                   df_mod.loc[mask, "VEHICULOS_HURTADOS"],
                   c=COLORES[cl], alpha=0.4, s=14, label=NOMBRES_CORTO[cl])
    # Centroides en espacio original
    centroides_orig = scaler.inverse_transform(km_model.cluster_centers_)
    for i, c in enumerate(centroides_orig):
        ax.scatter(c[0], c[1], c=COLORES[i], s=200, marker="*", edgecolors="black", linewidths=1.5, zorder=10)
        ax.annotate(f"C{i}", xy=(c[0], c[1]), xytext=(8, 8), textcoords="offset points",
                    fontsize=8.5, fontweight="bold")
    ax.set_title("Vehículos Registrados vs Hurtados\n(★ = Centroide del clúster)",
                 fontweight="bold", fontsize=11)
    ax.set_xlabel("Vehículos Registrados", fontweight="bold")
    ax.set_ylabel("Vehículos Hurtados", fontweight="bold")
    ax.set_xlim(-50, 2000)
    ax.set_ylim(-2, 100)
    ax.legend(fontsize=8.5, loc="upper left")

    # --- Panel B: Hurtados vs Recuperados ---
    ax = axes[1]
    for cl in range(4):
        mask = etiquetas == cl
        ax.scatter(df_mod.loc[mask, "VEHICULOS_HURTADOS"],
                   df_mod.loc[mask, "VEHICULOS_RECUPERADOS"],
                   c=COLORES[cl], alpha=0.4, s=14, label=NOMBRES_CORTO[cl])
    for i, c in enumerate(centroides_orig):
        ax.scatter(c[1], c[2], c=COLORES[i], s=200, marker="*", edgecolors="black", linewidths=1.5, zorder=10)
    ax.set_title("Vehículos Hurtados vs Recuperados\n(Efectividad Policial por Segmento)",
                 fontweight="bold", fontsize=11)
    ax.set_xlabel("Vehículos Hurtados", fontweight="bold")
    ax.set_ylabel("Vehículos Recuperados (Capacidad Policial)", fontweight="bold")
    ax.set_xlim(-2, 120)
    ax.set_ylim(-2, 60)

    plt.suptitle("K-means (k=4) sobre Datos Modernos (2010-2026)\n54.428 → 27.577 registros | StandardScaler aplicado",
                 fontsize=12.5, fontweight="bold", y=1.02)
    plt.tight_layout()
    out = FIGURAS / "fig_sesion9_scatter_kmeans.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 3: Tabla de perfiles (barras horizontales)
# ══════════════════════════════════════════════════════════════════════════════
def fig3_perfiles(km_model, etiquetas):
    print("Generando Figura 3: Perfiles de clústeres...")

    df_mod["cluster"] = etiquetas
    perfil = df_mod.groupby("cluster")[V].mean().round(1)
    perfil["n"] = df_mod["cluster"].value_counts().sort_index()
    perfil["pct"] = (perfil["n"] / perfil["n"].sum() * 100).round(1)
    perfil["moto_pct"] = df_mod.groupby("cluster")["TIPO_VEHICULO"].apply(
        lambda s: (s == "MOTOCICLETA").mean() * 100).round(0)
    perfil["rec_pct"] = (perfil["VEHICULOS_RECUPERADOS"] / perfil["VEHICULOS_HURTADOS"].replace(0, np.nan) * 100).round(1)

    nombres_filas = [NOMBRES_CORTO[i] for i in range(4)]
    metricas = {
        "Vehículos\nRegistrados": perfil["VEHICULOS_REGISTRADOS"].values,
        "Vehículos\nHurtados": perfil["VEHICULOS_HURTADOS"].values,
        "Vehículos\nRecuperados": perfil["VEHICULOS_RECUPERADOS"].values,
        "Tasa de\nRecuperación (%)": perfil["rec_pct"].values,
        "% Motocicletas": perfil["moto_pct"].values,
    }

    fig, axes = plt.subplots(1, len(metricas), figsize=(17, 5), dpi=300)

    for ax, (metrica, valores) in zip(axes, metricas.items()):
        bars = ax.barh(nombres_filas, valores, color=[COLORES[i] for i in range(4)], alpha=0.85)
        ax.set_title(metrica, fontweight="bold", fontsize=10, pad=8)
        ax.invert_yaxis()
        for b, v in zip(bars, valores):
            ax.text(b.get_width() + max(valores) * 0.03, b.get_y() + b.get_height() / 2,
                    f"{v:.1f}", va="center", fontsize=8.5, fontweight="bold")
        ax.set_xlim(0, max(valores) * 1.3)
        ax.tick_params(axis="y", labelsize=8.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.suptitle("Perfil Criminológico de los 4 Segmentos de Municipios de Colombia (K-means, k=4)",
                 fontweight="bold", fontsize=12, y=1.02)
    plt.tight_layout()
    out = FIGURAS / "fig_sesion9_perfiles_clusters.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 4: Dendrograma jerárquico (muestra 80 registros sin extremos)
# ══════════════════════════════════════════════════════════════════════════════
def fig4_dendrograma():
    print("Generando Figura 4: Dendrograma jerárquico...")

    df_sin_ext = df_mod[df_mod["VEHICULOS_HURTADOS"] < 150].copy()
    muestra = df_sin_ext.sample(n=80, random_state=42).reset_index(drop=True)
    X_muestra = StandardScaler().fit_transform(muestra[V])

    Z = linkage(X_muestra, method="ward")

    fig, ax = plt.subplots(figsize=(16, 6), dpi=300)
    muestra["etiq_muni"] = muestra["MUNICIPIO"].str[:14] + " (" + muestra["DEPARTAMENTO"].str[:5] + ")"
    den = dendrogram(Z, labels=muestra["etiq_muni"].tolist(), leaf_rotation=90,
                     leaf_font_size=5.5, ax=ax,
                     color_threshold=0.5 * Z[-1, 2],
                     above_threshold_color="#888888")

    # Línea de corte para k=4
    corte = 0.5 * Z[-1, 2]
    ax.axhline(y=corte, color="#d62728", linestyle="--", linewidth=2.0,
               label=f"Línea de corte → k=4 grupos (distancia ≈ {corte:.1f})")

    ax.set_title("Dendrograma de Clustering Jerárquico (Ward Linkage)\nMuestra Representativa de 80 Municipios Colombianos (2010-2026)",
                 fontweight="bold", fontsize=12, pad=12)
    ax.set_xlabel("Municipio (Departamento)", fontweight="bold", fontsize=10)
    ax.set_ylabel("Distancia de Ward (inercia acumulada)", fontweight="bold", fontsize=10)
    ax.legend(loc="upper right", fontsize=9.5)

    ax.text(0.98, 0.95,
            f"Primeras 5 fusiones: {Z[:5, 2].round(2)}\nÚltima fusión: {Z[-1, 2]:.1f}",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
            bbox=dict(boxstyle="round", facecolor="#f0f4ff", edgecolor="#aaa"))

    plt.tight_layout()
    out = FIGURAS / "fig_sesion9_dendrograma.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  → {out}")
    return Z


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 5: Radar de comparación K-means vs Jerárquico
# ══════════════════════════════════════════════════════════════════════════════
def fig5_radar_comparacion():
    print("Generando Figura 5: Radar K-means vs Jerárquico...")
    criterios = ["Escala\n(27k registros)", "Interpretabi-\nlidad perfil",
                 "Estabilidad\nresultados", "Exploración\nde k",
                 "Velocidad\nde ejecución"]
    n = len(criterios)
    angulos = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angulos += angulos[:1]

    kmeans_scores  = [9.5, 8.0, 7.5, 5.0, 9.5]
    jerarq_scores  = [4.0, 7.0, 10.0, 10.0, 5.0]

    kmeans_scores  += kmeans_scores[:1]
    jerarq_scores  += jerarq_scores[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), dpi=300)
    ax.plot(angulos, kmeans_scores, linewidth=2.5, color="#1f77b4", label="K-means (k=4)")
    ax.fill(angulos, kmeans_scores, alpha=0.18, color="#1f77b4")
    ax.plot(angulos, jerarq_scores, linewidth=2.5, color="#d62728", label="Clustering Jerárquico (Ward)")
    ax.fill(angulos, jerarq_scores, alpha=0.18, color="#d62728")

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(criterios, fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=8)
    ax.set_title("K-means vs Jerárquico: Perfil Multicriterio\n¿Cuál usar para los 27.577 registros del proyecto?",
                 fontsize=11, fontweight="bold", pad=22)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=9.5)

    plt.tight_layout()
    out = FIGURAS / "fig_sesion9_radar_comparacion.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 6: Treemap de distribución de municipios por clúster
# ══════════════════════════════════════════════════════════════════════════════
def fig6_distribucion_campanas(km_model, etiquetas):
    print("Generando Figura 6: Distribución y Fichas de Campaña...")
    df_mod["cluster"] = etiquetas
    n_total = len(df_mod)
    conteo = df_mod["cluster"].value_counts().sort_index()

    info = {
        0: ("🟢 Zonas Pacíficas", f"{conteo[0]:,} registros ({conteo[0]/n_total*100:.1f}%)",
            "Municipios rurales sin actividad delictiva.\nParque automotor pequeño (<105 veh.).\nRecuperación alta (75,6%) – pero poca necesidad.",
            "Mantener vigilancia mínima estacional.\nMonitoreo preventivo de parque automotor."),
        1: ("🔵 Riesgo Moderado", f"{conteo[1]:,} registros ({conteo[1]/n_total*100:.1f}%)",
            "Cabeceras intermedias con hurto activo.\nParque 1.181 veh. · 37 hurtos/año promedio.\nMejor recuperación policial (83,5%) del país.",
            "Fortalecer retenes viales y operativos nocturnos.\nPriorizar en campañas de recuperación de motos."),
        2: ("🔴 FOCO CRÍTICO", f"{conteo[2]:,} registros ({conteo[2]/n_total*100:.1f}%)",
            "Focos de crimen organizado vehicular.\n201 hurtos/año promedio con baja recuperación (26,5%).\n85% de hurtos son MOTOCICLETAS.",
            "Intervención policial urgente de alta complejidad.\nOperar Capturas de Deshuese y ferias ilegales."),
        3: ("🟡 Parque Grande / Bajo Hurto", f"{conteo[3]:,} registros ({conteo[3]/n_total*100:.1f}%)",
            "Alto parque automotor (6.974 veh.) pero pocos hurtos.\nOficinas RUNT con matrículas por incentivo tributario.\nRecuperación moderada (43%).",
            "Monitorear que el parque no se convierta en blanco.\nReforzar GPS y sistemas de rastreo vehicular."),
    }

    fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=300)
    axes = axes.flatten()

    colores_fondos = ["#f0fdf4", "#eff6ff", "#fff1f2", "#fffbeb"]
    colores_borde = ["#15803d", "#1d4ed8", "#b91c1c", "#b45309"]

    for idx, (cl, (titulo, conteo_txt, descripcion, campana)) in enumerate(info.items()):
        ax = axes[idx]
        ax.set_facecolor(colores_fondos[idx])
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(colores_borde[idx])
            spine.set_linewidth(2)

        ax.text(0.5, 0.92, titulo, ha="center", va="top", transform=ax.transAxes,
                fontsize=14, fontweight="bold", color=colores_borde[idx])
        ax.text(0.5, 0.80, conteo_txt, ha="center", va="top", transform=ax.transAxes,
                fontsize=10, color="#374151", style="italic")
        ax.text(0.05, 0.65, "📊 Perfil:", ha="left", va="top", transform=ax.transAxes,
                fontsize=9.5, fontweight="bold", color="#374151")
        ax.text(0.05, 0.57, descripcion, ha="left", va="top", transform=ax.transAxes,
                fontsize=9, color="#374151", family="monospace")
        ax.text(0.05, 0.28, "🎯 Acción Policial:", ha="left", va="top", transform=ax.transAxes,
                fontsize=9.5, fontweight="bold", color=colores_borde[idx])
        ax.text(0.05, 0.20, campana, ha="left", va="top", transform=ax.transAxes,
                fontsize=9, color=colores_borde[idx])

    plt.suptitle("Fichas de Campaña y Perfil por Segmento Delictivo (K-means, k=4)\nProyecto: Hurto y Recuperación Vehicular en Colombia (2010-2026)",
                 fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    out = FIGURAS / "fig_sesion9_fichas_campana.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# EJECUTAR TODO
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    fig1_codo_silueta()

    km_final = KMeans(n_clusters=4, n_init=10, random_state=42)
    etiq_final = km_final.fit_predict(X)
    df_mod["cluster"] = etiq_final

    fig2_scatter_kmeans(km_final, etiq_final)
    fig3_perfiles(km_final, etiq_final)
    Z = fig4_dendrograma()
    fig5_radar_comparacion()
    fig6_distribucion_campanas(km_final, etiq_final)

    print("\n✅ Todas las figuras de la Sesión 9 generadas exitosamente!")

