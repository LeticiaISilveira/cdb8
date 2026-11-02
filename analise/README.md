# Análise de comentários do YouTube

Esta pasta contém a primeira versão do dashboard em Streamlit e o coletor de comentários. O dashboard preserva a paleta, as fontes e os elementos Rococó de `index.html` e `mockup-dashboard.html`.

Os gráficos de sentimento e temas são demonstrativos nesta versão. O CSV coletado contém comentários brutos; ainda não há classificação de sentimento ou agrupamento temático.

## Preparar o ambiente

Na raiz do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r analise/requirements.txt
```

## Coletar comentários

Defina uma chave da YouTube Data API no ambiente; não a salve no código ou em arquivos versionados:

```bash
export YOUTUBE_API_KEY="sua-chave"
python analise/collect_youtube_comments.py
```

O coletor usa o vídeo `9LIJHRkvOo4` por padrão e grava `analise/youtube_comments.csv`. Para selecionar outro vídeo ou destino:

```bash
python analise/collect_youtube_comments.py --video-id ID_DO_VIDEO --output analise/youtube_comments.csv
```

## Abrir o dashboard

```bash
streamlit run analise/app.py
```

Se `analise/youtube_comments.csv` existir, o dashboard informa a quantidade de comentários e permite visualizar uma prévia dos dados brutos. A classificação de sentimentos e a análise dos temas ficam para a próxima versão.
