import requests

def buscar_emendas():
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/emendas"
    headers = {"chave-api-dados": "3ea1c266a28f917fbff20c86afd7448a"}
    todas_emendas = []
    
    for pagina in range(1, 6):
        params = {"pagina": pagina}
        resposta = requests.get(url, headers=headers, params=params)
        dados = resposta.json()
        if not dados:
            break
        todas_emendas.extend(dados)
        print(f"Página {pagina}: {len(dados)} emendas")
    
    return todas_emendas