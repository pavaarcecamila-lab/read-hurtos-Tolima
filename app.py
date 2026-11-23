"""
app.py — Observatorio de Inteligencia y Minería de Datos: Hurto Vehicular en Colombia
Énfasis Territorial: Departamento del Tolima
Autoras: Natalia Valencia & Camila Pava
Docente: Esteban Ernesto Morales Castro · UNIMINUTO Ibagué · 2026-2
"""

import sys
import os
from pathlib import Path

# Inyección defensiva de rutas para dependencias
for p in [
    "/opt/homebrew/lib/python3.11/site-packages",
    str(Path(__file__).resolve().parent.parent / ".local_python/lib/python3.11/site-packages"),
    "/Users/camilapava/Documents/OCTAVO SEMESTRE/MINERIA 3 CORTE/.local_python/lib/python3.11/site-packages"
]:
    if p not in sys.path and os.path.exists(p):
        sys.path.insert(0, p)

os.environ["MPLCONFIGDIR"] = "/tmp/mpl"

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix

try:
    from ui_templates import (
        cargar_estilos_css,
        render_hero_banner,
        render_context_box,
        render_kpi_card,
        render_model_card,
        render_cluster_kpi,
        render_cluster_card,
        render_alert_card,
        render_sidebar_authors
    )
except ImportError:
    from src.ui_templates import (
        cargar_estilos_css,
        render_hero_banner,
        render_context_box,
        render_kpi_card,
        render_model_card,
        render_cluster_kpi,
        render_cluster_card,
        render_alert_card,
        render_sidebar_authors
    )

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA Y ESTILO ESTÉTICO PROFESIONAL
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatorio de Seguridad Vehicular · Colombia & Tolima",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos desacoplados (static/css/styles.css)
cargar_estilos_css()

# ─────────────────────────────────────────────────────────────────────────────
# CARGA Y CACHÉ DE DATOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    candidatos = [
        Path(__file__).resolve().parent / "dataset/dataset_integrado.csv",
        Path("dataset/dataset_integrado.csv"),
        Path("read-hurtos-Tolima/dataset/dataset_integrado.csv"),
    ]
    ruta = next((c for c in candidatos if c.exists()), None)
    if not ruta:
        st.error("No se encontró el archivo de datos.")
        st.stop()
    df = pd.read_csv(ruta)
    df["TASA_RECUPERACION"] = np.where(
        df["VEHICULOS_HURTADOS"] > 0,
        (df["VEHICULOS_RECUPERADOS"] / df["VEHICULOS_HURTADOS"]) * 100,
        np.where(df["VEHICULOS_RECUPERADOS"] > 0, 100.0, 0.0)
    )
    df["TASA_RECUPERACION"] = df["TASA_RECUPERACION"].clip(upper=100.0)
    return df

df_raw = cargar_datos()

# ─────────────────────────────────────────────────────────────────────────────
# ENTRENAMIENTO DE MODELOS EN MEMORIA (CACHED)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def entrenar_modelos(df):
    df_mod = df[df["AÑO"] >= 2010].copy()
    
    # Clustering K-Means k=4
    vars_clus = ["VEHICULOS_REGISTRADOS", "VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]
    scaler_clus = StandardScaler()
    X_clus_sc = scaler_clus.fit_transform(df_mod[vars_clus])
    
    km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_mod["CLUSTER"] = km4.fit_predict(X_clus_sc)
    
    nombres_clus = {
        0: "🟢 C0: Zonas Pacíficas",
        1: "🟡 C1: Riesgo Moderado",
        2: "🔴 C2: FOCO CRÍTICO",
        3: "🟠 C3: Parque Grande / Bajo Hurto"
    }
    df_mod["CLUSTER_NOMBRE"] = df_mod["CLUSTER"].map(nombres_clus)

    # Clasificación Supervisada
    df["TARGET_HURTO"] = (df["VEHICULOS_HURTADOS"] > 0).astype(int)
    features_clf = ["AÑO", "CODIGO_DANE_MUNICIPIO", "VEHICULOS_REGISTRADOS", "VEHICULOS_RECUPERADOS"]
    X_clf = df[features_clf].values
    y_clf = df["TARGET_HURTO"].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_clf, y_clf, test_size=0.25, random_state=42, stratify=y_clf
    )
    
    # Árbol (Ganador)
    tree_clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    tree_clf.fit(X_train, y_train)
    
    # Naive Bayes
    gnb_clf = GaussianNB()
    gnb_clf.fit(X_train, y_train)
    
    # KNN (k=31)
    scaler_knn = StandardScaler()
    X_train_sc = scaler_knn.fit_transform(X_train)
    X_test_sc = scaler_knn.transform(X_test)
    knn_clf = KNeighborsClassifier(n_neighbors=31)
    knn_clf.fit(X_train_sc, y_train)
    
    y_pred_tree = tree_clf.predict(X_test)
    y_pred_knn = knn_clf.predict(X_test_sc)
    y_pred_gnb = gnb_clf.predict(X_test)

    metricas = {
        "tree": {
            "acc": accuracy_score(y_test, y_pred_tree),
            "recall": recall_score(y_test, y_pred_tree),
            "f1": f1_score(y_test, y_pred_tree),
            "cm": confusion_matrix(y_test, y_pred_tree)
        },
        "knn": {
            "acc": accuracy_score(y_test, y_pred_knn),
            "recall": recall_score(y_test, y_pred_knn),
            "f1": f1_score(y_test, y_pred_knn),
            "cm": confusion_matrix(y_test, y_pred_knn)
        },
        "gnb": {
            "acc": accuracy_score(y_test, y_pred_gnb),
            "recall": recall_score(y_test, y_pred_gnb),
            "f1": f1_score(y_test, y_pred_gnb),
            "cm": confusion_matrix(y_test, y_pred_gnb)
        }
    }
    
    return {
        "df_mod": df_mod,
        "tree_clf": tree_clf,
        "gnb_clf": gnb_clf,
        "knn_clf": knn_clf,
        "scaler_knn": scaler_knn,
        "metricas": metricas
    }

models_data = entrenar_modelos(df_raw)
df_clustered = models_data["df_mod"]

