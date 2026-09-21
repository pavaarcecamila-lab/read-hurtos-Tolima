from pathlib import Path
import pandas as pd

from limpieza import ProcesoLimpieza
#from diagnostico import GeneradorDiagnostico

from library import (
    ClasificadorVehiculos,
    AgregadorDatos,
    IntegradorDatos,
    ValidadorDatos,
    AnalizadorAtipicos,
    TransformadorDatos,
    normalizar_texto
)


# ============================================================
# RUTAS
# ============================================================

CARPETA_CODIGO = Path(__file__).resolve().parent
CARPETA_PROYECTO = CARPETA_CODIGO.parent
CARPETA_DATASETS = CARPETA_PROYECTO / "datasets"
CARPETA_ORIGINALES = (
    CARPETA_DATASETS / "originales"
)
CARPETA_LIMPIOS = (
    CARPETA_DATASETS / "limpios"
)
CARPETA_PROCESADOS = (
    CARPETA_DATASETS / "procesados"
)
CARPETA_RESULTADOS = (
    CARPETA_DATASETS / "resultados"
)
CARPETA_PROCESADOS.mkdir(
    parents=True,
    exist_ok=True
)
CARPETA_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# FUNCIONES DE PREPARACIÓN
# ============================================================

def preparar_runt(df):

    resultado = df.copy()

    resultado["AÑO"] = pd.to_numeric(
        resultado["FECHA DE REGISTRO"],
        errors="coerce"
    ).astype("Int64")

    resultado["DEPARTAMENTO_NORMALIZADO"] = (
        resultado["NOMBRE_DEPARTAMENTO"]
        .apply(normalizar_texto)
    )

    resultado["MUNICIPIO_NORMALIZADO"] = (
        resultado["NOMBRE_MUNICIPIO"]
        .apply(normalizar_texto)
    )

    return resultado


def preparar_hurto(df):

    resultado = df.copy()

    clasificador = ClasificadorVehiculos()

    resultado["TIPO_VEHICULO"] = (
        resultado["TIPO DELITO"]
        .apply(clasificador.clasificar_hurto)
    )

    resultado = resultado[
        resultado["TIPO_VEHICULO"].notna()
    ].copy()

    resultado["AÑO"] = (
        resultado["FECHA HECHO"]
        .dt.year
    )

    resultado["CODIGO_DANE_MUNICIPIO"] = (
        resultado["COD_MUNI"]
        .astype(str)
        .str.strip()
        .str.zfill(5)
    )

    return resultado


def preparar_recuperacion(df):

    resultado = df.copy()

    clasificador = ClasificadorVehiculos()

    resultado["TIPO_VEHICULO"] = (
        resultado["CLASE BIEN"]
        .apply(clasificador.clasificar_recuperacion)
    )

    resultado = resultado[
        resultado["TIPO_VEHICULO"].notna()
    ].copy()

    resultado["AÑO"] = (
        resultado["FECHA HECHO"]
        .dt.year
    )

    resultado["CODIGO_DANE_MUNICIPIO"] = (
        resultado["CODIGO DANE"]
        .astype(str)
        .str.strip()
        .str.zfill(5)
    )

    return resultado


# ============================================================
# MAPEO GEOGRÁFICO
# ============================================================

def construir_mapa_municipios(df_hurto, df_recuperacion):

    columnas_hurto = [
        "CODIGO_DANE_MUNICIPIO",
        "DEPARTAMENTO",
        "MUNICIPIO"
    ]

    columnas_recuperacion = [
        "CODIGO_DANE_MUNICIPIO",
        "DEPARTAMENTO",
        "MUNICIPIO"
    ]

    mapa_hurto = df_hurto[columnas_hurto].copy()
    mapa_recuperacion = df_recuperacion[columnas_recuperacion].copy()

    mapa = pd.concat(
        [mapa_hurto, mapa_recuperacion],
        ignore_index=True
    )

    mapa["DEPARTAMENTO"] = (
        mapa["DEPARTAMENTO"]
        .apply(normalizar_texto)
    )

    mapa["MUNICIPIO"] = (
        mapa["MUNICIPIO"]
        .apply(normalizar_texto)
    )

    mapa["MUNICIPIO"] = (
        mapa["MUNICIPIO"]
        .str.replace(r"\s*\(CT\)$", "", regex=True)
        .str.strip()
    )

    mapa = mapa.drop_duplicates()

    duplicados = mapa.duplicated(
        subset=["CODIGO_DANE_MUNICIPIO"],
        keep=False
    )

    return mapa, mapa[duplicados].copy()

