import requests

def buscar_irradiacao(lat, lon, potencia_kwp=5, perda=14):
    url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc"
    params = {"lat": lat, "lon": lon, "peakpower": potencia_kwp, "loss": perda, "outputformat": "json"}
    r = requests.get(url, params=params, timeout=20)
    if r.status_code != 200:
        return None
    d = r.json()
    return {"geracao_anual": d["outputs"]["totals"]["fixed"]["E_y"], "geracao_mensal": d["outputs"]["totals"]["fixed"]["E_m"]}

if __name__ == "__main__":
    r = buscar_irradiacao(-23.55, -46.63, 5)
    print("Geracao anual kWh:", r["geracao_anual"])
    print("Geracao mensal kWh:", r["geracao_mensal"])
