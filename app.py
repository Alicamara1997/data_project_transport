"""
🚇 Tableau de Bord — Trafic Transports en Commun Île-de-France
Application Streamlit complète avec monitoring temps réel et prédictions ML.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import pytz
import time
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# ── Imports internes ──────────────────────────────────────────────────────────
from src.data.lines_reference import (
    METRO_LINES, RER_LINES, TRANSILIEN_LINES, TRAM_LINES, BUS_LINES,
    ALL_LINES, TRANSPORT_TYPES, STATION_COORDS
)
from src.data.data_collector import (
    get_all_lines_status, get_line_status, get_next_passages,
    get_traffic_alerts, get_stops_for_line, get_hourly_traffic_data,
    get_global_stats
)
from src.models.traffic_predictor import predict, predict_day_profile, predict_week_heatmap
from src.utils.helpers import (
    format_wait, get_status_color, get_status_icon,
    get_status_label, congestion_color, congestion_label
)

PARIS_TZ = pytz.timezone("Europe/Paris")

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PAGE
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="IDF Transit — Tableau de Bord Trafic",
    page_icon="🚇",
    layout="centered",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS PERSONNALISÉ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background principal ── */
.stApp {
    background: #0f172a;
    color: #f8fafc;
}

/* ── Cartes métriques ── */
.metric-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
.metric-card:hover {
    border-color: #475569;
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.3);
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Cartes ligne ── */
.line-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.5rem;
    border: 1px solid #334155;
    border-left: 4px solid #6366f1;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
}
.line-badge {
    display: inline-block;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 0.8rem;
    font-weight: 700;
    color: white;
    margin-right: 8px;
}

/* ── Passages ── */
.passage-row {
    background: #1e293b;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
    border: 1px solid #334155;
    box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
}
.wait-time {
    font-size: 1.5rem;
    font-weight: 800;
    min-width: 60px;
    text-align: center;
}

/* ── Alertes ── */
.alert-card {
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    border-left: 4px solid;
    background: #1e293b;
    box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
}
.alert-disrupted  { border-color: #f59e0b; background: rgba(245,158,11,0.05); }
.alert-interrupted{ border-color: #ef4444; background: rgba(239,68,68,0.05); }

/* ── Titre principal ── */
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    text-align: center;
}
.hero-sub {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 4px;
    text-align: center;
}

/* ── Section headers ── */
.section-header {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::before {
    content: ''; display: block; width: 4px; height: 16px;
    background: #818cf8; border-radius: 4px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #1e293b;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #334155;
    box-shadow: 0 2px 4px rgb(0 0 0 / 0.1);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    color: #94a3b8 !important;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: #334155 !important;
    color: #f8fafc !important;
}

/* ── Mode simulation banner ── */
.sim-banner {
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #c4b5fd;
    margin-bottom: 1rem;
    text-align: center;
    font-weight: 500;
}

/* ── Masquer le header app default ── */
header[data-testid="stHeader"] {
    display: none;
}
[data-testid="stSidebarCollapsedControl"] {
    display: none;
}

/* ── Espace pour la bottom navigation ── */
.stApp {
    padding-bottom: 80px;
}

/* ── Barre de Navigation Fixée en Bas (Native st.radio Hack) ── */
div[role="radiogroup"] > label > div:first-child {
    display: none !important; /* Cache le point radio natif */
}
div[role="radiogroup"] {
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    background: #0f172a; /* Dark Slate bottom bar */
    padding: 10px 0 20px 0;
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    z-index: 99999;
    border-top: 1px solid #1e293b;
    box-shadow: 0 -4px 15px rgba(0,0,0,0.2);
    gap: 0 !important;
}
div[role="radiogroup"] > label {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    flex: 1;
    border: none !important;
}
div[role="radiogroup"] > label p {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    font-size: 0.70rem;
    font-weight: 600;
    color: #64748b;
    padding: 6px 12px;
    border-radius: 16px;
    transition: all 0.2s ease;
    margin: 0;
    white-space: pre-wrap;
    text-align: center;
}
div[role="radiogroup"] > label[aria-checked="true"] p {
    background: #22c55e;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS UI
# ══════════════════════════════════════════════════════════════════════════════

def render_metric_card(value, label, color="#6366f1", prefix="", suffix=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{color}">{prefix}{value}{suffix}</div>
        <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)


def render_status_badge(status: str):
    icon = get_status_icon(status)
    label = get_status_label(status)
    color = get_status_color(status)
    return f'<span style="color:{color};font-weight:600">{icon} {label}</span>'


def build_congestion_gauge(value: float, title: str = "Congestion") -> go.Figure:
    color = congestion_color(value)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%", "font": {"size": 28, "color": color, "family": "Inter"}},
        title={"text": title, "font": {"size": 13, "color": "#94a3b8", "family": "Inter"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8",
                     "tickfont": {"color": "#94a3b8", "size": 10}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 30],  "color": "rgba(34,197,94,0.12)"},
                {"range": [30, 60], "color": "rgba(245,158,11,0.12)"},
                {"range": [60, 85], "color": "rgba(249,115,22,0.12)"},
                {"range": [85, 100],"color": "rgba(239,68,68,0.12)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.8, "value": value}
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=10, l=15, r=15), height=180
    )
    return fig


def build_passage_timeline(passages: list, line_color: str) -> go.Figure:
    if not passages:
        return None
    df = pd.DataFrame(passages)
    fig = go.Figure()
    colors = [line_color if d == 0 else "#f59e0b" for d in df["delay_minutes"]]
    fig.add_trace(go.Bar(
        x=df["wait_minutes"],
        y=df["direction"],
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{w} min" for w in df["wait_minutes"]],
        textposition="outside",
        textfont=dict(color="#e2e8f0", size=11),
        hovertemplate="<b>%{y}</b><br>Dans %{x} min<br>Départ : %{customdata}<extra></extra>",
        customdata=df["expected_time"],
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, color="#94a3b8",
                   title=dict(text="Minutes avant passage", font=dict(size=11))),
        yaxis=dict(showgrid=False, color="#cbd5e1"),
        margin=dict(t=10, b=30, l=10, r=60),
        height=max(160, len(passages) * 45),
        showlegend=False, font=dict(family="Inter")
    )
    return fig


def build_day_profile_chart(df: pd.DataFrame, line_color: str) -> go.Figure:
    now_hour = datetime.now(PARIS_TZ).hour
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["hour_label"], y=df["congestion_pct"],
        mode="lines+markers",
        line=dict(color=line_color, width=2.5, shape="spline"),
        marker=dict(size=6, color=line_color, line=dict(color="white", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba({},{},{},0.15)".format(
            int(line_color.lstrip('#')[0:2], 16),
            int(line_color.lstrip('#')[2:4], 16),
            int(line_color.lstrip('#')[4:6], 16),
        ),
        name="Congestion",
        hovertemplate="<b>%{x}</b><br>Congestion : %{y:.0f}%<extra></extra>",
    ))
    # Ligne verticale heure actuelle (axe catégoriel → add_shape)
    hour_labels = list(df["hour_label"])
    if 5 <= now_hour <= 23:
        now_label = f"{now_hour:02d}h"
        if now_label in hour_labels:
            x_idx = hour_labels.index(now_label)
            fig.add_shape(type="line", x0=x_idx, x1=x_idx, y0=0, y1=1,
                          xref="x", yref="paper",
                          line=dict(color="rgba(99,102,241,0.7)", width=2, dash="dash"))
            fig.add_annotation(x=x_idx, y=1, xref="x", yref="paper",
                               text="Maintenant", showarrow=False,
                               font=dict(color="#818cf8", size=11),
                               yanchor="bottom", xanchor="center")
    # Zones de pointe
    fig.add_hrect(y0=85, y1=100, fillcolor="rgba(239,68,68,0.08)", line_width=0)
    fig.add_hrect(y0=60, y1=85, fillcolor="rgba(249,115,22,0.06)", line_width=0)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#94a3b8", tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.1)",
                   color="#94a3b8", range=[0, 105], ticksuffix="%",
                   tickfont=dict(size=10)),
        margin=dict(t=10, b=35, l=10, r=10), height=220,
        showlegend=False, font=dict(family="Inter")
    )
    return fig


def build_heatmap(df: pd.DataFrame) -> go.Figure:
    pivot = df.pivot(index="day", columns="hour_label", values="congestion_pct")
    days_order = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
    pivot = pivot.reindex([d for d in days_order if d in pivot.index])
    fig = px.imshow(
        pivot,
        color_continuous_scale=[[0,"#0f172a"],[0.3,"#22c55e"],[0.6,"#f59e0b"],
                                  [0.85,"#f97316"],[1,"#ef4444"]],
        aspect="auto",
        zmin=0, zmax=100,
        labels=dict(color="Congestion %"),
    )
    fig.update_traces(
        hovertemplate="<b>%{y} — %{x}</b><br>Congestion : %{z:.0f}%<extra></extra>"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(title="", ticksuffix="%",
                                tickfont=dict(color="#94a3b8", size=10),
                                thickness=12, len=0.8),
        xaxis=dict(tickfont=dict(size=9, color="#94a3b8"), showgrid=False),
        yaxis=dict(tickfont=dict(size=10, color="#cbd5e1"), showgrid=False),
        margin=dict(t=10, b=20, l=10, r=10), height=240,
        font=dict(family="Inter")
    )
    return fig


def build_network_overview_chart(all_status: list) -> go.Figure:
    """Graphique en barres — état de chaque ligne par type."""
    type_order = {"metro": 0, "rer": 1, "transilien": 2, "tram": 3, "bus": 4}
    sorted_status = sorted(all_status, key=lambda x: (type_order.get(x["type"], 9), x["line_name"]))

    labels = [s["line_name"].replace("Ligne ", "M").replace("Transilien ", "")
              .replace("Tram ", "").replace("Bus ", "").replace("RER ", "") for s in sorted_status]
    values = [s["congestion_pct"] for s in sorted_status]
    colors = [get_status_color(s["status"]) for s in sorted_status]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Congestion: %{y:.0f}%<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickangle=-45,
                   tickfont=dict(size=8, color="#475569")),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.15)",
                   color="#475569", ticksuffix="%", range=[0, 105],
                   tickfont=dict(size=9)),
        margin=dict(t=10, b=70, l=10, r=10), height=280,
        showlegend=False, font=dict(family="Inter")
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# HEADER & NAVIGATION MOBILE
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center;padding:1rem 0 0.5rem">
    <div style="font-size:2.5rem">🚇</div>
    <div style="font-size:1.5rem;font-weight:800;color:#0f172a">IDF Transit</div>
    <div style="font-size:0.8rem;color:#64748b;margin-top:2px">Tableau de Bord Trafic</div>
</div>
""", unsafe_allow_html=True)

