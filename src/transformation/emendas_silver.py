import pandas as pd
import sys

from src.config import DATA_PATH

def emendas_silver():
    df = pd.read_parquet(f"{DATA_PATH}/bronze/emendas.parquet")
    df_silver = df[["codigoEmenda", "ano", "tipoEmenda", "autor", "localidadeDoGasto", "funcao", "valorPago"]]
    df_silver['valorPago'] = df_silver['valorPago'].str.replace('.', '').str.replace(',', '.').astype(float)
    df_silver.to_parquet(f"{DATA_PATH}/silver/emendas.parquet", index=False)
    print(f"Salvo {len(df_silver)} emendas transformadas para silver.")

    print(df_silver.isnull().sum())
    print(df_silver.dtypes)
    print(df_silver.duplicated().sum())

if __name__ == "__main__":
    emendas_silver()
    print("Emendas transformadas para silver.")