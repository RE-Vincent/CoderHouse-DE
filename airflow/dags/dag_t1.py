from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from api_to_redshift import get_data, api_to_aws
import smtplib

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['rmforgcp2@gmail.com'],  # Dirección de correo electrónico de destino
    'email_on_failure': True,  # Envía correo electrónico en caso de fallo
    'email_on_retry': False,
    'task_instance_trigger_send_email': True, # Enviar todo el log al correo electronico
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

def transformar_data(**kwargs):
    data = get_data('etf')
    kwargs['ti'].xcom_push(key='data', value=data)
    return data

task_2 = PythonOperator(
    task_id='transformar_data',
    python_callable=transformar_data,
    provide_context=True,
    dag=ETL_aws
)

def conexion_redshift(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='transformar_data', key='data')
    api_to_aws(data)

task_3 = PythonOperator(
    task_id='conexion_redshift',
    python_callable=conexion_redshift,
    provide_context=True,
    dag=ETL_aws
)


task_1 >> task_2 >> task_3