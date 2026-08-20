"""
Shared design system for the N100 Analytics dashboard.

This module centralizes all styling and UI elements for consistent rendering across pages:
    - apply_global_theme()   -> Inject shared CSS & design system with Light/Dark adaptivity
    - render_sidebar_nav()   -> Render gradient sidebar navigation & handle page switching
    - page_header()          -> Render standard gradient page titles with optional subtitle
    - metric_card()          -> Render custom 3D glassmorphism KPI cards with hover effects
    - style_plot()           -> Apply 3D depth, isometric styling & theme to Plotly figures
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# =====================================================
# 1. Professional Color System
# =====================================================
PRIMARY = "#715AE7"
SECONDARY = "#5D40BE"
DEEP = "#44228F"
LAVENDER = "#7C3AED"
ACCENT = "#E05600"

SUCCESS = "#10B981"
WARNING = "#F59E0B"
ERROR = "#EF4444"


def apply_global_theme() -> None:
    """Inject the shared adaptive CSS design system into the app."""
    st.markdown(
        f"""
        <style>
        /* =====================================================
           2. Adaptive Light & Dark Mode Engine
           ===================================================== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* Dark Mode Tokens (Default / Dark Base) */
        :root {{
            --bg-base: #090710;
            --text-main: #F1F0F9;
            --text-muted: #A3A0C2;
            --kpi-val-color: #F1F0F9;
            --kpi-title-color: #A792E4;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-bg-hover: rgba(255, 255, 255, 0.07);
            --glass-border: rgba(255, 255, 255, 0.12);
            --glass-border-top: rgba(255, 255, 255, 0.28);
            --input-bg: rgba(18, 14, 36, 0.55);
            --input-text: #F1F0F9;
            --card-shadow: rgba(0, 0, 0, 0.45);
            --ambient-1: rgba(113, 90, 231, 0.25);
            --ambient-2: rgba(247, 158, 89, 0.18);
            --label-color: #A792E4;
            --table-header-bg: rgba(255, 255, 255, 0.05);
        }}

        /* Light Mode Overrides */
        @media (prefers-color-scheme: light) {{
            :root {{
                --bg-base: #F8FAFC;
                --text-main: #0F172A !important;
                --text-muted: #475569 !important;
                /* Primary color for KPI values and labels in Light Mode */
                --kpi-val-color: {PRIMARY} !important;
                --kpi-title-color: {SECONDARY} !important;
                --glass-bg: rgba(255, 255, 255, 0.85);
                --glass-bg-hover: rgba(255, 255, 255, 0.98);
                --glass-border: rgba(113, 90, 231, 0.22);
                --glass-border-top: rgba(255, 255, 255, 1);
                --input-bg: rgba(255, 255, 255, 0.9);
                --input-text: #0F172A;
                --card-shadow: rgba(113, 90, 231, 0.15);
                --ambient-1: rgba(113, 90, 231, 0.12);
                --ambient-2: rgba(247, 158, 89, 0.12);
                --label-color: {SECONDARY};
                --table-header-bg: rgba(113, 90, 231, 0.08);
            }}
        }}

        html, body, [class*="stAppViewContainer"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-main) !important;
            background-color: var(--bg-base) !important;
            background-image: 
                radial-gradient(circle at 15% 20%, var(--ambient-1) 0%, transparent 45%),
                radial-gradient(circle at 85% 60%, var(--ambient-2) 0%, transparent 40%) !important;
            background-attachment: fixed !important;
        }}

        .stMarkdown, p, span, label {{
            color: var(--text-main);
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(14px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes shimmer {{
            0%   {{ background-position: 0% center; }}
            100% {{ background-position: 200% center; }}
        }}

        .main .block-container {{
            animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1);
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }}

        /* =====================================================
           Headings & Titles
           ===================================================== */
        h1 {{
            background: linear-gradient(90deg, {PRIMARY}, {LAVENDER}, {ACCENT}, {PRIMARY});
            background-size: 300% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 10s linear infinite;
            font-weight: 900 !important;
            letter-spacing: -0.03em;
        }}

        h2, h3 {{
            font-weight: 800 !important;
            border-left: 4px solid {ACCENT};
            padding-left: 0.75rem;
            color: var(--text-main) !important;
        }}

        .n100-page-subtitle {{
            color: var(--text-muted) !important;
            font-size: 0.98rem;
            margin-top: -0.5rem;
            margin-bottom: 1.5rem;
            font-weight: 500;
        }}

        /* =====================================================
           3. Frosted Glass Cards (Custom & Native Streamlit)
           ===================================================== */
        .glass-card-3d {{
            background: var(--glass-bg) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-top: 1px solid var(--glass-border-top) !important;
            border-radius: 20px !important;
            padding: 1.25rem;
            box-shadow: 
                0 18px 36px var(--card-shadow),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            transform: perspective(1000px) translateZ(0);
        }}

        .glass-card-3d:hover {{
            background: var(--glass-bg-hover) !important;
            transform: perspective(1000px) translateZ(12px) translateY(-5px);
            border-color: {PRIMARY} !important;
            box-shadow: 
                0 25px 45px rgba(113, 90, 231, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
        }}

        /* KPI Custom Card Title & Value Color Overrides */
        .glass-card-title {{
            color: var(--kpi-title-color) !important;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .glass-card-value {{
            color: var(--kpi-val-color) !important;
            font-size: 1.85rem;
            font-weight: 900;
            margin-top: 4px;
            letter-spacing: -0.02em;
        }}

        /* Streamlit Native Metric Card Overrides (`st.metric`) */
        div[data-testid="stMetric"] {{
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) saturate(160%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
            border: 1px solid var(--glass-border) !important;
            border-top: 1px solid var(--glass-border-top) !important;
            border-radius: 18px !important;
            padding: 1rem 1.25rem !important;
            box-shadow: 0 12px 30px var(--card-shadow), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        }}

        div[data-testid="stMetric"]:hover {{
            background: var(--glass-bg-hover) !important;
            transform: perspective(1000px) translateY(-4px) translateZ(8px) !important;
            border-color: {ACCENT} !important;
        }}

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] * {{
            color: var(--kpi-title-color) !important;
            font-weight: 700 !important;
            font-size: 0.82rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {{
            color: var(--kpi-val-color) !important;
            font-size: 1.75rem !important;
            font-weight: 900 !important;
        }}

        /* =====================================================
           4. Glass Filter Controls
           ===================================================== */
        div[data-testid="stSelectbox"] label,
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stTextInput"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stSlider"] label {{
            color: var(--label-color) !important;
            font-weight: 800;
            font-size: 0.88rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 6px;
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            background: var(--input-bg) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid var(--glass-border) !important;
            border-top: 1px solid var(--glass-border-top) !important;
            border-radius: 14px !important;
            color: var(--input-text) !important;
            box-shadow: 0 4px 12px var(--card-shadow) !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }}

        div[data-baseweb="select"] span,
        div[data-baseweb="input"] input {{
            color: var(--input-text) !important;
            font-weight: 600 !important;
        }}

        div[data-baseweb="select"]:hover > div,
        div[data-baseweb="input"]:hover > div {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 18px rgba(113, 90, 231, 0.35) !important;
            transform: translateY(-1px);
        }}

        div[data-baseweb="select"]:focus-within > div,
        div[data-baseweb="input"]:focus-within > div {{
            border-color: {ACCENT} !important;
            box-shadow: 0 0 20px rgba(247, 158, 89, 0.4) !important;
        }}

        ul[data-baseweb="menu"] {{
            background: var(--bg-base) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
        }}

        li[data-baseweb="option"] {{
            color: var(--text-main) !important;
        }}

        span[data-baseweb="tag"] {{
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY}) !important;
            backdrop-filter: blur(8px) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2) !important;
            padding: 4px 8px !important;
        }}

        span[data-baseweb="tag"] span {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stSlider"] div[role="slider"] {{
            background-color: {ACCENT} !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 0 12px {ACCENT} !important;
        }}

        div[data-testid="stSlider"] div[data-baseweb="slider"] div {{
            background-color: {PRIMARY} !important;
        }}

        /* =====================================================
           5. Frosted Glass Plot Containers
           ===================================================== */
        div[data-testid="stPlotlyChart"] {{
            background: var(--glass-bg) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-top: 1px solid var(--glass-border-top) !important;
            border-radius: 22px !important;
            padding: 1.2rem;
            box-shadow: 0 20px 45px var(--card-shadow);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            transform: perspective(1200px) rotateX(1deg);
        }}

        div[data-testid="stPlotlyChart"]:hover {{
            background: var(--glass-bg-hover) !important;
            transform: perspective(1200px) rotateX(0deg) translateY(-6px) translateZ(10px);
            border-color: {PRIMARY} !important;
            box-shadow: 0 30px 60px rgba(113, 90, 231, 0.22);
        }}

        /* =====================================================
           6. Translucent Navigation Sidebar
           ===================================================== */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {DEEP} 0%, {SECONDARY} 60%, {PRIMARY} 100%) !important;
            backdrop-filter: blur(30px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(30px) saturate(190%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 8px 0 32px rgba(0, 0, 0, 0.3) !important;
        }}

        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div {{
            color: #FFFFFF !important;
        }}

        .n100-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 4px 20px 4px;
            margin-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.18);
        }}

        .n100-brand-title {{
            font-weight: 900;
            font-size: 1.25rem;
            color: #FFFFFF;
            letter-spacing: -0.01em;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }}

        .n100-brand-sub {{
            font-size: 0.72rem;
            font-weight: 600;
            color: #A792E4 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 14px;
            padding: 12px 16px !important;
            transition: all 0.25s cubic-bezier(0.165, 0.84, 0.44, 1);
            cursor: pointer;
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateX(6px);
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
            background: rgba(255, 255, 255, 0.32) !important;
            border-color: #F79E59 !important;
            box-shadow: 0 0 20px rgba(247, 158, 89, 0.5) !important;
        }}

        /* =====================================================
           7. DataFrames & Tables
           ===================================================== */
        div[data-testid="stDataFrame"] {{
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--glass-border);
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 0 15px 35px var(--card-shadow);
        }}

        /* =====================================================
           8. Buttons & Controls
           ===================================================== */
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stButton"] button {{
            border-radius: 12px;
            font-weight: 800;
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 0.6rem 1.4rem;
            box-shadow: 0 8px 20px rgba(113, 90, 231, 0.35);
            transition: all 0.25s ease;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        div[data-testid="stDownloadButton"] button:hover,
        div[data-testid="stButton"] button:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 28px rgba(247, 158, 89, 0.55);
            background: linear-gradient(135deg, #F79E59, {PRIMARY});
            color: #FFFFFF !important;
        }}

        button[data-baseweb="tab"] {{
            font-weight: 700;
            color: var(--text-muted) !important;
            border-radius: 10px 10px 0 0 !important;
            padding: 0.8rem 1.4rem !important;
        }}

        button[data-baseweb="tab"]:hover {{
            color: var(--label-color) !important;
        }}

        div[data-baseweb="tab-highlight"] {{
            background: linear-gradient(90deg, {PRIMARY}, #F79E59) !important;
            height: 4px !important;
        }}

        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
            margin: 1.5rem 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# Helper Functions
# =====================================================
def page_header(icon: str, title: str, subtitle: str | None = None) -> None:
    """Render a consistent gradient page title and subtitle."""
    st.title(f"{icon} {title}")
    if subtitle:
        st.markdown(
            f'<div class="n100-page-subtitle">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def metric_card(title: str, value: str, change: str | None = None, is_positive: bool = True) -> None:
    """Custom 3D Glassmorphism KPI card with theme-adaptive primary color typography."""
    change_html = ""
    if change:
        color = SUCCESS if is_positive else ERROR
        arrow = "▲" if is_positive else "▼"
        change_html = f'<div style="color: {color}; font-weight: 800; font-size: 0.85rem; margin-top: 6px;">{arrow} {change}</div>'

    html_code = f"""
    <div class="glass-card-3d">
        <div class="glass-card-title">{title}</div>
        <div class="glass-card-value">{value}</div>
        {change_html}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def style_plot(fig: go.Figure) -> go.Figure:
    """Apply isometric depth, soft ambient lighting & theme-aware text contrast to Plotly charts."""
    
    colors = [PRIMARY, "#F79E59", LAVENDER, SECONDARY, "#10B981", "#EF4444"]
    
    for i, trace in enumerate(fig.data):
        color_idx = i % len(colors)
        
        if trace.type == "bar":
            trace.marker.color = colors[color_idx]
            trace.marker.line = dict(color="rgba(255,255,255,0.4)", width=1.5)
            if hasattr(trace, "opacity") and trace.opacity is None:
                trace.opacity = 0.95
                
        elif trace.type in ["scatter", "lines"]:
            if hasattr(trace, "line") and trace.line.color is None:
                trace.line.color = colors[color_idx]
                trace.line.width = 3.5
            if trace.fill is None:
                trace.fill = "tonexty"
                trace.fillcolor = f"rgba(113, 90, 231, 0.1)"

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=25, r=25, t=45, b=25),
        
        scene=dict(
            xaxis=dict(
                backgroundcolor="rgba(113, 90, 231, 0.05)",
                gridcolor="rgba(113, 90, 231, 0.15)",
                showbackground=True,
                zerolinecolor="rgba(247, 158, 89, 0.4)",
            ),
            yaxis=dict(
                backgroundcolor="rgba(113, 90, 231, 0.05)",
                gridcolor="rgba(113, 90, 231, 0.15)",
                showbackground=True,
                zerolinecolor="rgba(247, 158, 89, 0.4)",
            ),
            zaxis=dict(
                backgroundcolor="rgba(113, 90, 231, 0.05)",
                gridcolor="rgba(113, 90, 231, 0.15)",
                showbackground=True,
                zerolinecolor="rgba(247, 158, 89, 0.4)",
            ),
            camera=dict(
                eye=dict(x=1.4, y=1.4, z=1.2)
            )
        ),
        
        xaxis=dict(
            gridcolor="rgba(113, 90, 231, 0.15)",
            zerolinecolor="rgba(113, 90, 231, 0.3)",
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor="rgba(113, 90, 231, 0.15)",
            zerolinecolor="rgba(113, 90, 231, 0.3)",
            showgrid=True,
        ),
        legend=dict(
            bgcolor="rgba(0, 0, 0, 0)",
            bordercolor="rgba(113, 90, 231, 0.2)",
            borderwidth=1,
        ),
    )
    return fig


def _auto_collapse_sidebar_on_mobile() -> None:
    """Auto-close sidebar on mobile viewports after selecting a page."""
    components.html(
        """
        <script>
        (function () {
            try {
                var doc = window.parent.document;
                var isMobile = window.parent.innerWidth <= 768;
                if (!isMobile) { return; }
                var btn = doc.querySelector('[data-testid="stSidebarCollapseButton"] button') 
                          || doc.querySelector('[data-testid="stSidebarCollapseButton"]');
                if (btn) { btn.click(); }
            } catch (e) {}
        })();
        </script>
        """,
        height=0,
    )


def render_sidebar_nav(pages: dict) -> str:
    """Render sidebar navigation and return selected page key."""
    with st.sidebar:
        st.markdown(
            """
            <div class="n100-brand">
                <div style="font-size: 2.2rem; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));">📊</div>
                <div>
                    <div class="n100-brand-title">N100 Analytics</div>
                    <div class="n100-brand-sub">Financial Intelligence</div>
                </div>
            </div>
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #A792E4; margin: 14px 2px 10px 2px;">
                Navigation
            </div>
            """,
            unsafe_allow_html=True,
        )

        options = list(pages.keys())
        labels = {key: f"{meta['icon']}  {meta['label']}" for key, meta in pages.items()}

        choice_label = st.radio(
            "Navigation",
            options=[labels[key] for key in options],
            label_visibility="collapsed",
            key="n100_nav_radio",
        )

        if st.session_state.get("_n100_last_nav") != choice_label:
            st.session_state["_n100_last_nav"] = choice_label
            _auto_collapse_sidebar_on_mobile()

        st.markdown(
            """
            <div style="margin-top: 30px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.12); font-size: 0.72rem; color: #A792E4; opacity: 0.75; line-height: 1.4;">
                Nifty 100 Analytics Platform<br/>
                Real-time Fundamentals &amp; Screening
            </div>
            """,
            unsafe_allow_html=True,
        )

    for key in options:
        if labels[key] == choice_label:
            return key
    return options[0]