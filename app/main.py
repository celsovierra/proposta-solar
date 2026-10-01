from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from jinja2 import Template
from weasyprint import HTML
import shutil, os
from datetime import datetime, timedelta
from app.core.calculos import analisar

app = FastAPI()
os.makedirs("app/static/uploads", exist_ok=True)

CIDADES = {
    "MA": {"Sao Luis": [-2.53, -44.30], "Timon": [-5.09, -42.83], "Imperatriz": [-5.53, -47.49], "Caxias": [-4.86, -43.35], "Bacabal": [-4.23, -44.78]},
    "PI": {"Teresina": [-5.09, -42.80], "Parnaiba": [-2.91, -41.78], "Picos": [-7.08, -41.47]},
    "SP": {"Sao Paulo": [-23.55, -46.63], "Campinas": [-22.91, -47.06], "Santos": [-23.96, -46.33], "Ribeirao Preto": [-21.18, -47.81], "Sorocaba": [-23.50, -47.46]},
    "RJ": {"Rio de Janeiro": [-22.91, -43.17], "Niteroi": [-22.88, -43.10], "Nova Iguacu": [-22.76, -43.45]},
    "MG": {"Belo Horizonte": [-19.92, -43.94], "Uberlandia": [-18.92, -48.28], "Contagem": [-19.93, -44.05]},
    "PR": {"Curitiba": [-25.43, -49.27], "Londrina": [-23.31, -51.16], "Maringa": [-23.42, -51.94]},
    "SC": {"Florianopolis": [-27.60, -48.55], "Joinville": [-26.30, -48.85], "Blumenau": [-26.92, -49.07]},
    "RS": {"Porto Alegre": [-30.03, -51.23], "Caxias do Sul": [-29.17, -51.18], "Pelotas": [-31.77, -52.34]},
    "BA": {"Salvador": [-12.97, -38.50], "Feira de Santana": [-12.27, -38.97], "Vitoria da Conquista": [-14.85, -40.84]},
    "PE": {"Recife": [-8.05, -34.88], "Olinda": [-8.01, -34.85]},
    "CE": {"Fortaleza": [-3.73, -38.52], "Caucaia": [-3.73, -38.66], "Juazeiro do Norte": [-7.21, -39.31]},
    "DF": {"Brasilia": [-15.79, -47.88]},
    "GO": {"Goiania": [-16.68, -49.25], "Anapolis": [-16.33, -48.95]},
    "MT": {"Cuiaba": [-15.60, -56.10], "Varzea Grande": [-15.65, -56.13]},
    "MS": {"Campo Grande": [-20.44, -54.65], "Dourados": [-22.22, -54.81]},
    "ES": {"Vitoria": [-20.32, -40.34], "Vila Velha": [-20.33, -40.29]},
    "AM": {"Manaus": [-3.12, -60.02]},
    "PA": {"Belem": [-1.46, -48.50], "Ananindeua": [-1.37, -48.37]},
    "RN": {"Natal": [-5.79, -35.21], "Mossoro": [-5.19, -37.34]},
    "PB": {"Joao Pessoa": [-7.12, -34.86], "Campina Grande": [-7.23, -35.88]},
    "AL": {"Maceio": [-9.66, -35.73]},
    "SE": {"Aracaju": [-10.91, -37.07]},
    "TO": {"Palmas": [-10.17, -48.33], "Araguaina": [-7.19, -48.21]},
    "RO": {"Porto Velho": [-8.76, -63.90]},
    "AC": {"Rio Branco": [-9.97, -67.81]},
    "AP": {"Macapa": [0.03, -51.07]},
    "RR": {"Boa Vista": [2.82, -60.67]}
}

CONFIG = {
    "logo": "/static/img/logo.png",
    "casa": "/static/img/casa.jpg",
    "painel": "/static/img/painel.jpg",
    "inversor": "/static/img/inversor.jpg",
    "quem_somos": "A RS SOLAR e uma empresa integradora no setor de energia solar, especializada em oferecer solucoes sustentaveis para residencias e empresas. Nosso compromisso e promover a utilizacao de energias renovaveis, contribuindo para a preservacao do meio ambiente e a reducao de custos com energia eletrica."
}

