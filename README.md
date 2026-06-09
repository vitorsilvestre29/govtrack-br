GovTrack BR
Pipeline de dados que reúne e processa informações públicas do governo federal brasileiro, unindo dados de deputados federais e emendas parlamentares numa arquitetura moderna de Data Lakehouse.
Fontes de dados

Câmara dos Deputados — API REST com dados de todos os deputados federais
Portal da Transparência — API com emendas parlamentares e gastos públicos

Stack
TecnologiaFunçãoPythonIngestão e transformação de dadosApache AirflowOrquestração do pipelinePostgreSQLArmazenamento relacionaldbtTransformações SQL com linhagemDockerContainerização de toda a infraestruturaPandas + PyArrowProcessamento e formato Parquet
Arquitetura Medallion
Bronze → Silver → Gold

Bronze — dados brutos das APIs em Parquet
Silver — dados limpos e normalizados
Gold — agregações prontas para consumo

Como rodar
bashgit clone https://github.com/vitorsilvestre29/govtrack-br
cd govtrack-br
docker compose up -d