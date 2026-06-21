# ============================================================
#  Aba 03 — Intervalo de Confiança Normal para a Média
#  Dataset: California Housing
# ============================================================

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from shiny import ui, render, reactive

from styles import COR_PRIMARIA, COR_ACCENT, COR_FUNDO, COR_TEXTO, COR_BORDA, COR_CARD

# ── UI da aba ────────────────────────────────────────────────
tab_ui = ui.nav_panel(
    "03 — Intervalo de Confiança",

    ui.div(
        # Sidebar
        ui.div(
            ui.tags.p("Configurações", class_="sidebar-title"),

            # Disclaimer — desvio padrão amostral
            ui.div(
                ui.tags.p("ℹ️ Sobre o cálculo", style="font-weight:700; font-size:0.78rem; margin-bottom:4px;"),
                ui.tags.p(
                    "Como a variância populacional não é assumida conhecida aqui, "
                    "o IC é calculado com o desvio padrão amostral (s) no lugar de σ. "
                    "Isso é válido pois a distribuição Normal é mantida.",
                    style="font-size:0.76rem; line-height:1.4; margin:0;"
                ),
                style="""
                    background:#EAF4F1; border:1px solid #C2DDD7;
                    border-left:3px solid #2E7D6B; border-radius:6px;
                    padding:10px 12px; color:#2E5D52;
                """
            ),

            ui.tags.label("Arquivo de dados (.csv)"),
            ui.input_file(
                "arquivo_ic",
                label=None,
                accept=[".csv"],
                button_label="Selecionar arquivo",
                multiple=False,
            ),

            ui.tags.label("Variável quantitativa"),
            ui.input_select(
                "variavel_ic",
                label=None,
                choices={"": "— carregue um arquivo —"},
            ),

            ui.tags.label("Nível de confiança (1 - α)"),
            ui.input_slider(
                "nivel_confianca",
                label=None,
                min=0.80, max=0.99,
                value=0.95, step=0.01,
            ),

            ui.input_action_button(
                "calcular_ic", "Calcular IC",
                class_="btn-analisar",
            ),

            class_="sidebar"
        ),

        # Conteúdo
        ui.div(
            ui.output_ui("conteudo_ic"),
            class_="content-area"
        ),

        class_="dash-body"
    )
)


