from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from api_to_redshift import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    }

ETL_aws =  DAG(
    default_args = default_args,
    dag_id = 'api_to_redshift',
    catchup = False,
    description = 'ETL API',
    schedule_interval = "@daily"
    )

task_1 = BashOperator(
    task_id='primera_tarea',
    bash_command='echo Iniciando...',
    dag=ETL_aws
)

task_2 = PythonOperator(
    task_id='transformar_data',
    python_callable=get_data,
    op_args = ['etf'],
    dag=ETL_aws
)

task_3 = PythonOperator(
    task_id='conexion_redshift',
    python_callable=api_to_aws,
    dag=ETL_aws
)


task_1 >> task_2 >> task_3