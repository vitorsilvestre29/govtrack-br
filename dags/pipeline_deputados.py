import sys
sys.path.insert(0, '/opt/airflow')

from src.ingestion.bronze import salvar_bronze
from src.transformation.deputados_silver import transformar_silver
from src.transformation.deputados_gold import transformar_gold
from src.ingestion.popular_banco import popular_banco
from src.ingestion.bronze_emendas import salvar_bronze_emendas
from src.transformation.emendas_silver import emendas_silver
from src.transformation.emendas_gold import emendas_gold
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    'pipeline_deputados',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    tarefa_bronze = PythonOperator(
        task_id='salvar_bronze',
        python_callable=salvar_bronze
    )

    tarefa_silver = PythonOperator(
        task_id='transformar_silver',
        python_callable=transformar_silver
    )

    tarefa_gold = PythonOperator(
        task_id='transformar_gold',
        python_callable=transformar_gold
    )

    tarefa_popular_banco = PythonOperator(
        task_id='popular_banco',
        python_callable=popular_banco
    )

    tarefa_salvar_bronze_emendas = PythonOperator(
        task_id='salvar_bronze_emendas',
        python_callable=salvar_bronze_emendas
    )

    tarefa_emendas_silver = PythonOperator(
        task_id='emendas_silver',
        python_callable=emendas_silver
    )

    tarefa_emendas_gold = PythonOperator(
        task_id='emendas_gold',
        python_callable=emendas_gold
    )

    tarefa_bronze >> tarefa_silver >> tarefa_gold >> tarefa_popular_banco
    tarefa_salvar_bronze_emendas >> tarefa_emendas_silver >> tarefa_emendas_gold
    