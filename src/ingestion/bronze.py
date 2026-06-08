import pandas as pd
from src.ingestion.deputados import buscar_deputados

def salvar_bronze():
    deputados = buscar_deputados()
    df = pd.DataFrame(deputados)
    df.to_parquet("/opt/airflow/data/bronze/deputados.parquet", index=False)
    print(f"Salvo {len(df)} deputados em bronze.")

if __name__ == "__main__":
    salvar_bronze()