from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from io import StringIO
import os

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

def extract_data_from_postgres():
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'nombre', 'departamento', 'fecha_altar'])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    with open('/tmp/empleados.csv', 'w') as f:
        f.write(csv_data)

def load_data_to_hdfs():
    os.system('hdfs dfs -put -f /tmp/empleados.csv /user/airflow/empleados/')

dag = DAG(
    'postgres_to_hdfs_dag',
    default_args=default_args,
    description='Extract data from PostgreSQL and load to HDFS',
    schedule_interval=None,
)

extract_task = PythonOperator(
    task_id='extract_data_from_postgres',
    python_callable=extract_data_from_postgres,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_hdfs',
    python_callable=load_data_to_hdfs,
    dag=dag,
)

extract_task >> load_task

