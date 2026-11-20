"""
Módulo de Clasificación II: Torneo de Modelos (Árbol vs Naive Bayes vs KNN)
Sesión 8 · Minería de Datos · UNIMINUTO Ibagué · 2026-2
Docente: Esteban Ernesto Morales Castro
Proyecto: Análisis del Hurto de Vehículos y Capacidad Policial en Tolima / Colombia
"""

import time
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def resolver_ruta_dataset():
    """Localiza el dataset integrado de forma robusta."""
    candidatos = [
        Path("read-hurtos-Tolima/dataset/dataset_integrado.csv"),
        Path("dataset/dataset_integrado.csv"),
        Path("../dataset/dataset_integrado.csv"),
        Path("../../dataset/dataset_integrado.csv")
    ]
    for c in candidatos:
        if c.exists():
            return c
    raise FileNotFoundError("No se encontró dataset_integrado.csv")


def ejemplo_bayes_manual(df):
    """
    Demostración del Teorema de Bayes con conteos directos sobre una tabla 2x2,
    siguiendo la metodología de la Sesión 8.
    """
    print("\n" + "="*80)
    print("1. TEOREMA DE BAYES CON DATOS REALES DEL PROYECTO (TABLA 2x2)")
    print("="*80)
    
    # Evento A: Municipio con Hurto Activo (> 0 hurtos)
    # Evento B: Municipio con Recuperaciones Policiales (> 0 recuperados)
    hurto = df['VEHICULOS_HURTADOS'] > 0
    recup = df['VEHICULOS_RECUPERADOS'] > 0
    
    tabla = pd.crosstab(hurto, recup, rownames=['Hurto Activo'], colnames=['Recuperación > 0'])
    print("\nTabla de Contingencia (Conteos Reales de Municipios):")
    print(tabla)
    
    total = len(df)
    p_hurto = hurto.mean()
    p_recup = recup.mean()
    p_recup_dado_hurto = (hurto & recup).sum() / hurto.sum()
    p_hurto_dado_recup = (hurto & recup).sum() / recup.sum()
    
    print("\n--- Probabilidades Marginales y Condicionales ---")
    print(f"• P(Hurto Activo) [A priori]:                        {p_hurto:.4f} ({p_hurto*100:.2f}%)")
    print(f"• P(Recuperación > 0) [Evidencia]:                   {p_recup:.4f} ({p_recup*100:.2f}%)")
    print(f"• P(Recuperación > 0 | Hurto Activo) [Verosimilitud]: {p_recup_dado_hurto:.4f} ({p_recup_dado_hurto*100:.2f}%)")
    print(f"• P(Hurto Activo | Recuperación > 0) [Posterior Bayes]: {p_hurto_dado_recup:.4f} ({p_hurto_dado_recup*100:.2f}%)")
    
    print("\nComprobación de la Fórmula de Bayes:")
    print("P(Hurto|Recup) = [P(Recup|Hurto) * P(Hurto)] / P(Recup)")
    calc = (p_recup_dado_hurto * p_hurto) / p_recup
    print(f"               = [{p_recup_dado_hurto:.4f} * {p_hurto:.4f}] / {p_recup:.4f} = {calc:.4f}")
    print("Interpretación: Saber que hubo vehículos recuperados eleva la probabilidad")
    print("de que el municipio tenga criminalidad activa del 44.31% al 61.57%.")


def ejemplo_distancia_knn_mano(df):
    """
    Cálculo a mano de la distancia euclidiana entre municipios de Tolima,
    demostrando el efecto destructivo de no escalar las variables.
    """
    print("\n" + "="*80)
    print("2. KNN Y DISTANCIA EUCLIDIANA A MANO (CASOS DEL TOLIMA)")
    print("="*80)
    
    tol = df[(df['DEPARTAMENTO'] == 'TOLIMA') & (df['AÑO'] == 2021) & (df['TIPO_VEHICULO'] == 'MOTOCICLETA')]
    seleccionados = ['IBAGUE', 'MELGAR', 'ESPINAL', 'CHAPARRAL', 'ALPUJARRA']
    sub_tol = tol[tol['MUNICIPIO'].isin(seleccionados)][['MUNICIPIO', 'VEHICULOS_REGISTRADOS', 'VEHICULOS_RECUPERADOS', 'VEHICULOS_HURTADOS']].copy()
    sub_tol = sub_tol.drop_duplicates(subset=['MUNICIPIO']).reset_index(drop=True)
    
    print("\nCasos Históricos de Tolima (Año 2021 - Motocicletas):")
    for _, r in sub_tol.iterrows():
        print(f"• {r['MUNICIPIO']:<12}: Registrados={r['VEHICULOS_REGISTRADOS']:>8.1f} | Recuperados={r['VEHICULOS_RECUPERADOS']:>4.0f} | Hurto={int(r['VEHICULOS_HURTADOS'])}")
    
    # Caso Nuevo a clasificar
    nuevo_nom = "CASO_NUEVO (Población Intermedia Tolimense)"
    nuevo_reg = 450.0
    nuevo_rec = 12.0
    print(f"\nCaso Nuevo a Evaluar: Registrados = {nuevo_reg}, Recuperados = {nuevo_rec}")
    
    # Sin escalar
    print("\nDistancias SIN ESCALAR:")
    for _, r in sub_tol.iterrows():
        d = np.sqrt((r['VEHICULOS_REGISTRADOS'] - nuevo_reg)**2 + (r['VEHICULOS_RECUPERADOS'] - nuevo_rec)**2)
        print(f"  d(Nuevo, {r['MUNICIPIO']:<10}) = sqrt(({r['VEHICULOS_REGISTRADOS']:.1f} - {nuevo_reg})^2 + ({r['VEHICULOS_RECUPERADOS']:.0f} - {nuevo_rec})^2) = {d:>10.2f}")
    
    print("Observación: La variable Registrados (en cientos/miles) anula totalmente a Recuperados (en unidades).")


