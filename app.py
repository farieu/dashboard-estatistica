# ============================================================
#  app.py — Entrada principal do dashboard
# ============================================================

from shiny import App, ui

from styles import CSS
from tabs.tab_01_descritiva import tab_ui as ui_01, tab_server as server_01
from tabs.tab_02_hipoteses  import tab_ui as ui_02, tab_server as server_02
from tabs.tab_03_ic         import tab_ui as ui_03, tab_server as server_03
from tabs.tab_04_regressao  import tab_ui as ui_04, tab_server as server_04

# ── UI ───────────────────────────────────────────────────────
app_ui = ui.page_fluid(
    ui.tags.style(CSS),

    # Header global
    ui.div(
        ui.tags.span("📊", style="font-size:1.6rem"),
        ui.tags.h1("Dashboard Estatístico"),
        ui.tags.span("Análise Exploratória", class_="badge"),
        class_="dash-header"
    ),

    # Abas
    ui.navset_tab(
        ui_01,
        ui_02,
        ui_03,
        ui_04,
    ),
)

# ── Server ───────────────────────────────────────────────────
def server(input, output, session):
    server_01(input, output, session)
    server_02(input, output, session)
    server_03(input, output, session)
    server_04(input, output, session)

# ── App ──────────────────────────────────────────────────────
app = App(app_ui, server)