# Mode simulation banner
stats = get_global_stats()
mode_color = "#ef4444" if "SIMULATION" in stats["mode"] else "#22c55e"
st.markdown(f"""
<div class="sim-banner">
    <span class="pulse" style="color:{mode_color}">●</span>
    &nbsp;<strong>{stats['mode']}</strong>
    <br><span style="color:#64748b">Actualisé à {stats['updated_at']}</span>
</div>""", unsafe_allow_html=True)

page = st.radio(
    "Navigation",
    ["🏠\nAccueil", "⏱️\nPassages", "📉\nPrédire", "🗺️\nCarte", "⚠️\nAlertes"],
    horizontal=True,
    label_visibility="collapsed"
)

# ── Remontée automatique en haut de page lors du changement d'onglet ──
if st.session_state.get('last_page') != page:
    # On ajoute time.time() dans le bloc JS pour forcer Streamlit à recharger l'IFrame
    components.html(f"""
        <script>
            // Execution context: {time.time()}
            const parent = window.parent;
            // Native window
            parent.scrollTo({{top: 0, behavior: 'instant'}});
            // Streamlit inner containers
            const viewContainer = parent.document.querySelector('[data-testid="stAppViewContainer"]');
            if (viewContainer) viewContainer.scrollTo({{top: 0, behavior: 'instant'}});
            const mainContainer = parent.document.querySelector('.stMain');
            if (mainContainer) mainContainer.scrollTo({{top: 0, behavior: 'instant'}});
        </script>
    """, height=0)
    st.session_state['last_page'] = page

