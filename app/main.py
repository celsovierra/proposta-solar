from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from weasyprint import HTML
import shutil, os, json
from datetime import datetime, timedelta
from app.core.calculos import analisar

app = FastAPI()
os.makedirs("app/static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

CIDADES = {
    "MA": {"Sao Luis": [-2.53, -44.30], "Timon": [-5.09, -42.83], "Imperatriz": [-5.53, -47.49]},
    "PI": {"Teresina": [-5.09, -42.80], "Parnaiba": [-2.91, -41.78]},
    "SP": {"Sao Paulo": [-23.55, -46.63], "Campinas": [-22.91, -47.06]},
    "RJ": {"Rio de Janeiro": [-22.91, -43.17]},
    "MG": {"Belo Horizonte": [-19.92, -43.94]},
    "BA": {"Salvador": [-12.97, -38.50]},
    "PR": {"Curitiba": [-25.43, -49.27]},
    "SC": {"Florianopolis": [-27.60, -48.55]},
    "RS": {"Porto Alegre": [-30.03, -51.23]},
    "PE": {"Recife": [-8.05, -34.88]},
    "CE": {"Fortaleza": [-3.73, -38.52]},
    "DF": {"Brasilia": [-15.79, -47.88]},
    "GO": {"Goiania": [-16.68, -49.25]},
    "ES": {"Vitoria": [-20.32, -40.34]},
    "AM": {"Manaus": [-3.12, -60.02]},
    "PA": {"Belem": [-1.46, -48.50]},
    "RN": {"Natal": [-5.79, -35.21]},
    "MT": {"Cuiaba": [-15.60, -56.10]},
    "MS": {"Campo Grande": [-20.44, -54.65]}
}

CONFIG = {
    "logo": "",
    "casa": "app/static/img/casa.jpg",
    "painel": "app/static/img/painel.jpg",
    "inversor": "app/static/img/inversor.jpg",
    "extras": [],
    "quem_somos": "A RS SOLAR e uma empresa integradora no setor de energia solar, especializada em oferecer solucoes sustentaveis para residencias e empresas."
}

def fmt(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def carregar_config():
    global CONFIG
    try:
        with open("app/static/uploads/config.json", "r") as f:
            salvo = json.load(f)
            CONFIG.update(salvo)
    except:
        pass

def salvar_config():
    with open("app/static/uploads/config.json", "w") as f:
        json.dump(CONFIG, f)

carregar_config()

@app.get("/", response_class=HTMLResponse)
def form():
    with open("app/templates/home.html", "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    return tpl.render(usuario="CELSO", inicial="C", prox_id="601", estados=list(CIDADES.keys()), cidades_json=json.dumps(CIDADES))

@app.get("/config", response_class=HTMLResponse)
def config_page():
    carregar_config()
    with open("app/templates/config.html", "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    return tpl.render(quem_somos=CONFIG["quem_somos"], extras_json=json.dumps(CONFIG["extras"]))

@app.post("/upload")
async def upload(logo: UploadFile = File(None), casa: UploadFile = File(None), painel: UploadFile = File(None), inversor: UploadFile = File(None), extra_img: UploadFile = File(None), quem_somos: str = Form(None), img_x: str = Form(None), img_y: str = Form(None), img_pagina: str = Form(None), extra_id: str = Form(None)):
    if logo and logo.filename:
        with open("app/static/uploads/logo.png", "wb") as f:
            shutil.copyfileobj(logo.file, f)
        CONFIG["logo"] = "app/static/uploads/logo.png"
    if casa and casa.filename:
        with open("app/static/uploads/casa.png", "wb") as f:
            shutil.copyfileobj(casa.file, f)
        CONFIG["casa"] = "app/static/uploads/casa.png"
    if painel and painel.filename:
        with open("app/static/uploads/painel.png", "wb") as f:
            shutil.copyfileobj(painel.file, f)
        CONFIG["painel"] = "app/static/uploads/painel.png"
    if inversor and inversor.filename:
        with open("app/static/uploads/inversor.png", "wb") as f:
            shutil.copyfileobj(inversor.file, f)
        CONFIG["inversor"] = "app/static/uploads/inversor.png"
    if extra_img and extra_img.filename:
        idx = len(CONFIG["extras"])
        nome = f"extra_{idx}.png"
        with open(f"app/static/uploads/{nome}", "wb") as f:
            shutil.copyfileobj(extra_img.file, f)
        CONFIG["extras"].append({"src": f"app/static/uploads/{nome}", "x": int(img_x or 0), "y": int(img_y or 0), "w": 180, "h": 0})
    if quem_somos:
        CONFIG["quem_somos"] = quem_somos
    salvar_config()
    return RedirectResponse("/config", status_code=303)


@app.post("/mover_extra")
def mover_extra(indice: int = Form(...), x: int = Form(...), y: int = Form(...), w: int = Form(None), h: int = Form(None)):
    carregar_config()
    if 0 <= indice < len(CONFIG["extras"]):
        CONFIG["extras"][indice]["x"] = x
        CONFIG["extras"][indice]["y"] = y
        if w is not None:
            CONFIG["extras"][indice]["w"] = w
        if h is not None:
            CONFIG["extras"][indice]["h"] = h
        salvar_config()
    return {"ok": True}

@app.post("/excluir_extra")
def excluir_extra(indice: int = Form(...)):
    print(">>> RECEBI EXCLUSAO indice=", indice)
    carregar_config()
    if 0 <= indice < len(CONFIG["extras"]):
        item = CONFIG["extras"].pop(indice)
        try:
            os.remove(item["src"])
        except Exception as e:
            print("Erro ao remover:", e)
        salvar_config()
        print("Excluido indice", indice, "- restam", len(CONFIG["extras"]))
    return RedirectResponse("/config", status_code=303)

@app.post("/limpar_extras")
def limpar_extras():
    carregar_config()
    CONFIG["extras"] = []
    salvar_config()
    import glob
    for f in glob.glob("app/static/uploads/extra_*"):
        try: os.remove(f)
        except: pass
    return RedirectResponse("/config", status_code=303)

@app.get("/preview")
def preview():
    r = analisar(8400, 13000)
    with open("app/templates/proposta.html", "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    linhas = ""
    for l in r["fluxo"]:
        linhas += f"<tr><td>{l['ano']}</td><td>{int(l['economia']/0.95)} kWh</td><td>R$ {fmt(l['economia'])}</td><td>R$ {fmt(l['acumulado'])}</td></tr>"
    hoje = datetime.now()
    html = tpl.render(cliente="Cliente Exemplo", kwp=r["kwp"], geracao_mes=r["geracao_mes"], area=r["area"], paineis=r["paineis"], invest_fmt=fmt(13000), economia_ano=fmt(r["economia_ano"]), economia_25=fmt(r["economia_ano"]*25), payback=r["payback"], linhas=linhas, cfg=CONFIG, extras=CONFIG["extras"], validade=(hoje+timedelta(days=3)).strftime("%d/%m/%Y"), data_emissao=hoje.strftime("%d/%m/%Y"))
    pdf = HTML(string=html, base_url=os.path.abspath(".")).write_pdf()
    return Response(content=pdf, media_type="application/pdf")

@app.post("/gerar")
def gerar(cliente: str = Form(...), consumo: float = Form(...), invest: float = Form(...), uf: str = Form(...), cidade: str = Form(...)):
    if uf not in CIDADES or cidade not in CIDADES[uf]:
        return HTMLResponse(f"<h3>Cidade nao encontrada. <a href=/>Voltar</a></h3>")
    r = analisar(consumo, invest)
    with open("app/templates/proposta.html", "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    linhas = ""
    for l in r["fluxo"]:
        linhas += f"<tr><td>{l['ano']}</td><td>{int(l['economia']/0.95)} kWh</td><td>R$ {fmt(l['economia'])}</td><td>R$ {fmt(l['acumulado'])}</td></tr>"
    hoje = datetime.now()
    html = tpl.render(cliente=cliente, kwp=r["kwp"], geracao_mes=r["geracao_mes"], area=r["area"], paineis=r["paineis"], invest_fmt=fmt(invest), economia_ano=fmt(r["economia_ano"]), economia_25=fmt(r["economia_ano"]*25), payback=r["payback"], linhas=linhas, cfg=CONFIG, extras=CONFIG["extras"], validade=(hoje+timedelta(days=3)).strftime("%d/%m/%Y"), data_emissao=hoje.strftime("%d/%m/%Y"))
    pdf = HTML(string=html, base_url=os.path.abspath(".")).write_pdf()
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"inline; filename=proposta_{cliente}.pdf"})
