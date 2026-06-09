import requests

def buscar_emendas():
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/emendas"
    headers = {"chave-api-dados": "3ea1c266a28f917fbff20c86afd7448a"}
    params = {"pagina": 1}
    resposta = requests.get(url, headers=headers, params=params)
    print(resposta.status_code)
    return resposta.json()

if __name__ == "__main__":
    emendas = buscar_emendas()
    print(emendas)