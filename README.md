# GovTrack BR

Pipeline de dados que reúne e processa informações públicas do governo federal brasileiro, unindo dados de deputados federais e emendas parlamentares numa arquitetura moderna de Data Lakehouse.

## Fontes de dados

- **Câmara dos Deputados** — API REST com dados de todos os deputados federais
- **Portal da Transparência** — API com emendas parlamentares e gastos públicos

## Stack

| Tecnologia | Função |
|---|---|
| Python | Ingestão e transformação de dados |
| Apache Airflow | Orquestração do pipeline |
| PostgreSQL | Armazenamento relacional |
| dbt | Transformações SQL com linhagem |
| Docker | Containerização de toda a infraestrutura |
| Pandas + PyArrow | Processamento e formato Parquet |

## Arquitetura Medallion

- **Bronze** — dados brutos das APIs em Parquet
- **Silver** — dados limpos e normalizados
- **Gold** — agregações prontas para consumo

## Como rodar

```bash
git clone https://github.com/vitorsilvestre29/govtrack-br
cd govtrack-br
docker compose up -d
```
<img width="1827" height="847" alt="image" src="https://github.com/user-attachments/assets/fcac0fed-6bd3-443b-b3ea-ebfb71026a2b" />