# ─────────────────────────────────────────────────────────────────────────────
# BARRA LATERAL (SIDEBAR) & FILTROS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 16px 0;">
        <div style="font-size: 1.2rem; font-weight: 800; color: #0F172A; display: flex; align-items: center; gap: 8px;">
            <span>🛡️</span> Observatorio IA
        </div>
        <div style="font-size: 0.8rem; color: #64748B; font-weight: 500; margin-top: 2px;">
            Minería de Datos · Corte 3
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 8px;'>Filtros de Exploración</div>", unsafe_allow_html=True)
    
    deps_disponibles = sorted(df_raw["DEPARTAMENTO"].dropna().unique().tolist())
    def_dep = ["TOLIMA"] if "TOLIMA" in deps_disponibles else [deps_disponibles[0]]
    dep_sel = st.multiselect("Departamento:", options=["TODOS"] + deps_disponibles, default=def_dep)
    
    # Filtro dinámico de Municipio / Ciudad en el panel lateral
    deps_activos = df_raw["DEPARTAMENTO"].unique().tolist() if ("TODOS" in dep_sel or len(dep_sel) == 0) else dep_sel
    munis_en_dep = sorted(df_raw[df_raw["DEPARTAMENTO"].isin(deps_activos)]["MUNICIPIO"].dropna().unique().tolist())
    muni_filtro = st.selectbox("Municipio / Ciudad (Filtro Global):", ["TODOS"] + munis_en_dep, index=0)
    
    anio_max = int(df_raw["AÑO"].max())
    rango_anios = st.slider("Rango de Años:", min_value=2010, max_value=anio_max, value=(2010, anio_max))
    
    tipos_veh = ["TODOS"] + sorted(df_raw["TIPO_VEHICULO"].dropna().unique().tolist())
    tipo_sel = st.selectbox("Tipo de Vehículo:", tipos_veh, index=0)
    
    st.markdown("<hr style='margin: 18px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    render_sidebar_authors()

# Filtro en caliente
df_filtrado = df_raw.copy()
if "TODOS" not in dep_sel and len(dep_sel) > 0:
    df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO"].isin(dep_sel)]
if muni_filtro != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["MUNICIPIO"] == muni_filtro]
df_filtrado = df_filtrado[(df_filtrado["AÑO"] >= rango_anios[0]) & (df_filtrado["AÑO"] <= rango_anios[1])]
if tipo_sel != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["TIPO_VEHICULO"] == tipo_sel]

# ─────────────────────────────────────────────────────────────────────────────
# BANNER PRINCIPAL (HERO)
# ─────────────────────────────────────────────────────────────────────────────
render_hero_banner(
    titulo="Observatorio de Inteligencia y Minería de Datos",
    subtitulo="Análisis Predictivo del Hurto Vehicular y Capacidad de Recuperación Policial en Colombia",
    autoras="Natalia Valencia & Camila Pava",
    docente="Esteban Ernesto Morales Castro",
    institucion="UNIMINUTO Ibagué · 2026-2"
)

