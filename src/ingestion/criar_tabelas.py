import psycopg2
from database import db_connect


sql = """
CREATE TABLE IF NOT EXISTS DEPUTADOS (
    id  INTEGER PRIMARY KEY,
    nome VARCHAR(255),
    siglaPartido VARCHAR(255),
    siglaUf VARCHAR(255),
    idLegislatura INTEGER,
    email VARCHAR(255)
);
"""
def criar_tabelas():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print("Tabela DEPUTADOS criada com sucesso!")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()    