with st.expander("⚙️ Paramètres & Infos"):
    auto_refresh = st.toggle("Actualisation auto (10s)", value=True)
    show_night = st.toggle("Inclure horaires nuit", value=False)
    st.markdown("""
    <div style="font-size:0.72rem;color:#64748b;text-align:center;padding:0.5rem 0; border-top:1px solid #e2e8f0; margin-top:10px;">
        Source : API IDFM PRIM<br>
        <a href="https://prim.iledefrance-mobilites.fr" style="color:#6366f1" target="_blank">prim.iledefrance-mobilites.fr</a><br><br>
        © 2025 IDF Transit Dashboard
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AUTO REFRESH
# ══════════════════════════════════════════════════════════════════════════════
if auto_refresh:
    st_autorefresh(interval=10000, limit=None, key="data_refresh")


# ══════════════════════════════════════════════════════════════════════════════
# CHARGEMENT DES DONNÉES
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=10)
def load_all_status():
    return get_all_lines_status()

@st.cache_data(ttl=10)
def load_stats():
    return get_global_stats()

@st.cache_data(ttl=10)
def load_alerts():
    return get_traffic_alerts()

all_status = load_all_status()
stats = load_stats()
alerts = load_alerts()
now = datetime.now(PARIS_TZ)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : VUE GÉNÉRALE
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠\nAccueil":

    st.markdown('<h1 class="hero-title">Vue d\'Ensemble</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-sub">Temps réel simulé • {now.strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    
    col_h1, col_h2 = st.columns([3, 1])
    with col_h2:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI cards ──
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_metric_card(stats["total_lines"], "Lignes surveillées", "#6366f1")
    with c2:
        render_metric_card(stats["normal"], "Trafic normal", "#22c55e", "✅ ")
    with c3:
        render_metric_card(stats["disrupted"], "Perturbées", "#f59e0b", "⚠️ ")
    with c4:
        render_metric_card(stats["interrupted"], "Interrompues", "#ef4444", "🔴 ")
    with c5:
        render_metric_card(f"{stats['reliability_pct']}%", "Taux de régularité", "#06b6d4")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Graphique global réseau ──
    st.markdown('<div class="section-header">📊 Congestion en temps réel — toutes les lignes</div>', unsafe_allow_html=True)
    st.plotly_chart(build_network_overview_chart(all_status), use_container_width=True)

    # ── Lignes par type ──
    st.markdown('<div class="section-header">🗂️ État détaillé par type de transport</div>', unsafe_allow_html=True)

    tabs = st.tabs(["🚇 Métro", "🚆 RER", "🚉 Transilien", "🚊 Tramway", "🚌 Bus"])

    def render_lines_tab(lines_dict: dict, prefix: str, tab):
        with tab:
            for line_id, line_info in lines_dict.items():
                lk = f"{prefix}_{line_id}"
                s = next((x for x in all_status if x["line_key"] == lk), None)
                if not s:
                    continue
                sc = get_status_color(s["status"])
                si = get_status_icon(s["status"])
                freq = s["current_frequency_min"]
                cong = s["congestion_pct"]
                col1, col2, col3, col4 = st.columns([2.5, 2.5, 2, 2])
                with col1:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0">'
                        f'<span style="background:{line_info["color"]};padding:3px 10px;border-radius:7px;'
                        f'font-weight:800;font-size:0.82rem;color:white;white-space:nowrap">{line_id}</span>'
                        f'<span style="font-size:0.88rem;color:#cbd5e1">{line_info["name"]}</span>'
                        f'</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div style="padding:9px 0;font-size:0.88rem">{si} <span style="color:{sc};font-weight:600">{get_status_label(s["status"])}</span></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div style="padding:9px 0;font-size:0.88rem;color:#64748b">⏱ Toutes les <strong style="color:#0f172a">{freq} min</strong></div>', unsafe_allow_html=True)
                with col4:
                    bar_w = max(0, min(100, cong))
                    bar_c = congestion_color(cong)
                    st.markdown(f"""
                    <div style="padding:8px 0">
                        <div style="display:flex;align-items:center;gap:8px">
                            <div style="flex:1;height:8px;background:rgba(71,85,105,0.4);border-radius:4px;overflow:hidden">
                                <div style="width:{bar_w}%;height:100%;background:{bar_c};border-radius:4px;transition:width 0.4s"></div>
                            </div>
                            <span style="font-size:0.78rem;color:{bar_c};font-weight:600;min-width:36px">{cong:.0f}%</span>
                        </div>
                    </div>""", unsafe_allow_html=True)

    render_lines_tab(METRO_LINES, "metro", tabs[0])
    render_lines_tab(RER_LINES, "rer", tabs[1])
    render_lines_tab(TRANSILIEN_LINES, "transilien", tabs[2])
    render_lines_tab(TRAM_LINES, "tram", tabs[3])
    render_lines_tab(BUS_LINES, "bus", tabs[4])


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : PROCHAINS PASSAGES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⏱️\nPassages":

    st.markdown('<h1 class="hero-title">⏱ Passages</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-sub">Temps réel simulé • {now.strftime("%A %d %B %Y — %H:%M:%S")}</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sélection transport ──
    col1, col2, col3 = st.columns(3)
    with col1:
        transport_type = st.selectbox(
            "Type de transport",
            options=list(TRANSPORT_TYPES.keys()),
            format_func=lambda x: TRANSPORT_TYPES[x]["label"],
            key="sel_type"
        )
    lines_dict = TRANSPORT_TYPES[transport_type]["lines"]
    with col2:
        line_id = st.selectbox(
            "Ligne",
            options=list(lines_dict.keys()),
            format_func=lambda x: lines_dict[x]["name"],
            key="sel_line"
        )
    line_key = f"{transport_type}_{line_id}"
    stops = get_stops_for_line(line_key)
    with col3:
        stop_name = st.selectbox("Arrêt", options=stops, key="sel_stop")

    line_info = lines_dict[line_id]
    line_status = get_line_status(line_key)
    line_color = line_info["color"]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Etat de la ligne sélectionnée ──
    sc = get_status_color(line_status["status"])
    si = get_status_icon(line_status["status"])
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(30,41,59,0.9),rgba(15,23,42,0.9));
                border-radius:16px;padding:1.2rem 1.5rem;
                border:1px solid rgba(99,102,241,0.2);
                border-left:6px solid {line_color};margin-bottom:1.5rem">
        <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
            <div>
                <span style="background:{line_color};padding:5px 16px;border-radius:10px;
                             font-weight:900;font-size:1.1rem;color:white">{line_id}</span>
            </div>
            <div>
                <div style="font-size:1rem;font-weight:700;color:#e2e8f0">{line_info['name']}</div>
                <div style="font-size:0.82rem;color:#64748b">
                    {' ↔ '.join(line_info['terminus'])}
                </div>
            </div>
            <div style="margin-left:auto;text-align:right">
                <div style="font-size:0.9rem;color:{sc};font-weight:600">{si} {get_status_label(line_status['status'])}</div>
                <div style="font-size:0.8rem;color:#475569">{line_status['message']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Passages ──
    passages = get_next_passages(line_key, stop_name, n=6)

    col_pass, col_gauge = st.columns([3, 1])

    with col_pass:
        st.markdown(f'<div class="section-header">🚏 Prochains passages — {stop_name}</div>', unsafe_allow_html=True)

        if not passages:
            if line_status["status"] == "interrupted":
                st.error("🚨 **Service interrompu ou terminé.** Aucun passage prévu pour le moment sur cette ligne.")
            else:
                st.info("Aucun passage prévu dans les prochaines minutes.")
        else:
            for p in passages:
                delay_text = f' <span style="color:#f59e0b;font-size:0.75rem">(+{p["delay_minutes"]} min)</span>' if p["delay_minutes"] > 0 else ''
                wait_color = "#22c55e" if p["wait_minutes"] <= 5 else "#f59e0b" if p["wait_minutes"] <= 10 else "#94a3b8"
                st.markdown(f"""
                <div class="passage-row">
                    <div class="wait-time" style="color:{wait_color}">{p['wait_minutes']}'</div>
                    <div style="flex:1">
                        <div style="font-size:0.9rem;font-weight:600;color:#e2e8f0">
                            ➜ {p['direction']}{delay_text}
                        </div>
                        <div style="font-size:0.75rem;color:#475569">
                            Départ à {p['expected_time']} &nbsp;•&nbsp; {p['status']}
                        </div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:0.72rem;color:#334155">{p.get('vehicle_id','')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

        # Graphique timeline
        if passages:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Visualisation des passages</div>', unsafe_allow_html=True)
            fig = build_passage_timeline(passages, line_color)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

    with col_gauge:
        st.markdown('<div class="section-header">📈 Affluence</div>', unsafe_allow_html=True)
        fig_gauge = build_congestion_gauge(line_status["congestion_pct"], "Affluence actuelle")
        st.plotly_chart(fig_gauge, use_container_width=True)

        cong_label = congestion_label(line_status["congestion_pct"])
        cong_c = congestion_color(line_status["congestion_pct"])
        st.markdown(f"""
        <div style="text-align:center;margin-top:-10px">
            <span style="font-size:1.1rem;font-weight:700;color:{cong_c}">{cong_label}</span>
        </div>
        <div style="margin-top:1rem;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:0.8rem">
            <div style="font-size:0.78rem;color:#64748b;margin-bottom:4px">Fréquence théorique</div>
            <div style="font-size:0.95rem;font-weight:700;color:#0f172a">Toutes les {line_status['theoretical_frequency_min']} min</div>
            <div style="font-size:0.78rem;color:#64748b;margin-top:8px;margin-bottom:4px">Fréquence actuelle</div>
            <div style="font-size:0.95rem;font-weight:700;color:{cong_c}">Toutes les {line_status['current_frequency_min']} min</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : PRÉDICTIONS ML
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📉\nPrédire":

    st.markdown('<h1 class="hero-title">🤖 Prédictions ML du Trafic</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Modèle analytique entraîné sur les patterns horaires IDF — vacances, pointes, week-ends</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sélection ──
    col1, col2, col3 = st.columns(3)
    with col1:
        t_type = st.selectbox("Type de transport", list(TRANSPORT_TYPES.keys()),
                              format_func=lambda x: TRANSPORT_TYPES[x]["label"],
                              key="pred_type")
    lines_d = TRANSPORT_TYPES[t_type]["lines"]
    with col2:
        l_id = st.selectbox("Ligne", list(lines_d.keys()),
                             format_func=lambda x: lines_d[x]["name"], key="pred_line")
    with col3:
        pred_date = st.date_input("Date de prédiction", value=now.date())

    l_key = f"{t_type}_{l_id}"
    l_info = lines_d[l_id]
    l_color = l_info["color"]

    import datetime as dt_mod
    pred_datetime = PARIS_TZ.localize(
        dt_mod.datetime.combine(pred_date, dt_mod.time(now.hour, 0, 0))
    )

    # ── Prédiction pour l'heure actuelle ──
    pred_now = predict(
        pred_datetime, t_type,
        l_info["frequency_peak"], l_info["frequency_offpeak"]
    )

    st.markdown('<div class="section-header">🎯 Prédiction — Maintenant</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card(f"{pred_now['congestion_pct']:.0f}%", "Congestion prédite",
                           pred_now["level_color"])
    with c2:
        render_metric_card(f"{pred_now['frequency_min']} min", "Intervalle estimé",
                           l_color)
    with c3:
        render_metric_card(pred_now["traffic_level"], "Niveau de trafic",
                           pred_now["level_color"])
    with c4:
        render_metric_card(f"{int(pred_now['confidence']*100)}%", "Confiance du modèle",
                           "#06b6d4")

    # ── Contexte ──
    ctx_items = []
    if pred_now["is_peak_morning"]: ctx_items.append("🚨 Heure de pointe matin")
    if pred_now["is_peak_evening"]: ctx_items.append("🚨 Heure de pointe soir")
    if pred_now["is_weekend"]:      ctx_items.append("🟡 Week-end")
    if pred_now["is_school_holiday"]: ctx_items.append("🎒 Vacances scolaires")
    if not ctx_items: ctx_items.append("🟢 Période normale")
    st.markdown(
        f'<div style="margin:0.8rem 0 1.5rem;font-size:0.85rem;color:#94a3b8">'
        + " &nbsp;|&nbsp; ".join(ctx_items) + "</div>",
        unsafe_allow_html=True
    )

    # ── Profil journalier ──
    st.markdown('<div class="section-header">📈 Profil de congestion sur la journée</div>', unsafe_allow_html=True)
    day_df = predict_day_profile(t_type, l_info["frequency_peak"], l_info["frequency_offpeak"], pred_datetime)
    st.plotly_chart(build_day_profile_chart(day_df, l_color), use_container_width=True)

    # ── Tableau détaillé ──
    with st.expander("📋 Voir le tableau complet des prédictions horaires"):
        display_df = day_df[["hour_label", "congestion_pct", "frequency_min", "traffic_level", "is_peak"]].copy()
        display_df.columns = ["Heure", "Congestion (%)", "Intervalle (min)", "Niveau", "Heure de pointe"]
        display_df["Heure de pointe"] = display_df["Heure de pointe"].map({True: "⚡ Oui", False: "—"})
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # ── Heatmap semaine ──
    st.markdown('<div class="section-header">🗓️ Heatmap — Congestion semaine complète</div>', unsafe_allow_html=True)
    with st.spinner("Calcul de la heatmap..."):
        heatmap_df = predict_week_heatmap(t_type)
    st.plotly_chart(build_heatmap(heatmap_df), use_container_width=True)

    # ── Comparaison types de transport ──
    st.markdown('<div class="section-header">🔄 Comparaison — Congestion par type de transport</div>', unsafe_allow_html=True)
    types_pred = {}
    for tp in ["metro", "rer", "transilien", "tram", "bus"]:
        p = predict(pred_datetime, tp)
        types_pred[tp] = p["congestion_pct"]

    type_labels = {"metro": "🚇 Métro", "rer": "🚆 RER", "transilien": "🚉 Transilien", "tram": "🚊 Tramway", "bus": "🚌 Bus"}
    type_colors = {"metro": "#6366f1", "rer": "#ef4444", "transilien": "#8b5cf6", "tram": "#06b6d4", "bus": "#22c55e"}

    fig_comp = go.Figure()
    for tp, val in types_pred.items():
        fig_comp.add_trace(go.Bar(
            x=[type_labels[tp]], y=[val],
            marker_color=type_colors[tp],
            marker_line_width=0,
            showlegend=False,
            hovertemplate=f"<b>{type_labels[tp]}</b><br>Congestion : {val:.0f}%<extra></extra>",
        ))
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#475569"),
        yaxis=dict(showgrid=True, gridcolor="rgba(71,85,105,0.15)",
                   color="#475569", ticksuffix="%", range=[0, 105]),
        margin=dict(t=10, b=30, l=10, r=10), height=200,
        font=dict(family="Inter")
    )
    st.plotly_chart(fig_comp, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : CARTE DU RÉSEAU
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️\nCarte":

    st.markdown('<h1 class="hero-title">🗺️ Carte du Réseau IDF</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Principales stations — état du trafic en temps réel</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Scatter map plotly ──
    lats, lons, labels, hovers, marker_colors, marker_sizes = [], [], [], [], [], []

    for station, (lat, lon) in STATION_COORDS.items():
        lats.append(lat)
        lons.append(lon)
        labels.append(station)
        hovers.append(f"<b>{station}</b>")
        marker_colors.append("#6366f1")
        marker_sizes.append(10)

    fig_map = go.Figure()

    # Stations
    fig_map.add_trace(go.Scattermapbox(
        lat=lats, lon=lons,
        mode="markers+text",
        marker=dict(size=marker_sizes, color=marker_colors, opacity=0.9),
        text=labels,
        textposition="top right",
        textfont=dict(size=9, color="white"),
        hovertemplate="%{text}<extra></extra>",
        name="Stations",
    ))

    fig_map.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=48.856614, lon=2.3522219),
            zoom=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0, b=0, l=0, r=0),
        height=520,
        showlegend=False,
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ── Légende ──
    st.markdown("""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:0.5rem;font-size:0.82rem;color:#64748b">
        <span>🟣 Stations principales</span>
        <span>• Zoom et déplacement disponibles</span>
        <span>• Survoler les marqueurs pour les détails</span>
    </div>""", unsafe_allow_html=True)

    # ── Statistiques réseau ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Réseau en chiffres</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    counts = {
        "metro": len(METRO_LINES),
        "rer": len(RER_LINES),
        "transilien": len(TRANSILIEN_LINES),
        "tram": len(TRAM_LINES),
        "bus": len(BUS_LINES),
    }
    with c1: render_metric_card(counts["metro"], "Lignes Métro", "#6366f1")
    with c2: render_metric_card(counts["rer"], "Lignes RER", "#ef4444")
    with c3: render_metric_card(counts["transilien"], "Lignes Transilien", "#8b5cf6")
    with c4: render_metric_card(counts["tram"], "Lignes Tram", "#06b6d4")
    with c5: render_metric_card(counts["bus"], "Lignes Bus", "#22c55e")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : ALERTES TRAFIC
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚠️\nAlertes":

    st.markdown('<h1 class="hero-title">⚠️ Alertes & Perturbations</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-sub">Mis à jour à {now.strftime("%H:%M:%S")} • Rafraîchissement automatique toutes les 30s</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPIs alertes ──
    interrupted = [a for a in alerts if a["status"] == "interrupted"]
    disrupted = [a for a in alerts if a["status"] == "disrupted"]

    c1, c2, c3 = st.columns(3)
    with c1: render_metric_card(len(alerts), "Alertes actives", "#f59e0b" if alerts else "#22c55e")
    with c2: render_metric_card(len(interrupted), "Lignes interrompues", "#ef4444")
    with c3: render_metric_card(len(disrupted), "Lignes perturbées", "#f59e0b")

    st.markdown("<br>", unsafe_allow_html=True)

    if not alerts:
        st.markdown("""
        <div style="text-align:center;padding:3rem 0;background:rgba(34,197,94,0.08);
                    border-radius:16px;border:1px solid rgba(34,197,94,0.2)">
            <div style="font-size:3rem">✅</div>
            <div style="font-size:1.2rem;font-weight:700;color:#22c55e;margin-top:0.5rem">Trafic normal sur l'ensemble du réseau</div>
            <div style="font-size:0.85rem;color:#475569;margin-top:0.3rem">Aucune perturbation signalée</div>
        </div>""", unsafe_allow_html=True)
    else:
        # ── Interrompues ──
        if interrupted:
            st.markdown('<div class="section-header" style="color:#b91c1c">🔴 Lignes Interrompues</div>', unsafe_allow_html=True)
            for a in interrupted:
                sc = get_status_color(a["status"])
                st.markdown(f"""
                <div class="alert-card alert-interrupted">
                    <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
                        <span style="background:{a['color']};padding:4px 12px;border-radius:8px;
                                     font-weight:800;color:white;font-size:0.85rem">{a['line_name'].split()[-1]}</span>
                        <div>
                            <div style="font-size:0.92rem;font-weight:700;color:#b91c1c">{a['line_name']}</div>
                            <div style="font-size:0.8rem;color:#ef4444;opacity:0.9">{a['message']}</div>
                        </div>
                        <div style="margin-left:auto;text-align:right">
                            <div style="font-size:0.78rem;color:#ef4444">Congestion : {a['congestion_pct']:.0f}%</div>
                            <div style="font-size:0.72rem;color:#475569">MAJ {a['updated_at']}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

        # ── Perturbées ──
        if disrupted:
            st.markdown('<div class="section-header" style="color:#b45309;margin-top:1rem">⚠️ Lignes Perturbées</div>', unsafe_allow_html=True)
            for a in disrupted:
                st.markdown(f"""
                <div class="alert-card alert-disrupted">
                    <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
                        <span style="background:{a['color']};padding:4px 12px;border-radius:8px;
                                     font-weight:800;color:white;font-size:0.85rem">{a['line_name'].split()[-1]}</span>
                        <div>
                            <div style="font-size:0.92rem;font-weight:700;color:#b45309">{a['line_name']}</div>
                            <div style="font-size:0.8rem;color:#b45309;opacity:0.9">{a['message']}</div>
                        </div>
                        <div style="margin-left:auto;text-align:right">
                            <div style="font-size:0.78rem;color:#f59e0b">Congestion : {a['congestion_pct']:.0f}%</div>
                            <div style="font-size:0.72rem;color:#475569">MAJ {a['updated_at']}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Historique simulé ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Historique des incidents (aujourd\'hui)</div>', unsafe_allow_html=True)
    history_data = [
        {"Heure": "08:23", "Ligne": "RER A", "Type": "Perturbation", "Message": "Incident voyageur — Trafic ralenti", "Durée": "18 min", "Etat": "Résolu ✅"},
        {"Heure": "10:47", "Ligne": "Métro 4", "Type": "Perturbation", "Message": "Régulation en cours", "Durée": "6 min", "Etat": "Résolu ✅"},
        {"Heure": "13:15", "Ligne": "RER B", "Type": "Perturbation", "Message": "Affluence voyageurs", "Durée": "12 min", "Etat": "Résolu ✅"},
        {"Heure": "17:02", "Ligne": "Métro 13", "Type": "Perturbation", "Message": "Malaise voyageur — départ retardé", "Durée": "8 min", "Etat": "Résolu ✅"},
    ]
    # Ajouter les alertes actives
    for a in alerts:
        history_data.append({
            "Heure": a["updated_at"],
            "Ligne": a["line_name"],
            "Type": "Interruption" if a["status"] == "interrupted" else "Perturbation",
            "Message": a["message"],
            "Durée": "En cours",
            "Etat": "🔴 En cours" if a["status"] == "interrupted" else "⚠️ En cours",
        })
    hist_df = pd.DataFrame(history_data)
    st.dataframe(hist_df, use_container_width=True, hide_index=True)
