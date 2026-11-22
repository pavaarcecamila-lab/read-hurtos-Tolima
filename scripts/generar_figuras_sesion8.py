"""
Generador de Figuras Oficiales para la Sesión 8: Torneo de Clasificación
(Árbol de Decisión vs Naive Bayes vs KNN)
Minería de Datos · UNIMINUTO Sede Ibagué · 2026-2
Docente: Esteban Ernesto Morales Castro
"""

import os
import sys
from pathlib import Path

# Configurar entorno para matplotlib en sandbox
os.environ["MPLCONFIGDIR"] = "/tmp/mpl"
local_pkgs = Path(__file__).resolve().parent.parent.parent / ".local_python" / "lib" / "python3.11" / "site-packages"
if local_pkgs.exists() and str(local_pkgs) not in sys.path:
    sys.path.insert(0, str(local_pkgs))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Estilo visual corporativo / académico
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

CARPETA_FIGURAS = Path(__file__).resolve().parent.parent / "docs" / "figuras"
CARPETA_FIGURAS.mkdir(parents=True, exist_ok=True)

# 1. Cargar y preparar datos
ruta_csv = Path(__file__).resolve().parent.parent / "dataset" / "dataset_integrado.csv"
df = pd.read_csv(ruta_csv)
num = ["AÑO", "VEHICULOS_REGISTRADOS", "VEHICULOS_RECUPERADOS"]
X = pd.get_dummies(df[num + ["TIPO_VEHICULO"]], columns=["TIPO_VEHICULO"], drop_first=True)
y = (df["VEHICULOS_HURTADOS"] > 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"Dataset cargado: {len(df):,} filas. Train: {len(X_train):,}, Test: {len(X_test):,}")


