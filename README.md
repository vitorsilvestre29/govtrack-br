# GovTrack BR

Pipeline de dados que reúne e processa informações públicas do governo federal brasileiro, unindo dados de deputados federais e emendas parlamentares numa arquitetura moderna de Data Lakehouse.

## Dashboard

![GovTrack BR Dashboard](docs/dashboard.png)

## Fontes de dados

- **Câmara dos Deputados** — API REST com dados de todos os deputados federais
- **Portal da Transparência** — API com emendas parlamentares e gastos públicos

## Stack

| Tecnologia | Função |
|---|---|
| Python | Ingestão e transformação de dados |
| Apache Airflow | Orquestração do pipeline |
| Apache Kafka | Streaming de dados em tempo real |
| PostgreSQL | Armazenamento relacional |
| dbt | Transformações SQL com linhagem e testes de qualidade |
| Apache Superset | Dashboard interativo |
| Docker | Containerização de toda a infraestrutura |
| GitHub Actions | CI/CD automatizado |
| Pandas + PyArrow | Processamento e formato Parquet |

## Arquitetura Medallion

- **Bronze** — dados brutos das APIs em Parquet
- **Silver** — dados limpos e normalizados
- **Gold** — agregações prontas para consumo

## Streaming com Kafka

Os deputados federais são publicados em tempo real no topic `deputados` via Producer e consumidos pelo Consumer que insere diretamente no PostgreSQL.

```bash
# Publicar deputados no Kafka
python3 src/ingestion/kafka_producer.py

# Consumir e inserir no banco
python3 src/ingestion/kafka_consumer.py
```

## CI/CD

Cada push na branch `main` dispara automaticamente o GitHub Actions que roda `dbt seed`, `dbt run` e `dbt test`. Se algum teste falhar o pipeline fica vermelho.

## Como rodar

```bash
git clone https://github.com/vitorsilvestre29/govtrack-br
cd govtrack-br
docker compose up -d
```

### Inicializar o Superset

```bash
docker exec -it govtrack-br-superset-1 superset db upgrade
docker exec -it govtrack-br-superset-1 superset fab create-admin \
  --username admin --firstname Admin --lastname Admin \
  --email admin@govtrack.com --password admin123
docker exec -it govtrack-br-superset-1 superset init
```

Acessa `localhost:8088` — login: `admin` / `admin123`

<img width="1827" height="847" alt="image" src="https://github.com/user-attachments/assets/fcac0fed-6bd3-443b-b3ea-ebfb71026a2b" />
