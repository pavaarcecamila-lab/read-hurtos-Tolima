import pandas as pd
import unicodedata
from pathlib import Path


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


def sin_tildes(texto):
    """Elimina acentos y tildes preservando los caracteres base."""
    if pd.isna(texto):
        return texto
    texto = str(texto)
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def normalizar_texto(texto):
    """Limpia espacios en blanco, remueve tildes y convierte a mayúsculas consistentes."""
    if pd.isna(texto):
        return texto
    texto = sin_tildes(texto)
    texto = texto.strip().upper()
    while "  " in texto:
        texto = texto.replace("  ", " ")
    return texto


def normalizar_municipio(texto):
    """Normaliza nombres municipales removiendo sufijos institucionales."""
    if pd.isna(texto):
        return texto
    texto = normalizar_texto(texto)
    texto = texto.replace("(CT)", "").strip()
    texto = texto.replace(" D.C.", "").replace(" D.C", "").replace(" DC", "").strip()
    return texto


class ParqueAutomotor:
    """Clase modular para diagnóstico, limpieza y exportación del dataset de Crecimiento del Parque Automotor (RUNT)."""

    def __init__(self, ruta):
        self.ruta = resolver_ruta(ruta)
        self.df = None

    def cargar(self):
        """Carga el dataset de parque automotor RUNT con pandas."""
        self.ruta = resolver_ruta(self.ruta)
        self.df = pd.read_csv(self.ruta, low_memory=False)
        return self.df

    def diagnosticar(self):
        """Presenta un diagnóstico de dimensiones, nulos y duplicados."""
        if self.df is None:
            raise ValueError("Debe cargar los datos primero con .cargar()")
        print("Filas:", f"{len(self.df):,}")
        print("Columnas:", len(self.df.columns))
        print("\nValores nulos por columna:")
        print(self.df.isnull().sum())
        print("\nDuplicados exactos:", f"{self.df.duplicated().sum():,}")

    def limpiar(self):
        """Ejecuta el pipeline de limpieza y estandarización del dataset de parque automotor."""
        if self.df is None:
            raise ValueError("Debe cargar los datos primero con .cargar()")

        self.df = self.df.copy()

        # 1. Deduplicación
        self.df = self.df.drop_duplicates().reset_index(drop=True)

        # 2. Filtrar únicamente vehículos con estado activo
        if "ESTADO_DEL_VEHICULO" in self.df.columns:
            self.df = self.df[self.df["ESTADO_DEL_VEHICULO"].astype(str).str.upper() == "ACTIVO"].copy()

        # 3. Normalización de texto
        if "NOMBRE_DEPARTAMENTO" in self.df.columns:
            self.df["DEPARTAMENTO"] = self.df["NOMBRE_DEPARTAMENTO"].apply(normalizar_texto)
        if "NOMBRE_MUNICIPIO" in self.df.columns:
            self.df["MUNICIPIO"] = self.df["NOMBRE_MUNICIPIO"].apply(normalizar_municipio)
        if "NOMBRE_DE_LA_CLASE" in self.df.columns:
            self.df["CLASE"] = self.df["NOMBRE_DE_LA_CLASE"].apply(normalizar_texto)

        # 4. Tratamiento del año de matrícula y outliers '1900'
        if "FECHA DE REGISTRO" in self.df.columns:
            self.df["AÑO"] = pd.to_numeric(self.df["FECHA DE REGISTRO"], errors="coerce")
            mediana_valida = self.df.loc[self.df["AÑO"] > 1901, "AÑO"].median()
            mediana_valida = int(mediana_valida) if not pd.isna(mediana_valida) else 2018
            self.df.loc[self.df["AÑO"] <= 1901, "AÑO"] = mediana_valida
            self.df["AÑO"] = self.df["AÑO"].fillna(mediana_valida).astype(int)

        # 5. Clasificación canónica de vehículo: MOTOCICLETA vs AUTOMOTOR
        if "NOMBRE_DE_LA_CLASE" in self.df.columns:
            self.df["TIPO_VEHICULO"] = self.df["NOMBRE_DE_LA_CLASE"].apply(
                lambda x: "MOTOCICLETA" if "MOTO" in str(x).upper() else "AUTOMOTOR"
            )

        # 6. Limpieza de cantidad
        if "CANTIDAD" in self.df.columns:
            self.df["CANTIDAD"] = pd.to_numeric(self.df["CANTIDAD"], errors="coerce").fillna(1)
            self.df = self.df[self.df["CANTIDAD"] > 0].copy()

        # 7. Eliminar metadatos prescindibles de publicación
        columnas_descartar = ["MES DE PUBLICACION", "AÑO DE PUBLICACIÓN"]
        self.df = self.df.drop(columns=[c for c in columnas_descartar if c in self.df.columns], errors="ignore")

        return self.df

    def guardar(self, ruta_salida):
        """Guarda el archivo limpio en disco con encoding UTF-8 BOM."""
        if self.df is None:
            raise ValueError("No hay datos limpios para guardar.")
        salida = Path(ruta_salida)
        salida.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(salida, index=False, encoding="utf-8-sig")
        print("Archivo limpio guardado correctamente en:", salida)
