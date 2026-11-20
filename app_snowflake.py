"""
app_snowflake.py — Versión optimizada para Streamlit in Snowflake (SiS)
Proyecto: Observatorio de Hurto Vehicular en Colombia (Tolima)
Autoras: Natalia Valencia & Camila Pava
Docente: Esteban Ernesto Morales Castro · UNIMINUTO Ibagué · 2026-2
"""

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

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatorio de Seguridad Vehicular · Colombia & Tolima",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS estéticos para Snowflake
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .hero-banner {
        background: linear-gradient(135deg, #0A192F 0%, #172A45 50%, #1E3A5F 100%);
        border-radius: 18px;
        padding: 28px 32px;
        color: #F8FAFC;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -10px rgba(10, 25, 47, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        margin-top: 6px;
        margin-bottom: 14px;
        font-weight: 500;
    }
    .meta-chip {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.08);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        color: #CBD5E1;
        border: 1px solid rgba(255, 255, 255, 0.12);
        margin-right: 8px;
        margin-bottom: 4px;
    }
    .meta-chip b { color: #38BDF8; margin-left: 4px; }

    .context-box {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 22px 26px;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #0EA5E9;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        margin-bottom: 22px;
    }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        height: 100%;
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-number {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #0F172A;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 6px;
    }
    .section-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 22px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 20px -2px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CARGA Y CACHÉ DE DATOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    candidatos = [
        "dataset_integrado.csv",
        "dataset/dataset_integrado.csv",
        "https://raw.githubusercontent.com/pavaarcecamila-lab/read-hurtos-Tolima/main/dataset/dataset_integrado.csv"
    ]
    df = None
    for c in candidatos:
        try:
            df = pd.read_csv(c)
            break
        except Exception:
            continue
    if df is None:
        st.error("No se pudo cargar el archivo 'dataset_integrado.csv'. Por favor sube el archivo a los Files de Snowflake.")
        st.stop()
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
    
    # 1. Clustering K-Means k=4
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

    # 2. Clasificación Supervisada
    df["TARGET_HURTO"] = (df["VEHICULOS_HURTADOS"] > 0).astype(int)
    features_clf = ["AÑO", "CODIGO_DANE_MUNICIPIO", "VEHICULOS_REGISTRADOS", "VEHICULOS_RECUPERADOS"]
    X_clf = df[features_clf].values
    y_clf = df["TARGET_HURTO"].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_clf, y_clf, test_size=0.25, random_state=42, stratify=y_clf
    )
    
    tree_clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    tree_clf.fit(X_train, y_train)
    
    gnb_clf = GaussianNB()
    gnb_clf.fit(X_train, y_train)
    
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
    st.markdown("### 🛡️ Observatorio IA · Snowflake")
    st.caption("Minería de Datos · Corte 3")
    
    seccion = st.radio(
        "MÓDULOS DE ANÁLISIS",
        [
            "📊 Diagnóstico & Contexto Estratégico",
            "🌲 Clasificación Supervisada (Árbol, KNN, Bayes)",
            "🎯 Segmentación Territorial (K-Means & Jerárquico)",
            "🔍 Ficha Táctica Municipal",
            "📑 Conclusiones & Recomendaciones"
        ]
    )
    
    st.divider()
    deps_disponibles = sorted(df_raw["DEPARTAMENTO"].dropna().unique().tolist())
    def_dep = ["TOLIMA"] if "TOLIMA" in deps_disponibles else [deps_disponibles[0]]
    dep_sel = st.multiselect("Departamento:", options=["TODOS"] + deps_disponibles, default=def_dep)
    
    anio_max = int(df_raw["AÑO"].max())
    rango_anios = st.slider("Rango de Años:", min_value=2010, max_value=anio_max, value=(2010, anio_max))
    
    tipos_veh = ["TODOS"] + sorted(df_raw["TIPO_VEHICULO"].dropna().unique().tolist())
    tipo_sel = st.selectbox("Tipo de Vehículo:", tipos_veh, index=0)
    
    st.divider()
    st.markdown("""
    **Autoras:**<br>
    • Natalia Valencia<br>
    • Camila Pava<br><br>
    **Docente:**<br>
    Esteban Ernesto Morales Castro<br><br>
    **Institución:**<br>
    UNIMINUTO Ibagué · 2026-2
    """, unsafe_allow_html=True)

df_filtrado = df_raw.copy()
if "TODOS" not in dep_sel and len(dep_sel) > 0:
    df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO"].isin(dep_sel)]
