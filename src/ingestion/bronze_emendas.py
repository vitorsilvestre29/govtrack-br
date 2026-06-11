import sys
import pandas as pd
from transparencia import buscar_emendas

sys.path.insert(0, '../..')
from src.config import DATA_PATH

def salvar_bronze_emendas():

    emendas = buscar_emendas()
    df = pd.DataFrame(emendas)
    df.to_parquet(f"{DATA_PATH}/bronze/emendas.parquet", index=False)
    print(f"Salvo {len(df)} emendas em bronze.")

if __name__ == "__main__":
    salvar_bronze_emendas()
    print("Emendas salvas em bronze.")