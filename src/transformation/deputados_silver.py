import pandas as pd

def transformar_silver():
    df = pd.read_parquet("data/bronze/deputados.parquet")
    df_silver = df[["id", "nome", "siglaPartido", "siglaUf", "idLegislatura", "email"]]
    df_silver.to_parquet("data/silver/deputados.parquet", index=False)
    print(f"Salvo {len(df_silver)} deputados transformados para silver.")


if __name__ == "__main__":
transformar_silver()


