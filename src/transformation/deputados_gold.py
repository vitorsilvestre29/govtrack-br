import pandas as pd

def transformar_gold():
    df = pd.read_parquet("data/silver/deputados.parquet")
    df = df.groupby("siglaPartido").size().reset_index(name="total_deputados")
    df.to_parquet("data/gold/deputados_por_partido.parquet", index=False)
    print(f"Salvo deputados por partido em gold.")

if __name__ == "__main__":
    transformar_gold()