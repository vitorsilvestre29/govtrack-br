import json

from deputados import buscar_deputados
from kafka import KafkaProducer




def publicar_deputados(deputados):
    producer = KafkaProducer(bootstrap_servers='localhost:29092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for deputado in deputados:
        producer.send('deputados', deputado)
    producer.flush()

if __name__ == "__main__":
    deputados = buscar_deputados()
    publicar_deputados(deputados)
    print(f"Publicado {len(deputados)} deputados no Kafka.")