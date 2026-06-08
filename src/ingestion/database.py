import psycopg2

def db_connect ():
    return psycopg2.connect(host="postgres", database="govtrack", port=5432, user="govtrack", password="govtrack123")

if __name__ == "__main__":
    conn = db_connect()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    conn.close()
    