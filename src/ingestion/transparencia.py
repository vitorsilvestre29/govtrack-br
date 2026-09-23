import os
import requests

def buscar_emendas():
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/emendas"
    headers = {"chave-api-dados": os.environ["PORTAL_TRANSPARENCIA_API_KEY"]}
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