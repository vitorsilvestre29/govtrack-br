# GovTrack BR

![CI](https://img.shields.io/github/actions/workflow/status/vitorsilvestre29/govtrack-br/dbt_test.yml?branch=main&style=flat-square&label=dbt%20parse)
![Python](https://img.shields.io/badge/python-3.11-blue?style=flat-square)
![dbt](https://img.shields.io/badge/dbt--bigquery-1.8.0-orange?style=flat-square)
![Docker](https://img.shields.io/badge/docker-compose-2496ED?style=flat-square&logo=docker&logoColor=white)

Pipeline de dados que reúne e processa informações públicas do governo federal brasileiro, unindo dados de deputados federais e emendas parlamentares numa arquitetura de Data Lakehouse em camadas (Medallion), com BigQuery como data warehouse.

## Dashboard

<img width="1827" height="847" alt="image" src="https://github.com/user-attachments/assets/fcac0fed-6bd3-443b-b3ea-ebfb71026a2b" />

Dashboard construído no Apache Superset, sobre as tabelas do PostgreSQL, mostrando os 513 deputados federais por partido/estado e o total de emendas parlamentares pagas por função (`SUM(valorpago)`).

## Fontes de dados

- **[Câmara dos Deputados](https://dadosabertos.camara.leg.br/)** — API REST com dados de todos os deputados federais em exercício.
- **[Portal da Transparência](https://portaldatransparencia.gov.br/api-de-dados)** — API com emendas parlamentares e valores pagos, paginada.

## Arquitetura

```
Fontes (Câmara / Portal da Transparência)
            │
            │  batch, Airflow            streaming, Kafka
            ▼                                  │
+---------------------------+                  │
|          BRONZE           |                  │
|  deputados.parquet        |                  │
|  emendas.parquet          |                  │
|  (dados brutos das APIs)  |                  │
+-------------+-------------+                  │
              │ limpeza, tipagem, seleção       │
              ▼ de colunas                      │
+---------------------------+                   │
|          SILVER           |                   │
|  deputados.parquet        |──► BigQuery       │
|  emendas.parquet          |   GovTrackBr_Base │
|  (dados normalizados)     |   .deputados_bruto│
+-------------+-------------+                   │
              │                                 │
              ▼ dbt: test → run                 │
+---------------------------+                   │
|   BigQuery (GovTrackBr_Analitico)             │
|   stg_deputados → mart_deputados_por_partido  │
+---------------------------+                   │
              │ agregações                      │
              ▼                                 │
+---------------------------+                   │
|           GOLD            |                   │
|  deputados_por_partido    |                   │
|  emendas por função/ano   |                   │
+-------------+-------------+                   │
              │                                 │
              ▼                                 ▼
+-----------------------------------------------+
|                   PostgreSQL                   |
|   (tabela deputados + emendas, via pipeline)   |
+---------------------------+--------------------+
                             │
                             ▼
                  +-----------------------+
                  |    Apache Superset     |
                  |       Dashboard        |
                  +-----------------------+
```

Também é possível representar o mesmo fluxo em Mermaid:

```mermaid
flowchart LR
    A[Câmara dos Deputados API] -->|batch, Airflow| B[Bronze]
    A -->|streaming, Kafka Producer/Consumer| F[(PostgreSQL)]
    C[Portal da Transparência API] -->|batch, Airflow| B
    B --> D[Silver]
    D -->|carga, Airflow| H[(BigQuery - Base)]
    H -->|dbt: test + run| I[(BigQuery - Analitico)]
    D --> E[Gold]
    E --> F
    F --> G[Superset Dashboard]
```

## Camadas do Data Lake (Medallion)

O pipeline segue a arquitetura Medallion, com cada camada em Parquet gerado via Pandas/PyArrow:

- **Bronze** — cópia fiel do retorno das APIs (Câmara e Portal da Transparência), sem transformação, em `data/bronze/*.parquet`. Serve como histórico bruto e ponto de reprocessamento caso a lógica de Silver/Gold mude.
- **Silver** — seleção das colunas relevantes, normalização de tipos (ex.: conversão de `valorPago` de string em formato BR para `float`) e checagem básica de qualidade (nulos, duplicados, dtypes) impressa no log da task. Grava em `data/silver/*.parquet`.
- **Gold** — agregações prontas para consumo: total de deputados por partido (`groupby siglaPartido`) e soma de emendas pagas por ano/tipo/localidade do gasto. Grava em `data/gold/*.parquet`.

Além dos Parquet, a Silver de deputados é carregada no BigQuery (`GovTrackBr_Base.deputados_bruto`, com `WRITE_TRUNCATE`). A partir dessa tabela, o dbt cria as views de `GovTrackBr_Analitico`. A Gold e a tabela `deputados` do PostgreSQL continuam sendo a fonte do dashboard no Superset.

## Stack

| Tecnologia | Função |
|---|---|
| Python | Ingestão e transformação de dados |
| Apache Airflow | Orquestração do pipeline (DAG `pipeline_deputados`) |
| Apache Kafka | Streaming de deputados em tempo real (producer/consumer) |
| PostgreSQL | Armazenamento relacional usado pelo dashboard (tabela `deputados`, emendas) |
| BigQuery | Data warehouse: `GovTrackBr_Base` (dado bruto da Silver) e `GovTrackBr_Analitico` (modelos dbt) |
| dbt | Staging, modelo mart e testes de qualidade sobre os dados de deputados |
| Apache Superset | Dashboard interativo |
| Docker / Docker Compose | Containerização de toda a infraestrutura |
| GitHub Actions | CI — roda `dbt parse` a cada push/PR na `main` |
| Pandas + PyArrow | Processamento e leitura/escrita em Parquet |

## Pipeline do Airflow

A DAG `pipeline_deputados` roda diariamente (`@daily`). Dentro dela, a cadeia dos deputados é:

```
salvar_bronze → transformar_silver → salvar_silver_bigquery
  → tarefa_bash_teste (dbt test) → tarefa_bash (dbt run)
  → transformar_gold → popular_banco
```

- `tarefa_bash_teste` roda `dbt test` antes de `dbt run`. Se um teste falhar, a tarefa fica vermelha e as views não são recriadas.
- A cadeia de emendas (`salvar_bronze_emendas → emendas_silver → emendas_gold`) roda em paralelo e não passa pelo BigQuery.

## Streaming com Kafka

Como caminho alternativo ao pipeline batch do Airflow, os deputados também podem ser publicados em tempo real no topic `deputados` via Producer e consumidos por um Consumer que insere diretamente no PostgreSQL (`ON CONFLICT (id) DO NOTHING`), sem passar pelas camadas Bronze/Silver/Gold.

```bash
# Publicar deputados no Kafka
python3 src/ingestion/kafka_producer.py

# Consumir e inserir no banco
python3 src/ingestion/kafka_consumer.py
```

## Transformações com dbt

O projeto `govtrack_dbt` contém:

- **Source** (`models/staging/schema.yml`) — aponta para `GovTrackBr_Base.deputados_bruto`, a tabela carregada pelo Airflow a partir da Silver.
- **Staging** (`models/staging/stg_deputados.sql`) — normaliza nomes de coluna e filtra registros sem nome. Materializada como view em `GovTrackBr_Analitico`.
- **Mart** (`models/mart/mart_deputados_por_partido.sql`) — total de deputados por partido, agregado a partir da staging. Também uma view.
- **Testes de schema** (`models/staging/schema.yml`) — `not_null` e `unique` nos campos-chave de `stg_deputados` e `mart_deputados_por_partido`.

## CI/CD

O workflow `.github/workflows/dbt_test.yml` roda `dbt parse` a cada push ou pull request na branch `main`. Ele valida que o projeto dbt está bem formado (modelos, sources e YAML), mas não conecta no BigQuery, porque o CI não tem credenciais. Os testes de dados rodam no Airflow, onde a credencial já existe.

## Como rodar localmente

Pré-requisitos: Docker e Docker Compose, e uma conta Google Cloud com acesso ao projeto `govtrackbr`.

```bash
git clone https://github.com/vitorsilvestre29/govtrack-br
cd govtrack-br
cp .env.example .env  # preencha DB_PASSWORD, AIRFLOW_DB_PASSWORD, SUPERSET_SECRET_KEY, PORTAL_TRANSPARENCIA_API_KEY, BIGQUERY_PROJECT_ID e BIGQUERY_DATASET
gcloud auth application-default login
docker compose up -d
```

O `gcloud auth application-default login` gera o arquivo de credencial que os containers do Airflow montam via volume. Sem ele, a carga para o BigQuery e o `dbt` falham com `DefaultCredentialsError`.

Isso sobe PostgreSQL (app e Airflow), Airflow webserver/scheduler, Superset, Zookeeper e Kafka. O Airflow fica disponível em `localhost:8081` e o Adminer (cliente web do Postgres) em `localhost:8080`.

### Inicializar o Superset

```bash
docker exec -it govtrack-br-superset-1 superset db upgrade
docker exec -it govtrack-br-superset-1 superset fab create-admin \
  --username admin --firstname Admin --lastname Admin \
  --email admin@govtrack.com --password <sua-senha>
docker exec -it govtrack-br-superset-1 superset init
```

Acesse `localhost:8088` com o usuário e senha definidos no passo acima.

### Rodar os modelos dbt

Pré-requisito: ADC configurado na sua máquina com `gcloud auth application-default login`.

```bash
cd govtrack_dbt
dbt run --profiles-dir .
dbt test --profiles-dir .
```

Os comandos usam o `profiles.yml` do próprio projeto (`--profiles-dir .`), configurado para o BigQuery (projeto `govtrackbr`, dataset `GovTrackBr_Analitico`, autenticação por `oauth`).

### Scripts de ingestão/transformação fora do Airflow

Os módulos em `src/ingestion` e `src/transformation` também podem ser executados diretamente (o Airflow apenas os orquestra via `PythonOperator`), desde que as dependências deles — `pandas`, `pyarrow`, `psycopg2`, `requests`, `google-cloud-bigquery` e, para o streaming, `kafka-python` — estejam instaladas no ambiente Python local.

## Estrutura do repositório

```
dags/                  DAG do Airflow (pipeline_deputados)
src/ingestion/         Coleta das APIs, Bronze, carga para BigQuery, Kafka producer/consumer, conexão com o banco
src/transformation/    Transformações Silver e Gold (deputados e emendas)
govtrack_dbt/          Projeto dbt (sources, staging, mart, testes)
.github/workflows/     CI (dbt parse)
docker-compose.yml     Orquestração de toda a infraestrutura
```
