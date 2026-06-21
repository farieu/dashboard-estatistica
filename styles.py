# ============================================================
#  styles.py — Paleta e CSS global do dashboard
# ============================================================

COR_PRIMARIA = "#2E7D6B"
COR_ACCENT   = "#F4A261"
COR_FUNDO    = "#F7F9F8"
COR_CARD     = "#FFFFFF"
COR_TEXTO    = "#1C2826"
COR_BORDA    = "#D6E4E0"

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Serif+Display&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    background-color: {COR_FUNDO};
    color: {COR_TEXTO};
    font-family: 'Inter', sans-serif;
    font-size: 15px;
}}

/* ── Header ── */
.dash-header {{
    background: {COR_PRIMARIA};
    color: #fff;
    padding: 18px 32px;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 4px solid {COR_ACCENT};
}}
.dash-header h1 {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    font-weight: 400;
    letter-spacing: 0.01em;
}}
.dash-header .badge {{
    background: {COR_ACCENT};
    color: {COR_TEXTO};
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 4px 10px;
    border-radius: 4px;
}}

/* ── Nav tabs ── */
.nav-tabs {{
    border-bottom: 2px solid {COR_BORDA};
    padding: 0 24px;
    background: {COR_CARD};
}}
.nav-tabs .nav-link {{
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #6B8A85;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 14px 18px;
    margin-bottom: -2px;
    border-radius: 0 !important;
    transition: all 0.2s;
}}
.nav-tabs .nav-link:hover {{ color: {COR_PRIMARIA}; }}
.nav-tabs .nav-link.active {{
    color: {COR_PRIMARIA} !important;
    border-bottom: 3px solid {COR_PRIMARIA} !important;
    background: transparent !important;
}}

/* ── Layout principal ── */
.dash-body {{
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 0;
    min-height: calc(100vh - 100px);
}}

/* ── Sidebar ── */
.sidebar {{
    background: {COR_CARD};
    border-right: 1px solid {COR_BORDA};
    padding: 24px 18px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}}
.sidebar-title {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8AA8A1;
    padding-bottom: 8px;
    border-bottom: 1px solid {COR_BORDA};
}}
.sidebar label {{
    font-size: 0.82rem;
    font-weight: 600;
    color: {COR_TEXTO};
    margin-bottom: 4px;
    display: block;
}}
.form-control, .form-select {{
    border: 1.5px solid {COR_BORDA};
    border-radius: 6px;
    font-size: 0.85rem;
    padding: 8px 10px;
    width: 100%;
    background: {COR_FUNDO};
    color: {COR_TEXTO};
    transition: border-color 0.2s;
}}
.form-control:focus, .form-select:focus {{
    border-color: {COR_PRIMARIA};
    outline: none;
    box-shadow: 0 0 0 3px rgba(46,125,107,0.12);
}}
.btn-analisar {{
    background: {COR_PRIMARIA};
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 10px 0;
    width: 100%;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s;
    letter-spacing: 0.03em;
}}
.btn-analisar:hover {{ background: #235f51; }}

/* ── Conteúdo ── */
.content-area {{
    padding: 28px;
    display: flex;
    flex-direction: column;
    gap: 24px;
}}

/* ── Value boxes ── */
.vbox-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}}
.vbox {{
    background: {COR_CARD};
    border: 1px solid {COR_BORDA};
    border-radius: 10px;
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    border-left: 4px solid {COR_PRIMARIA};
}}
.vbox.accent {{ border-left-color: {COR_ACCENT}; }}
.vbox-label {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #8AA8A1;
}}
.vbox-value {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: {COR_PRIMARIA};
    line-height: 1;
}}
.vbox.accent .vbox-value {{ color: {COR_ACCENT}; }}

/* ── Cards de gráficos ── */
.chart-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}}
.chart-card {{
    background: {COR_CARD};
    border: 1px solid {COR_BORDA};
    border-radius: 10px;
    overflow: hidden;
}}
.chart-card-header {{
    padding: 12px 18px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8AA8A1;
    border-bottom: 1px solid {COR_BORDA};
    background: {COR_FUNDO};
}}
.chart-card img {{ width: 100%; display: block; }}

/* ── Mensagem inicial ── */
.msg-inicial {{
    text-align: center;
    padding: 60px 20px;
    color: #8AA8A1;
    font-size: 0.95rem;
}}
.msg-inicial .icon {{ font-size: 2.5rem; margin-bottom: 12px; }}

/* ── Info do dataset ── */
.dataset-info {{
    background: {COR_CARD};
    border: 1px solid {COR_BORDA};
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.82rem;
    color: #5A7A74;
    display: flex;
    gap: 24px;
    align-items: center;
    flex-wrap: wrap;
}}
.dataset-info strong {{ color: {COR_PRIMARIA}; }}
"""
