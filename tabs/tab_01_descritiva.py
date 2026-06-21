# ============================================================
#  Aba 01 — Análise Descritiva
# ============================================================

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shiny import ui, render, reactive

from styles import COR_PRIMARIA, COR_ACCENT, COR_FUNDO, COR_TEXTO, COR_BORDA, COR_CARD

# ── UI da aba ────────────────────────────────────────────────
tab_ui = ui.nav_panel(
    "01 — Análise Descritiva",

    ui.div(
        # Sidebar
        ui.div(
            ui.tags.p("Configurações", class_="sidebar-title"),

            ui.tags.label("Arquivo de dados (.csv)"),
            ui.input_file(
                "arquivo",
                label=None,
                accept=[".csv"],
                button_label="Selecionar arquivo",
                multiple=False,
            ),

            ui.tags.label("Variável quantitativa"),
            ui.input_select(
                "variavel",
                label=None,
                choices={"": "— carregue um arquivo —"},
            ),

            ui.tags.label("Nº de bins — Histograma"),
            ui.input_slider(
                "bins", label=None,
                min=5, max=50, value=15, step=1,
            ),

            ui.input_action_button(
                "analisar", "Analisar",
                class_="btn-analisar",
            ),

            class_="sidebar"
        ),

        # Conteúdo
        ui.div(
            ui.output_ui("conteudo_descritiva"),
            class_="content-area"
        ),

        class_="dash-body"
    )
)


# ── Server da aba ────────────────────────────────────────────
def tab_server(input, output, session):

    # Carrega o dataframe quando o arquivo é enviado
    @reactive.calc
    def dados():
        f = input.arquivo()
        if not f:
            return None
        import pandas as pd
        return pd.read_csv(f[0]["datapath"])

    # Atualiza o seletor de variáveis quando o df muda
    @reactive.effect
    def _atualiza_select():
        df = dados()
        if df is None:
            return
        numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        numericas = [c for c in numericas if c.lower() != "id"]
        ui.update_select("variavel", choices={c: c for c in numericas})

    # Renderiza todo o conteúdo da aba
    @output
    @render.ui
    def conteudo_descritiva():
        df = dados()
        if df is None:
            return ui.div(
                ui.div(
                    ui.tags.div("📂", class_="icon"),
                    ui.tags.p("Selecione um arquivo CSV e clique em Analisar."),
                    class_="msg-inicial"
                )
            )

        input.analisar()

        col = input.variavel()
        if not col or col not in df.columns:
            return ui.div(
                ui.div(
                    ui.tags.div("↩", class_="icon"),
                    ui.tags.p("Escolha uma variável e clique em Analisar."),
                    class_="msg-inicial"
                )
            )

        serie   = df[col].dropna()
        n       = int(len(serie))
        media   = float(serie.mean())
        mediana = float(serie.median())
        dp      = float(serie.std())
        minimo  = float(serie.min())
        maximo  = float(serie.max())

        return ui.div(
            # Info do dataset
            ui.div(
                ui.tags.span("Arquivo: "),
                ui.tags.strong(input.arquivo()[0]["name"]),
                ui.tags.span("  ·  "),
                ui.tags.span("Variável: "),
                ui.tags.strong(col),
                ui.tags.span("  ·  "),
                ui.tags.span("Observações válidas: "),
                ui.tags.strong(str(n)),
                class_="dataset-info"
            ),

            # Value boxes — linha 1
            ui.div(
                _vbox("Média",         f"{media:.4f}",   False),
                _vbox("Mediana",       f"{mediana:.4f}", False),
                _vbox("Desvio-padrão", f"{dp:.4f}",      False),
                class_="vbox-row"
            ),

            # Value boxes — linha 2
            ui.div(
                _vbox("Tamanho (n)", str(n),          True),
                _vbox("Mínimo",      f"{minimo:.4f}", True),
                _vbox("Máximo",      f"{maximo:.4f}", True),
                class_="vbox-row"
            ),

            # Gráficos
            ui.div(
                ui.div(
                    ui.div("Histograma", class_="chart-card-header"),
                    ui.output_plot("plot_hist"),
                    class_="chart-card"
                ),
                ui.div(
                    ui.div("Boxplot", class_="chart-card-header"),
                    ui.output_plot("plot_box"),
                    class_="chart-card"
                ),
                class_="chart-row"
            ),
        )

    # Histograma
    @output
    @render.plot
    def plot_hist():
        input.analisar()
        df  = dados()
        col = input.variavel()
        if df is None or not col or col not in df.columns:
            return

        serie = df[col].dropna()
        bins  = input.bins()

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(COR_FUNDO)
        ax.set_facecolor(COR_FUNDO)

        ax.hist(serie, bins=bins, color=COR_PRIMARIA,
                edgecolor="white", linewidth=0.6, alpha=0.9)
        ax.axvline(serie.mean(),   color=COR_ACCENT,  linewidth=2,
                   linestyle="--", label=f"Média: {serie.mean():.2f}")
        ax.axvline(serie.median(), color="#E76F51",    linewidth=2,
                   linestyle=":",  label=f"Mediana: {serie.median():.2f}")

        ax.set_xlabel(col, fontsize=10, color=COR_TEXTO)
        ax.set_ylabel("Frequência", fontsize=10, color=COR_TEXTO)
        ax.tick_params(colors=COR_TEXTO, labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor(COR_BORDA)
        ax.legend(fontsize=9, framealpha=0.7)
        fig.tight_layout(pad=1.5)
        return fig

    # Boxplot
    @output
    @render.plot
    def plot_box():
        input.analisar()
        df  = dados()
        col = input.variavel()
        if df is None or not col or col not in df.columns:
            return

        serie = df[col].dropna()

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(COR_FUNDO)
        ax.set_facecolor(COR_FUNDO)

        ax.boxplot(
            serie,
            vert=True,
            patch_artist=True,
            widths=0.45,
            medianprops=dict(color=COR_ACCENT, linewidth=2.5),
            boxprops=dict(facecolor=COR_PRIMARIA, alpha=0.7, linewidth=1.2),
            whiskerprops=dict(color=COR_TEXTO, linewidth=1.2),
            capprops=dict(color=COR_TEXTO, linewidth=1.5),
            flierprops=dict(marker="o", color=COR_ACCENT,
                            markerfacecolor=COR_ACCENT, markersize=5),
        )

        ax.set_xticks([1])
        ax.set_xticklabels([col], fontsize=10, color=COR_TEXTO)
        ax.set_ylabel("Valores", fontsize=10, color=COR_TEXTO)
        ax.tick_params(colors=COR_TEXTO, labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor(COR_BORDA)
        fig.tight_layout(pad=1.5)
        return fig


# ── Helper ───────────────────────────────────────────────────
def _vbox(label: str, valor: str, accent: bool):
    cls = "vbox accent" if accent else "vbox"
    return ui.div(
        ui.tags.span(label, class_="vbox-label"),
        ui.tags.span(valor, class_="vbox-value"),
        class_=cls,
    )
