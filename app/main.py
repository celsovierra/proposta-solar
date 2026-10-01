from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from app.core.calculos import analisar
from app.api.pvgis import buscar_irradiacao

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def form():
    return """<html><body><h2>Proposta Solar</h2><form method=post action=/gerar><input name=cliente placeholder=Cliente><br><input name=consumo placeholder=Consumo kWh><br><input name=invest placeholder=Investimento R$><br><input name=lat placeholder=Latitude value=-23.55><br><input name=lon placeholder=Longitude value=-46.63><br><button type=submit>Gerar</button></form></body></html>"""

@app.post("/gerar", response_class=HTMLResponse)
def gerar(cliente: str = Form(...), consumo: float = Form(...), invest: float = Form(...), lat: float = Form(...), lon: float = Form(...)):
    r = analisar(consumo, invest)
    pv = buscar_irradiacao(lat, lon, r["kwp"])
    html = f"<h2>{cliente}</h2><p>kWp: {r[chr(107)+chr(119)+chr(112)]}</p><p>Paineis: {r[chr(112)+chr(97)+chr(105)+chr(110)+chr(101)+chr(105)+chr(115)]}</p><p>Geracao mes: {r[chr(103)+chr(101)+chr(114)+chr(97)+chr(99)+chr(97)+chr(111)+chr(95)+chr(109)+chr(101)+chr(115)]}</p><p>Payback: {r[chr(112)+chr(97)+chr(121)+chr(98)+chr(97)+chr(99)+chr(107)]}</p>"
    if pv:
        html += f"<p>PVGIS anual: {pv[chr(103)+chr(101)+chr(114)+chr(97)+chr(99)+chr(97)+chr(111)+chr(95)+chr(97)+chr(110)+chr(117)+chr(97)+chr(108)]}</p>"
    return html
