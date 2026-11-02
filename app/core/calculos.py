from datetime import datetime

IRRADIACAO = 141.7
AREA_KWP = 4.19
TARIFA = 0.952
REAJUSTE = 0.10

def potencia(consumo, irr=IRRADIACAO):
    return round(consumo / (irr * 12), 2)

def geracao_mensal(kwp, irr=IRRADIACAO):
    return round(kwp * irr, 2)

def area(kwp):
    return round(kwp * AREA_KWP, 2)

def payback(invest, economia):
    return round(invest / economia, 1)

def fluxo(invest, geracao):
    tarifa = TARIFA
    acumulado = -invest
    lista = []
    for i in range(1, 11):
        economia = round(geracao * tarifa, 2)
        acumulado = round(acumulado + economia, 2)
        lista.append({"ano": datetime.now().year + i, "economia": economia, "acumulado": acumulado})
        tarifa = round(tarifa * (1 + REAJUSTE), 3)
    return lista

def analisar(consumo, invest, irr=IRRADIACAO):
    kwp = potencia(consumo, irr)
    paineis = int((kwp * 1000) / 620) + 1
    kwp = round((paineis * 620) / 1000, 2)
    ger = geracao_mensal(kwp, irr)
    ger_ano = round(ger * 12)
    econ = round(ger_ano * TARIFA, 2)
    return {"kwp": kwp, "paineis": paineis, "geracao_mes": ger, "geracao_ano": ger_ano, "area": area(kwp), "economia_ano": econ, "payback": payback(invest, econ), "fluxo": fluxo(invest, ger_ano)}

if __name__ == "__main__":
    r = analisar(8520, 13000)
    print("kWp:", r["kwp"], "| Geracao mes:", r["geracao_mes"], "| Payback:", r["payback"])
