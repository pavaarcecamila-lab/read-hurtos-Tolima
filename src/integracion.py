import pandas as pd
import numpy as np
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


class Integracion:
    """Clase modular para integrar los datasets de Hurto, Recuperación y Parque Automotor."""

    def __init__(
        self,
        ruta_hurto="../dataset/HurtoVehiculos_limpio.csv",
        ruta_recuperacion="../dataset/RecuperacionPoliciaNacional_limpio.csv",
        ruta_parque="../dataset/CrecimientoParqueAutomotor_limpio.csv",
        ruta_dane="../dataset/municipios_dane.xlsx"
    ):
        self.ruta_hurto = resolver_ruta(ruta_hurto)
        self.ruta_recuperacion = resolver_ruta(ruta_recuperacion)
        self.ruta_parque = resolver_ruta(ruta_parque)
        self.ruta_dane = resolver_ruta(ruta_dane)
        self.df_integrado = None

    def cargar_datos(self):
        """Carga las fuentes limpias individuales."""
        self.ruta_hurto = resolver_ruta(self.ruta_hurto)
        self.ruta_recuperacion = resolver_ruta(self.ruta_recuperacion)
        self.ruta_parque = resolver_ruta(self.ruta_parque)
        self.ruta_dane = resolver_ruta(self.ruta_dane)

        df_hurto = pd.read_csv(self.ruta_hurto, low_memory=False) if self.ruta_hurto.exists() else None
        df_rec = pd.read_csv(self.ruta_recuperacion, low_memory=False) if self.ruta_recuperacion.exists() else None
        df_parque = pd.read_csv(self.ruta_parque, low_memory=False) if self.ruta_parque.exists() else None
        df_dane = pd.read_excel(self.ruta_dane) if self.ruta_dane.exists() else None
        return df_hurto, df_rec, df_parque, df_dane

    def integrar(self, base_existente=None):
        """
        Integra las tres fuentes a nivel de Año, Municipio, Departamento y Tipo de Vehículo.
        Si se pasa un dataframe o existe dataset_integrado.csv consolidado, garantiza correspondencia 100%.
        """
        if base_existente is not None:
            self.df_integrado = base_existente.copy()
        else:
            # Buscar consolidado previo si existe
            ruta_cand = resolver_ruta("dataset/dataset_integrado.csv")
            if ruta_cand.exists():
                self.df_integrado = pd.read_csv(ruta_cand, low_memory=False)
            else:
                df_hurto, df_rec, df_parque, df_dane = self.cargar_datos()

                claves = ["AÑO", "CODIGO_DANE_MUNICIPIO", "DEPARTAMENTO", "MUNICIPIO", "TIPO_VEHICULO"]

                h_agg = df_hurto.groupby(claves, as_index=False)["CANTIDAD"].sum().rename(
                    columns={"CANTIDAD": "VEHICULOS_HURTADOS"}
                )
                r_agg = df_rec.groupby(claves, as_index=False)["CANTIDAD"].sum().rename(
                    columns={"CANTIDAD": "VEHICULOS_RECUPERADOS"}
                )

                claves_p = ["AÑO", "DEPARTAMENTO", "MUNICIPIO", "TIPO_VEHICULO"]
                p_agg = df_parque.groupby(claves_p, as_index=False)["CANTIDAD"].sum().rename(
                    columns={"CANTIDAD": "VEHICULOS_REGISTRADOS"}
                )

                merged = pd.merge(h_agg, r_agg, on=claves, how="outer")
                self.df_integrado = pd.merge(merged, p_agg, on=claves_p, how="outer")

        cols_metricas = ["VEHICULOS_REGISTRADOS", "VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]
        for c in cols_metricas:
            if c in self.df_integrado.columns:
                self.df_integrado[c] = pd.to_numeric(self.df_integrado[c], errors="coerce").fillna(0)

        if "AÑO" in self.df_integrado.columns:
            self.df_integrado = self.df_integrado.sort_values(
                by=[c for c in ["AÑO", "DEPARTAMENTO", "MUNICIPIO"] if c in self.df_integrado.columns]
            ).reset_index(drop=True)

        return self.df_integrado

    def diagnosticar(self):
        """Muestra estadísticas del dataset integrado."""
        if self.df_integrado is None:
            raise ValueError("Debe ejecutar .integrar() primero.")
        print("Dimensiones dataset integrado:", self.df_integrado.shape)
        print("\nColumnas:")
        for col in self.df_integrado.columns:
            print(f" - {col}")
        print("\nResumen numérico:")
        print(self.df_integrado.describe().round(2))

    def guardar(self, ruta_salida_csv, ruta_salida_excel=None):
        """Guarda el dataset integrado en CSV y opcionalmente en Excel."""
        if self.df_integrado is None:
            raise ValueError("No hay datos integrados para guardar.")
        salida_csv = Path(ruta_salida_csv)
        salida_csv.parent.mkdir(parents=True, exist_ok=True)
        self.df_integrado.to_csv(salida_csv, index=False, encoding="utf-8-sig")
        print("✅ Dataset integrado guardado en CSV:", salida_csv)

        if ruta_salida_excel:
            salida_excel = Path(ruta_salida_excel)
            df_excel = self.df_integrado.head(100000) if len(self.df_integrado) > 100000 else self.df_integrado
            df_excel.to_excel(salida_excel, index=False)
            print("✅ Dataset integrado guardado en Excel:", salida_excel)
