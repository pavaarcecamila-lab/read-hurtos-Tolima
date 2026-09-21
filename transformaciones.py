# Sesión 4 · Minería de Datos · Proyecto Hurto Vehículos
# Transformación y reducción: escalado, codificación (One-Hot y Ordinal), discretización y PCA
# Ejecutar desde este directorio o la raíz del proyecto:
# python3 codigo/transformaciones.py

from pathlib import Path
import warnings

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import (
    KBinsDiscretizer,
    MinMaxScaler,
    RobustScaler,
    StandardScaler,
    OrdinalEncoder
)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Rutas del proyecto
CARPETA_CODIGO = Path(__file__).resolve().parent
CARPETA_PROYECTO = CARPETA_CODIGO.parent
RUTA_DATASET = CARPETA_PROYECTO / "datasets" / "resultados" / "dataset_final.csv"
RUTA_SALIDA = CARPETA_PROYECTO / "datasets" / "resultados" / "matriz_features_final.csv"

NUMERICAS = ["AÑO", "VEHICULOS_REGISTRADOS", "VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]
CATEGORICAS = ["TIPO_VEHICULO", "DEPARTAMENTO"]

print("=" * 60)
print("PROCESO DE TRANSFORMACIÓN Y REDUCCIÓN DE DIMENSIONALIDAD")
print("=" * 60)

df = pd.read_csv(RUTA_DATASET)
X = df[NUMERICAS]
print(f"Dataset cargado: {df.shape} | Matriz numérica: {X.shape}")


# 1 · POR QUÉ ESCALAR: la distancia la domina la variable con unidades grandes
def distancia(a, b):
    return ((a - b) ** 2).sum() ** 0.5


c1, c2 = X.iloc[0], X.iloc[1]
print("\n--- 1. Distancia entre dos registros SIN escalar ---")
for col in NUMERICAS:
    print(f"  {col:<25} aporta {abs(c1[col] - c2[col]):>10.1f}")
print("Distancia total sin escalar :", round(distancia(c1, c2), 1))

X_minmax = pd.DataFrame(MinMaxScaler().fit_transform(X), columns=NUMERICAS)
c1e, c2e = X_minmax.iloc[0], X_minmax.iloc[1]
print("Distancia total con MinMax  :", round(distancia(c1e, c2e), 3))

# 2 · LOS TRES ESCALADORES
print("\n--- 2. MinMaxScaler (todo a [0, 1]) ---")
print("Antes  : min", X.min().round(1).tolist())
print("Después: min", X_minmax.min().round(3).tolist(), "max", X_minmax.max().round(3).tolist())

print("\n--- StandardScaler (media=0, desviación=1) ---")
X_std = pd.DataFrame(StandardScaler().fit_transform(X), columns=NUMERICAS)
print("Medias tras escalar:", X_std.mean().round(3).tolist())
print("Desv. estándar     :", X_std.std().round(3).tolist())

print("\n--- RobustScaler (usa mediana e IQR, resiste outliers) ---")
X_rob = pd.DataFrame(RobustScaler().fit_transform(X), columns=NUMERICAS)
print("Mediana tras escalar:", X_rob.median().round(3).tolist())

# 3 · CODIFICACIÓN DE CATEGÓRICAS: One-Hot y Ordinal Encoding
print("\n--- 3. Codificación One-Hot (get_dummies) ---")
X_cat_onehot = pd.get_dummies(df[CATEGORICAS], prefix=CATEGORICAS, dtype=int)
print(f"Columnas One-Hot generadas ({len(X_cat_onehot.columns)}):", X_cat_onehot.columns.tolist()[:5], "...")

print("\n--- Codificación Ordinal (OrdinalEncoder) ---")
enc_ordinal = OrdinalEncoder(categories=[["MOTOCICLETA", "AUTOMOTOR"]])
X_cat_ordinal = pd.DataFrame(
    enc_ordinal.fit_transform(df[["TIPO_VEHICULO"]]),
    columns=["TIPO_VEHICULO_ORDINAL"],
    dtype=int
)
print("Distribución Ordinal (0=MOTOCICLETA, 1=AUTOMOTOR):")
print(X_cat_ordinal["TIPO_VEHICULO_ORDINAL"].value_counts().to_string())

# 4 · DISCRETIZACIÓN por KBinsDiscretizer (rangos ordinales)
print("\n--- 4. KBinsDiscretizer: AÑO -> 4 categorías ordinales ---")
try:
    discretizador_anio = KBinsDiscretizer(n_bins=4, encode="ordinal", strategy="quantile")
    anio_bins = discretizador_anio.fit_transform(df[["AÑO"]]).ravel()
    bordes_anio = discretizador_anio.bin_edges_[0].round(0)
except Exception:
    discretizador_anio = KBinsDiscretizer(n_bins=4, encode="ordinal", strategy="uniform")
    anio_bins = discretizador_anio.fit_transform(df[["AÑO"]]).ravel()
    bordes_anio = discretizador_anio.bin_edges_[0].round(0)

print("Bordes de los rangos de AÑO:", bordes_anio)
print(pd.Series(anio_bins, name="AÑO_BIN_ORDINAL").value_counts().sort_index().to_string())

print("\n--- KBinsDiscretizer: VEHICULOS_REGISTRADOS -> 4 categorías ordinales ---")
discretizador_reg = KBinsDiscretizer(n_bins=4, encode="ordinal", strategy="uniform")
reg_bins = discretizador_reg.fit_transform(df[["VEHICULOS_REGISTRADOS"]]).ravel()
bordes_reg = discretizador_reg.bin_edges_[0].round(0)
print("Bordes de VEHICULOS_REGISTRADOS:", bordes_reg)
print(pd.Series(reg_bins, name="REGISTRADOS_BIN_ORDINAL").value_counts().sort_index().to_string())

# 5 · PCA sobre las numéricas estandarizadas
print("\n--- 5. PCA: ¿cuántas dimensiones resumen los datos? ---")
pca = PCA()
componentes = pca.fit_transform(X_std)
razones = pca.explained_variance_ratio_
acumulada = razones.cumsum().round(4)
print("Varianza explicada por componente :", razones.round(4))
print("Varianza acumulada                :", acumulada)
para_80 = int((acumulada < 0.80).sum()) + 1
para_90 = int((acumulada < 0.90).sum()) + 1
print(f"Componentes para explicar >=80%: {para_80} | para >=90%: {para_90} (de {len(NUMERICAS)})")

df_pca = pd.DataFrame(
    componentes,
    columns=[f"PCA_{i+1}" for i in range(componentes.shape[1])]
)

# 6 · MATRIZ DE FEATURES LISTA PARA MODELADO
X_final = pd.concat([
    df[["AÑO", "CODIGO_DANE_MUNICIPIO", "DEPARTAMENTO", "MUNICIPIO"]],
    X_std.add_suffix("_std"),
    X_cat_onehot,
    X_cat_ordinal,
    pd.Series(anio_bins, name="AÑO_BIN_ORDINAL"),
    pd.Series(reg_bins, name="REGISTRADOS_BIN_ORDINAL"),
    df_pca
], axis=1)

print("\n--- 6. Matriz final para modelado ---")
print("Forma final:", X_final.shape)
print("Muestra de columnas:", X_final.columns.tolist()[:10], "...")

X_final.to_csv(RUTA_SALIDA, index=False, encoding="utf-8-sig")
print(f"\nMatriz de features guardada en: {RUTA_SALIDA}")
print("=" * 60)
