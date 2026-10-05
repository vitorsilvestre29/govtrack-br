import sys
sys.path.insert(0, '/opt/airflow')

from src.ingestion.bronze import salvar_bronze
from src.transformation.deputados_silver import transformar_silver
from src.transformation.deputados_gold import transformar_gold
from src.ingestion.popular_banco import popular_banco
from src.ingestion.bronze_emendas import salvar_bronze_emendas
from src.transformation.emendas_silver import emendas_silver
from src.transformation.emendas_gold import emendas_gold
from src.ingestion.silver_bigquery import carregar_silver_bigquery
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
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

    tarefa_silver_bigquery = PythonOperator(
        task_id='salvar_silver_bigquery',
        python_callable=carregar_silver_bigquery
    )

    tarefa_bash_teste = BashOperator(
            task_id='tarefa_bash_teste',
            bash_command='cd /opt/airflow/govtrack_dbt && dbt test --profiles-dir .'
        )

    tarefa_bash = BashOperator(
        task_id='tarefa_bash',
        bash_command='cd /opt/airflow/govtrack_dbt && dbt run --profiles-dir .'
    )

    tarefa_bronze >> tarefa_silver >> tarefa_silver_bigquery >> tarefa_bash_teste >> tarefa_bash >> tarefa_gold >> tarefa_popular_banco
    tarefa_salvar_bronze_emendas >> tarefa_emendas_silver >> tarefa_emendas_gold
    