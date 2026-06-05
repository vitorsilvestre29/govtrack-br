import requests

def buscar_deputados():
    reposta = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados?itens=513")
    dados = reposta.json()
    return dados["dados"]
