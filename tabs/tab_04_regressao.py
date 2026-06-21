# ============================================================
#  Aba 04 — Regressão Linear Simples
#  Usuário carrega os 3 datasets de uma vez e escolhe qual usar
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
    "04 — Regressão Linear",

    ui.div(
        # Sidebar
        ui.div(
            ui.tags.p("Configurações", class_="sidebar-title"),

            # Upload dos 3 datasets de uma vez
            ui.tags.label("Carregar datasets (selecione os 3)"),
            ui.input_file(
                "arquivos_reg",
                label=None,
                accept=[".csv"],
                button_label="Selecionar arquivos",
                multiple=True,
            ),

            # Seletor do dataset ativo
            ui.tags.label("Dataset"),
            ui.input_select(
                "dataset_reg",
                label=None,
                choices={"": "— carregue os arquivos primeiro —"},
            ),

            ui.tags.label("Variável explicativa (X)"),
            ui.input_select(
                "var_x",
                label=None,
                choices={"": "—"},
            ),

            ui.tags.label("Variável resposta (Y)"),
            ui.input_select(
                "var_y",
                label=None,
                choices={"": "—"},
            ),

            ui.input_action_button(
                "calcular_reg", "Ajustar Regressão",
                class_="btn-analisar",
            ),

            class_="sidebar"
        ),

        # Conteúdo
        ui.div(
            ui.output_ui("conteudo_regressao"),
            class_="content-area"
        ),

        class_="dash-body"
    )
)


