from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, "/opt/airflow")

from src.extract.extract import extrair_dados_crypto
from src.transform.transform import ler_dados_bronze, transformar_dados
from src.aggregate.aggregate import ler_dados_prata, agregar_metricas
from src.load.load import salva_na_bronze, salva_na_prata, salva_na_ouro


def task_extract():
    data = extrair_dados_crypto()
    salva_na_bronze(data)

def task_transform():
    data = ler_dados_bronze()
    df = transformar_dados(data)
    salva_na_prata(df)


def task_aggregate():
    df = ler_dados_prata()
    df_gold = agregar_metricas(df)
    salva_na_ouro(df_gold)


default_args = {
    'owner': 'João H',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id="crypto_pipeline",
    default_args=default_args,
    description="Pipeline de dados de criptomoedas - Medalhão",
    schedule_interval="@daily",
    start_date= datetime(2026, 5, 8),
    catchup=False 
) as dag:
    
    extract = PythonOperator(
        task_id= "extrair_dados_bronze",
        python_callable=task_extract
    )

    transform = PythonOperator(
        task_id="transformar_dados_prata",
        python_callable=task_transform
    )

    aggregate = PythonOperator(
        task_id="agregacoes_dados_ouro",
        python_callable=task_aggregate
    )

    extract >> transform >> aggregate