def ejecutar_torneo_clasificacion():
    """
    Ejecuta el torneo completo de los tres modelos de clasificación sobre el dataset integrado.
    """
    ruta = resolver_ruta_dataset()
    df = pd.read_csv(ruta)
    
    ejemplo_bayes_manual(df)
    ejemplo_distancia_knn_mano(df)
    
    print("\n" + "="*80)
    print("3. EL GRAN TORNEO DE CLASIFICACIÓN (SESIÓN 8)")
    print("="*80)
    
    # Preparación rigurosa de variables
    num = ["AÑO", "VEHICULOS_REGISTRADOS", "VEHICULOS_RECUPERADOS"]
    X = pd.get_dummies(df[num + ["TIPO_VEHICULO"]], columns=["TIPO_VEHICULO"], drop_first=True)
    y = (df["VEHICULOS_HURTADOS"] > 0).astype(int)
    
    # Partición equitativa (exactamente la misma para todos)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"Observaciones Totales: {len(df):,}")
    print(f"Conjunto Entrenamiento (Train 75%): {len(X_train):,} filas")
    print(f"Conjunto Prueba (Test 25%):         {len(X_test):,} filas")
    print(f"Distribución de Clases en Test: 0 (Sin hurto)={sum(y_test==0):,}, 1 (Hurto activo)={sum(y_test==1):,}")
    
    modelos = {
        "Arbol (prof=4)": DecisionTreeClassifier(max_depth=4, random_state=42),
        "Naive Bayes (GaussianNB)": GaussianNB(),
        "KNN (k=5, SIN escalar)": KNeighborsClassifier(n_neighbors=5),
        "KNN (k=5, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
        "KNN (k=11, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=11)),
        "KNN (k=31, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=31)),
        "KNN (k=51, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=51)),
        "KNN (k=101, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=101)),
    }
    
    resultados = []
    
    print("\n" + "-"*115)
    print(f"{'Modelo':<28} {'Fit(s)':>8} {'Pred(s)':>8} {'Acc_Tr':>8} {'Acc_Te':>8} {'Gap(%)':>7} {'Prec':>7} {'Recall':>8} {'F1':>7}")
    print("-"*115)
    
    for nombre, modelo in modelos.items():
        t0 = time.perf_counter()
        modelo.fit(X_train, y_train)
        t_fit = time.perf_counter() - t0
        
        t0 = time.perf_counter()
        y_pred = modelo.predict(X_test)
        t_pred = time.perf_counter() - t0
        
        acc_tr = modelo.score(X_train, y_train)
        acc_te = accuracy_score(y_test, y_pred)
        gap = (acc_tr - acc_te) * 100
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"{nombre:<28} {t_fit:>8.4f} {t_pred:>8.4f} {acc_tr:>8.4f} {acc_te:>8.4f} {gap:>7.2f}% {prec:>7.4f} {rec:>8.4f} {f1:>7.4f}")
        
        resultados.append({
            "modelo": nombre,
            "t_fit": t_fit,
            "t_pred": t_pred,
            "acc_train": acc_tr,
            "acc_test": acc_te,
            "gap": gap,
            "precision": prec,
            "recall": rec,
            "f1_score": f1
        })
    print("-"*115)
    
    # Análisis de Matrices de Confusión Clave
    print("\n" + "="*80)
    print("4. MATRICES DE CONFUSIÓN DE LOS CONTENDIENTES PRINCIPALES")
    print("="*80)
    
    modelos_clave = {
        "Árbol de Decisión (prof=4)": DecisionTreeClassifier(max_depth=4, random_state=42),
        "Naive Bayes (GaussianNB)": GaussianNB(),
        "KNN (k=31, StandardScaler)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=31))
    }
    
    for nom, mod in modelos_clave.items():
        mod.fit(X_train, y_train)
        preds = mod.predict(X_test)
        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel()
        print(f"\n--- {nom} ---")
        print(f"Verdaderos Negativos (TN): {tn:>6,} | Falsos Positivos (FP):  {fp:>6,}")
        print(f"Falsos Negativos (FN):     {fn:>6,} | Verdaderos Positivos (TP):{tp:>6,}")
        print(f"-> Tasa de Falsos Negativos (Crimen no detectado): {fn / (fn + tp) * 100:.2f}%")
        print(f"-> Recall (Sensibilidad de detección):           {tp / (fn + tp) * 100:.2f}%")
    
    return pd.DataFrame(resultados)


if __name__ == "__main__":
    df_res = ejecutar_torneo_clasificacion()

