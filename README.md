# ToolFlow AI - versão com AdSense e melhorias

Projeto FastAPI com ferramentas de IA para currículo, textos e LinkedIn.

## Inclui
- Google Analytics instalado: `G-HB5PH8V46W`
- Google AdSense instalado: `ca-pub-5160731650313944`
- Espaços de anúncio na home e na página de resultado
- Página Sobre
- Política de Privacidade, Termos e Contato
- `/ads.txt`, `/robots.txt` e `/sitemap.xml`
- Melhorias de SEO e responsividade
- Favicon SVG
- Loading nos botões

## Rodar localmente

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env`:

```env
GEMINI_API_KEY=sua_chave
GEMINI_MODEL=gemini-2.0-flash
```

Execute:

```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Deploy no Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port $PORT
```

Variáveis de ambiente no Render:

```env
GEMINI_API_KEY=sua_chave
GEMINI_MODEL=gemini-2.0-flash
```


## Atualização final

- Loading premium com barra de progresso
- Mensagens específicas por ferramenta
- Overlay responsivo para desktop e mobile
- Botões com estado de processamento
- Mantém Analytics, AdSense e páginas obrigatórias
