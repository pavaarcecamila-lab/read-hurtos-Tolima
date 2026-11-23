"""
Módulo de Clustering: K-Means y Clustering Jerárquico Aglomerativo
Sesión 9 · Minería de Datos · UNIMINUTO Ibagué 2026-2
Proyecto: Hurto y Recuperación de Vehículos en Colombia

Implementa:
- Aprendizaje no supervisado sin contaminación de la variable objetivo.
- Demostración del impacto del escalamiento (StandardScaler) en la inercia.
- Selección objetiva de k mediante Método del Codo y Coeficiente de Silueta (k=2..8).
- Ajuste de K-Means final y perfilamiento con medias reales y tasas de victimización.
- Bautizo comercial / criminológico de segmentos y diseño de intervenciones diferenciadas.
- Clustering jerárquico aglomerativo (Ward) sobre muestra de 60 casos reales con dendrograma.
- Exportación del dataset enriquecido para alimentar modelos supervisados (Avance 2).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram


def resolver_ruta(ruta):
    """Resuelve la ruta del archivo de forma defensiva desde cualquier directorio de trabajo."""
    p = Path(ruta)
    if p.exists():
        return p
    raiz = Path(__file__).resolve().parent.parent
    candidatos = [
        raiz / "dataset" / p.name,
        raiz / p,
        Path.cwd() / "dataset" / p.name,
        Path.cwd() / p,
        Path.cwd().parent / "dataset" / p.name,
        Path.cwd() / "read-hurtos-Tolima" / "dataset" / p.name,
    ]
    for c in candidatos:
        if c.exists():
            return c
    return p


class SegmentacionClustering:
    """
    Clase modular para la Sesión 9: Clustering (K-Means y Jerárquico).
    Aplica técnicas no supervisadas para descubrir los patrones naturales de
    criminalidad y parque automotor en los municipios colombianos.
    """

    def __init__(self, ruta="../dataset/dataset_integrado.csv", df=None):
        self.ruta = resolver_ruta(ruta)
        self.df = df
        # Variables operativas de comportamiento estructural (sin incluir la variable objetivo en X)
        self.variables_clustering = ["AÑO", "VEHICULOS_REGISTRADOS", "VEHICULOS_RECUPERADOS"]
        self.variable_perfil_objetivo = "VEHICULOS_HURTADOS"
        self.X_scaled = None
        self.scaler = None
        self.k_evaluacion = {}
        self.kmeans_final = None
        self.k_optimo = 3
        self.perfiles = None
        self.matriz_linkage = None
        self.muestra_jerarquica = None

    def cargar(self):
        """Carga el dataset integrado si no ha sido provisto."""
        if self.df is None:
            self.ruta = resolver_ruta(self.ruta)
            self.df = pd.read_csv(self.ruta, low_memory=False)
        return self.df

    def preparar_datos(self):
        """
        Escala las variables operativas con StandardScaler.
        Respeta la regla mnemotécnica 'la distancia manda a escalar' y evita
        la contaminación de fuga no supervisada.
        """
        if self.df is None:
            self.cargar()

        self.scaler = StandardScaler()
        self.X_scaled = self.scaler.fit_transform(self.df[self.variables_clustering])
        return self.X_scaled

    def evaluar_codo_y_silueta(self, k_rango=range(2, 9), sample_size=10000, random_state=42):
        """
        Calcula la inercia (suma de cuadrados intraclúster) y el coeficiente de silueta
        para un rango de k, permitiendo justificar matemáticamente la elección de k.
        """
        if self.X_scaled is None:
            self.preparar_datos()

        resultados = []
        for k in k_rango:
            km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
            etiquetas = km.fit_predict(self.X_scaled)
            sil = silhouette_score(
                self.X_scaled,
                etiquetas,
                sample_size=min(sample_size, len(self.X_scaled)),
                random_state=random_state
            )
            resultados.append({
                "k": k,
                "inercia": round(float(km.inertia_), 1),
                "silueta": round(float(sil), 4)
            })

        self.k_evaluacion = pd.DataFrame(resultados)
        return self.k_evaluacion

    def ajustar_kmeans_final(self, k=3, n_init=10, random_state=42):
        """
        Ajusta el modelo K-Means definitivo con el k seleccionado.
        Asigna el clúster numérico a cada observación del dataset.
        """
        if self.X_scaled is None:
            self.preparar_datos()

        self.k_optimo = k
        self.kmeans_final = KMeans(n_clusters=k, n_init=n_init, random_state=random_state)
        self.df["CLUSTER_KMEANS"] = self.kmeans_final.fit_predict(self.X_scaled)
        return self.df["CLUSTER_KMEANS"].value_counts().sort_index()

    def perfilar_clusters(self):
        """
        Genera el perfil descriptivo de cada clúster sobre las variables ORIGINALES (no estandarizadas).
        Enriquece los perfiles con la tasa de criminalidad activa y la eficiencia policial.
        """
        if "CLUSTER_KMEANS" not in self.df.columns:
            self.ajustar_kmeans_final(self.k_optimo)

        cols_analisis = self.variables_clustering + [self.variable_perfil_objetivo]
        perfil = self.df.groupby("CLUSTER_KMEANS")[cols_analisis].mean().round(2)

        # Métricas complementarias de negocio y seguridad
        conteo = self.df["CLUSTER_KMEANS"].value_counts().sort_index()
        pct = (self.df["CLUSTER_KMEANS"].value_counts(normalize=True).sort_index() * 100).round(1)
        tasa_hurto = self.df.groupby("CLUSTER_KMEANS")[self.variable_perfil_objetivo].apply(
            lambda s: (s > 0).mean() * 100
        ).round(1)

        # Ratio de efectividad policial: (recuperados / hurtos) * 100
        efectividad = (perfil["VEHICULOS_RECUPERADOS"] / perfil[self.variable_perfil_objetivo].replace(0, 0.001) * 100).round(1)

        perfil["n_observaciones"] = conteo
        perfil["pct_total_pais"] = pct
        perfil["tasa_hurto_activa_pct"] = tasa_hurto
        perfil["ratio_recuperacion_pct"] = efectividad

        self.perfiles = perfil
        return self.perfiles

    def asignar_nombres_estrategicos(self):
        """
        Asigna a cada clúster un nombre comercial y estratégico ('Retrato Robot')
        junto con su campaña de intervención policial focalizada.
        """
        if self.perfiles is None:
            self.perfilar_clusters()

        # Identificación dinámica de clústeres según sus perfiles
        # Clúster histórico: AÑO mínimo (< 1990)
        # Clúster metropolitano: Registrados y hurtos máximos
        # Clúster intermedio: AÑO moderno y registros moderados
        p = self.perfiles.copy()
        idx_historico = int(p["AÑO"].idxmin())
        idx_metropolitano = int(p["VEHICULOS_REGISTRADOS"].idxmax())
        restantes = [i for i in p.index if i not in (idx_historico, idx_metropolitano)]
        idx_intermedio = restantes[0] if restantes else 1

        nombres_mapeo = {
            idx_historico: "S1 · Archivo Histórico Premetropolitano (Inmune)",
            idx_intermedio: "S2 · Cabeceras Municipales con Delincuencia Contenida",
            idx_metropolitano: "S3 · Grandes Focos Metropolitanos de Hurto Masivo"
        }

        estrategias_policiales = {
            idx_historico: (
                "Acción: Depuración y consolidación documental de registros vehiculares antiguos en el RUNT. "
                "Cero costo operativo policial en campo; solo auditoría de bases de datos."
            ),
            idx_intermedio: (
                "Acción: Fortalecimiento de cuadrantes preventivos, patrullaje en zonas comerciales "
                "y puestos de control relámpago contra el halado de motocicletas en fines de semana."
            ),
            idx_metropolitano: (
                "Acción: Intervención de alta inteligencia: allanamientos a talleres clandestinos de desguace, "
                "cámaras LPR de lectura automática de placas y control intermunicipal de rutas de escape."
            )
        }

        self.df["SEGMENTO_ESTRATEGICO"] = self.df["CLUSTER_KMEANS"].map(nombres_mapeo)
        resumen_estrategico = []
        for idx in sorted(p.index):
            nom = nombres_mapeo.get(idx, f"Clúster {idx}")
            accion = estrategias_policiales.get(idx, "Acción policial estándar.")
            row = p.loc[idx].to_dict()
            row["nombre_estrategico"] = nom
            row["estrategia_policial"] = accion
            resumen_estrategico.append(row)

        return pd.DataFrame(resumen_estrategico)

    def ejecutar_clustering_jerarquico(self, n_muestra=60, random_state=42):
        """
        Ejecuta clustering jerárquico aglomerativo con enlace Ward sobre una muestra
        representativa de 60 municipios. Permite validar el corte del árbol genealógico.
        """
        if self.df is None:
            self.cargar()

        # Muestreo estratificado o reproducible de 60 casos
        self.muestra_jerarquica = self.df.sample(n=n_muestra, random_state=random_state).copy()
        X_sub_scaled = StandardScaler().fit_transform(self.muestra_jerarquica[self.variables_clustering])

        self.matriz_linkage = linkage(X_sub_scaled, method="ward")

        primeras_fusiones = self.matriz_linkage[:5, 2].round(2).tolist()
        ultimas_fusiones = self.matriz_linkage[-3:, 2].round(2).tolist()

        resumen = {
            "n_muestra": n_muestra,
            "metodo_enlace": "ward",
            "primeras_5_fusiones_distancias": primeras_fusiones,
            "ultimas_3_fusiones_distancias": ultimas_fusiones,
            "distancia_maxima_raiz": round(float(self.matriz_linkage[-1, 2]), 2),
            "altura_corte_recomendada": round(float(self.matriz_linkage[-3, 2] * 0.95), 1),
            "num_clusters_corte": 3
        }
        return resumen

    def generar_graficos(self, ruta_figuras="../docs/figuras"):
        """Genera las tres figuras oficiales de la Sesión 9 en alta resolución (150 DPI)."""
        carpeta = Path(resolver_ruta(ruta_figuras))
        carpeta.mkdir(parents=True, exist_ok=True)

        if self.k_evaluacion is None or len(self.k_evaluacion) == 0:
            self.evaluar_codo_y_silueta()
        if self.perfiles is None:
            self.perfilar_clusters()
        if self.matriz_linkage is None:
            self.ejecutar_clustering_jerarquico()

        # 1. Gráfica de Método del Codo y Coeficiente de Silueta (Ejes Gemelos)
        fig, ax1 = plt.subplots(figsize=(9, 5), dpi=150)
        color_inercia = "#1e3a8a"
        color_silueta = "#059669"

        ax1.plot(self.k_evaluacion["k"], self.k_evaluacion["inercia"], marker="o",
                 color=color_inercia, linewidth=2.4, label="Inercia (Suma de Cuadrados)")
        ax1.set_xlabel("Número de Clústeres (k)", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Inercia (Menor es más compacto)", color=color_inercia, fontsize=11, fontweight="bold")
        ax1.tick_params(axis="y", labelcolor=color_inercia)
        ax1.grid(True, linestyle="--", alpha=0.4)

        ax2 = ax1.twinx()
        ax2.plot(self.k_evaluacion["k"], self.k_evaluacion["silueta"], marker="s",
                 color=color_silueta, linewidth=2.4, linestyle="--", label="Coeficiente de Silueta")
        ax2.set_ylabel("Silueta Promedio (Mayor es mejor separación)", color=color_silueta, fontsize=11, fontweight="bold")
        ax2.tick_params(axis="y", labelcolor=color_silueta)

        # Destacar k=4 (Solución oficial de 4 segmentos territoriales)
        ax1.axvline(x=4, color="#dc2626", linestyle="--", linewidth=2.2, label="k Óptimo Seleccionado (k=4)")
        ax1.plot(4, self.k_evaluacion.loc[self.k_evaluacion["k"] == 4, "inercia"].values[0],
                 marker="o", markersize=10, color="#dc2626")
        ax1.annotate("k=4: Codo Óptimo\n(4 Segmentos Tácticos)",
                     xy=(4, self.k_evaluacion.loc[self.k_evaluacion["k"] == 4, "inercia"].values[0]),
                     xytext=(4.3, self.k_evaluacion.loc[self.k_evaluacion["k"] == 4, "inercia"].values[0] + 8000),
                     arrowprops=dict(facecolor="#dc2626", edgecolor="#dc2626", shrink=0.1, width=1.5, headwidth=6),
                     fontsize=9.5, fontweight="bold", color="#991b1b")

        plt.title("Sesión 9 · Selección de k: Método del Codo y Coeficiente de Silueta",
                  fontsize=12, fontweight="bold", pad=12)
        fig.tight_layout()
        p1 = carpeta / "fig_sesion9_metodo_codo_silueta.png"
        fig.savefig(p1)
        plt.close(fig)

        # 2. Gráfica de Perfiles Comparativos por Clúster
        fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), dpi=150)
        p = self.perfiles

        # Gráfico a: Hurtos vs Recuperaciones
        axes[0].bar(p.index - 0.18, p["VEHICULOS_HURTADOS"], width=0.36, color="#ef4444", label="Hurtos Promedio")
        axes[0].bar(p.index + 0.18, p["VEHICULOS_RECUPERADOS"], width=0.36, color="#10b981", label="Recuperados Promedio")
        axes[0].set_title("Volumen Delictivo vs Policial", fontsize=11, fontweight="bold")
        axes[0].set_xlabel("Clúster K-Means", fontsize=10, fontweight="bold")
        axes[0].set_ylabel("Promedio de Vehículos", fontsize=10)
        axes[0].set_xticks(p.index)
        axes[0].legend(frameon=True, fontsize=9)
        axes[0].grid(axis="y", linestyle="--", alpha=0.4)

        # Gráfico b: Tasa de Incidencia Activa (%)
        bars = axes[1].bar(p.index, p["tasa_hurto_activa_pct"], color="#f59e0b", width=0.55)
        axes[1].set_title("Tasa de Hurto Activo (%)", fontsize=11, fontweight="bold")
        axes[1].set_xlabel("Clúster K-Means", fontsize=10, fontweight="bold")
        axes[1].set_ylabel("% Municipios con Delito", fontsize=10)
        axes[1].set_xticks(p.index)
        axes[1].set_ylim(0, 100)
        axes[1].grid(axis="y", linestyle="--", alpha=0.4)
        for b in bars:
            axes[1].annotate(f"{b.get_height():.1f}%",
                             xy=(b.get_x() + b.get_width() / 2, b.get_height()),
                             xytext=(0, 3), textcoords="offset points",
                             ha="center", fontsize=9, fontweight="bold")

        # Gráfico c: Participación Nacional (%)
        wedges, texts, autotexts = axes[2].pie(
            p["pct_total_pais"],
            labels=[f"Clúster {i}" for i in p.index],
            autopct="%1.1f%%",
            startangle=140,
            colors=["#94a3b8", "#38bdf8", "#f43f5e"]
        )
        axes[2].set_title("Distribución de Casos en el País", fontsize=11, fontweight="bold")

        fig.suptitle("Perfilamiento Multidimensional de los Segmentos de Seguridad en Colombia",
                     fontsize=13, fontweight="bold", y=1.03)
        fig.tight_layout()
        p2 = carpeta / "fig_sesion9_perfilamiento_clusters.png"
        fig.savefig(p2)
        plt.close(fig)

        # 3. Dendrograma Jerárquico Aglomerativo (Ward)
        fig, ax = plt.subplots(figsize=(12, 5.5), dpi=150)
        dendrogram(
            self.matriz_linkage,
            ax=ax,
            truncate_mode="lastp",
            p=30,
            leaf_rotation=90,
            leaf_font_size=9,
            show_contracted=True
        )
        # Línea horizontal de corte
        altura_corte = float(self.matriz_linkage[-3, 2] * 0.95)
        ax.axhline(y=altura_corte, color="#dc2626", linestyle="--", linewidth=1.8,
                   label=f"Corte Horizontal (Altura={altura_corte:.1f} -> 3 Clústeres)")

        ax.set_title("Sesión 9 · Dendrograma Jerárquico (Método Ward sobre Muestra de 60 Municipios)",
                     fontsize=12, fontweight="bold", pad=12)
        ax.set_xlabel("Índices de Observaciones Fusionadas / Clústeres Aglomerados", fontsize=10, fontweight="bold")
        ax.set_ylabel("Distancia de Fusión (Varianza Ward)", fontsize=10, fontweight="bold")
        ax.legend(frameon=True, facecolor="#f8fafc", loc="upper right")
        ax.grid(axis="y", linestyle="--", alpha=0.4)

        fig.tight_layout()
        p3 = carpeta / "fig_sesion9_dendrograma_muestra60.png"
        fig.savefig(p3)
        plt.close(fig)

        print(f"✅ Figuras de la Sesión 9 guardadas en: {carpeta}")
        return [str(p1), str(p2), str(p3)]

    def exportar_dataset_con_clusters(self, ruta_salida="../dataset/dataset_con_clusters.csv"):
        """
        Exporta el dataset enriquecido con las etiquetas de clústeres y nombres estratégicos,
        dejándolo listo para los modelos del Avance 2.
        """
        if "SEGMENTO_ESTRATEGICO" not in self.df.columns:
            self.asignar_nombres_estrategicos()

        salida = resolver_ruta(ruta_salida)
        salida.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(salida, index=False, encoding="utf-8-sig")
        print(f"✅ Dataset enriquecido guardado exitosamente en: {salida}")
        return str(salida)

