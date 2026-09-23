import psycopg2
import os

def db_connect ():
    return psycopg2.connect(host=os.getenv("DB_HOST", "localhost"), database="govtrack", port=5432, user="govtrack", password=os.environ["DB_PASSWORD"])

if __name__ == "__main__":
    conn = db_connect()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    conn.close()
    