"""
Módulo de Gestión de Plantillas HTML y Estilos CSS
Desacopla la capa de presentación visual de la lógica en Python (Streamlit).
"""

from pathlib import Path
import streamlit as st

_actual = Path(__file__).resolve().parent
BASE_DIR = _actual if (_actual / "templates").exists() else _actual.parent
STATIC_DIR = BASE_DIR / "static" / "css"
TEMPLATES_DIR = BASE_DIR / "templates"


def _leer_archivo(ruta: Path) -> str:
    """Lee de forma segura un archivo de texto/plantilla en UTF-8."""
    if ruta.exists():
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def cargar_estilos_css():
    """Inyecta la hoja de estilos CSS externa en la aplicación Streamlit."""
    css_content = _leer_archivo(STATIC_DIR / "styles.css")
    if css_content:
        st.markdown(f"<style>\n{css_content}\n</style>", unsafe_allow_html=True)


def render_hero_banner(titulo: str, subtitulo: str, autoras: str, docente: str, institucion: str):
    """Renderiza el banner principal de lujo desde templates/hero_banner.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "hero_banner.html")
    if plantilla:
        html = plantilla.format(
            titulo=titulo,
            subtitulo=subtitulo,
            autoras=autoras,
            docente=docente,
            institucion=institucion
        )
        st.markdown(html, unsafe_allow_html=True)


def render_context_box():
    """Renderiza la caja de contexto académico desde templates/context_box.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "context_box.html")
    if plantilla:
        st.markdown(plantilla, unsafe_allow_html=True)


def render_kpi_card(label: str, numero: str, subtexto: str, color_borde: str, color_numero: str = "#0F172A", color_sub: str = "#64748B"):
    """Renderiza una tarjeta KPI desde templates/kpi_card.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "kpi_card.html")
    if plantilla:
        html = plantilla.format(
            label=label,
            numero=numero,
            subtexto=subtexto,
            color_borde=color_borde,
            color_numero=color_numero,
            color_sub=color_sub
        )
        st.markdown(html, unsafe_allow_html=True)


def render_model_card(pill_class: str, pill_text: str, title: str, subtitle: str, acc: str, recall: str, f1: str, note: str, border_color: str = "#E2E8F0", bg_color: str = "#FFFFFF", title_color: str = "#0F172A", recall_color: str = "#0F172A", note_color: str = "#64748B"):
    """Renderiza la tarjeta de evaluación de modelo desde templates/model_card.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "model_card.html")
    if plantilla:
        html = plantilla.format(
            pill_class=pill_class,
            pill_text=pill_text,
            title=title,
            subtitle=subtitle,
            acc=acc,
            recall=recall,
            f1=f1,
            note=note,
            border_color=border_color,
            bg_color=bg_color,
            title_color=title_color,
            recall_color=recall_color,
            note_color=note_color
        )
        st.markdown(html, unsafe_allow_html=True)


def render_cluster_card(nombre_cluster: str, volumen: str, hurtos_prom: str, recup_prom: str, estrategia: str, color_borde: str = "#0EA5E9"):
    """Renderiza una tarjeta descriptiva de cluster desde templates/cluster_card.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "cluster_card.html")
    if plantilla:
        html = plantilla.format(
            nombre_cluster=nombre_cluster,
            volumen=volumen,
            hurtos_prom=hurtos_prom,
            recup_prom=recup_prom,
            estrategia=estrategia,
            color_borde=color_borde
        )
        st.markdown(html, unsafe_allow_html=True)


def render_cluster_kpi(tag: str, nombre: str, porcentaje: str, registros: str, hurto_prom: str, recup_prom: str, color_borde: str, bg_color: str = "#FFFFFF", title_color: str = "#0F172A", sub_color: str = "#64748B"):
    """Renderiza la tarjeta KPI de cluster desde templates/cluster_kpi.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "cluster_kpi.html")
    if plantilla:
        html = plantilla.format(
            tag=tag,
            nombre=nombre,
            porcentaje=porcentaje,
            registros=registros,
            hurto_prom=hurto_prom,
            recup_prom=recup_prom,
            color_borde=color_borde,
            bg_color=bg_color,
            title_color=title_color,
            sub_color=sub_color
        )
        st.markdown(html, unsafe_allow_html=True)


def render_alert_card(titulo: str, probabilidad: str, dictamen: str, recomendacion: str, es_alerta: bool):
    """Renderiza la alerta interactiva del simulador desde templates/alert_card.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "alert_card.html")
    if plantilla:
        if es_alerta:
            bg_color = "#FFF1F2"
            border_color = "#F43F5E"
            title_color = "#9F1239"
            text_color = "#881337"
        else:
            bg_color = "#ECFDF5"
            border_color = "#10B981"
            title_color = "#065F46"
            text_color = "#064E3B"

        html = plantilla.format(
            titulo=titulo,
            probabilidad=probabilidad,
            dictamen=dictamen,
            recomendacion=recomendacion,
            bg_color=bg_color,
            border_color=border_color,
            title_color=title_color,
            text_color=text_color
        )
        st.markdown(html, unsafe_allow_html=True)


def render_sidebar_authors():
    """Renderiza el bloque de autoras en el panel lateral desde templates/sidebar_authors.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "sidebar_authors.html")
    if plantilla:
        st.markdown(plantilla, unsafe_allow_html=True)


def render_tactical_comparison(m_sel: str, c_motos: str, h_motos: str, pct_motos: str, r_motos: str, t_motos: str, color_t_motos: str, c_autos: str, h_autos: str, pct_autos: str, r_autos: str, t_autos: str, color_t_autos: str):
    """Renderiza la caja comparativa Motos vs Carros desde templates/tactical_comparison.html."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "tactical_comparison.html")
    if plantilla:
        html = plantilla.format(
            m_sel=m_sel,
            c_motos=c_motos,
            h_motos=h_motos,
            pct_motos=pct_motos,
            r_motos=r_motos,
            t_motos=t_motos,
            color_t_motos=color_t_motos,
            c_autos=c_autos,
            h_autos=h_autos,
            pct_autos=pct_autos,
            r_autos=r_autos,
            t_autos=t_autos,
            color_t_autos=color_t_autos
        )
        st.markdown(html, unsafe_allow_html=True)


def render_tactical_alert(bg_alerta: str, border_alerta: str, color_tit_alerta: str, titulo_alerta: str, puntos_html: str):
    """Renderiza el dictamen táctico policial desde templates/tactical_alert.html sin sangría Markdown."""
    plantilla = _leer_archivo(TEMPLATES_DIR / "tactical_alert.html")
    if plantilla:
        html = plantilla.format(
            bg_alerta=bg_alerta,
            border_alerta=border_alerta,
            color_tit_alerta=color_tit_alerta,
            titulo_alerta=titulo_alerta,
            puntos_html=puntos_html
        )
        st.markdown(html, unsafe_allow_html=True)