# ── Server da aba ────────────────────────────────────────────
def tab_server(input, output, session):

    # Armazena todos os datasets carregados como dict {nome: df}
    @reactive.calc
    def todos_datasets():
        import pandas as pd
        files = input.arquivos_reg()
        if not files:
            return {}
        resultado = {}
        for f in files:
            nome = f["name"].replace(".csv", "")
            df   = pd.read_csv(f["datapath"])
            resultado[nome] = df
        return resultado

    # Atualiza seletor de datasets quando os arquivos são carregados
    @reactive.effect
    def _atualiza_datasets():
        dfs = todos_datasets()
        if not dfs:
            return
        choices = {nome: nome for nome in dfs.keys()}
        ui.update_select("dataset_reg", choices=choices)

    # Atualiza seletores de X e Y quando o dataset selecionado muda
    @reactive.effect
    def _atualiza_variaveis():
        dfs  = todos_datasets()
        nome = input.dataset_reg()
        if not dfs or not nome or nome not in dfs:
            return
        df        = dfs[nome]
        numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        excluir   = {"id", "longitude", "latitude", "outcome"}
        numericas = [c for c in numericas if c.lower() not in excluir]
        choices   = {c: c for c in numericas}
        ui.update_select("var_x", choices=choices)
        ui.update_select("var_y", choices=choices)

    # Conteúdo principal
    @output
    @render.ui
    def conteudo_regressao():
        dfs = todos_datasets()
        if not dfs:
            return ui.div(
                ui.div(
                    ui.tags.div("📂", class_="icon"),
                    ui.tags.p("Carregue os 3 arquivos CSV e clique em Ajustar Regressão."),
                    class_="msg-inicial"
                )
            )

        input.calcular_reg()

        nome  = input.dataset_reg()
        var_x = input.var_x()
        var_y = input.var_y()

        if not nome or nome not in dfs:
            return ui.div(
                ui.div(
                    ui.tags.div("↩", class_="icon"),
                    ui.tags.p("Selecione um dataset."),
                    class_="msg-inicial"
                )
            )

        if not var_x or not var_y:
            return ui.div(
                ui.div(
                    ui.tags.div("↩", class_="icon"),
                    ui.tags.p("Escolha as variáveis X e Y e clique em Ajustar Regressão."),
                    class_="msg-inicial"
                )
            )

        if var_x == var_y:
            return ui.div(
                ui.div(
                    ui.tags.div("⚠️", class_="icon"),
                    ui.tags.p("X e Y não podem ser a mesma variável."),
                    class_="msg-inicial"
                )
            )

        df    = dfs[nome]
        dados = df[[var_x, var_y]].dropna()
        x     = dados[var_x].values
        y     = dados[var_y].values
        n     = len(x)

        # Regressão
        slope, intercept, r, p_value, std_err = stats.linregress(x, y)
        r2      = r ** 2
        sinal   = "+" if intercept >= 0 else "-"
        eq_reta = f"ŷ = {slope:.4f}x {sinal} {abs(intercept):.4f}"

        return ui.div(
            # Info
            ui.div(
                ui.tags.span("Dataset: "),
                ui.tags.strong(nome),
                ui.tags.span("  ·  "),
                ui.tags.span("X: "),
                ui.tags.strong(var_x),
                ui.tags.span("  ·  "),
                ui.tags.span("Y: "),
                ui.tags.strong(var_y),
                ui.tags.span("  ·  "),
                ui.tags.span("n = "),
                ui.tags.strong(str(n)),
                class_="dataset-info"
            ),

            # Value boxes — métricas principais
            ui.div(
                _vbox4("Coeficiente R",   f"{r:.4f}",  False),
                _vbox4("Coeficiente R²",  f"{r2:.4f}", False),
                _vbox4("Equação da reta", eq_reta,     False),
                class_="vbox-row"
            ),

            # Value boxes — coeficientes
            ui.div(
                _vbox4("Intercepto (β₀)",  f"{intercept:.4f}", True),
                _vbox4("Inclinação (β₁)",  f"{slope:.4f}",     True),
                _vbox4("Erro padrão (β₁)", f"{std_err:.4f}",   True),
                class_="vbox-row"
            ),

            # Interpretação
            ui.div(
                ui.tags.span("📌 INTERPRETAÇÃO", class_="vbox-label"),
                ui.tags.p(
                    f"Para cada aumento de 1 unidade em {var_x}, "
                    f"{var_y} {'aumenta' if slope > 0 else 'diminui'} em média "
                    f"{abs(slope):.4f} unidades. "
                    f"O modelo explica {r2*100:.2f}% da variabilidade de {var_y}.",
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
                    f"Dispersão — {var_x} vs {var_y} com linha de regressão",
                    class_="chart-card-header"
                ),
                ui.output_plot("plot_dispersao"),
                class_="chart-card"
            ),
        )

    # Gráfico de dispersão + linha de regressão
    @output
    @render.plot
    def plot_dispersao():
        input.calcular_reg()
        dfs   = todos_datasets()
        nome  = input.dataset_reg()
        var_x = input.var_x()
        var_y = input.var_y()

        if not dfs or not nome or not var_x or not var_y or var_x == var_y:
            return
        if nome not in dfs:
            return

        df    = dfs[nome]
        dados = df[[var_x, var_y]].dropna()
        x     = dados[var_x].values
        y     = dados[var_y].values

        slope, intercept, r, _, _ = stats.linregress(x, y)
        x_line = np.linspace(x.min(), x.max(), 200)
        y_line = slope * x_line + intercept

        fig, ax = plt.subplots(figsize=(8, 4.5))
        fig.patch.set_facecolor(COR_FUNDO)
        ax.set_facecolor(COR_FUNDO)

        ax.scatter(x, y, color=COR_PRIMARIA, alpha=0.45, s=18,
                   edgecolors="none", label="Observações")

        sinal = "+ " if intercept >= 0 else "- "
        ax.plot(x_line, y_line, color=COR_ACCENT, linewidth=2.5,
                label=f"ŷ = {slope:.4f}x {sinal}{abs(intercept):.4f}  (R²={r**2:.4f})")

        ax.set_xlabel(var_x, fontsize=10, color=COR_TEXTO)
        ax.set_ylabel(var_y, fontsize=10, color=COR_TEXTO)
        ax.tick_params(colors=COR_TEXTO, labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor(COR_BORDA)
        ax.legend(fontsize=9, framealpha=0.8)
        fig.tight_layout(pad=1.5)
        return fig


# ── Helper ───────────────────────────────────────────────────
def _vbox4(label: str, valor: str, accent: bool):
    cls = "vbox accent" if accent else "vbox"
    return ui.div(
        ui.tags.span(label, class_="vbox-label"),
        ui.tags.span(valor, class_="vbox-value", style="font-size:1.2rem;"),
        class_=cls,
    )
