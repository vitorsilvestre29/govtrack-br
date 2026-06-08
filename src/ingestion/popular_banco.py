import pandas as pd
from src.ingestion.database import db_connect

def popular_banco():
    df = pd.read_parquet("data/silver/deputados.parquet")
    conn = db_connect()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO deputados (id, nome, siglaPartido, siglaUf, idLegislatura, email)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
""", (row['id'], row['nome'], row['siglaPartido'], row['siglaUf'], row['idLegislatura'], row['email']))
    conn.commit()
    print(f"Populado banco com {len(df)} deputados.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    popular_banco()

