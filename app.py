from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from dotenv import load_dotenv
import os
import fitz

load_dotenv()
app = FastAPI(title="ToolFlow AI", version="6.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
api_key = os.getenv("GEMINI_API_KEY", "").strip()
gemini_model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
if api_key:
    genai.configure(api_key=api_key)
model = genai.GenerativeModel(gemini_model_name)

def generate_ai_response(prompt: str) -> str:
    if not api_key:
        return "Erro: GEMINI_API_KEY não encontrada. Crie o arquivo .env na raiz do projeto."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as error:
        return (
            "Não foi possível gerar a resposta da IA.\\n\\n"
            f"Modelo atual: {gemini_model_name}\\n"
            f"Erro técnico: {error}\\n\\n"
            "No arquivo .env, teste GEMINI_MODEL=gemini-2.5-flash ou GEMINI_MODEL=gemini-2.0-flash."
        )

def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        return "\\n".join(page.get_text() for page in doc).strip()
    except Exception:
        return ""

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"page_title": "ToolFlow AI"})
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html")

@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    return templates.TemplateResponse(request, "privacy.html")
@app.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    return templates.TemplateResponse(request, "terms.html")
@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html")
@app.post("/ats-checker", response_class=HTMLResponse)
async def ats_checker(request: Request, file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_pdf_text(pdf_bytes)
    if not text:
        result = "Não consegui extrair texto desse PDF. Teste com um PDF que tenha texto selecionável."
    else:
        prompt = f"""
Você é especialista em recrutamento, ATS e currículo profissional.
Analise o currículo abaixo em português brasileiro.
Entregue:
1. Nota ATS de 0 a 100
2. Diagnóstico geral
3. Pontos fortes
4. Problemas que podem prejudicar no ATS
5. Palavras-chave faltando
6. Melhorias práticas
7. Versão melhorada do resumo profissional
8. Próximos passos
Currículo:
{text}
"""
        result = generate_ai_response(prompt)
    return templates.TemplateResponse(request, "result.html", {"title": "Resultado da Análise ATS", "result": result})
@app.post("/humanizer", response_class=HTMLResponse)
async def humanizer(request: Request, text: str = Form(...)):
    prompt = f"""
Reescreva o texto abaixo de forma mais humana, natural e profissional.
Preserve o sentido original, remova aparência robótica e use português brasileiro claro.
Texto:
{text}
"""
    result = generate_ai_response(prompt)
    return templates.TemplateResponse(request, "result.html", {"title": "Texto Humanizado", "result": result})
@app.post("/ai-detector", response_class=HTMLResponse)
async def ai_detector(request: Request, text: str = Form(...)):
    prompt = f"""
Analise o texto abaixo e indique se ele parece ter sido escrito por IA.
Não diga que é uma certeza. Dê uma estimativa qualitativa e sugestões de melhoria.
Estrutura:
1. Probabilidade aparente: baixa, média ou alta
2. Justificativa
3. Padrões suspeitos
4. Recomendações
Texto:
{text}
"""
    result = generate_ai_response(prompt)
    return templates.TemplateResponse(request, "result.html", {"title": "Análise de Texto IA", "result": result})
@app.post("/linkedin-generator", response_class=HTMLResponse)
async def linkedin_generator(request: Request, role: str = Form(...), experience: str = Form(...), goal: str = Form(...)):
    prompt = f"""
Crie uma seção 'Sobre' para LinkedIn em português brasileiro.
Cargo/área: {role}
Experiência: {experience}
Objetivo profissional: {goal}
Regras:
- Tom profissional e humano
- Boa para recrutadores
- Máximo 4 parágrafos
- Inclua palavras-chave relevantes
"""
    result = generate_ai_response(prompt)
    return templates.TemplateResponse(request, "result.html", {"title": "Perfil LinkedIn Gerado", "result": result})

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /\nSitemap: https://toolflow-ai.onrender.com/sitemap.xml\n"

@app.get("/ads.txt", response_class=PlainTextResponse)
async def ads_txt():
    return "google.com, pub-5160731650313944, DIRECT, f08c47fec0942fa0\n"

@app.get("/sitemap.xml")
async def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://toolflow-ai.onrender.com/</loc><priority>1.0</priority></url>
  <url><loc>https://toolflow-ai.onrender.com/about</loc><priority>0.7</priority></url>
  <url><loc>https://toolflow-ai.onrender.com/privacy</loc><priority>0.5</priority></url>
  <url><loc>https://toolflow-ai.onrender.com/terms</loc><priority>0.5</priority></url>
  <url><loc>https://toolflow-ai.onrender.com/contact</loc><priority>0.5</priority></url>
</urlset>"""
    return Response(content=xml, media_type="application/xml")
