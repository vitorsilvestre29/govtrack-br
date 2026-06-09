import pandas as pd
import sys

from src.config import DATA_PATH

def emendas_gold():
    df = pd.read_parquet(f"{DATA_PATH}/silver/emendas.parquet")
    df_gold = df.groupby(['ano', 'tipoEmenda', 'localidadeDoGasto']).agg({'valorPago': 'sum'}).reset_index()
    df_gold.to_parquet(f"{DATA_PATH}/gold/emendas.parquet", index=False)
    print(f"Salvo {len(df_gold)} emendas transformadas para gold.")

    print(df_gold.isnull().sum())
    print(df_gold.dtypes)
    print(df_gold.duplicated().sum())

if __name__ == "__main__":
    emendas_gold()
    print("Emendas transformadas para gold.")