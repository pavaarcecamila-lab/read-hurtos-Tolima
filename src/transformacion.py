import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import (
    MinMaxScaler,
    StandardScaler,
    RobustScaler,
    KBinsDiscretizer
)


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
    ]
    for c in candidatos:
        if c.exists():
            return c
    return p


class Transformacion:
    """
    Clase modular para la Sesión 4: Transformación, escalamiento y reducción de datos (PCA)
    según la metodología CRISP-DM y PEA UNIMINUTO.
    """

    def __init__(self, ruta="../dataset/dataset_integrado.csv", df=None):
        self.ruta = resolver_ruta(ruta)
        self.df = df
        self.numericas = ["AÑO", "VEHICULOS_REGISTRADOS", "VEHICULOS_RECUPERADOS"]
        self.categoricas = ["TIPO_VEHICULO", "DEPARTAMENTO"]
        self.variable_objetivo = "VEHICULOS_HURTADOS"
        self.pca_model = None
        self.df_reducido = None

    def cargar(self):
        """Carga el dataset integrado desde disco si no fue provisto en memoria."""
        if self.df is None:
            self.ruta = resolver_ruta(self.ruta)
            self.df = pd.read_csv(self.ruta, low_memory=False)
        return self.df

    def diagnosticar(self):
        """Diagnóstico inicial de variables y dimensiones."""
        if self.df is None:
            self.cargar()
        print("Dimensiones:", f"{self.df.shape[0]:,} filas × {self.df.shape[1]} columnas")
        print("\nVariables continuas predictoras:", self.numericas)
        print("Variables categóricas:", self.categoricas)
        print("Variable objetivo:", self.variable_objetivo)
        print("\nEstadísticos descriptivos básicos:")
        print(self.df[self.numericas].describe().round(2))

    @staticmethod
    def distancia_euclidea(a, b):
        """Calcula la distancia euclídea entre dos vectores."""
        return float(np.sqrt(((a - b) ** 2).sum()))

    def demostrar_impacto_distancia(self, idx1=50465, idx2=50224):
        """
        Demuestra cómo una variable de gran magnitud secuestra la distancia euclídea
        si los datos no son escalados previamente.
        """
        if self.df is None:
            self.cargar()

        idx_a = idx1 if idx1 in self.df.index else self.df.index[0]
        idx_b = idx2 if idx2 in self.df.index else self.df.index[1]

        c1 = self.df.loc[idx_a, self.numericas]
        c2 = self.df.loc[idx_b, self.numericas]

        dist_cruda = self.distancia_euclidea(c1, c2)

        scaler = MinMaxScaler()
        X_esc = pd.DataFrame(scaler.fit_transform(self.df[self.numericas]), columns=self.numericas, index=self.df.index)
        dist_escalada = self.distancia_euclidea(X_esc.loc[idx_a], X_esc.loc[idx_b])

        resumen = {
            "municipio_a": self.df.loc[idx_a, "MUNICIPIO"] if "MUNICIPIO" in self.df.columns else "Mpio A",
            "municipio_b": self.df.loc[idx_b, "MUNICIPIO"] if "MUNICIPIO" in self.df.columns else "Mpio B",
            "distancia_sin_escalar": round(dist_cruda, 2),
            "distancia_escalada_minmax": round(dist_escalada, 4),
            "conclusion": "Sin escalamiento, la variable con mayor varianza domina el 99%+ de la distancia euclídea."
        }
        return resumen

    def comparar_escaladores(self):
        """
        Compara MinMaxScaler, StandardScaler y RobustScaler sobre las variables numéricas.
        Retorna los dataframes transformados y sus estadísticas.
        """
        if self.df is None:
            self.cargar()

        X = self.df[self.numericas]
        df_minmax = pd.DataFrame(MinMaxScaler().fit_transform(X), columns=[f"{c}_minmax" for c in self.numericas], index=self.df.index)
        df_std = pd.DataFrame(StandardScaler().fit_transform(X), columns=[f"{c}_std" for c in self.numericas], index=self.df.index)
        df_rob = pd.DataFrame(RobustScaler().fit_transform(X), columns=[f"{c}_rob" for c in self.numericas], index=self.df.index)

        return df_minmax, df_std, df_rob

    def codificar_onehot(self):
        """Aplica One-Hot Encoding sobre las variables categóricas nominales."""
        if self.df is None:
            self.cargar()
        return pd.get_dummies(self.df[self.categoricas], prefix=self.categoricas, dtype=int)

    def discretizar(self, columna="AÑO", n_bins=4, estrategia="quantile"):
        """Discretiza una variable continua en intervalos usando KBinsDiscretizer."""
        if self.df is None:
            self.cargar()
        try:
            discretizador = KBinsDiscretizer(n_bins=n_bins, encode="ordinal", strategy=estrategia)
            bins = discretizador.fit_transform(self.df[[columna]]).ravel()
            bordes = discretizador.bin_edges_[0].round(0)
        except Exception:
            discretizador = KBinsDiscretizer(n_bins=n_bins, encode="ordinal", strategy="uniform")
            bins = discretizador.fit_transform(self.df[[columna]]).ravel()
            bordes = discretizador.bin_edges_[0].round(0)
        return pd.Series(bins, name=f"{columna}_BIN", index=self.df.index), bordes

    def aplicar_pca(self, n_componentes=5):
        """
        Aplica PCA sobre las variables continuas estandarizadas.
        Retorna el dataframe de componentes y el resumen de varianza explicada.
        """
        if self.df is None:
            self.cargar()

        X_num = StandardScaler().fit_transform(self.df[self.numericas])

        n_comp_reales = min(n_componentes, len(self.numericas))
        self.pca_model = PCA(n_components=n_comp_reales)
        componentes = self.pca_model.fit_transform(X_num)

        varianzas = self.pca_model.explained_variance_ratio_
        acumulada = varianzas.cumsum()

        cols_pca = [f"PC{i+1}" for i in range(n_comp_reales)]
        df_pca = pd.DataFrame(componentes, columns=cols_pca, index=self.df.index)

        resumen = {
            "n_componentes": n_comp_reales,
            "varianza_individual": varianzas.round(4).tolist(),
            "varianza_acumulada": acumulada.round(4).tolist(),
            "pct_total_explicado": round(float(acumulada[-1]) * 100, 2)
        }
        return df_pca, resumen

    def generar_dataset_reducido(self, n_componentes=5):
        """
        Construye el dataset reducido consolidado con metadatos clave,
        componentes principales y variable objetivo.
        """
        if self.df is None:
            self.cargar()

        df_pca, resumen_pca = self.aplicar_pca(n_componentes=n_componentes)

        cols_meta = [c for c in ["AÑO", "CODIGO_DANE_MUNICIPIO", "DEPARTAMENTO", "MUNICIPIO", "TIPO_VEHICULO"] if c in self.df.columns]
        meta = self.df[cols_meta].copy()
        target = self.df[[self.variable_objetivo]].copy() if self.variable_objetivo in self.df.columns else pd.DataFrame(index=self.df.index)

        self.df_reducido = pd.concat([meta, df_pca, target], axis=1)
        return self.df_reducido, resumen_pca

    def guardar_reducido(self, ruta_salida="../dataset/dataset_reducido.csv"):
        """Exporta el dataset reducido a disco."""
        if self.df_reducido is None:
            self.generar_dataset_reducido()

        salida = resolver_ruta(ruta_salida)
        salida.parent.mkdir(parents=True, exist_ok=True)
        self.df_reducido.to_csv(salida, index=False, encoding="utf-8-sig")
        print("✅ Dataset reducido guardado exitosamente en:", salida)
        print(f"Dimensiones finales: {self.df_reducido.shape[0]:,} filas × {self.df_reducido.shape[1]} columnas")
