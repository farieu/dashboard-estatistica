# ============================================================
#  Aba 02 — Teste de Hipóteses (Z, variância conhecida)
#  Dataset: Body Performance
# ============================================================

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from shiny import ui, render, reactive

from styles import COR_PRIMARIA, COR_ACCENT, COR_FUNDO, COR_TEXTO, COR_BORDA, COR_CARD

# ── Legenda das colunas do Body Performance ──────────────────
LEGENDA_COLUNAS = {
    "age":                   "Idade (anos)",
    "height_cm":             "Altura (cm)",
    "weight_kg":             "Peso (kg)",
    "body fat_%":            "Percentual de gordura corporal (%)",
    "diastolic":             "Pressão arterial diastólica (mmHg)",
    "systolic":              "Pressão arterial sistólica (mmHg)",
    "gripForce":             "Força de preensão manual (kgf)",
    "sit and bend forward_cm": "Flexibilidade — sentar e alcançar (cm)",
    "sit-ups counts":        "Número de abdominais realizados (reps)",
    "broad jump_cm":         "Salto em distância (cm)",
}

# ── UI da aba ────────────────────────────────────────────────
tab_ui = ui.nav_panel(
    "02 — Teste de Hipóteses",

    ui.div(
        # Sidebar
        ui.div(
            ui.tags.p("Configurações", class_="sidebar-title"),

            ui.tags.label("Arquivo de dados (.csv)"),
            ui.input_file(
                "arquivo_h",
                label=None,
                accept=[".csv"],
                button_label="Selecionar arquivo",
                multiple=False,
            ),

            ui.tags.label("Variável quantitativa"),
            ui.input_select(
                "variavel_h",
                label=None,
                choices={"": "— carregue um arquivo —"},
            ),

            # Variância — toggle automático / manual
            ui.tags.label("Variância populacional (σ²)"),
            ui.input_radio_buttons(
                "modo_variancia",
                label=None,
                choices={
                    "auto":   "Calcular automaticamente da amostra",
                    "manual": "Informar manualmente",
                },
                selected="auto",
            ),
            ui.output_ui("campo_variancia"),

            # Disclaimer variância e distribuição
            ui.div(
                ui.tags.p("ℹ️ Variância e distribuição", style="font-weight:700; font-size:0.78rem; margin-bottom:4px;"),
                ui.output_ui("disclaimer_variancia"),
                style="""
                    background:#EAF4F1; border:1px solid #C2DDD7;
                    border-left:3px solid #2E7D6B; border-radius:6px;
                    padding:10px 12px; color:#2E5D52;
                """
            ),

            # Disclaimer referências μ₀
            ui.div(
                ui.tags.p("📋 Referências para μ₀", style="font-weight:700; font-size:0.78rem; margin-bottom:6px;"),
                ui.tags.table(
                    ui.tags.tr(
                        ui.tags.th("Variável",    style="text-align:left; padding-right:8px;"),
                        ui.tags.th("μ₀ sugerido", style="text-align:left;"),
                    ),
                    ui.tags.tr(ui.tags.td("age"),                    ui.tags.td("36 anos")),
                    ui.tags.tr(ui.tags.td("body fat_%"),             ui.tags.td("25 %")),
                    ui.tags.tr(ui.tags.td("systolic"),               ui.tags.td("120 mmHg")),
                    ui.tags.tr(ui.tags.td("diastolic"),              ui.tags.td("80 mmHg")),
                    ui.tags.tr(ui.tags.td("gripForce"),              ui.tags.td("36 kgf")),
                    ui.tags.tr(ui.tags.td("sit-ups counts"),         ui.tags.td("30 reps")),
                    ui.tags.tr(ui.tags.td("broad jump_cm"),          ui.tags.td("170 cm")),
                    style="font-size:0.75rem; border-collapse:collapse; width:100%;"
                ),
                style="""
                    background:#FFF8F2; border:1px solid #F5D9C0;
                    border-left:3px solid #F4A261; border-radius:6px;
                    padding:10px 12px; color:#7A4A1E;
                """
            ),

            ui.tags.label("Tipo de teste"),
            ui.input_radio_buttons(
                "tipo_teste",
                label=None,
                choices={
                    "bilateral": "Bilateral  (H₁: μ ≠ μ₀)",
                    "direita":   "Unilateral direita  (H₁: μ > μ₀)",
                    "esquerda":  "Unilateral esquerda  (H₁: μ < μ₀)",
                },
                selected="bilateral",
            ),

            ui.tags.label("Valor de μ₀"),
            ui.output_ui("slider_mu0"),

            ui.tags.label("Nível de significância (α)"),
            ui.input_slider(
                "alpha",
                label=None,
                min=0.01, max=0.10,
                value=0.05, step=0.01,
            ),

            ui.input_action_button(
                "testar", "Executar Teste",
                class_="btn-analisar",
            ),

            class_="sidebar"
        ),

        # Conteúdo
        ui.div(
            ui.output_ui("legenda_colunas"),
            ui.output_ui("conteudo_hipoteses"),
            class_="content-area"
        ),

        class_="dash-body"
    )
)


