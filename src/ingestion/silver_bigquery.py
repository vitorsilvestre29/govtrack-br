import pandas as pd
import os
import google.cloud.bigquery as bigquery

def carregar_silver_bigquery():
    df = pd.read_parquet("/opt/airflow/data/silver/deputados.parquet")
    project_id = os.environ["BIGQUERY_PROJECT_ID"]
    print(f"Carregado {len(df)} deputados do silver para o BigQuery.")
    client = bigquery.Client(project=project_id)
    client.load_table_from_dataframe(df, "govtrackbr.GovTrackBr_Base.deputados_bruto", job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")).result()