# ============================================================
# RUNT: ASIGNACIÓN GEOGRÁFICA
# ============================================================

def agregar_codigo_dane_runt(
    df_runt,
    mapa_municipios
):

    resultado = df_runt.copy()

    resultado = resultado.merge(
        mapa_municipios[
            [
                "CODIGO_DANE_MUNICIPIO",
                "DEPARTAMENTO",
                "MUNICIPIO"
            ]
        ],
        left_on=[
            "DEPARTAMENTO_NORMALIZADO",
            "MUNICIPIO_NORMALIZADO"
        ],
        right_on=[
            "DEPARTAMENTO",
            "MUNICIPIO"
        ],
        how="left"
    )

    return resultado


# ============================================================
# AGREGACIÓN
# ============================================================

def agregar_runt(df):

    resultado = df.copy()

    resultado = resultado[
        resultado["CODIGO_DANE_MUNICIPIO"].notna()
    ].copy()

    resultado["TIPO_VEHICULO"] = (
        resultado["NOMBRE_DE_LA_CLASE"]
        .apply(
            lambda clase:
            ClasificadorVehiculos()
            .clasificar_recuperacion(clase)
        )
    )

    resultado = resultado[
        resultado["TIPO_VEHICULO"].notna()
    ].copy()

    agregador = AgregadorDatos()

    return agregador.agregar(
        resultado,
        [
            "AÑO",
            "CODIGO_DANE_MUNICIPIO",
            "TIPO_VEHICULO"
        ],
        "CANTIDAD"
    ).rename(
        columns={
            "CANTIDAD": "VEHICULOS_REGISTRADOS"
        }
    )


def agregar_hurto(df):

    agregador = AgregadorDatos()

    return agregador.agregar(
        df,
        [
            "AÑO",
            "CODIGO_DANE_MUNICIPIO",
            "TIPO_VEHICULO"
        ],
        "CANTIDAD"
    ).rename(
        columns={
            "CANTIDAD": "VEHICULOS_HURTADOS"
        }
    )


