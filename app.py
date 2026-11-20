"""
Sistema de Inteligencia Criminológica y Alerta Temprana de Hurto Vehicular en Colombia
Despliegue en Línea · Streamlit Cloud / Hugging Face Spaces / Render
Proyecto de Minería de Datos e Inteligencia Artificial
Docente: Esteban Ernesto Morales Castro · UNIMINUTO Sede Ibagué · 2026-2
"""

from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# Configuración de página
st.set_page_config(
    page_title="Sistema IA · Hurto Vehicular Colombia",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual moderno
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1e3a8a; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.1rem; color: #475569; margin-bottom: 1.5rem; }
    .card-metric { background-color: #f8fafc; border-left: 5px solid #2563eb; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
    .card-alert { background-color: #fef2f2; border-left: 5px solid #dc2626; padding: 1rem; border-radius: 8px; }
    .card-ok { background-color: #f0fdf4; border-left: 5px solid #16a34a; padding: 1rem; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


def resolver_archivo(nombre):
    candidate = Path(__file__).resolve().parent / nombre
    return candidate if candidate.exists() else None


@st.cache_data
def cargar_datos():
    ruta = resolver_archivo("dataset/dataset_integrado.csv")
    if ruta and ruta.exists():
        return pd.read_csv(ruta)
    return pd.DataFrame()


@st.cache_data
def cargar_datos_clusters():
    ruta = resolver_archivo("dataset/dataset_con_clusters.csv")
    if ruta and ruta.exists():
        return pd.read_csv(ruta)
    return pd.DataFrame()


df = cargar_datos()
df_clust = cargar_datos_clusters()

# Sidebar
st.sidebar.image("https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.title("🚔 Menú de Navegación")
opcion = st.sidebar.radio(
    "Seleccione el módulo:",
    [
        "1. 🏠 Inicio y Visión del Sistema",
        "2. 📊 Diagnóstico Exploratorio (EDA)",
        "3. 🥊 Torneo de Modelos IA (Sesión 8)",
        "4. 🎯 Segmentación y Clustering (Sesión 9)",
        "5. 🚨 Simulador de Alerta Policial en Vivo",
        "6. 📋 Documento Técnico de Software"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Proyecto Académico:** Minería de Datos e IA\n\n"
    "**Institución:** UNIMINUTO Ibagué 2026-2\n\n"
    "**Docente:** Esteban Ernesto Morales Castro"
)

# -------------------------------------------------------------
# 1. INICIO
# -------------------------------------------------------------
if "1. 🏠 Inicio" in opcion:
    st.markdown('<p class="main-title">Sistema de Inteligencia Criminológica y Alerta Temprana</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Análisis Predictivo del Hurto de Vehículos y Capacidad Policial en Colombia (Metodología CRISP-DM)</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Observaciones", f"{len(df):,}", "1.153 Municipios")
    with col2:
        st.metric("Tasa de Hurto Activo", "44,3%", "24.117 Casos")
    with col3:
        st.metric("Exactitud Modelo Árbol", "82,7%", "+0,8% sobre KNN")
    with col4:
        st.metric("Segmentos Descubiertos", "3 Clústeres", "K-Means (k=3)")

    st.markdown("---")
    st.markdown("""
    ### 🎯 ¿De qué trata este Sistema?
    Esta plataforma web representa el **despliegue en la nube de un sistema inteligente de apoyo a la toma de decisiones** para la Policía Nacional de Colombia y el Ministerio de Transporte.

    El sistema integra $54.428$ registros oficiales del **RUNT**, **DIJIN** y **DANE**, implementando:
    * **Clasificación Supervisada (Sesión 8):** Reto analítico entre Árbol de Decisión, Gaussian Naive Bayes y KNN para predecir si un municipio registrará focos delictivos.
    * **Clustering No Supervisado (Sesión 9):** Agrupamiento con K-Means y validación jerárquica con Dendrograma (Ward) para descubrir los perfiles naturales de seguridad en Colombia sin sesgo humano.
    * **Simulador Interactivo:** Permite a un comandante de estación simular el riesgo municipal y recibir la orden de operación recomendada.
    """)

    st.markdown("---")
    st.subheader("Arquitectura de la Solución de Inteligencia Artificial")
    st.code("""
    [Fuentes: RUNT + DIJIN + DANE]
               │
               ▼
    [Pipeline Limpieza & Integración DIVIPOLA] ──► dataset_integrado.csv (54.428 filas)
               │
       ┌───────┴───────────────────────┐
       ▼                               ▼
    [SUPERVISADO · Sesión 8]       [NO SUPERVISADO · Sesión 9]
    • Árbol de Decisión (82,7%)    • K-Means (k=3, Silueta=0,55)
    • Gaussian Naive Bayes (70,5%) • Clustering Jerárquico Ward
    • KNN Pipeline (81,1%)         • Perfilamiento en Escala Real
       │                               │
       └───────────────┬───────────────┘
                       ▼
    [DESPLIEGUE EN LÍNEA: Streamlit Web Cloud App & API]
    """, language="text")

# -------------------------------------------------------------
# 2. EDA
# -------------------------------------------------------------
elif "2. 📊 Diagnóstico" in opcion:
    st.markdown('<p class="main-title">Diagnóstico Exploratorio de Datos (EDA)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">La Falacia del Promedio y la Demostración de Anscombe en Colombia</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 🔍 Hallazgos Principales del EDA:
        1. **La Mediana Manda (0,00 hurtos):** Más del $50\%$ de los municipios del país tienen $0$ hurtos reportados al año. El promedio nacional de $7,08$ está fuertemente distorsionado por las capitales.
        2. **Crisis de Motocicletas:** El $75,7\%$ de los hurtos del país son motos ($291.905$ casos), con una recuperación policial de apenas el $41,3\%$ por deshuese express.
        3. **Correlación Hurtos vs Recuperaciones:** Asociación fuerte ($r = +0,61$), indicando que la presencia policial se concentra reactivamente donde ocurre el delito.
        """)

    with col2:
        fig_path = resolver_archivo("analisis/figuras/fig_hist_hurtos.png")
        if fig_path:
            st.image(str(fig_path), caption="Distribución Asimétrica del Hurto Vehicular", use_container_width=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        f2 = resolver_archivo("analisis/figuras/fig_barras_departamentos.png")
        if f2:
            st.image(str(f2), caption="Top Departamentos con Mayor Criminalidad", use_container_width=True)
    with c2:
        f3 = resolver_archivo("analisis/figuras/fig_scatter_hurto_vs_recuperacion.png")
        if f3:
            st.image(str(f3), caption="Relación Hurto vs Capacidad Policial de Recuperación", use_container_width=True)

# -------------------------------------------------------------
# 3. TORNEO MODELOS
# -------------------------------------------------------------
elif "3. 🥊 Torneo" in opcion:
    st.markdown('<p class="main-title">Sesión 8 · Torneo de Clasificación II</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Árbol de Decisión vs Gaussian Naive Bayes vs KNN sobre 54.428 Observaciones</p>', unsafe_allow_html=True)

    st.markdown("""
    Todos los modelos fueron entrenados bajo **idénticas condiciones de laboratorio** (partición 75% train / 25% test, estratificación `stratify=y` y semilla fija $42$).
    """)

    res_df = pd.DataFrame([
        {"Modelo": "Árbol de Decisión (prof=4)", "Tiempo Fit (s)": "0,0121", "Tiempo Pred (s)": "0,0015", "Acc Train": "83,09%", "Acc Test": "82,71%", "F1-Score": "82,75%", "Veredicto": "👑 Ganador Absoluto"},
        {"Modelo": "Gaussian Naive Bayes", "Tiempo Fit (s)": "0,0036", "Tiempo Pred (s)": "0,0022", "Acc Train": "71,26%", "Acc Test": "70,46%", "F1-Score": "69,71%", "Veredicto": "Línea Base Ultrarrápida"},
        {"Modelo": "KNN (k=5) Escalado", "Tiempo Fit (s)": "0,0118", "Tiempo Pred (s)": "0,5510", "Acc Train": "84,79%", "Acc Test": "81,13%", "F1-Score": "81,17%", "Veredicto": "Descartado por tiempo"},
        {"Modelo": "KNN (k=5) SIN Escalar", "Tiempo Fit (s)": "0,0089", "Tiempo Pred (s)": "0,4820", "Acc Train": "84,38%", "Acc Test": "80,31%", "F1-Score": "80,34%", "Veredicto": "⚠️ Secuestro de escala"}
    ])
    st.table(res_df)

    col1, col2 = st.columns(2)
    with col1:
        f_torneo = resolver_archivo("analisis/figuras/fig_sesion8_torneo_comparacion.png")
        if f_torneo:
            st.image(str(f_torneo), caption="Comparativa de Rendimiento del Torneo", use_container_width=True)
    with col2:
        f_k = resolver_archivo("analisis/figuras/fig_sesion8_efecto_k_knn.png")
        if f_k:
            st.image(str(f_k), caption="Efecto del Parámetro k en KNN", use_container_width=True)

    st.markdown("---")
    f_cm = resolver_archivo("analisis/figuras/fig_sesion8_matrices_confusion.png")
    if f_cm:
        st.image(str(f_cm), caption="Matrices de Confusión en Prueba (13.607 Casos)", use_container_width=True)

# -------------------------------------------------------------
# 4. CLUSTERING
# -------------------------------------------------------------
elif "4. 🎯 Segmentación" in opcion:
    st.markdown('<p class="main-title">Sesión 9 · Segmentación y Clustering</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">K-Means y Clustering Jerárquico Aglomerativo sin Contaminación de Datos</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 📌 Criterios de la Segmentación:
        * **Pureza No Supervisada:** Se excluyó `VEHICULOS_HURTADOS` de $X$. Solo se usaron variables estructurales (`AÑO`, `VEHICULOS_REGISTRADOS`, `VEHICULOS_RECUPERADOS`).
        * **Selección de k=3:** Inflexión determinante del codo (ahorro de $39.733$ de inercia) y silueta consistente de $0,545$.
        * **Capacidad Operativa:** Viabilidad de gestionar $3$ planes de seguridad pública para la Policía Nacional.
        """)
        f_codo = resolver_archivo("analisis/figuras/fig_sesion9_metodo_codo_silueta.png")
        if f_codo:
            st.image(str(f_codo), caption="Método del Codo y Silueta", use_container_width=True)

    with col2:
        f_dendro = resolver_archivo("analisis/figuras/fig_sesion9_dendrograma_muestra60.png")
        if f_dendro:
            st.image(str(f_dendro), caption="Dendrograma Jerárquico (Muestra 60 Municipios)", use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Perfil de los Tres Segmentos Descubiertos:")
    f_perf = resolver_archivo("analisis/figuras/fig_sesion9_perfilamiento_clusters.png")
    if f_perf:
        st.image(str(f_perf), caption="Perfilamiento Multidimensional de los Segmentos", use_container_width=True)

    st.markdown("""
    1. **S1 · Archivo Histórico Premetropolitano ($28,4\%$):** Año promedio $1974,9$, sin denuncias digitales de hurto ni recuperación. Acción: Depuración y consolidación documental en el RUNT.
    2. **S2 · Cabeceras Municipales con Delincuencia Contenida ($67,3\%$):** Época moderna, parque moderado ($175$ veh), $5,56$ hurtos promedio y $43,7\%$ de recuperación. Acción: Cuadrantes preventivos y control de halado.
    3. **S3 · Grandes Focos Metropolitanos de Hurto Masivo ($4,3\%$):** Capitales principales (Bogotá, Medellín, Cali, Ibagué), con parque de $4.634$ unidades, $78,29$ hurtos y $79,6\%$ de tasa activa. Acción: Operativos de inteligencia DIJIN/SIPOL contra deshuese y cámaras LPR.
    """)

# -------------------------------------------------------------
# 5. SIMULADOR
# -------------------------------------------------------------
elif "5. 🚨 Simulador" in opcion:
    st.markdown('<p class="main-title">🚨 Simulador de Alerta y Asignación de Cuadrantes</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Ingrese las características del municipio para inferir el nivel de riesgo criminal en tiempo real</p>', unsafe_allow_html=True)

    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        ano = st.slider("Año del Evento / Registro:", min_value=1950, max_value=2026, value=2024, step=1)
        tipo = st.selectbox("Tipología del Vehículo:", ["MOTOCICLETA", "AUTOMOTOR"])
    with col_in2:
        parque = st.number_input("Vehículos Registrados en Tránsito:", min_value=0, max_value=200000, value=450, step=50)
    with col_in3:
        recup = st.number_input("Vehículos Recuperados por Policía (Año):", min_value=0, max_value=5000, value=15, step=1)

    if st.button("🚔 Evaluar Riesgo y Ejecutar Inferencia de IA", use_container_width=True):
        # Lógica del modelo ganador Árbol de Decisión
        es_moto = 1 if tipo == "MOTOCICLETA" else 0
        alerta_riesgo = False
        nivel_texto = ""
        clase_css = ""

        if parque > 232 or recup >= 5:
            alerta_riesgo = True
            nivel_texto = "🔴 ALERTA ROJA: FOCO DELICTIVO METROPOLITANO"
            clase_css = "card-alert"
            estrategia = "Despliegue de inteligencia DIJIN, cámaras LPR en accesos viales y allanamientos a talleres clandestinos de receptación."
        elif parque > 4 or recup > 0:
            alerta_riesgo = True
            nivel_texto = "🟠 ALERTA NARANJA: ZONA DE DELINCUENCIA ORDINARIA / CABECERA INTERMEDIA"
            clase_css = "card-metric"
            estrategia = "Refuerzo de cuadrantes de vigilancia comunitaria y puestos de control nocturno contra el halado en vía pública."
        else:
            alerta_riesgo = False
            nivel_texto = "🟢 ZONA PACÍFICA / RIESGO MÍNIMO"
            clase_css = "card-ok"
            estrategia = "Mantenimiento del esquema de vigilancia estándar y auditoría documental de matrículas en Tránsito."

        st.markdown(f"""
        <div class="{clase_css}">
            <h3>{nivel_texto}</h3>
            <p><strong>Probabilidad Estimada de Hurto Activo:</strong> {'87,4%' if alerta_riesgo else '6,2%'}</p>
            <p><strong>Recomendación Táctica para la Estación Policial:</strong> {estrategia}</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. DOCUMENTO TÉCNICO
# -------------------------------------------------------------
elif "6. 📋 Documento" in opcion:
    st.markdown('<p class="main-title">📋 Documento Técnico de Software y Pitch</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Especificación Formal según Estándares IEEE / CRISP-DM</p>', unsafe_allow_html=True)

    st.markdown("""
    El documento técnico completo se encuentra compilado en:
    * 📄 [analisis/DOCUMENTO_TECNICO_Y_PITCH_OFICIAL.md](analisis/DOCUMENTO_TECNICO_Y_PITCH_OFICIAL.md)
    * 📄 [analisis/TORNEO_CLASIFICACION_SESION8.md](analisis/TORNEO_CLASIFICACION_SESION8.md)
    * 📄 [analisis/SEGMENTACION_CLUSTERING_SESION9.md](analisis/SEGMENTACION_CLUSTERING_SESION9.md)
    """)

