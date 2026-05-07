# ToolFlow AI v6 Responsivo

Versão corrigida e melhorada:
- mantém todas as ferramentas funcionando;
- remove seções internas de negócio que o usuário não precisa ver;
- adiciona seção "Como funciona";
- mantém páginas para AdSense: Privacidade, Termos e Contato;
- contato: daniloj.dev@gmail.com;
- layout responsivo para desktop, tablet e celular;
- espaços reservados para anúncios no início e na página de resultado.

## Como rodar

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` na raiz:

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.5-flash
```

Execute:

```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Abra:

```text
http://127.0.0.1:8000
```

## Onde os anúncios entram

Existem dois blocos reservados:
- página inicial, logo após o hero;
- página de resultado, antes da resposta da IA.

Depois, esses blocos podem ser substituídos pelo código real do Google AdSense.