def agregar_recuperacion(df):

    agregador = AgregadorDatos()

    return agregador.agregar(
        df,
        [
            "AÑO",
            "CODIGO_DANE_MUNICIPIO",
            "TIPO_VEHICULO"
        ],
        "CANTIDAD"
    ).rename(
        columns={
            "CANTIDAD": "VEHICULOS_RECUPERADOS"
        }
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print("PROCESO DE MINERÍA DE DATOS")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. LIMPIEZA
    # --------------------------------------------------------

    print("\n1. INICIANDO LIMPIEZA")

    proceso = ProcesoLimpieza(
        CARPETA_ORIGINALES,
        CARPETA_LIMPIOS
    )

    runt, atipicos_runt = proceso.limpiar_runt()

    hurto, atipicos_hurto = proceso.limpiar_hurto()

    recuperacion, atipicos_recuperacion = (
        proceso.limpiar_recuperacion()
    )

    ruta_bitacora = proceso.guardar_bitacora()

    print("Limpieza completada.")
    print(f"Bitácora: {ruta_bitacora}")

    print(
        f"RUNT: {len(runt)} registros limpios"
    )

    print(
        f"Hurto: {len(hurto)} registros limpios"
    )

    print(
        f"Recuperación: {len(recuperacion)} registros limpios"
    )

    # --------------------------------------------------------
    # 2. PREPARACIÓN
    # --------------------------------------------------------

    print("\n2. PREPARANDO LOS DATASETS")

    runt_preparado = preparar_runt(runt)

    hurto_preparado = preparar_hurto(hurto)

    recuperacion_preparada = preparar_recuperacion(
        recuperacion
    )

    # --------------------------------------------------------
    # 3. MAPA DE MUNICIPIOS
    # --------------------------------------------------------

    print("\n3. CONSTRUYENDO CORRESPONDENCIA GEOGRÁFICA")

    mapa_municipios, ambiguos = construir_mapa_municipios(
    hurto_preparado,
    recuperacion_preparada
)

    print("\nCANTIDAD DE COMBINACIONES POR CÓDIGO:")
    cantidad_combinaciones = (
        ambiguos
        .groupby("CODIGO_DANE_MUNICIPIO")
        .size()
        .sort_values(ascending=False)
    )

    print(cantidad_combinaciones)
    # --------------------------------------------------------
    # 4. ASIGNAR DANE AL RUNT
    # --------------------------------------------------------

    runt_preparado = agregar_codigo_dane_runt(
        runt_preparado,
        mapa_municipios
    )

    # --------------------------------------------------------
    # 5. PREPARAR CLASIFICACIÓN RUNT
    # --------------------------------------------------------

    print("\n4. CLASIFICANDO TIPOS DE VEHÍCULO")

    runt_preparado["TIPO_VEHICULO"] = (
        runt_preparado["NOMBRE_DE_LA_CLASE"]
        .apply(
            lambda clase:
            ClasificadorVehiculos()
            .clasificar_recuperacion(clase)
        )
    )

    clases_no_mapeadas = (
        runt_preparado[
            runt_preparado["TIPO_VEHICULO"].isna()
        ]["NOMBRE_DE_LA_CLASE"]
        .value_counts()
        .reset_index()
    )

    clases_no_mapeadas.columns = [
        "CLASE_RUNT",
        "REGISTROS"
    ]

    clases_no_mapeadas.to_csv(
        CARPETA_RESULTADOS
        / "clases_runt_no_mapeadas.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # --------------------------------------------------------
    # 6. GUARDAR PROCESADOS
    # --------------------------------------------------------

    runt_preparado.to_csv(
        CARPETA_PROCESADOS
        / "RUNT_procesado.csv",
        index=False,
        encoding="utf-8-sig"
    )

    hurto_preparado.to_csv(
        CARPETA_PROCESADOS
        / "Hurto_procesado.csv",
        index=False,
        encoding="utf-8-sig"
    )

    recuperacion_preparada.to_csv(
        CARPETA_PROCESADOS
        / "Recuperacion_procesado.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # --------------------------------------------------------
    # 7. AGREGAR
    # --------------------------------------------------------

    print("\n5. AGREGANDO LOS DATOS")

    registrados = agregar_runt(
        runt_preparado
    )

    hurtados = agregar_hurto(
        hurto_preparado
    )

    recuperados = agregar_recuperacion(
        recuperacion_preparada
    )

    # --------------------------------------------------------
    # 8. INFORMACIÓN GEOGRÁFICA
    # --------------------------------------------------------

    informacion_geografica = (
        mapa_municipios[
            [
                "CODIGO_DANE_MUNICIPIO",
                "DEPARTAMENTO",
                "MUNICIPIO"
            ]
        ]
        .drop_duplicates(
            subset=["CODIGO_DANE_MUNICIPIO"]
        )
    )

    # --------------------------------------------------------
    # 9. INTEGRACIÓN
    # --------------------------------------------------------

    print("\n6. INTEGRANDO LOS DATASETS")

    integrador = IntegradorDatos()

    final = integrador.cruzar(
        registrados,
        hurtados,
        recuperados
    )

    final = final.merge(
        informacion_geografica,
        on="CODIGO_DANE_MUNICIPIO",
        how="left"
    )

    # --------------------------------------------------------
    # 10. COMPLETAR AUSENCIAS REALES
    # --------------------------------------------------------

    columnas_cantidad = [
        "VEHICULOS_REGISTRADOS",
        "VEHICULOS_HURTADOS",
        "VEHICULOS_RECUPERADOS"
    ]

    for columna in columnas_cantidad:

        if columna not in final.columns:
            final[columna] = 0

        final[columna] = final[columna].fillna(0)

    # --------------------------------------------------------
    # 11. ORGANIZAR COLUMNAS
    # --------------------------------------------------------

    columnas_finales = [
        "AÑO",
        "CODIGO_DANE_MUNICIPIO",
        "DEPARTAMENTO",
        "MUNICIPIO",
        "TIPO_VEHICULO",
        "VEHICULOS_REGISTRADOS",
        "VEHICULOS_HURTADOS",
        "VEHICULOS_RECUPERADOS"
    ]

    final = final[columnas_finales]

    # --------------------------------------------------------
    # 12. TIPOS
    # --------------------------------------------------------

    final["AÑO"] = pd.to_numeric(
        final["AÑO"],
        errors="coerce"
    ).astype("Int64")

    final["CODIGO_DANE_MUNICIPIO"] = (
        final["CODIGO_DANE_MUNICIPIO"]
        .astype(str)
        .str.strip()
        .str.zfill(5)
    )

    # --------------------------------------------------------
    # 13. VALIDACIÓN
    # --------------------------------------------------------

    print("\n7. VALIDANDO DATASET FINAL")

    validador = ValidadorDatos(final)

    validacion = validador.validar_todo()

    print(
        f"Filas finales: {validacion['FILAS']}"
    )

    print(
        f"Columnas finales: {validacion['COLUMNAS']}"
    )

    print(
        f"Duplicados exactos: "
        f"{validacion['DUPLICADOS_EXACTOS']}"
    )

    print(
        "Duplicados por clave:",
        validador.validar_claves(
            [
                "AÑO",
                "CODIGO_DANE_MUNICIPIO",
                "TIPO_VEHICULO"
            ]
        )
    )

    print(
        "Tipos de vehículo:",
        validacion["TIPOS_VEHICULO"]
    )

    # --------------------------------------------------------
    # 14. GUARDAR VALIDACIÓN
    # --------------------------------------------------------

    filas_validacion = []

    filas_validacion.append({
        "INDICADOR": "FILAS",
        "VALOR": len(final)
    })

    filas_validacion.append({
        "INDICADOR": "COLUMNAS",
        "VALOR": len(final.columns)
    })

    filas_validacion.append({
        "INDICADOR": "DUPLICADOS_EXACTOS",
        "VALOR": final.duplicated().sum()
    })

    filas_validacion.append({
        "INDICADOR": "DUPLICADOS_CLAVE",
        "VALOR": final.duplicated(
            subset=[
                "AÑO",
                "CODIGO_DANE_MUNICIPIO",
                "TIPO_VEHICULO"
            ]
        ).sum()
    })

    pd.DataFrame(
        filas_validacion
    ).to_csv(
        CARPETA_RESULTADOS
        / "validacion_final.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # --------------------------------------------------------
    # 15. GUARDAR DATASET FINAL
    # --------------------------------------------------------

    ruta_final = (
        CARPETA_RESULTADOS
        / "dataset_final.csv"
    )

    final.to_csv(
        ruta_final,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n8. PROCESO TERMINADO")

    print(
        f"Dataset final guardado en:\n{ruta_final}"
    )

    print("\nColumnas finales:")

    for columna in final.columns:
        print(f"- {columna}")

    print("\n9. COMPROBANDO COBERTURA DEL DATASET FINAL")

    df_final = pd.read_csv(
        "datasets/resultados/dataset_final.csv",
        dtype={
            "CODIGO_DANE_MUNICIPIO": str
        }
    )
    print(f"Total de filas: {len(df_final)}")

    print("\nValores nulos por columna:")
    print(df_final.isnull().sum())

    print("\nCOMPROBANDO FILAS COMPLETAS")

    filas_completas = df_final.notna().all(axis=1).sum()

    filas_incompletas = df_final.isna().any(axis=1).sum()

    print("Filas completamente completas:", filas_completas)
    print("Filas con algún valor faltante:", filas_incompletas)
    print("\nCÓDIGOS DANE SIN DEPARTAMENTO/MUNICIPIO:")

    sin_geografia = df_final[
        df_final["DEPARTAMENTO"].isna() |
        df_final["MUNICIPIO"].isna()
    ]

    print(
        sin_geografia[
            [
                "AÑO",
                "CODIGO_DANE_MUNICIPIO",
                "TIPO_VEHICULO",
                "VEHICULOS_REGISTRADOS",
                "VEHICULOS_HURTADOS",
                "VEHICULOS_RECUPERADOS"
            ]
        ].head(50).to_string(index=False)
    )

    print("\nCantidad de códigos DANE sin geografía:")
    print(
        sin_geografia["CODIGO_DANE_MUNICIPIO"]
        .nunique()
    )

    print("\n" + "=" * 60)
    print("DIAGNÓSTICO DEL DATASET FINAL")
    print("=" * 60)

    print("\n1. DIMENSIONES")
    print("Filas:", len(df_final))
    print("Columnas:", len(df_final.columns))

    print("\n2. VALORES NULOS")
    print(df_final.isna().sum())

    print("\n3. NULOS TOTALES")
    print(df_final.isna().sum().sum())

    print("\n4. DUPLICADOS EXACTOS")
    print(df_final.duplicated().sum())

    print("\n5. TIPOS DE DATOS")
    print(df_final.dtypes)

    print("\n6. ESTADÍSTICOS DESCRIPTIVOS")
    print(
        df_final[
            [
                "VEHICULOS_REGISTRADOS",
                "VEHICULOS_HURTADOS",
                "VEHICULOS_RECUPERADOS"
            ]
        ].describe()
    )
    print("\n7. CATEGORÍAS")

    print("\nTipos de vehículo:")
    print(df_final["TIPO_VEHICULO"].value_counts())

    print("\nDepartamentos:")
    print("Cantidad:", df_final["DEPARTAMENTO"].nunique())

    print("\nMunicipios:")
    print("Cantidad:", df_final["MUNICIPIO"].nunique())
    print("\n9. CÓDIGOS DANE")

    codigo_dane = (
        df_final["CODIGO_DANE_MUNICIPIO"]
        .astype(str)
        .str.strip()
    )
    print("\nCÓDIGOS DE 4 DÍGITOS:")
    print(
        df_final.loc[
            codigo_dane.str.len() == 4,
            "CODIGO_DANE_MUNICIPIO"
        ].drop_duplicates().head(30)
)
    codigos_5 = codigo_dane.str.fullmatch(r"\d{5}")

    print(f"Códigos con 5 dígitos: {codigos_5.sum()}")
    print(f"Códigos diferentes de 5 dígitos: {(~codigos_5).sum()}")

    print("\nEjemplos diferentes de 5 dígitos:")
    print(
        df_final.loc[
            ~codigos_5,
            "CODIGO_DANE_MUNICIPIO"
        ].drop_duplicates().head(30)
    )

    print("\n" + "=" * 60)
    print("ANÁLISIS DE OUTLIERS CON IQR")
    print("=" * 60)

    analizador = AnalizadorAtipicos(df_final)

    for columna in [
        "VEHICULOS_REGISTRADOS",
        "VEHICULOS_HURTADOS",
        "VEHICULOS_RECUPERADOS"
    ]:

        resultado = analizador.calcular_iqr(columna)

        print(f"\n{columna}")

        print("Q1:", resultado["Q1"])
        print("Q3:", resultado["Q3"])
        print("IQR:", resultado["IQR"])
        print("Límite inferior:", resultado["LIMITE_INFERIOR"])
        print("Límite superior:", resultado["LIMITE_SUPERIOR"])
        print("Valores atípicos:", resultado["VALORES_ATIPICOS"])

    print("\n" + "=" * 60)
    print("10. TRANSFORMACIÓN Y REDUCCIÓN DE DIMENSIONALIDAD (PCA)")
    print("=" * 60)

    transformador = TransformadorDatos(df_final)
    matriz_final, resumen_pca = transformador.construir_matriz_final()

    ruta_matriz_features = CARPETA_RESULTADOS / "matriz_features_final.csv"
    matriz_final.to_csv(ruta_matriz_features, index=False, encoding="utf-8-sig")

    print(f"Matriz de features generada: {matriz_final.shape}")
    print(f"Guardada en: {ruta_matriz_features}")
    print("\nResumen PCA:")
    print(f"- Varianza explicada por componentes: {resumen_pca['varianza_explicada']}")
    print(f"- Componentes para >=80% varianza: {resumen_pca['componentes_para_80']}")
    print(f"- Componentes para >=90% varianza: {resumen_pca['componentes_para_90']}")




# ============================================================
# EJECUCIÓN
# ============================================================

main()

