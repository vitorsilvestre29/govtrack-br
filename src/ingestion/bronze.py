import pandas as pd
from deputados import buscar_deputados

def salvar_bronze():
    deputados = buscar_deputados()
    df = pd.DataFrame(deputados)
    df.to_parquet("data/bronze/deputados.parquet", index=False)
    print(f"Salvo {len(df)} deputados em bronze.")

if __name__ == "__main__":
    salvar_bronze()