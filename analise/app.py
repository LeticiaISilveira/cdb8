from pathlib import Path

import pandas as pd
import streamlit as st


ANALYSIS_DIR = Path(__file__).resolve().parent
DATA_FILES = (
    ANALYSIS_DIR / "youtube_comments.csv",
    ANALYSIS_DIR.parent / "youtube_comments.csv",
)

st.set_page_config(
    page_title="Dashboard de Sentimentos · Rococó",
    page_icon="❧",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Poiret+One&family=Sora:wght@400;500;600;700&display=swap');

    :root {
      --rose: #B2627D;
      --rose-pale: #E5C3CE;
      --sage: #d1e5c3;
      --leaf: #84B262;
      --gold: #BFA360;
      --gold-highlight: #CCA752;
      --ink: #593f45;
      --muted: #75676a;
      --paper: #fffaf3;
    }

    html, body, [class*="css"] {
      font-family: "Sora", sans-serif;
      color: #33443d;
    }

    [data-testid="stAppViewContainer"] {
      background:
        radial-gradient(ellipse at 10% 12%, rgb(178 98 125 / 12%), transparent 32%),
        radial-gradient(ellipse at 90% 85%, rgb(132 178 98 / 15%), transparent 34%),
        radial-gradient(ellipse at center, transparent 48%, rgb(119 81 53 / 16%) 100%),
        linear-gradient(135deg, #F2E7EB, #EFF4EB);
    }

    [data-testid="stHeader"] {
      background: transparent;
    }

    .block-container {
      max-width: 1440px;
      padding: 2rem clamp(1rem, 3vw, 2.5rem) 3rem;
    }

    h1, .rococo-title {
      color: var(--ink) !important;
      font-family: "Poiret One", sans-serif !important;
      font-weight: 400 !important;
      letter-spacing: -0.035em;
    }

    h2, h3, .card-title {
      color: var(--ink) !important;
      font-family: "Fraunces", serif !important;
      font-weight: 600 !important;
    }

    p, label, [data-testid="stMarkdownContainer"] {
      font-family: "Sora", sans-serif;
    }

    .rococo-shell {
      position: relative;
      margin: 0 0 1.2rem;
      padding: clamp(1.3rem, 3vw, 2.4rem);
      border: 1px solid #c9ad76;
      border-radius: 30px;
      background:
        radial-gradient(ellipse at 50% 0, rgb(255 255 255 / 90%), transparent 68%),
        linear-gradient(145deg, #fffdfa, #fff9f5 55%, #f8f6ec);
      box-shadow:
        0 20px 55px rgb(83 55 54 / 14%),
        inset 0 0 0 5px rgb(255 255 255 / 75%),
        inset 0 0 0 6px rgb(191 163 96 / 25%);
    }

    .eyebrow {
      margin: 0 0 .45rem;
      color: #98614f;
      font-size: .68rem;
      font-weight: 700;
      letter-spacing: .18em;
      text-transform: uppercase;
    }

    .rococo-title {
      margin: 0;
      font-size: clamp(2.4rem, 5vw, 4rem);
      line-height: 1.05;
    }

    .subtitle {
      max-width: 68ch;
      margin: .55rem 0 0;
      color: var(--muted);
      font-size: .88rem;
      line-height: 1.7;
    }

    .ornament {
      display: flex;
      align-items: center;
      gap: .9rem;
      margin: 1.4rem 0;
      color: var(--gold);
      font-family: "Fraunces", serif;
      font-size: 1.2rem;
      line-height: 1;
    }

    .ornament::before, .ornament::after {
      height: 1px;
      flex: 1;
      background: linear-gradient(90deg, transparent, rgb(178 139 77 / 65%), transparent);
      content: "";
    }

    .source-link {
      display: inline-block;
      margin-top: 1rem;
      padding: .62rem 1rem;
      border: 1px solid rgb(191 163 96 / 65%);
      border-radius: 999px;
      background: rgb(255 255 255 / 65%);
      color: #98614f !important;
      font-size: .75rem;
      font-weight: 600;
      text-decoration: none;
    }

    .source-link:hover {
      background: white;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
      border: 1px solid #b98c43 !important;
      border-radius: 20px !important;
      background:
        linear-gradient(145deg, #d1e5c3, #fff 78%) !important;
      box-shadow:
        inset 0 0 0 4px #fff9eb,
        inset 0 0 0 5px rgb(191 163 96 / 45%),
        0 8px 22px rgb(83 55 54 / 9%) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] > div {
      padding: 1rem !important;
    }

    .card-heading {
      margin: 0 0 .2rem;
      color: var(--ink);
      font-family: "Fraunces", serif;
      font-size: 1.18rem;
      font-weight: 600;
    }

    .card-caption, .demo-note {
      margin: 0 0 .8rem;
      color: var(--muted);
      font-size: .72rem;
      line-height: 1.5;
    }

    .demo-note {
      color: #98614f;
      font-weight: 600;
    }

    .bar-list {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: .85rem 2rem;
      padding: .25rem 0;
    }

    .bar-row {
      display: grid;
      grid-template-columns: minmax(100px, .75fr) 2fr 38px;
      align-items: center;
      gap: .65rem;
      color: #69585a;
      font-size: .72rem;
    }

    .bar-track {
      height: 12px;
      overflow: hidden;
      border: 1px solid rgb(169 119 43 / 20%);
      border-radius: 999px;
      background: #f8f6ec;
    }

    .bar-fill {
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, var(--rose), var(--rose-pale));
    }

    .bar-row:nth-child(even) .bar-fill {
      background: linear-gradient(90deg, var(--leaf), var(--sage));
    }

    .bar-row strong {
      color: #98614f;
      font-size: .68rem;
      text-align: right;
    }

    .pie-layout {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1.3rem;
      min-height: 210px;
    }

    .pie-chart {
      width: 148px;
      aspect-ratio: 1;
      flex: 0 0 auto;
      border: 5px solid var(--paper);
      border-radius: 50%;
      background: conic-gradient(
        var(--rose) 0 40%,
        var(--leaf) 40% 65%,
        var(--gold) 65% 85%,
        var(--rose-pale) 85% 100%
      );
      box-shadow: 0 0 0 1px #c9ad76;
    }

    .legend {
      display: grid;
      gap: .65rem;
      color: #69585a;
      font-size: .7rem;
    }

    .legend-row {
      display: grid;
      grid-template-columns: 9px auto auto;
      align-items: center;
      gap: .45rem;
    }

    .legend-row strong {
      color: #98614f;
    }

    .legend-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--dot);
    }

    .stacked-track {
      display: flex;
      height: 20px;
      overflow: hidden;
      margin: 1rem 0;
      border: 1px solid rgb(169 119 43 / 35%);
      border-radius: 999px;
      background: var(--paper);
    }

    .stacked-track span:nth-child(1) { width: 62%; background: var(--rose); }
    .stacked-track span:nth-child(2) { width: 24%; background: var(--gold); }
    .stacked-track span:nth-child(3) { width: 14%; background: var(--leaf); }

    .sentiment-legend {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: .5rem;
      color: #69585a;
      font-size: .7rem;
    }

    .sentiment-legend strong {
      color: var(--ink);
    }

    .small-footnote {
      margin: 1rem 0 0;
      color: #75676a;
      font-size: .68rem;
      text-align: center;
    }

    @media (max-width: 760px) {
      .bar-list { grid-template-columns: 1fr; }
    }

    @media (max-width: 560px) {
      .rococo-shell { padding: 1.3rem; }
      .pie-layout { flex-direction: column; padding: 1rem 0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_comments() -> tuple[pd.DataFrame | None, Path | None]:
    csv_path = next((path for path in DATA_FILES if path.exists()), None)
    if csv_path is None:
        return None, None
    return pd.read_csv(csv_path, encoding="utf-8-sig"), csv_path


def render_heading(title: str, caption: str, note: str | None = None) -> None:
    st.markdown(f'<h2 class="card-heading">{title}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="card-caption">{caption}</p>', unsafe_allow_html=True)
    if note:
        st.markdown(f'<p class="demo-note">{note}</p>', unsafe_allow_html=True)


def render_competitor_bars() -> None:
    competitors = [
        ("Competidor A", 72),
        ("Competidor B", 64),
        ("Competidor C", 58),
        ("Competidor D", 48),
        ("Competidor E", 35),
        ("Competidor F", 22),
    ]
    rows = "".join(
        f'<div class="bar-row"><span>{name}</span>'
        f'<div class="bar-track"><div class="bar-fill" style="width: {score}%"></div></div>'
        f"<strong>{score}%</strong></div>"
        for name, score in competitors
    )
    st.markdown(
        f'<div class="bar-list" role="img" aria-label="Percentual ilustrativo de sentimento positivo por competidor">{rows}</div>',
        unsafe_allow_html=True,
    )


def render_signs_pie() -> None:
    signs = [
        ("Sagitário", 40, "#B2627D"),
        ("Leão", 25, "#84B262"),
        ("Libra", 20, "#BFA360"),
        ("Peixes", 15, "#E5C3CE"),
    ]
    legend = "".join(
        f'<div class="legend-row"><span class="legend-dot" style="--dot: {color}"></span>'
        f"<span>{sign}</span><strong>{value}%</strong></div>"
        for sign, value, color in signs
    )
    st.markdown(
        '<div class="pie-layout">'
        '<div class="pie-chart" role="img" aria-label="Gráfico de pizza plano: Sagitário 40%, Leão 25%, Libra 20%, Peixes 15%"></div>'
        f'<div class="legend">{legend}</div></div>',
        unsafe_allow_html=True,
    )


def render_topics() -> None:
    topics = [
        ("Provas", 42),
        ("Alianças", 68),
        ("Convivência", 51),
        ("Eliminações", 78),
    ]
    rows = "".join(
        f'<div class="bar-row"><span>{topic}</span>'
        f'<div class="bar-track"><div class="bar-fill" style="width: {volume}%"></div></div>'
        f"<strong>{volume}</strong></div>"
        for topic, volume in topics
    )
    st.markdown(
        f'<div class="bar-list" role="img" aria-label="Volume ilustrativo de menções por tema">{rows}</div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    comments, csv_path = load_comments()
    st.markdown(
        """
        <section class="rococo-shell">
          <p class="eyebrow">Design system · Rococó</p>
          <h1 class="rococo-title">Dashboard de Sentimentos</h1>
          <p class="subtitle">Uma leitura dos comentários do YouTube para acompanhar a percepção do público sobre os competidores do reality.</p>
          <a class="source-link" href="https://www.youtube.com/watch?v=9LIJHRkvOo4" target="_blank" rel="noopener noreferrer">✦ &nbsp; Comentários do YouTube</a>
          <div class="ornament" aria-hidden="true">❧</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if comments is None:
        st.info("Versão 1 visual: os gráficos abaixo usam valores ilustrativos. Para carregar comentários, gere `analise/youtube_comments.csv` com o coletor.")
    else:
        st.success(f"CSV encontrado em `{csv_path}` · {len(comments):,} comentários brutos carregados. A análise de sentimentos ainda não foi aplicada.")

    st.markdown('<p class="eyebrow">Painel · dados demonstrativos</p>', unsafe_allow_html=True)
    with st.container(border=True):
        render_heading(
            "Sentimento positivo por competidor",
            "Percentual ilustrativo de comentários positivos identificados",
            "Valores de demonstração — não representam análise real.",
        )
        render_competitor_bars()

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            render_heading(
                "Sentimento por episódio",
                "Exemplo de evolução do sentimento positivo · escala de 0 a 100",
                "Dados ilustrativos",
            )
            timeline = pd.DataFrame(
                {"Índice positivo": [42, 51, 48, 63, 72, 68]},
                index=["Ep. 1", "Ep. 2", "Ep. 3", "Ep. 4", "Ep. 5", "Ep. 6"],
            )
            st.line_chart(timeline, color="#B2627D")

    with right:
        with st.container(border=True):
            render_heading(
                "Signos do zodíaco",
                "Signos dos comentadores · informação coletada separadamente",
            )
            render_signs_pie()

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            render_heading(
                "Temas mais mencionados",
                "Volume relativo de comentários por assunto",
                "Valores ilustrativos",
            )
            render_topics()

    with right:
        with st.container(border=True):
            render_heading(
                "Sentimento geral",
                "Polaridade estimada dos comentários analisados",
                "Distribuição ilustrativa",
            )
            st.markdown(
                '<div class="stacked-track" role="img" aria-label="62% positivo, 24% neutro e 14% negativo">'
                "<span></span><span></span><span></span></div>"
                '<div class="sentiment-legend">'
                "<span>Positivo <strong>62%</strong></span>"
                "<span>Neutro <strong>24%</strong></span>"
                "<span>Negativo <strong>14%</strong></span></div>",
                unsafe_allow_html=True,
            )

    if comments is not None:
        with st.expander("Prévia dos comentários coletados"):
            st.dataframe(comments.head(20), hide_index=True, use_container_width=True)

    st.markdown(
        '<p class="small-footnote">❧ &nbsp; Valores de demonstração até a implementação da análise dos comentários &nbsp; ❧</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