# ─────────────────────────────────────────────────────────────────────────────
# MENÚ DE NAVEGACIÓN VERTICAL (ACCESIBLE SIEMPRE EN LA PÁGINA)
# ─────────────────────────────────────────────────────────────────────────────
seccion = st.radio(
    "🧭 Menú de Navegación entre Módulos:",
    [
        "📊 Diagnóstico & Contexto Estratégico",
        "🌲 Clasificación Supervisada (Árbol, KNN, Bayes)",
        "🎯 Segmentación Territorial (K-Means & Jerárquico)",
        "🔍 Ficha Táctica Municipal (Seleccionar Ciudad)",
        "📐 Métodos Numéricos (Regresión & Lagrange)",
        "📑 Conclusiones & Recomendaciones"
    ],
    horizontal=False,
    index=0
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1: DIAGNÓSTICO & CONTEXTO ESTRATÉGICO
# ─────────────────────────────────────────────────────────────────────────────
if "📊 Diagnóstico" in seccion:
    
    # Tarjeta de Contexto Académico
    render_context_box()

    # Tarjetas KPI Principales
    total_h = int(df_filtrado["VEHICULOS_HURTADOS"].sum())
    total_r = int(df_filtrado["VEHICULOS_RECUPERADOS"].sum())
    tasa_g = (total_r / total_h * 100) if total_h > 0 else 0.0
    mun_c = df_filtrado.groupby("MUNICIPIO")["VEHICULOS_HURTADOS"].sum().idxmax() if len(df_filtrado) > 0 else "N/A"
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Vehículos Hurtados", f"{total_h:,}", "Casos en filtro seleccionado", "#F43F5E", "#E11D48", "#E11D48")
    with col2:
        render_kpi_card("Vehículos Recuperados", f"{total_r:,}", "Efectividad policial registrada", "#10B981", "#059669", "#059669")
    with col3:
        render_kpi_card("Tasa de Recuperación", f"{tasa_g:.1f}%", "Recuperados vs Hurtados", "#0EA5E9", "#0284C7", "#64748B")
    with col4:
        render_kpi_card("Municipio Más Afectado", mun_c, "Mayor concentración criminal", "#F59E0B", "#D97706", "#D97706")

    st.info("💡 **¿Desea explorar la ficha táctica de una ciudad específica?** Seleccione arriba el botón **'🔍 Ficha Táctica Municipal (Seleccionar Ciudad)'** o utilice el filtro del panel lateral izquierdo.")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    c_left, c_right = st.columns([1.6, 1])
    with c_left:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0 0 14px 0; color:#0F172A;'>📈 Evolución Histórica: Hurtos vs Recuperaciones</h4>", unsafe_allow_html=True)
        df_lin = df_filtrado.groupby("AÑO")[["VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]].sum().reset_index()
        fig_l = go.Figure()
        fig_l.add_trace(go.Scatter(
            x=df_lin["AÑO"], y=df_lin["VEHICULOS_HURTADOS"],
            mode="lines+markers", name="Hurtados",
            line=dict(color="#F43F5E", width=3, shape="spline"),
            marker=dict(size=7, color="#F43F5E")
        ))
        fig_l.add_trace(go.Scatter(
            x=df_lin["AÑO"], y=df_lin["VEHICULOS_RECUPERADOS"],
            mode="lines+markers", name="Recuperados",
            line=dict(color="#10B981", width=3, shape="spline"),
            marker=dict(size=7, color="#10B981")
        ))
        fig_l.update_layout(
            template="plotly_white",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            xaxis_title="<b>Eje X:</b> Año Calendario (Línea de Tiempo Histórica)",
            yaxis_title="<b>Eje Y:</b> Total de Vehículos (Casos Registrados)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
            height=340
        )
        st.plotly_chart(fig_l, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with c_right:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0 0 14px 0; color:#0F172A;'>🏍️ vs 🚗 Brecha por Tipo de Vehículo</h4>", unsafe_allow_html=True)
        df_pie = df_filtrado.groupby("TIPO_VEHICULO")["VEHICULOS_HURTADOS"].sum().reset_index()
        fig_p = px.pie(
            df_pie, values="VEHICULOS_HURTADOS", names="TIPO_VEHICULO",
            hole=0.55,
            color_discrete_sequence=["#0EA5E9", "#6366F1"]
        )
        fig_p.update_layout(
            template="plotly_white",
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_p, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Ranking Top 10
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0 0 14px 0; color:#0F172A;'>🚨 Top 10 Municipios con Mayor Afectación Delictiva</h4>", unsafe_allow_html=True)
    df_top = (
        df_filtrado.groupby(["MUNICIPIO", "DEPARTAMENTO"])[["VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]]
        .sum().reset_index()
        .sort_values(by="VEHICULOS_HURTADOS", ascending=False)
        .head(10)
    )
    df_top["TASA_REC"] = (df_top["VEHICULOS_RECUPERADOS"] / df_top["VEHICULOS_HURTADOS"] * 100).round(1)
    
    fig_bar = px.bar(
        df_top, x="VEHICULOS_HURTADOS", y="MUNICIPIO",
        orientation="h", color="TASA_REC",
        color_continuous_scale=["#F43F5E", "#FBBF24", "#10B981"],
        labels={"VEHICULOS_HURTADOS": "Eje X: Hurtos Totales", "TASA_REC": "Tasa Recuperación (%)", "MUNICIPIO": "Eje Y: Ciudad"},
        text="VEHICULOS_HURTADOS"
    )
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_title="<b>Eje X:</b> Total de Vehículos Hurtados (Casos Anuales)",
        yaxis_title="<b>Eje Y:</b> Municipio / Ciudad",
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=330
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2: CLASIFICACIÓN SUPERVISADA (ÁRBOL, KNN, BAYES)
# ─────────────────────────────────────────────────────────────────────────────
elif "🌲 Clasificación" in seccion:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">Torneo de Clasificación Supervisada</h2>
        <p style="color: #64748B; margin:0; font-size: 0.95rem;">
            Evaluación comparativa rigurosa: predecir si un municipio presenta <b>Hurto Activo (y=1)</b> o <b>Cero Hurtos (y=0)</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    t_m = models_data["metricas"]["tree"]
    k_m = models_data["metricas"]["knn"]
    g_m = models_data["metricas"]["gnb"]
    
    with m_col1:
        render_model_card(
            pill_class="pill-win",
            pill_text="🏆 GANADOR OFICIAL",
            title="Árbol de Decisión",
            subtitle="Profundidad óptima = 4",
            acc=f"{t_m['acc']*100:.2f}%",
            recall=f"{t_m['recall']*100:.2f}%",
            f1=f"{t_m['f1']:.3f}",
            note="✓ Velocidad de inferencia: 0.0009s · 100% interpretable en estrados y mandos policiales.",
            border_color="#10B981",
            bg_color="#FAFDFB",
            title_color="#065F46",
            recall_color="#059669",
            note_color="#047857"
        )

    with m_col2:
        render_model_card(
            pill_class="pill-runner",
            pill_text="SUBCAMPEÓN",
            title="KNN (k = 31)",
            subtitle="Normalización StandardScaler",
            acc=f"{k_m['acc']*100:.2f}%",
            recall=f"{k_m['recall']*100:.2f}%",
            f1=f"{k_m['f1']:.3f}",
            note="⚠️ 46 veces más lento en inferencia. Inviable para despliegue en tiempo real con 54k filas.",
            border_color="#BFDBFE",
            bg_color="#FFFFFF",
            title_color="#1E40AF",
            recall_color="#1E40AF",
            note_color="#64748B"
        )

    with m_col3:
        render_model_card(
            pill_class="pill-fail",
            pill_text="DESCARTADO",
            title="Gaussian Naive Bayes",
            subtitle="Supuesto de independencia",
            acc=f"{g_m['acc']*100:.2f}%",
            recall=f"{g_m['recall']*100:.2f}%",
            f1=f"{g_m['f1']:.3f}",
            note="🚨 2,750 falsos negativos. Deja sin protección policial a municipios con crimen activo.",
            border_color="#FECDD3",
            bg_color="#FFFFFF",
            title_color="#9F1239",
            recall_color="#BE123C",
            note_color="#BE123C"
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # Simulador Táctico
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0 0 8px 0; color:#0F172A;'>🎮 Simulador Predictivo en Tiempo Real</h4>", unsafe_allow_html=True)
    st.caption("Ajusta las variables de un municipio para consultar la inferencia en milisegundos con el modelo ganador:")
    
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        s_anio = st.number_input("Año de Planificación:", 2024, 2030, 2026)
    with sc2:
        s_parque = st.number_input("Parque Automotor Registrado:", 1, 250000, 2200)
    with sc3:
        s_recup = st.number_input("Recuperaciones Históricas Previas:", 0, 5000, 8)
        
    if st.button("⚡ Ejecutar Inferencia de Riesgo", type="primary"):
        vec = np.array([[s_anio, 73001, s_parque, s_recup]])
        pred = models_data["tree_clf"].predict(vec)[0]
        prob = models_data["tree_clf"].predict_proba(vec)[0][1]
        
        if pred == 1:
            render_alert_card(
                titulo="🚨 ALERTA: MUNICIPIO EN CONDICIÓN DE HURTO ACTIVO",
                probabilidad=f"{prob*100:.1f}%",
                dictamen=f"La concentración del parque automotor ({s_parque:,}) supera el umbral crítico de exposición criminal.",
                recomendacion="Asignación prioritaria de patrullaje por cuadrantes y puestos de control móvil.",
                es_alerta=True
            )
        else:
            render_alert_card(
                titulo="✅ ZONA SEGURA: BAJO RIESGO DE HURTO VEHICULAR",
                probabilidad=f"{prob*100:.1f}%",
                dictamen="Municipio en rango de baja incidencia delictiva.",
                recomendacion="Monitoreo preventivo ordinario.",
                es_alerta=False
            )
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3: SEGMENTACIÓN TERRITORIAL (CLUSTERING)
# ─────────────────────────────────────────────────────────────────────────────
elif "🎯 Segmentación" in seccion:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">Segmentación Territorial No Supervisada</h2>
        <p style="color: #64748B; margin:0; font-size: 0.95rem;">
            Descubrimiento de grupos naturales de municipios según exposición al hurto y capacidad de recuperación policial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4 Tarjetas de Clusters
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_cluster_kpi("🟢 CLUSTER 0", "Zonas Pacíficas", "88.9%", "24,521 registros", "3.8 / año", "75.6%", "#10B981")
    with c2:
        render_cluster_kpi("🟡 CLUSTER 1", "Riesgo Moderado", "5.4%", "1,482 registros", "37.2 / año", "83.5%", "#F59E0B")
    with c3:
        render_cluster_kpi("🔴 CLUSTER 2", "FOCO CRÍTICO", "2.4%", "666 registros", "201.8 / año", "26.5%", "#F43F5E", bg_color="#FFFBFB", title_color="#9F1239", sub_color="#F43F5E")
    with c4:
        render_cluster_kpi("🟠 CLUSTER 3", "Parque Grande", "3.3%", "908 registros", "38.0 / año", "43.0%", "#0EA5E9")

    st.info("💡 **¿Desea explorar la ficha táctica de una ciudad específica?** Seleccione arriba el botón **'🔍 Ficha Táctica Municipal (Seleccionar Ciudad)'** o utilice el filtro del panel lateral izquierdo.")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Gráfico de dispersión
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0 0 12px 0; color:#0F172A;'>🌌 Mapa Espacial de Clusters (Plotly)</h4>", unsafe_allow_html=True)
    df_samp = df_clustered.sample(min(2500, len(df_clustered)), random_state=42)
    fig_scat = px.scatter(
        df_samp,
        x="VEHICULOS_HURTADOS",
        y="VEHICULOS_RECUPERADOS",
        color="CLUSTER_NOMBRE",
        size="VEHICULOS_REGISTRADOS",
        hover_data=["MUNICIPIO", "DEPARTAMENTO", "AÑO"],
        color_discrete_map={
            "🟢 C0: Zonas Pacíficas": "#10B981",
            "🟡 C1: Riesgo Moderado": "#F59E0B",
            "🔴 C2: FOCO CRÍTICO": "#F43F5E",
            "🟠 C3: Parque Grande / Bajo Hurto": "#0EA5E9"
        },
        labels={
            "VEHICULOS_HURTADOS": "Eje X: Vehículos Hurtados (Incidencia Delictiva)",
            "VEHICULOS_RECUPERADOS": "Eje Y: Vehículos Recuperados (Efectividad Policial)",
            "CLUSTER_NOMBRE": "Clúster / Segmento",
            "VEHICULOS_REGISTRADOS": "Parque Automotor Registrado"
        }
    )
    fig_scat.update_layout(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="<b>Eje X (Causa):</b> Vehículos Hurtados Anuales (Incidencia Criminal)",
        yaxis_title="<b>Eje Y (Efecto):</b> Vehículos Recuperados Anuales (Operatividad Policial)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=400
    )
    st.plotly_chart(fig_scat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4: FICHA TÁCTICA MUNICIPAL
# ─────────────────────────────────────────────────────────────────────────────
elif "🔍 Ficha Táctica" in seccion:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="display:inline-flex; align-items:center; gap:8px; background:#EFF6FF; border:1px solid #BFDBFE; color:#1D4ED8; padding:4px 14px; border-radius:20px; font-size:0.82rem; font-weight:700; margin-bottom:8px;">
            <span>🛡️</span> INTELIGENCIA OPERATIVA POLICIAL
        </div>
        <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">🔍 Ficha Táctica Territorial por Municipio</h2>
        <p style="color: #64748B; margin:0; font-size: 0.95rem;">
            Perfil criminológico individualizado: radiografía delictiva, brecha motos vs carros, asignación de clúster y dictamen de planeación policial territorial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Selectores de Exploración ──
    col_sel1, col_sel2, col_sel3 = st.columns([1.2, 1.8, 1.2])
    
    with col_sel1:
        deps_disponibles = sorted([d for d in df_clustered["DEPARTAMENTO"].dropna().unique().tolist() if str(d).strip() != ""])
        opciones_dep = ["TODOS"] + deps_disponibles
        idx_dep_def = opciones_dep.index("TOLIMA") if "TOLIMA" in opciones_dep else 0
        dep_ficha = st.selectbox("🏛️ Departamento:", opciones_dep, index=idx_dep_def)
    
    df_pool = df_clustered if dep_ficha == "TODOS" else df_clustered[df_clustered["DEPARTAMENTO"] == dep_ficha]
    munis_disponibles = sorted([m for m in df_pool["MUNICIPIO"].dropna().unique().tolist() if str(m).strip() != ""])
    idx_mun_def = munis_disponibles.index("IBAGUE") if "IBAGUE" in munis_disponibles else 0
    
    with col_sel2:
        m_sel = st.selectbox("🏙️ Ciudad / Municipio a Consultar:", munis_disponibles, index=idx_mun_def)
        
    with col_sel3:
        periodo_ficha = st.selectbox(
            "📅 Ventana Temporal:",
            ["Periodo Oficial (2010–2024)", "Histórico Completo (2010+)"],
            index=0
        )
    
    df_m = df_pool[df_pool["MUNICIPIO"] == m_sel].copy()
    if "2010–2024" in periodo_ficha:
        df_m = df_m[(df_m["AÑO"] >= 2010) & (df_m["AÑO"] <= 2024)]
        
    if len(df_m) > 0:
        dep_real = df_m["DEPARTAMENTO"].iloc[0]
        h_m = int(df_m["VEHICULOS_HURTADOS"].sum())
        r_m = int(df_m["VEHICULOS_RECUPERADOS"].sum())
        t_m = (r_m / h_m * 100) if h_m > 0 else 0.0
        
        # Desglose Motos vs Automotores
        df_motos = df_m[df_m["TIPO_VEHICULO"] == "MOTOCICLETA"]
        df_autos = df_m[df_m["TIPO_VEHICULO"] == "AUTOMOTOR"]
        
        h_motos = int(df_motos["VEHICULOS_HURTADOS"].sum())
        r_motos = int(df_motos["VEHICULOS_RECUPERADOS"].sum())
        t_motos = (r_motos / h_motos * 100) if h_motos > 0 else 0.0
        pct_motos = (h_motos / h_m * 100) if h_m > 0 else 0.0
        
        h_autos = int(df_autos["VEHICULOS_HURTADOS"].sum())
        r_autos = int(df_autos["VEHICULOS_RECUPERADOS"].sum())
        t_autos = (r_autos / h_autos * 100) if h_autos > 0 else 0.0
        pct_autos = (h_autos / h_m * 100) if h_m > 0 else 0.0
        
        # Clúster táctico
        c_m = df_m["CLUSTER_NOMBRE"].mode()[0] if len(df_m) > 0 else "🟢 C0: Zonas Pacíficas"
        c_motos = df_motos["CLUSTER_NOMBRE"].mode()[0] if len(df_motos) > 0 else c_m
        c_autos = df_autos["CLUSTER_NOMBRE"].mode()[0] if len(df_autos) > 0 else c_m
        
        # Color semafórico de efectividad
        color_efectividad = "#10B981" if t_m >= 60 else ("#F59E0B" if t_m >= 35 else "#F43F5E")
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # ── Grid de KPIs Principales ──
        fk1, fk2, fk3, fk4, fk5 = st.columns(5)
        with fk1:
            render_kpi_card("Hurtos Totales", f"{h_m:,}", f"{dep_real} · {periodo_ficha.split(' ')[0]}", "#F43F5E", "#E11D48", "#E11D48")
        with fk2:
            render_kpi_card("Recuperaciones", f"{r_m:,}", "Operatividad Policial", "#10B981", "#059669", "#059669")
        with fk3:
            render_kpi_card("Efectividad Policial", f"{t_m:.1f}%", "Tasa Global Recuperación", color_efectividad, color_efectividad, "#64748B")
        with fk4:
            render_kpi_card("Impacto Motos", f"{pct_motos:.1f}%", f"{h_motos:,} motos hurtadas", "#6366F1", "#4F46E5", "#4F46E5")
        with fk5:
            color_clus = "#EF4444" if "C2" in c_m else ("#F59E0B" if "C1" in c_m else ("#10B981" if "C0" in c_m else "#6366F1"))
            render_kpi_card("Clúster Territorial", c_m.split(":")[0], c_m.split(":")[1].strip(), color_clus, "#0F172A", "#64748B")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # ── Caja Comparativa: Radiografía Motos vs Carros ──
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:20px; box-shadow:0 4px 18px -2px rgba(0,0,0,0.03); margin-bottom:20px;">
            <div style="font-size:1.1rem; font-weight:800; color:#0F172A; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                <span>⚖️</span> Radiografía Delictiva Comparada: Motocicletas vs Automotores en {m_sel}
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:4px solid #6366F1; border-radius:12px; padding:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-weight:800; color:#1E1B4B; font-size:1.05rem;">🏍️ MOTOCICLETAS</span>
                        <span style="background:#EEF2FF; color:#4338CA; padding:3px 10px; border-radius:12px; font-size:0.78rem; font-weight:700;">{c_motos}</span>
                    </div>
                    <div style="font-size:0.88rem; color:#334155; line-height:1.7;">
                        • <b>Hurtos Registrados:</b> <span style="color:#DC2626; font-weight:700;">{h_motos:,}</span> ({pct_motos:.1f}% del total municipal)<br>
                        • <b>Recuperaciones:</b> <span style="color:#16A34A; font-weight:700;">{r_motos:,}</span><br>
                        • <b>Tasa de Recuperación:</b> <span style="font-weight:800; color:{'#16A34A' if t_motos>=50 else '#DC2626'};">{t_motos:.1f}%</span><br>
                        • <b>Dinámica Criminológica:</b> Desguace y receptación ilícita exprés (&lt;120 min), alteración de sistemas de identificación y comercialización clandestina de repuestos.
                    </div>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:4px solid #0EA5E9; border-radius:12px; padding:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-weight:800; color:#082F49; font-size:1.05rem;">🚗 AUTOMOTORES</span>
                        <span style="background:#F0F9FF; color:#0369A1; padding:3px 10px; border-radius:12px; font-size:0.78rem; font-weight:700;">{c_autos}</span>
                    </div>
                    <div style="font-size:0.88rem; color:#334155; line-height:1.7;">
                        • <b>Hurtos Registrados:</b> <span style="color:#DC2626; font-weight:700;">{h_autos:,}</span> ({pct_autos:.1f}% del total municipal)<br>
                        • <b>Recuperaciones:</b> <span style="color:#16A34A; font-weight:700;">{r_autos:,}</span><br>
                        • <b>Tasa de Recuperación:</b> <span style="font-weight:800; color:{'#16A34A' if t_autos>=50 else '#DC2626'};">{min(t_autos, 100.0):.1f}%</span><br>
                        • <b>Dinámica Criminológica:</b> Modalidad predominante de halado y gemeleo/clonación de placas; alta efectividad policial por trazabilidad GPS y arcos LPR.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ── Visualizaciones Tácticas Interactivas ──
        col_g1, col_g2 = st.columns([1.5, 1])
        
        with col_g1:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0 0 12px 0; color:#0F172A;'>📈 Evolución Histórica: Hurtos vs Recuperaciones en {m_sel}</h4>", unsafe_allow_html=True)
            df_evo = df_m.groupby("AÑO")[["VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]].sum().reset_index()
            fig_evo = go.Figure()
            fig_evo.add_trace(go.Scatter(
                x=df_evo["AÑO"], y=df_evo["VEHICULOS_HURTADOS"],
                mode="lines+markers", name="Vehículos Hurtados",
                line=dict(color="#F43F5E", width=3, shape="spline"),
                marker=dict(size=7, color="#F43F5E")
            ))
            fig_evo.add_trace(go.Scatter(
                x=df_evo["AÑO"], y=df_evo["VEHICULOS_RECUPERADOS"],
                mode="lines+markers", name="Vehículos Recuperados",
                line=dict(color="#10B981", width=3, shape="spline"),
                marker=dict(size=7, color="#10B981")
            ))
            fig_evo.update_layout(
                template="plotly_white",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                hovermode="x unified",
                xaxis_title="<b>Eje X:</b> Año Calendario (Serie Observada)",
                yaxis_title="<b>Eje Y:</b> Cantidad de Vehículos",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=10, r=10, t=10, b=10),
                height=320
            )
            st.plotly_chart(fig_evo, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0 0 12px 0; color:#0F172A;'>📊 Distribución por Tipo de Vehículo en {m_sel}</h4>", unsafe_allow_html=True)
            df_tipo_bar = df_m.groupby("TIPO_VEHICULO")[["VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS"]].sum().reset_index()
            fig_bar_tipo = go.Figure()
            fig_bar_tipo.add_trace(go.Bar(
                name="Hurtados", x=df_tipo_bar["TIPO_VEHICULO"], y=df_tipo_bar["VEHICULOS_HURTADOS"],
                marker_color="#F43F5E"
            ))
            fig_bar_tipo.add_trace(go.Bar(
                name="Recuperados", x=df_tipo_bar["TIPO_VEHICULO"], y=df_tipo_bar["VEHICULOS_RECUPERADOS"],
                marker_color="#10B981"
            ))
            fig_bar_tipo.update_layout(
                barmode="group",
                template="plotly_white",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="<b>Eje X:</b> Modalidad de Transporte",
                yaxis_title="<b>Eje Y:</b> Total Casos",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=10, r=10, t=10, b=10),
                height=320
            )
            st.plotly_chart(fig_bar_tipo, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Plan de Acción Táctico Policial (Dictamen Operativo Inteligente) ──
        if "C2" in c_m or h_motos >= 1000 or m_sel == "IBAGUE":
            titulo_alerta = f"🚨 DICTAMEN TÁCTICO: INTERVENCIÓN ESTRATÉGICA METROPOLITANA — {m_sel}"
            bg_alerta = "#FFF1F2"
            border_alerta = "#F43F5E"
            color_tit_alerta = "#9F1239"
            if m_sel == "IBAGUE":
                rec_candado = "Cierre en ventana dorada (&lt;15 min) en los 3 ejes de fuga: (1) Variante Ibagué-Bogotá / Picaleña, (2) Corredor Cajamarca-Túnel de La Línea (hacia Eje Cafetero), y (3) Vía al Norte del Tolima (Alvarado-Honda)."
                rec_talleres = "Inspección técnica judicial prioritaria en talleres y bodegas clandestinas de la Calle 21, Barrio El Carmen y sector Mirolindo para erradicar el mercado ilícito de autopartes."
            elif m_sel == "ESPINAL":
                rec_candado = "Control perimetral sobre la rotonda La Tambora, interceptando las salidas hacia El Guamo, Flandes/Girardot y la variante a Neiva."
                rec_talleres = "Fiscalización intensiva a desguazaderos de motos ante una concentración récord de 94.3% de hurtos en motocicletas."
            else:
                rec_candado = "Activación del Plan Candado Metropolitano con bloqueo coordinado en los principales corredores intermunicipales de escape."
                rec_talleres = "Allanamientos conjuntos SIJIN-Fiscalía a bodegas de autopartes ilegales y mercados clandestinos de receptación."
            
            puntos_accion = f"""
            • <b>Plan Candado Exprés (Ventana Dorada 15 min):</b> {rec_candado}<br>
            • <b>Lucha contra el Desguace y Receptación:</b> {rec_talleres}<br>
            • <b>Arcos de Fotodetección y Cámaras LPR:</b> Lectura automática de placas en los accesos urbanos para detectar motocicletas y automotores con reporte vigente en tiempo real.<br>
            • <b>Patrullaje Preventivo Nocturno:</b> Disuasión activa en puntos críticos entre las 18:00 y las 04:00 horas frente a la modalidad de halado en parqueo informal.
            """
        elif "C1" in c_m or (h_m >= 200 and t_m >= 50):
            titulo_alerta = f"🟡 DICTAMEN TÁCTICO: CABECERA INTERMEDIA CON RIESGO ACTIVO Y ALTA RESPUESTA — {m_sel}"
            bg_alerta = "#FEFCE8"
            border_alerta = "#EAB308"
            color_tit_alerta = "#854D0E"
            puntos_accion = f"""
            • <b>Sostener la Tasa de Respuesta:</b> El municipio muestra una capacidad de recuperación destacada ({t_m:.1f}%), siendo referente operativo.<br>
            • <b>Puestos de Control Viales Móviles:</b> Ubicar retenes en fines de semana y festivos sobre los corredores turísticos y de conexión intermunicipal.<br>
            • <b>Campañas de Marcación Gratuita de Motos:</b> Promover la marcación profunda de chasis y piezas visibles para frenar el halado oportunista.<br>
            • <b>Vigilancia Comunitaria:</b> Fortalecer frentes de seguridad local en sectores comerciales y de esparcimiento nocturno.
            """
        elif "C0" in c_m:
            titulo_alerta = f"🟢 DICTAMEN TÁCTICO: ZONA PACÍFICA / CONTROL PREVENTIVO COMUNITARIO — {m_sel}"
            bg_alerta = "#ECFDF5"
            border_alerta = "#10B981"
            color_tit_alerta = "#065F46"
            puntos_accion = f"""
            • <b>Bajo Nivel de Amenaza:</b> Registro delictivo marginal o nulo con alta tasa de efectividad preventiva ({t_m:.1f}%).<br>
            • <b>Filtro de Tránsito Intermunicipal:</b> Evitar que el municipio sea utilizado como zona de enfriamiento o parqueadero de vehículos hurtados en ciudades capitales.<br>
            • <b>Patrullaje Rural y Verificación de Antecedentes:</b> Consultas periódicas en el sistema SICOQ y RUNT a vehículos foráneos en ferias patronales o temporadas turísticas.
            """
        else:
            titulo_alerta = f"🟠 DICTAMEN TÁCTICO: MONITOREO Y FISCALIZACIÓN DE REGISTROS — {m_sel}"
            bg_alerta = "#FFF7ED"
            border_alerta = "#F97316"
            color_tit_alerta = "#9A3412"
            puntos_accion = f"""
            • <b>Zona con Alta Matrícula Vehicular:</b> Parque automotor considerable respecto a la incidencia delictiva directa.<br>
            • <b>Auditoría y Trazabilidad RUNT:</b> Fiscalizar los procesos de matrícula y traspaso para evitar trámites fraudulentos o gemeleo administrativo.<br>
            • <b>Monitoreo Tecnológico:</b> Instalación de GPS obligatorio en vehículos comerciales y de servicio público.
            """

        st.markdown(f"""
        <div style="background:{bg_alerta}; border:1px solid {border_alerta}; border-left:6px solid {border_alerta}; border-radius:14px; padding:20px; margin-bottom:20px;">
            <div style="font-size:1.05rem; font-weight:800; color:{color_tit_alerta}; margin-bottom:8px;">
                {titulo_alerta}
            </div>
            <div style="font-size:0.88rem; color:#1E293B; line-height:1.7;">
                {puntos_accion}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Historial Cronológico y Exportación ──
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.markdown(f"<h4 style='margin:0; color:#0F172A;'>📋 Historial Cronológico de Registros ({m_sel})</h4>", unsafe_allow_html=True)
        with col_t2:
            csv_data = df_m[[
                "AÑO", "DEPARTAMENTO", "MUNICIPIO", "TIPO_VEHICULO",
                "VEHICULOS_REGISTRADOS", "VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS",
                "CLUSTER_NOMBRE"
            ]].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Exportar Ficha (CSV)",
                data=csv_data,
                file_name=f"ficha_tactica_{m_sel.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        df_mostrar = df_m[[
            "AÑO", "TIPO_VEHICULO", "VEHICULOS_REGISTRADOS",
            "VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS", "CLUSTER_NOMBRE"
        ]].copy().sort_values(by=["AÑO", "TIPO_VEHICULO"], ascending=[False, True])
        
        df_mostrar["TASA_RECUPERACION_%"] = np.where(
            df_mostrar["VEHICULOS_HURTADOS"] > 0,
            (df_mostrar["VEHICULOS_RECUPERADOS"] / df_mostrar["VEHICULOS_HURTADOS"] * 100).round(1),
            np.where(df_mostrar["VEHICULOS_RECUPERADOS"] > 0, 100.0, 0.0)
        )
        
        df_mostrar = df_mostrar.rename(columns={
            "AÑO": "Año",
            "TIPO_VEHICULO": "Tipo de Vehículo",
            "VEHICULOS_REGISTRADOS": "Vehículos Registrados",
            "VEHICULOS_HURTADOS": "Hurtos",
            "VEHICULOS_RECUPERADOS": "Recuperaciones",
            "TASA_RECUPERACION_%": "Efectividad Policial (%)",
            "CLUSTER_NOMBRE": "Segmento Clúster"
        })
        
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN: MÉTODOS NUMÉRICOS (REGRESIÓN & LAGRANGE)
# ─────────────────────────────────────────────────────────────────────────────
elif "📐 Métodos Numéricos" in seccion:
    import streamlit.components.v1 as components
    
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">📐 Sustentación de Métodos Numéricos: Regresión Lineal & Lagrange</h2>
        <p style="color: #64748B; margin:0; font-size: 0.95rem;">
            Implementación comparativa interactiva: Regresión Lineal por Mínimos Cuadrados (MCO) e Interpolación Polinomial de Lagrange sobre la serie histórica 2010–2024 de la Policía Nacional.
        </p>
    </div>
    """, unsafe_allow_html=True)

    ruta_html = Path(__file__).resolve().parent / "templates" / "presentacion_metodos_numericos.html"
    if not ruta_html.exists():
        ruta_html = Path(__file__).resolve().parent / "docs" / "metodos_numericos" / "presentacion_metodos_numericos.html"
        
    if ruta_html.exists():
        with open(ruta_html, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        c_down1, c_down2 = st.columns([1.5, 4])
        with c_down1:
            st.download_button(
                label="📥 Descargar Presentación HTML",
                data=html_content,
                file_name="presentacion_metodos_numericos.html",
                mime="text/html",
                use_container_width=True
            )
        
        components.html(html_content, height=1350, scrolling=True)
    else:
        st.error("No se encontró el archivo de presentación HTML.")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5: CONCLUSIONES & SÍNTESIS TÉCNICA
# ─────────────────────────────────────────────────────────────────────────────
elif "📑 Conclusiones" in seccion:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">Conclusiones de la Investigación & Recomendaciones para Autoridades</h2>
        <p style="color: #64748B; margin:0; font-size: 0.95rem;">
            Síntesis conclusiva del estudio empírico y formulación de políticas públicas de seguridad basadas en datos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Conclusiones Principales del Proyecto
    st.markdown("""
    <div class="section-card" style="border-left: 6px solid #0EA5E9;">
        <h3 style="color: #0F172A; margin: 0 0 10px 0; font-size: 1.25rem;">📌 Conclusiones Fundamentales del Estudio</h3>
        <div style="color: #334155; font-size: 0.92rem; line-height: 1.7;">
            <b>1. Existencia de un Umbral Crítico de Exposición:</b> La escala del parque automotor municipal es el factor determinante primario. Los municipios pequeños (< 100 vehículos) presentan tasas nulas de criminalidad vehicular (96% clasificados como cero hurto), pero al superar la masa crítica metropolitana, la probabilidad de hurto activo supera el 85%.<br><br>
            <b>2. Hiperconcentración Delictiva Severa:</b> A través del clustering se comprobó que el fenómeno delictivo no está disperso homogéneamente por el país: el <b>2.4% de los municipios (FOCO CRÍTICO)</b> absorbe más de 200 hurtos anuales por localidad, mientras que el 88.9% del territorio nacional promedia menos de 4 hurtos al año.<br><br>
            <b>3. La Paradoja de Saturación Policial:</b> Aunque las autoridades recuperan mayor cantidad neta de vehículos en las áreas metropolitanas, la tasa de éxito cae del <b>75.6% en zonas periféricas a solo 26.5% en grandes urbes</b>, demostrando que el volumen delictivo desborda la capacidad operativa convencional.<br><br>
            <b>4. Mayor Vulnerabilidad en Motocicletas:</b> Las motocicletas sufren el mayor impacto del hurto y la menor tasa de recuperación debido a la facilidad de adulteración de placas, rapidez de desensamble en desguazaderos y la alta demanda en mercados negros de autopartes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Veredictos de Modelos (Lado a Lado)
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown("""
        <div class="section-card">
            <h4 style="color: #0F172A; margin-top:0;">🌲 Veredicto Clasificación (Supervisado)</h4>
            <p style="color: #334155; font-size: 0.9rem; line-height: 1.6;">
                <b>Ganador: Árbol de Decisión (profundidad 4)</b>
            </p>
            <ul style="color: #475569; font-size: 0.85rem; line-height: 1.6;">
                <li><b>Recall de 89.72%:</b> Garantiza la mínima tasa de desatención a municipios con actividad criminal activa.</li>
                <li><b>Inferencia inmediata (0.0009s):</b> 46 veces más veloz que KNN, ideal para salas de mando en tiempo real.</li>
                <li><b>Interpretabilidad total:</b> Genera reglas lógicas transparentes, auditables ante la justicia y mandos de policía.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_b:
        st.markdown("""
        <div class="section-card">
            <h4 style="color: #0F172A; margin-top:0;">🎯 Veredicto Clustering (No Supervisado)</h4>
            <p style="color: #334155; font-size: 0.9rem; line-height: 1.6;">
                <b>Ganador: K-Means (k=4)</b>
            </p>
            <ul style="color: #475569; font-size: 0.85rem; line-height: 1.6;">
                <li><b>Silhouette de 0.7748:</b> Separación matemática compacta y nítida.</li>
                <li><b>Aislamiento del FOCO CRÍTICO:</b> Identifica con precisión quirúrgica el 2.4% de municipios prioritarios para inversión estatal.</li>
                <li><b>Validación cruzada independiente:</b> El dendrograma del Clustering Jerárquico (Ward) confirmó la robustez de los 4 grupos sin sesgo previo.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 3. Recomendaciones a las Autoridades
    st.markdown("<h3 style='color: #065F46; margin: 24px 0 14px 0; font-size: 1.3rem;'>🛡️ Recomendaciones Estratégicas para las Autoridades</h3>", unsafe_allow_html=True)
    
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        st.markdown("""<div class="section-card" style="border-top: 4px solid #10B981; height: 100%;">
<b style="color: #0F172A; font-size: 1rem;">👮‍♂️ 1. Policía Nacional (DETOL & METIB)</b>
<div style="color: #475569; font-size: 0.86rem; margin-top: 10px; line-height: 1.6;">
• <b>Patrullaje Focalizado por Cuadrantes:</b> Redirigir el pie de fuerza hacia los puntos calientes metropolitanos identificados por el Árbol en Ibagué, Espinal y Melgar.<br><br>
• <b>Plan Candado Exprés (15 Minutos):</b> Protocolo de cierre inmediato en peajes y corredores de salida (hacia Girardot, Bogotá y Eje Cafetero) antes de que el vehículo ingrese a desguazaderos clandestinos.
</div>
</div>""", unsafe_allow_html=True)

    with r_col2:
        st.markdown("""<div class="section-card" style="border-top: 4px solid #0EA5E9; height: 100%;">
<b style="color: #0F172A; font-size: 1rem;">🏛️ 2. Alcaldías & Gobernación del Tolima</b>
<div style="color: #475569; font-size: 0.86rem; margin-top: 10px; line-height: 1.6;">
• <b>Arcos de Fotodetección y Placas (LPR):</b> Implementar cámaras inteligentes de lectura de placas en las entradas y salidas de las áreas metropolitanas conectadas al RUNT en tiempo real.<br><br>
• <b>Fiscalización de Talleres y Desguazaderos:</b> Inspección administrativa periódica a negocios de autopartes usadas para cortar la cadena económica de receptación que financia el hurto de motocicletas.
</div>
</div>""", unsafe_allow_html=True)

    with r_col3:
        st.markdown("""<div class="section-card" style="border-top: 4px solid #6366F1; height: 100%;">
<b style="color: #0F172A; font-size: 1rem;">⚖️ 3. MinTransporte & Fiscalía General</b>
<div style="color: #475569; font-size: 0.86rem; margin-top: 10px; line-height: 1.6;">
• <b>Marcación Gratuita de Motopartes:</b> Campañas masivas de grabado químico o láser del número de placa en partes vitales de motocicletas para dificultar su comercialización ilegal.<br><br>
• <b>Sistema Predictivo de Alerta Temprana:</b> Integrar modelos de Machine Learning (como el desarrollado en este estudio) dentro de los tableros analíticos del SIEDCO para anticipar picos delictivos.
</div>
</div>""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 30px 0 16px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; color: #94A3B8;">
    <span>Observatorio de Minería de Datos · <b>Natalia Valencia & Camila Pava</b></span>
    <span>Docente: Esteban Ernesto Morales Castro · UNIMINUTO Ibagué · 2026-2</span>
</div>
""", unsafe_allow_html=True)