# ── Server da aba ────────────────────────────────────────────
def tab_server(input, output, session):

    # Carrega o dataframe sem nenhuma modificação
    @reactive.calc
    def dados_h():
        f = input.arquivo_h()
        if not f:
            return None
        import pandas as pd
        return pd.read_csv(f[0]["datapath"])

    # Atualiza seletor — exclui colunas não numéricas (gender, class)
    @reactive.effect
    def _atualiza_select_h():
        df = dados_h()
        if df is None:
            return
        numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        excluir   = {"id"}
        numericas = [c for c in numericas if c.lower() not in excluir]
        ui.update_select("variavel_h", choices={c: c for c in numericas})

    # Legenda das colunas — só aparece se o arquivo for bodyPerformance.csv
    @output
    @render.ui
    def legenda_colunas():
        f = input.arquivo_h()
        if not f:
            return ui.div()
        nome = f[0]["name"].lower().replace(" ", "").replace("-", "").replace("_", "")
        if "bodyperformance" not in nome:
            return ui.div()
        return ui.div(
            ui.tags.p("📖 Legenda das variáveis — Body Performance",
                      style="font-weight:700; font-size:0.85rem; margin-bottom:10px;"),
            ui.div(
                *[
                    ui.div(
                        ui.tags.span(col,  style="font-weight:600; font-size:0.78rem; display:block; color:#1A3D35;"),
                        ui.tags.span(desc, style="font-size:0.75rem; color:#3B5A52;"),
                        style="padding:6px 10px; border-right:0.5px solid #C2DDD7; min-width:130px;"
                    )
                    for col, desc in LEGENDA_COLUNAS.items()
                ],
                style="display:flex; flex-wrap:wrap; gap:0;"
            ),
            style="""
                background:#F0F7F5; border:1px solid #C2DDD7;
                border-left:4px solid #2E7D6B; border-radius:8px;
                padding:14px 16px; margin-bottom:16px; color:#2E5D52;
            """
        )

    # Campo de variância — aparece só no modo manual
    @output
    @render.ui
    def campo_variancia():
        if input.modo_variancia() == "manual":
            return ui.input_numeric(
                "variancia_manual",
                label=None,
                value=100.0,
                min=0.0001,
                step=0.01,
            )
        return ui.div()

    # Disclaimer dinâmico — muda conforme o modo
    @output
    @render.ui
    def disclaimer_variancia():
        df  = dados_h()
        col = input.variavel_h()
        if input.modo_variancia() == "auto":
            if df is not None and col and col in df.columns:
                var_calc = float(df[col].dropna().var())
                return ui.tags.p(
                    f"A variância é calculada automaticamente da variável selecionada "
                    f"(σ² = {var_calc:.4f}). O teste utiliza a distribuição Normal (Z), "
                    f"assumindo variância conhecida.",
                    style="font-size:0.76rem; line-height:1.4; margin:0;"
                )
            return ui.tags.p(
                "A variância será calculada automaticamente ao carregar o arquivo e "
                "selecionar a variável. O teste utiliza a distribuição Normal (Z).",
                style="font-size:0.76rem; line-height:1.4; margin:0;"
            )
        return ui.tags.p(
            "Você está informando a variância manualmente. Certifique-se de usar "
            "o valor populacional (σ²) correto. O teste utiliza a distribuição Normal (Z).",
            style="font-size:0.76rem; line-height:1.4; margin:0;"
        )

    # Resolve sigma2 conforme o modo escolhido
    def _resolve_sigma2(serie):
        if input.modo_variancia() == "auto":
            return float(serie.var())
        val = input.variancia_manual() if hasattr(input, "variancia_manual") else None
        if val is None or val <= 0:
            return float(serie.var())
        return float(val)

    # Slider de μ₀ dinâmico — ajusta ao min/max da variável selecionada
    @output
    @render.ui
    def slider_mu0():
        df  = dados_h()
        col = input.variavel_h()
        if df is None or not col or col not in df.columns:
            return ui.input_slider("mu0", label=None, min=0, max=100, value=50, step=0.5)
        serie = df[col].dropna()
        vmin  = float(round(serie.min(), 1))
        vmax  = float(round(serie.max(), 1))
        vmid  = float(round(serie.mean(), 1))
        return ui.input_slider("mu0", label=None, min=vmin, max=vmax, value=vmid, step=0.5)

    # Conteúdo principal
    @output
    @render.ui
    def conteudo_hipoteses():
        df = dados_h()
        if df is None:
            return ui.div(
                ui.div(
                    ui.tags.div("📂", class_="icon"),
                    ui.tags.p("Selecione um arquivo CSV e clique em Executar Teste."),
                    class_="msg-inicial"
                )
            )

        input.testar()

        col = input.variavel_h()
        if not col or col not in df.columns:
            return ui.div(
                ui.div(
                    ui.tags.div("↩", class_="icon"),
                    ui.tags.p("Escolha uma variável e clique em Executar Teste."),
                    class_="msg-inicial"
                )
            )

        serie       = df[col].dropna()
        n           = len(serie)
        media       = float(serie.mean())
        sigma2      = _resolve_sigma2(serie)
        sigma       = np.sqrt(sigma2)
        mu0         = float(input.mu0())
        alpha       = float(input.alpha())
        tipo        = input.tipo_teste()
        modo        = input.modo_variancia()

        # Estatística Z
        erro_padrao = sigma / np.sqrt(n)
        z_calc      = (media - mu0) / erro_padrao

        # Valor-p e região crítica
        if tipo == "bilateral":
            p_valor  = 2 * (1 - stats.norm.cdf(abs(z_calc)))
            z_crit   = stats.norm.ppf(1 - alpha / 2)
            rejeita  = abs(z_calc) > z_crit
            h1_texto = f"μ ≠ {mu0}"
            rc_texto = f"|Z| > {z_crit:.4f}"
        elif tipo == "direita":
            p_valor  = 1 - stats.norm.cdf(z_calc)
            z_crit   = stats.norm.ppf(1 - alpha)
            rejeita  = z_calc > z_crit
            h1_texto = f"μ > {mu0}"
            rc_texto = f"Z > {z_crit:.4f}"
        else:
            p_valor  = stats.norm.cdf(z_calc)
            z_crit   = stats.norm.ppf(alpha)
            rejeita  = z_calc < z_crit
            h1_texto = f"μ < {mu0}"
            rc_texto = f"Z < {z_crit:.4f}"

        decisao     = "Rejeitar H₀" if rejeita else "Não rejeitar H₀"
        cor_decisao = "#C0392B" if rejeita else "#27AE60"
        icone_dec   = "✗" if rejeita else "✓"
        origem_var  = "calculada da amostra" if modo == "auto" else "informada manualmente"

        return ui.div(
            # Info do dataset
            ui.div(
                ui.tags.span("Arquivo: "),
                ui.tags.strong(input.arquivo_h()[0]["name"]),
                ui.tags.span("  ·  "),
                ui.tags.span("Variável: "),
                ui.tags.strong(col),
                ui.tags.span("  ·  "),
                ui.tags.span("n = "),
                ui.tags.strong(str(n)),
                class_="dataset-info"
            ),

            # Hipóteses e parâmetros
            ui.div(
                ui.div(
                    ui.tags.span("HIPÓTESES", class_="vbox-label"),
                    ui.tags.p(
                        ui.tags.b("H₀: "), f"μ = {mu0}",
                        style="margin:6px 0 2px; font-size:1rem;"
                    ),
                    ui.tags.p(
                        ui.tags.b("H₁: "), h1_texto,
                        style="margin:0; font-size:1rem;"
                    ),
                    style=f"""
                        background:{COR_CARD}; border:1px solid {COR_BORDA};
                        border-left:4px solid {COR_PRIMARIA}; border-radius:10px;
                        padding:16px 18px; flex:1;
                    """
                ),
                ui.div(
                    ui.tags.span("PARÂMETROS", class_="vbox-label"),
                    ui.tags.p(
                        f"σ² = {sigma2:.4f}  |  σ = {sigma:.4f}  ({origem_var})",
                        style="margin:6px 0 2px; font-size:0.95rem;"
                    ),
                    ui.tags.p(
                        f"α = {alpha}  |  Região crítica: {rc_texto}",
                        style="margin:0; font-size:0.95rem;"
                    ),
                    style=f"""
                        background:{COR_CARD}; border:1px solid {COR_BORDA};
                        border-left:4px solid {COR_ACCENT}; border-radius:10px;
                        padding:16px 18px; flex:1;
                    """
                ),
                style="display:flex; gap:16px;"
            ),

            # Value boxes
            ui.div(
                _vbox2("Média amostral (x̄)", f"{media:.4f}",    False),
                _vbox2("Estatística Z",        f"{z_calc:.4f}",  False),
                _vbox2("Valor-p",              f"{p_valor:.4f}", False),
                class_="vbox-row"
            ),

            # Decisão em destaque
            ui.div(
                ui.tags.span(icone_dec, style=f"font-size:2rem; color:{cor_decisao}; margin-right:12px;"),
                ui.div(
                    ui.tags.span("DECISÃO DO TESTE", class_="vbox-label"),
                    ui.tags.p(
                        decisao,
                        style=f"font-size:1.3rem; font-weight:700; color:{cor_decisao}; margin:4px 0 2px;"
                    ),
                    ui.tags.p(
                        f"{'H₀ é rejeitada' if rejeita else 'Não há evidência suficiente para rejeitar H₀'} "
                        f"ao nível de significância α = {alpha}.",
                        style="font-size:0.85rem; color:#5A7A74; margin:0;"
                    ),
                ),
                style=f"""
                    background:{COR_CARD}; border:1px solid {COR_BORDA};
                    border-left:4px solid {cor_decisao}; border-radius:10px;
                    padding:18px 22px; display:flex; align-items:center;
                """
            ),

            # Gráfico
            ui.div(
                ui.div(
                    "Distribuição Normal — Região Crítica e Z calculado",
                    class_="chart-card-header"
                ),
                ui.output_plot("plot_normal"),
                class_="chart-card"
            ),
        )

    # Gráfico da curva normal
    @output
    @render.plot
    def plot_normal():
        input.testar()
        df  = dados_h()
        col = input.variavel_h()
        if df is None or not col or col not in df.columns:
            return

        serie       = df[col].dropna()
        n           = len(serie)
        media       = float(serie.mean())
        sigma2      = _resolve_sigma2(serie)
        sigma       = np.sqrt(sigma2)
        mu0         = float(input.mu0())
        alpha       = float(input.alpha())
        tipo        = input.tipo_teste()

        erro_padrao = sigma / np.sqrt(n)
        z_calc      = (media - mu0) / erro_padrao

        if tipo == "bilateral":
            z_crit = stats.norm.ppf(1 - alpha / 2)
        elif tipo == "direita":
            z_crit = stats.norm.ppf(1 - alpha)
        else:
            z_crit = stats.norm.ppf(alpha)

        x = np.linspace(-4, 4, 400)
        y = stats.norm.pdf(x)

        fig, ax = plt.subplots(figsize=(8, 3.5))
        fig.patch.set_facecolor(COR_FUNDO)
        ax.set_facecolor(COR_FUNDO)

        ax.plot(x, y, color=COR_PRIMARIA, linewidth=2)
        ax.fill_between(x, y, color=COR_PRIMARIA, alpha=0.08)

        # Região de rejeição
        if tipo == "bilateral":
            ax.fill_between(x, y, where=(x <= -z_crit), color="#C0392B", alpha=0.25, label="Região de rejeição")
            ax.fill_between(x, y, where=(x >=  z_crit), color="#C0392B", alpha=0.25)
            ax.axvline(-z_crit, color="#C0392B", linewidth=1.4, linestyle="--")
            ax.axvline( z_crit, color="#C0392B", linewidth=1.4, linestyle="--", label=f"Z crítico = ±{z_crit:.2f}")
        elif tipo == "direita":
            ax.fill_between(x, y, where=(x >= z_crit), color="#C0392B", alpha=0.25, label="Região de rejeição")
            ax.axvline(z_crit, color="#C0392B", linewidth=1.4, linestyle="--", label=f"Z crítico = {z_crit:.2f}")
        else:
            ax.fill_between(x, y, where=(x <= z_crit), color="#C0392B", alpha=0.25, label="Região de rejeição")
            ax.axvline(z_crit, color="#C0392B", linewidth=1.4, linestyle="--", label=f"Z crítico = {z_crit:.2f}")

        # Z calculado
        z_plot = max(min(z_calc, 4), -4)
        ax.axvline(z_plot, color=COR_ACCENT, linewidth=2, linestyle="-",
                   label=f"Z calc = {z_calc:.2f}")

        ax.set_xlabel("Z", fontsize=10, color=COR_TEXTO)
        ax.set_ylabel("Densidade", fontsize=10, color=COR_TEXTO)
        ax.tick_params(colors=COR_TEXTO, labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor(COR_BORDA)
        ax.legend(fontsize=9, framealpha=0.8, loc="upper right")
        fig.tight_layout(pad=1.5)
        return fig


# ── Helper ───────────────────────────────────────────────────
def _vbox2(label: str, valor: str, accent: bool):
    cls = "vbox accent" if accent else "vbox"
    return ui.div(
        ui.tags.span(label, class_="vbox-label"),
        ui.tags.span(valor, class_="vbox-value"),
        class_=cls,
    )