df_filtrado = df_filtrado[(df_filtrado["AÑO"] >= rango_anios[0]) & (df_filtrado["AÑO"] <= rango_anios[1])]
if tipo_sel != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["TIPO_VEHICULO"] == tipo_sel]

# ─────────────────────────────────────────────────────────────────────────────
# BANNER PRINCIPAL (HERO)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">Observatorio de Inteligencia y Minería de Datos</h1>
    <div class="hero-subtitle">
        Análisis Predictivo del Hurto Vehicular y Capacidad de Recuperación Policial en Colombia
    </div>
    <div>
        <span class="meta-chip">👥 Autoras: <b>Natalia Valencia & Camila Pava</b></span>
        <span class="meta-chip">👨‍🏫 Docente: <b>Esteban Ernesto Morales Castro</b></span>
        <span class="meta-chip">🏛️ <b>UNIMINUTO Ibagué · 2026-2</b></span>
        <span class="meta-chip">❄️ <b>Snowflake Deployment</b></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1: DIAGNÓSTICO & CONTEXTO ESTRATÉGICO
# ─────────────────────────────────────────────────────────────────────────────
if seccion == "📊 Diagnóstico & Contexto Estratégico":
    st.markdown("""
    <div class="context-box">
        <h4 style="color:#0F172A; margin:0 0 8px 0;">🎯 Contexto Estratégico y Propósito del Proyecto</h4>
        <p style="color:#475569; font-size:0.92rem; line-height:1.6; margin:0 0 10px 0;">
            El hurto de automotores y motocicletas representa uno de los fenómenos delictivos con mayor impacto económico y de percepción de seguridad ciudadana en Colombia. Esta investigación aplica <b>técnicas avanzadas de Minería de Datos</b> sobre un registro histórico integrado de <b>54,428 observaciones municipales</b>, analizando la correlación entre el crecimiento del parque automotor, los incidentes de hurto y la efectividad operativa de recuperación por parte de la Policía Nacional, con especial énfasis en el <b>departamento del Tolima</b>.
        </p>
        <p style="color:#0F172A; font-size:0.92rem; margin:0; line-height:1.6;">
            <b>📌 Pregunta de Investigación Central:</b><br>
            <i>¿De qué manera la tipología vehicular y la escala del parque automotor registrado en los municipios colombianos condicionan la incidencia del hurto, y cuál es la efectividad real de la capacidad policial de recuperación frente a la hiperconcentración del delito en áreas metropolitanas?</i>
        </p>
    </div>
    """, unsafe_allow_html=True)

    total_h = int(df_filtrado["VEHICULOS_HURTADOS"].sum())
    total_r = int(df_filtrado["VEHICULOS_RECUPERADOS"].sum())
    tasa_g = (total_r / total_h * 100) if total_h > 0 else 0.0
    mun_c = df_filtrado.groupby("MUNICIPIO")["VEHICULOS_HURTADOS"].sum().idxmax() if len(df_filtrado) > 0 else "N/A"
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #F43F5E;">
            <div class="kpi-label">Vehículos Hurtados</div>
            <div class="kpi-number" style="color: #E11D48;">{total_h:,}</div>
            <div class="kpi-sub" style="color: #E11D48;">Casos en filtro seleccionado</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #10B981;">
            <div class="kpi-label">Vehículos Recuperados</div>
            <div class="kpi-number" style="color: #059669;">{total_r:,}</div>
            <div class="kpi-sub" style="color: #059669;">Efectividad policial registrada</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #0EA5E9;">
            <div class="kpi-label">Tasa de Recuperación</div>
            <div class="kpi-number" style="color: #0284C7;">{tasa_g:.1f}%</div>
            <div class="kpi-sub" style="color: #64748B;">Recuperados vs Hurtados</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #F59E0B;">
            <div class="kpi-label">Municipio Más Afectado</div>
            <div class="kpi-number" style="font-size: 1.45rem; color: #D97706;">{mun_c}</div>
            <div class="kpi-sub" style="color: #D97706;">Mayor concentración criminal</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
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
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
            height=320
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
        labels={"VEHICULOS_HURTADOS": "Hurtos Totales", "TASA_REC": "Tasa Recuperación (%)"},
        text="VEHICULOS_HURTADOS"
    )
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2: CLASIFICACIÓN SUPERVISADA (ÁRBOL, KNN, BAYES)
# ─────────────────────────────────────────────────────────────────────────────
elif seccion == "🌲 Clasificación Supervisada (Árbol, KNN, Bayes)":
    st.markdown("""
    <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">Torneo de Clasificación Supervisada</h2>
    <p style="color: #64748B; margin:0 0 20px 0; font-size: 0.95rem;">
        Predicción algorítmica: <b>Hurto Activo (y=1)</b> vs <b>Cero Hurtos (y=0)</b>.
    </p>
    """, unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    t_m = models_data["metricas"]["tree"]
    k_m = models_data["metricas"]["knn"]
    g_m = models_data["metricas"]["gnb"]
    
    with m_col1:
        st.markdown(f"""
        <div class="kpi-card" style="border: 2px solid #10B981; background: #FAFDFB;">
            <span style="background:#ECFDF5; color:#047857; padding:4px 12px; border-radius:14px; font-size:0.78rem; font-weight:700;">🏆 GANADOR OFICIAL</span>
            <h3 style="margin: 12px 0 6px 0; color: #065F46; font-size: 1.3rem;">Árbol de Decisión</h3>
            <p style="margin:0; font-size: 0.85rem; color: #475569;">Profundidad óptima = 4</p>
            <hr style="margin: 12px 0; border: none; border-top: 1px solid #D1FAE5;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color:#64748B; font-size:0.85rem;">Accuracy Test:</span>
                <b style="color:#0F172A;">{t_m['acc']*100:.2f}%</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color:#64748B; font-size:0.85rem;">Recall:</span>
                <b style="color:#059669;">{t_m['recall']*100:.2f}%</b>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color:#64748B; font-size:0.85rem;">F1-Score:</span>
                <b style="color:#0F172A;">{t_m['f1']:.3f}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown(f"""
        <div class="kpi-card" style="border: 1px solid #BFDBFE;">
            <span style="background:#EFF6FF; color:#1D4ED8; padding:4px 12px; border-radius:14px; font-size:0.78rem; font-weight:700;">SUBCAMPEÓN</span>
            <h3 style="margin: 12px 0 6px 0; color: #1E40AF; font-size: 1.3rem;">KNN (k = 31)</h3>
            <p style="margin:0; font-size: 0.85rem; color: #475569;">Normalización StandardScaler</p>
            <hr style="margin: 12px 0; border: none; border-top: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color:#64748B; font-size:0.85rem;">Accuracy Test:</span>
                <b style="color:#0F172A;">{k_m['acc']*100:.2f}%</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color:#64748B; font-size:0.85rem;">Recall:</span>
                <b style="color:#1E40AF;">{k_m['recall']*100:.2f}%</b>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color:#64748B; font-size:0.85rem;">F1-Score:</span>
                <b style="color:#0F172A;">{k_m['f1']:.3f}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m_col3:
        st.markdown(f"""
        <div class="kpi-card" style="border: 1px solid #FECDD3;">
            <span style="background:#FFF1F2; color:#BE123C; padding:4px 12px; border-radius:14px; font-size:0.78rem; font-weight:700;">DESCARTADO</span>
            <h3 style="margin: 12px 0 6px 0; color: #9F1239; font-size: 1.3rem;">Gaussian Naive Bayes</h3>
            <p style="margin:0; font-size: 0.85rem; color: #475569;">Supuesto de independencia</p>
            <hr style="margin: 12px 0; border: none; border-top: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color:#64748B; font-size:0.85rem;">Accuracy Test:</span>
                <b style="color:#0F172A;">{g_m['acc']*100:.2f}%</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color:#64748B; font-size:0.85rem;">Recall:</span>
                <b style="color:#BE123C;">{g_m['recall']*100:.2f}%</b>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color:#64748B; font-size:0.85rem;">F1-Score:</span>
                <b style="color:#0F172A;">{g_m['f1']:.3f}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0 0 8px 0; color:#0F172A;'>🎮 Simulador Predictivo en Tiempo Real</h4>", unsafe_allow_html=True)
    st.caption("Ajusta las variables para consultar la inferencia en milisegundos con el modelo ganador:")
    
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
            st.error(f"🚨 ALERTA: MUNICIPIO EN CONDICIÓN DE HURTO ACTIVO (Probabilidad: {prob*100:.1f}%)")
        else:
            st.success(f"✅ ZONA SEGURA: BAJO RIESGO DE HURTO VEHICULAR (Probabilidad: {prob*100:.1f}%)")
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3: SEGMENTACIÓN TERRITORIAL (CLUSTERING)
# ─────────────────────────────────────────────────────────────────────────────
elif seccion == "🎯 Segmentación Territorial (K-Means & Jerárquico)":
    st.markdown("""
    <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">Segmentación Territorial No Supervisada</h2>
    <p style="color: #64748B; margin:0 0 20px 0; font-size: 0.95rem;">
        Agrupamiento natural de municipios: K-Means (k=4) con Silhouette de 0.7748.
    </p>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class="kpi-card" style="border-left: 5px solid #10B981;">
        <div style="font-size:0.8rem; font-weight:700; color:#10B981;">🟢 CLUSTER 0</div>
        <h4 style="margin:4px 0;">Zonas Pacíficas (88.9%)</h4>
        <p style="font-size:0.8rem; color:#64748B; margin:0;">Hurtos: 3.8/año · Recup: 75.6%</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-card" style="border-left: 5px solid #F59E0B;">
        <div style="font-size:0.8rem; font-weight:700; color:#F59E0B;">🟡 CLUSTER 1</div>
        <h4 style="margin:4px 0;">Riesgo Moderado (5.4%)</h4>
        <p style="font-size:0.8rem; color:#64748B; margin:0;">Hurtos: 37.2/año · Recup: 83.5%</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kpi-card" style="border-left: 5px solid #F43F5E; background:#FFFBFB;">
        <div style="font-size:0.8rem; font-weight:700; color:#F43F5E;">🔴 CLUSTER 2</div>
        <h4 style="margin:4px 0; color:#9F1239;">FOCO CRÍTICO (2.4%)</h4>
        <p style="font-size:0.8rem; color:#F43F5E; margin:0; font-weight:600;">Hurtos: 201.8/año · Recup: 26.5%</p>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="kpi-card" style="border-left: 5px solid #0EA5E9;">
        <div style="font-size:0.8rem; font-weight:700; color:#0EA5E9;">🟠 CLUSTER 3</div>
        <h4 style="margin:4px 0;">Parque Grande (3.3%)</h4>
        <p style="font-size:0.8rem; color:#64748B; margin:0;">Hurtos: 38.0/año · Recup: 43.0%</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
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
        labels={"VEHICULOS_HURTADOS": "Hurtos", "VEHICULOS_RECUPERADOS": "Recuperaciones"}
    )
    fig_scat.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=10, b=10), height=380)
    st.plotly_chart(fig_scat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4: FICHA TÁCTICA MUNICIPAL
# ─────────────────────────────────────────────────────────────────────────────
elif seccion == "🔍 Ficha Táctica Municipal":
    st.markdown("""
    <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">Ficha Táctica por Municipio</h2>
    <p style="color: #64748B; margin:0 0 20px 0; font-size: 0.95rem;">
        Consulta individualizada para planeación policial territorial.
    </p>
    """, unsafe_allow_html=True)
    
    municipios = sorted(df_clustered["MUNICIPIO"].dropna().unique().tolist())
    def_idx = municipios.index("IBAGUE") if "IBAGUE" in municipios else 0
    m_sel = st.selectbox("Seleccione Municipio para Exploración:", municipios, index=def_idx)
    
    df_m = df_clustered[df_clustered["MUNICIPIO"] == m_sel]
    if len(df_m) > 0:
        h_m = int(df_m["VEHICULOS_HURTADOS"].sum())
        r_m = int(df_m["VEHICULOS_RECUPERADOS"].sum())
        t_m = (r_m / h_m * 100) if h_m > 0 else 0.0
        c_m = df_m["CLUSTER_NOMBRE"].mode()[0]
        
        fc1, fc2, fc3, fc4 = st.columns(4)
        fc1.metric("Hurtos Totales", f"{h_m:,}")
        fc2.metric("Recuperaciones", f"{r_m:,}")
        fc3.metric("Efectividad Policial", f"{t_m:.1f}%")
        fc4.metric("Cluster Asignado", c_m)
            
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.dataframe(
            df_m[["AÑO", "TIPO_VEHICULO", "VEHICULOS_REGISTRADOS", "VEHICULOS_HURTADOS", "VEHICULOS_RECUPERADOS", "CLUSTER_NOMBRE"]]
            .sort_values(by="AÑO", ascending=False),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5: CONCLUSIONES & RECOMENDACIONES
# ─────────────────────────────────────────────────────────────────────────────
elif seccion == "📑 Conclusiones & Recomendaciones":
    st.markdown("""
    <h2 style="color: #0F172A; margin:0 0 6px 0; font-size: 1.6rem;">Conclusiones & Recomendaciones para Autoridades</h2>
    <p style="color: #64748B; margin:0 0 20px 0; font-size: 0.95rem;">
        Síntesis conclusiva del estudio empírico y formulación de políticas públicas de seguridad.
    </p>
    """, unsafe_allow_html=True)
    
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
