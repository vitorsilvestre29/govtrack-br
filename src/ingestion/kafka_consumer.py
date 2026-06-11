import json
from kafka import KafkaConsumer
from database import db_connect

def consumir_deputados():
    consumer = KafkaConsumer('deputados',
                             bootstrap_servers='localhost:29092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             auto_offset_reset='earliest'
    )
    conn = db_connect()
    cur = conn.cursor()

    deputados = []
    for message in consumer:
        deputado = message.value
        cur.execute(
            """INSERT INTO deputados (id, nome, siglapartido, siglauf, idlegislatura, email) 
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
                (deputado['id'], deputado['nome'], deputado['siglaPartido'], deputado['siglaUf'], deputado['idLegislatura'], deputado['email'])
            )
        conn.commit()
        print(f"Inserido: {deputado['nome']}")

if __name__ == "__main__":
    consumir_deputados()
    print("Consumo de deputados finalizado.")           