# ── Server da aba ────────────────────────────────────────────
def tab_server(input, output, session):

    # Carrega o dataframe sem nenhuma modificação
    @reactive.calc
    def dados_ic():
        f = input.arquivo_ic()
        if not f:
            return None
        import pandas as pd
        return pd.read_csv(f[0]["datapath"])

    # Atualiza seletor de variáveis
    @reactive.effect
    def _atualiza_select_ic():
        df = dados_ic()
        if df is None:
            return
        numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        excluir   = {"id", "longitude", "latitude"}
        numericas = [c for c in numericas if c.lower() not in excluir]
        ui.update_select("variavel_ic", choices={c: c for c in numericas})

    # Conteúdo principal
    @output
    @render.ui
    def conteudo_ic():
        df = dados_ic()
        if df is None:
            return ui.div(
                ui.div(
                    ui.tags.div("📂", class_="icon"),
                    ui.tags.p("Selecione um arquivo CSV e clique em Calcular IC."),
                    class_="msg-inicial"
                )
            )

        input.calcular_ic()

        col = input.variavel_ic()
        if not col or col not in df.columns:
            return ui.div(
                ui.div(
                    ui.tags.div("↩", class_="icon"),
                    ui.tags.p("Escolha uma variável e clique em Calcular IC."),
                    class_="msg-inicial"
                )
            )

        serie      = df[col].dropna()
        n          = len(serie)
        media      = float(serie.mean())
        dp         = float(serie.std())
        confianca  = float(input.nivel_confianca())
        alpha      = 1 - confianca
        z_crit     = stats.norm.ppf(1 - alpha / 2)
        margem     = z_crit * (dp / np.sqrt(n))
        lim_inf    = media - margem
        lim_sup    = media + margem

        return ui.div(
            # Info do dataset
            ui.div(
                ui.tags.span("Arquivo: "),
                ui.tags.strong(input.arquivo_ic()[0]["name"]),
                ui.tags.span("  ·  "),
                ui.tags.span("Variável: "),
                ui.tags.strong(col),
                ui.tags.span("  ·  "),
                ui.tags.span("n = "),
                ui.tags.strong(str(n)),
                class_="dataset-info"
            ),

            # Nível de confiança em destaque
            ui.div(
                ui.div(
                    ui.tags.span("NÍVEL DE CONFIANÇA", class_="vbox-label"),
                    ui.tags.span(f"{confianca*100:.0f}%", class_="vbox-value"),
                    class_="vbox"
                ),
                ui.div(
                    ui.tags.span("Z CRÍTICO (z α/2)", class_="vbox-label"),
                    ui.tags.span(f"{z_crit:.4f}", class_="vbox-value"),
                    class_="vbox"
                ),
                ui.div(
                    ui.tags.span("MÉDIA AMOSTRAL (x̄)", class_="vbox-label"),
                    ui.tags.span(f"{media:.4f}", class_="vbox-value"),
                    class_="vbox"
                ),
                class_="vbox-row"
            ),

            # Limites do IC em destaque
            ui.div(
                ui.div(
                    ui.tags.span("LIMITE INFERIOR", class_="vbox-label"),
                    ui.tags.span(f"{lim_inf:.4f}", class_="vbox-value"),
                    class_="vbox accent"
                ),
                ui.div(
                    ui.tags.span("LIMITE SUPERIOR", class_="vbox-label"),
                    ui.tags.span(f"{lim_sup:.4f}", class_="vbox-value"),
                    class_="vbox accent"
                ),
                ui.div(
                    ui.tags.span("MARGEM DE ERRO", class_="vbox-label"),
                    ui.tags.span(f"± {margem:.4f}", class_="vbox-value"),
                    class_="vbox accent"
                ),
                class_="vbox-row"
            ),

            # Interpretação
            ui.div(
                ui.tags.span("📌 INTERPRETAÇÃO", class_="vbox-label"),
                ui.tags.p(
                    f"Com {confianca*100:.0f}% de confiança, a média populacional de {col} "
                    f"está entre {lim_inf:.4f} e {lim_sup:.4f}.",
                    style="font-size:0.95rem; margin:6px 0 0; line-height:1.5;"
                ),
                style=f"""
                    background:{COR_CARD}; border:1px solid {COR_BORDA};
                    border-left:4px solid {COR_PRIMARIA}; border-radius:10px;
                    padding:16px 18px;
                """
            ),

            # Gráfico
            ui.div(
                ui.div(
                    "Intervalo de Confiança — Distribuição Normal",
                    class_="chart-card-header"
                ),
                ui.output_plot("plot_ic"),
                class_="chart-card"
            ),
        )

    # Gráfico do IC na curva normal
    @output
    @render.plot
    def plot_ic():
        input.calcular_ic()
        df  = dados_ic()
        col = input.variavel_ic()
        if df is None or not col or col not in df.columns:
            return

        serie     = df[col].dropna()
        n         = len(serie)
        media     = float(serie.mean())
        dp        = float(serie.std())
        confianca = float(input.nivel_confianca())
        alpha     = 1 - confianca
        z_crit    = stats.norm.ppf(1 - alpha / 2)
        margem    = z_crit * (dp / np.sqrt(n))
        lim_inf   = media - margem
        lim_sup   = media + margem

        x = np.linspace(-4, 4, 400)
        y = stats.norm.pdf(x)

        fig, ax = plt.subplots(figsize=(8, 3.5))
        fig.patch.set_facecolor(COR_FUNDO)
        ax.set_facecolor(COR_FUNDO)

        # Curva normal
        ax.plot(x, y, color=COR_PRIMARIA, linewidth=2)

        # Região de confiança (interior)
        ax.fill_between(x, y,
                        where=(x >= -z_crit) & (x <= z_crit),
                        color=COR_PRIMARIA, alpha=0.20,
                        label=f"IC {confianca*100:.0f}%")

        # Regiões de rejeição
        ax.fill_between(x, y, where=(x <= -z_crit), color=COR_ACCENT, alpha=0.30, label="α/2")
        ax.fill_between(x, y, where=(x >=  z_crit), color=COR_ACCENT, alpha=0.30)

        # Linhas críticas
        ax.axvline(-z_crit, color=COR_ACCENT, linewidth=1.5, linestyle="--")
        ax.axvline( z_crit, color=COR_ACCENT, linewidth=1.5, linestyle="--",
                    label=f"±z = ±{z_crit:.2f}")

        # Linha da média
        ax.axvline(0, color=COR_PRIMARIA, linewidth=1.5, linestyle=":",
                   label="μ (centro)")

        ax.set_xlabel("Z", fontsize=10, color=COR_TEXTO)
        ax.set_ylabel("Densidade", fontsize=10, color=COR_TEXTO)
        ax.tick_params(colors=COR_TEXTO, labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor(COR_BORDA)
        ax.legend(fontsize=9, framealpha=0.8, loc="upper right")
        fig.tight_layout(pad=1.5)
        return fig
