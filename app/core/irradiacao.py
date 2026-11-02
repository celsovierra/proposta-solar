import json
from app.api.pvgis import buscar_irradiacao

PADRAO = 141.7
CACHE = "app/core/irr_cache.json"

def obter_irradiacao(lat, lon):
    chave = str(round(lat, 2)) + "," + str(round(lon, 2))
    try:
        cache = json.load(open(CACHE, encoding="utf-8"))
    except Exception:
        cache = {}
    if chave in cache:
        return cache[chave], "cache"
    try:
        r = buscar_irradiacao(lat, lon, 1)
        if r:
            irr = round(r["geracao_anual"] / 12, 2)
            cache[chave] = irr
            json.dump(cache, open(CACHE, "w", encoding="utf-8"))
            return irr, "pvgis"
    except Exception as e:
        print("PVGIS falhou:", e)
    return PADRAO, "padrao"
