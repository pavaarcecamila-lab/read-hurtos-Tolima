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


class Hurto:
    """Clase modular para diagnóstico, limpieza y exportación del dataset de Hurto de Vehículos."""

    def __init__(self, ruta):
        self.ruta = resolver_ruta(ruta)
        self.df = None

    def cargar(self):
        """Carga el dataset de hurto con pandas de forma defensiva."""
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
        """Ejecuta el pipeline de limpieza y estandarización del dataset."""
        if self.df is None:
            raise ValueError("Debe cargar los datos primero con .cargar()")

        self.df = self.df.copy()

        # 1. Deduplicación
        self.df = self.df.drop_duplicates().reset_index(drop=True)

        # 2. Normalización de texto
        if "DEPARTAMENTO" in self.df.columns:
            self.df["DEPARTAMENTO"] = self.df["DEPARTAMENTO"].apply(normalizar_texto)
        if "MUNICIPIO" in self.df.columns:
            self.df["MUNICIPIO"] = self.df["MUNICIPIO"].apply(normalizar_municipio)
        if "TIPO DELITO" in self.df.columns:
            self.df["TIPO DELITO"] = self.df["TIPO DELITO"].apply(normalizar_texto)
        if "ZONA" in self.df.columns:
            self.df["ZONA"] = self.df["ZONA"].apply(normalizar_texto)

        # 3. Código DANE de municipio a 5 dígitos
        if "COD_MUNI" in self.df.columns:
            self.df["CODIGO_DANE_MUNICIPIO"] = (
                self.df["COD_MUNI"]
                .astype(str)
                .str.strip()
                .str.zfill(5)
            )

        # 4. Formateo de fecha y extracción del año
        if "FECHA HECHO" in self.df.columns:
            self.df["FECHA"] = pd.to_datetime(
                self.df["FECHA HECHO"],
                format="%d/%m/%Y",
                errors="coerce"
            )
            self.df["AÑO"] = self.df["FECHA"].dt.year
            mediana_anio = int(self.df["AÑO"].dropna().median())
            self.df["AÑO"] = self.df["AÑO"].fillna(mediana_anio).astype(int)

        # 5. Clasificación canónica de vehículo: MOTOCICLETA vs AUTOMOTOR
        if "TIPO DELITO" in self.df.columns:
            self.df["TIPO_VEHICULO"] = self.df["TIPO DELITO"].apply(
                lambda x: "MOTOCICLETA" if "MOTOCICLETA" in str(x).upper() else "AUTOMOTOR"
            )

        # 6. Limpieza de cantidad
        if "CANTIDAD" in self.df.columns:
            self.df["CANTIDAD"] = pd.to_numeric(self.df["CANTIDAD"], errors="coerce").fillna(1)
            self.df = self.df[self.df["CANTIDAD"] > 0].copy()

        return self.df

    def guardar(self, ruta_salida):
        """Guarda el archivo limpio en disco con encoding UTF-8 BOM."""
        if self.df is None:
            raise ValueError("No hay datos limpios para guardar.")
        salida = Path(ruta_salida)
        salida.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(salida, index=False, encoding="utf-8-sig")
        print("Archivo limpio guardado correctamente en:", salida)