def fmt(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.get("/", response_class=HTMLResponse)
def form():
    with open("app/templates/home.html", "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    import json
    return tpl.render(usuario="CELSO", inicial="C", prox_id="601", estados=list(CIDADES.keys()), cidades_json=json.dumps(CIDADES))

@app.get("/config", response_class=HTMLResponse)
def config_page():
    html = """<!DOCTYPE html>
<html><head><meta charset=UTF-8><title>Configuracoes</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:Arial,sans-serif}
body{background:#f5f7fa;min-height:100vh}
.header{background:#fff;border-bottom:1px solid #e5e7eb;padding:14px 32px;display:flex;align-items:center;justify-content:space-between}
.logo{font-weight:700;color:#1a3a5c;font-size:16px}
.user-area{display:flex;align-items:center;gap:18px;font-size:13px;color:#4b5563}
.user-area a{color:#4b5563;text-decoration:none}
.user-avatar{width:32px;height:32px;border-radius:50%;background:#e5e7eb;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600}
.btn-logout{border:1px solid #d1d5db;background:#fff;padding:6px 14px;border-radius:6px;font-size:13px;cursor:pointer}
.container{display:flex;justify-content:center;padding:50px 20px}
.card{background:#fff;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.08);width:100%;max-width:640px;padding:32px}
.card h2{font-size:22px;color:#111827;margin-bottom:6px}
.card .sub{font-size:13px;color:#6b7280;margin-bottom:24px}
label{display:block;font-size:11px;font-weight:600;color:#374151;letter-spacing:0.5px;margin-bottom:6px;margin-top:16px}
input[type=file]{width:100%;padding:10px 14px;border:1px dashed #d1d5db;border-radius:8px;font-size:13px;background:#fafbfc}
textarea{width:100%;padding:11px 14px;border:1px solid #d1d5db;border-radius:8px;font-size:13px;font-family:Arial;outline:none;resize:vertical}
textarea:focus{border-color:#2d6a9f;box-shadow:0 0 0 3px rgba(45,106,159,0.1)}
.btn-salvar{width:100%;background:#1f4e3d;color:#fff;border:none;padding:14px;border-radius:8px;font-size:14px;font-weight:600;margin-top:24px;cursor:pointer}
.btn-salvar:hover{background:#163a2e}
.btn-voltar{display:inline-block;margin-top:16px;color:#4b5563;text-decoration:none;font-size:13px}
</style></head><body>
<div class=header><div class=logo>PROPOSTA SOLAR</div>
<div class=user-area><div class=user-avatar>C</div><span>CELSO</span><a href=/>Voltar ao inicio</a><button class=btn-logout>Logout</button></div></div>
<div class=container><div class=card>
<h2>Configuracoes</h2><p class=sub>Personalize as imagens e textos da proposta</p>
<form method=post action=/upload enctype=multipart/form-data>
<label>LOGO DA EMPRESA</label><input type=file name=logo accept=image/*>
<label>IMAGEM DA CASA (capa e beneficios)</label><input type=file name=casa accept=image/*>
<label>IMAGEM DO PAINEL SOLAR</label><input type=file name=painel accept=image/*>
<label>IMAGEM DO INVERSOR</label><input type=file name=inversor accept=image/*>
<label>TEXTO QUEM SOMOS</label><textarea name=quem_somos rows=5>""" + CONFIG["quem_somos"] + """</textarea>
<button class=btn-salvar type=submit>Salvar Configuracoes</button>
</form>
<a href=/ class=btn-voltar>&larr; Voltar ao inicio</a>
</div></div></body></html>"""
    return html

@app.post("/upload")
async def upload(logo: UploadFile = File(None), casa: UploadFile = File(None), painel: UploadFile = File(None), inversor: UploadFile = File(None), quem_somos: str = Form(None)):
    for campo, arq in [("logo", logo), ("casa", casa), ("painel", painel), ("inversor", inversor)]:
        if arq and arq.filename:
            with open(f"app/static/uploads/{campo}.png", "wb") as f:
                shutil.copyfileobj(arq.file, f)
            CONFIG[campo] = f"/static/uploads/{campo}.png"
    if quem_somos:
        CONFIG["quem_somos"] = quem_somos
    return RedirectResponse("/config", status_code=303)

@app.post("/gerar")
def gerar(cliente: str = Form(...), consumo: float = Form(...), invest: float = Form(...), uf: str = Form(...), cidade: str = Form(...)):
    coords = CIDADES.get(uf, {}).get(cidade)
    if not coords:
        disponiveis = ", ".join(CIDADES.get(uf, {}).keys())
        return HTMLResponse(f"<h3>Cidade '{cidade}' nao encontrada em {uf}.</h3><p>Cidades disponiveis: {disponiveis}</p><a href=/>Voltar</a>")
    r = analisar(consumo, invest)
    with open("app/templates/proposta.html", "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    linhas = ""
    for l in r["fluxo"]:
        linhas += f"<tr><td>{l['ano']}</td><td>{int(l['economia']/0.95)} kWh</td><td>R$ {fmt(l['economia'])}</td><td>R$ {fmt(l['acumulado'])}</td></tr>"
    hoje = datetime.now()
    html = tpl.render(
        cliente=cliente, kwp=r["kwp"], geracao_mes=r["geracao_mes"], area=r["area"],
        paineis=r["paineis"], invest_fmt=fmt(invest), economia_ano=fmt(r["economia_ano"]),
        economia_25=fmt(r["economia_ano"]*25), payback=r["payback"], linhas=linhas, cfg=CONFIG,
        validade=(hoje+timedelta(days=3)).strftime("%d/%m/%Y"),
        data_emissao=hoje.strftime("%d/%m/%Y")
    )
    pdf = HTML(string=html, base_url=".").write_pdf()
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"inline; filename=proposta_{cliente}.pdf"})