# ==============================================================================
# FIGURA 1: TORNEO DE CLASIFICACIÓN (Accuracy Train vs Test y Métricas)
# ==============================================================================
def generar_figura_torneo():
    print("Generando Figura 1: Torneo de Clasificación...")
    modelos = {
        "Árbol (prof=4)": DecisionTreeClassifier(max_depth=4, random_state=42),
        "Naive Bayes": GaussianNB(),
        "KNN (k=5, Sin Escala)": KNeighborsClassifier(n_neighbors=5),
        "KNN (k=5, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
        "KNN (k=31, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=31)),
    }

    nombres = []
    acc_tr_l = []
    acc_te_l = []
    rec_l = []
    f1_l = []

    for nom, mod in modelos.items():
        mod.fit(X_train, y_train)
        pred = mod.predict(X_test)
        nombres.append(nom)
        acc_tr_l.append(mod.score(X_train, y_train) * 100)
        acc_te_l.append(accuracy_score(y_test, pred) * 100)
        rec_l.append(recall_score(y_test, pred) * 100)
        f1_l.append(f1_score(y_test, pred) * 100)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Panel 1: Accuracy Train vs Test
    x = np.arange(len(nombres))
    ancho = 0.35

    bar1 = ax1.bar(x - ancho/2, acc_tr_l, ancho, label="Train (Entrenamiento 75%)", color="#1f77b4", alpha=0.9)
    bar2 = ax1.bar(x + ancho/2, acc_te_l, ancho, label="Test (Prueba 25%)", color="#2ca02c", alpha=0.9)

    ax1.set_title("Comparativa de Exactitud (Train vs Test)\nSesión 8 · Minería de Datos", fontsize=12, fontweight="bold", pad=12)
    ax1.set_ylabel("Accuracy (%)", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(nombres, rotation=20, ha="right", fontsize=9)
    ax1.set_ylim(60, 95)
    ax1.legend(loc="upper right", frameon=True)
    ax1.axhline(82.0, color="#d62728", linestyle="--", linewidth=1.2, label="Línea Base Sesión 7 (82.0%)")

    for b in bar1:
        h = b.get_height()
        ax1.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")
    for b in bar2:
        h = b.get_height()
        ax1.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#1b5e20")

    # Panel 2: Recall y F1-Score (Efectividad Policial)
    bar_rec = ax2.bar(x - ancho/2, rec_l, ancho, label="Recall / Sensibilidad (Detección)", color="#ff7f0e", alpha=0.9)
    bar_f1 = ax2.bar(x + ancho/2, f1_l, ancho, label="F1-Score (Balance Armónico)", color="#9467bd", alpha=0.9)

    ax2.set_title("Efectividad Criminológica (Recall y F1-Score)\n¿Quién detecta más delitos activos?", fontsize=12, fontweight="bold", pad=12)
    ax2.set_ylabel("Puntaje (%)", fontsize=11, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(nombres, rotation=20, ha="right", fontsize=9)
    ax2.set_ylim(45, 100)
    ax2.legend(loc="lower right", frameon=True)

    for b in bar_rec:
        h = b.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")
    for b in bar_f1:
        h = b.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")

    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "fig_torneo_clasificacion.png"
    plt.savefig(ruta_salida, bbox_inches="tight")
    plt.close()
    print(f"  -> Guardada: {ruta_salida}")


# ==============================================================================
# FIGURA 2: MATRICES DE CONFUSIÓN COMPARADAS
# ==============================================================================
def generar_figura_matrices_confusion():
    print("Generando Figura 2: Matrices de Confusión...")
    modelos_clave = {
        "1. Árbol de Decisión (prof=4)\n[GANADOR OFICIAL]": DecisionTreeClassifier(max_depth=4, random_state=42),
        "2. KNN (k=31, StandardScaler)\n[2° LUGAR ANALÍTICO]": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=31)),
        "3. Naive Bayes (GaussianNB)\n[DESCARTADO: 45.6% FN]": GaussianNB()
    }

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300)

    for idx, (titulo, mod) in enumerate(modelos_clave.items()):
        mod.fit(X_train, y_train)
        preds = mod.predict(X_test)
        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel()
        rec = tp / (tp + fn) * 100
        tasa_fn = fn / (tp + fn) * 100

        cmap = "Greens" if idx == 0 else ("Blues" if idx == 1 else "Reds")
        sns.heatmap(cm, annot=True, fmt=",d", cmap=cmap, cbar=False, ax=axes[idx],
                    xticklabels=["0: Sin Hurto", "1: Hurto Activo"],
                    yticklabels=["0: Sin Hurto", "1: Hurto Activo"],
                    annot_kws={"size": 11, "weight": "bold"})

        axes[idx].set_title(titulo, fontsize=11, fontweight="bold", pad=10)
        axes[idx].set_xlabel("Predicción del Modelo", fontsize=10, fontweight="bold")
        axes[idx].set_ylabel("Valor Real Histórico", fontsize=10, fontweight="bold")

        # Texto informativo bajo la matriz
        info_text = (
            f"Sensibilidad (Recall): {rec:.2f}%\n"
            f"Falsos Negativos (FN): {fn:,} ({tasa_fn:.1f}%)\n"
            f"Falsos Positivos (FP): {fp:,}"
        )
        axes[idx].text(0.5, -0.28, info_text, transform=axes[idx].transAxes,
                       ha="center", va="center", fontsize=9,
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8f9fa", edgecolor="#ced4da"))

    plt.suptitle("Matrices de Confusión en Test (13.607 Observaciones)\nEvaluación del Riesgo de Omisión Delictiva",
                 fontsize=13, fontweight="bold", y=1.05)
    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "fig_matrices_confusion_torneo.png"
    plt.savefig(ruta_salida, bbox_inches="tight")
    plt.close()
    print(f"  -> Guardada: {ruta_salida}")


# ==============================================================================
# FIGURA 3: CURVA DE SESGO-VARIANZA EN KNN (EFECTO DE K)
# ==============================================================================
def generar_figura_curva_k():
    print("Generando Figura 3: Curva de k en KNN...")
    k_valores = [1, 3, 5, 9, 15, 21, 31, 41, 51, 71, 101]
    pipe = make_pipeline(StandardScaler(), KNeighborsClassifier())

    tr_scores = []
    te_scores = []

    for k in k_valores:
        pipe.set_params(kneighborsclassifier__n_neighbors=k)
        pipe.fit(X_train, y_train)
        tr_scores.append(pipe.score(X_train, y_train) * 100)
        te_scores.append(pipe.score(X_test, y_test) * 100)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    ax.plot(k_valores, tr_scores, marker="o", color="#1f77b4", linewidth=2.2, label="Accuracy Train (Entrenamiento 75%)")
    ax.plot(k_valores, te_scores, marker="s", color="#2ca02c", linewidth=2.5, label="Accuracy Test (Prueba 25%)")

    # Resaltar punto óptimo
    idx_opt = k_valores.index(31)
    ax.scatter([31], [te_scores[idx_opt]], color="#d62728", s=140, zorder=5)
    ax.annotate("PUNTO ÓPTIMO: k=31\nTest: 82.55% | Brecha: 1.51%",
                xy=(31, te_scores[idx_opt]), xytext=(40, 80.8),
                arrowprops=dict(facecolor="#d62728", shrink=0.08, width=1.5, headwidth=7),
                fontsize=9.5, fontweight="bold", color="#b71c1c",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor="#ef9a9a"))

    # Zonas de sobreajuste y subajuste
    ax.axvspan(1, 7, color="#ffebee", alpha=0.5, label="Zona de Sobreajuste (Overfitting: k pequeño)")
    ax.axvspan(11, 45, color="#e8f5e9", alpha=0.5, label="Zona Óptima de Generalización")
    ax.axvspan(60, 101, color="#fff3e0", alpha=0.5, label="Zona de Subajuste (Underfitting: dilución)")

    ax.set_title("Efecto del Hiperparámetro k en KNeighborsClassifier (StandardScaler)\nDilema Sesgo-Varianza en Hurto Vehicular",
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Número de Vecinos (k)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Accuracy (%)", fontsize=11, fontweight="bold")
    ax.set_xticks(k_valores)
    ax.set_ylim(76, 89)
    ax.legend(loc="upper right", frameon=True)

    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "fig_curva_k_knn.png"
    plt.savefig(ruta_salida, bbox_inches="tight")
    plt.close()
    print(f"  -> Guardada: {ruta_salida}")


# ==============================================================================
# FIGURA 4: RADAR DE DECISIÓN MULTICRITERIO
# ==============================================================================
def generar_figura_radar_tradeoff():
    print("Generando Figura 4: Radar Multicriterio de Decisión...")
    criterios = [
        "Exactitud Test\n(Accuracy)",
        "Sensibilidad\n(Recall Policial)",
        "Explicabilidad\n(Caja Blanca)",
        "Velocidad Inferencia\n(Baja Latencia)",
        "Inmunidad a\nOutliers"
    ]
    num_criterios = len(criterios)

    # Puntuaciones normalizadas de 0 a 10
    # Árbol: Acc=8.3, Rec=9.0, Explic=10, Vel=9.8, Outliers=9.5
    # KNN:   Acc=8.3, Rec=8.7, Explic=5.0, Vel=3.0, Outliers=7.0
    # NB:    Acc=7.0, Rec=5.4, Explic=4.0, Vel=9.9, Outliers=4.0
    scores = {
        "Árbol de Decisión (prof=4)": [8.3, 9.0, 10.0, 9.8, 9.5],
        "KNN (k=31 Escalado)":        [8.3, 8.7, 5.0, 3.0, 7.0],
        "Naive Bayes (GaussianNB)":   [7.0, 5.4, 4.0, 9.9, 4.0],
    }

    angulos = np.linspace(0, 2 * np.pi, num_criterios, endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True), dpi=300)

    colores = {"Árbol de Decisión (prof=4)": "#2ca02c", "KNN (k=31 Escalado)": "#1f77b4", "Naive Bayes (GaussianNB)": "#d62728"}

    for modelo, valores in scores.items():
        vals = valores + valores[:1]
        ax.plot(angulos, vals, linewidth=2.2, label=modelo, color=colores[modelo])
        ax.fill(angulos, vals, alpha=0.15, color=colores[modelo])

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(criterios, fontsize=9.5, fontweight="bold")
    ax.set_rlabel_position(30)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color="#666666", fontsize=8)
    ax.set_ylim(0, 10)

    ax.set_title("Evaluación Multicriterio de Modelos\n¿Por qué el Árbol gana el contrato analítico?",
                 fontsize=12, fontweight="bold", pad=24)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), frameon=True)

    plt.tight_layout()
    ruta_salida = CARPETA_FIGURAS / "fig_radar_tradeoff_modelos.png"
    plt.savefig(ruta_salida, bbox_inches="tight")
    plt.close()
    print(f"  -> Guardada: {ruta_salida}")


if __name__ == "__main__":
    generar_figura_torneo()
    generar_figura_matrices_confusion()
    generar_figura_curva_k()
    generar_figura_radar_tradeoff()
    print("\n✅ ¡Todas las figuras de la Sesión 8 fueron generadas exitosamente!")

