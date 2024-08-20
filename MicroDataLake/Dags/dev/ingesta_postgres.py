from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from hdfs import InsecureClient
import pandas as pd
from io import StringIO
import os

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

def extract_data_from_postgres(**kwargs):
    try:
        postgres_hook = PostgresHook(postgres_conn_id='postgres_dev')
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staging.empleados")
        data = cursor.fetchall()
        
        if data:
            print(f"Data retrieved successfully, number of rows: {len(data)}")
        else:
            print("No data returned from the query.")
            return  
        
        kwargs['ti'].xcom_push(key='query_data', value=data)
        
        
        try:
            df = pd.DataFrame(data, columns=['id', 'nombre', 'departamento', 'fecha_alta'])
            print("DataFrame created successfully.")
        except Exception as e:
            print(f"Failed to create DataFrame: {str(e)}")
            raise

        try:
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            print("CSV data created successfully.")
        except Exception as e:
            print(f"Failed to create CSV: {str(e)}")
            raise

        try:
            with open('/usr/local/airflow/ingesta/empleados.csv', 'w') as f:
                f.write(csv_data)
            print("CSV file written to /usr/local/airflow/ingesta/empleados.csv successfully.")
        except Exception as e:
            print(f"Failed to write CSV to file: {str(e)}")
            raise

    except Exception as e:
        print(f"Connection or data extraction failed: {str(e)}")
        raise

def load_data_to_hdfs(**kwargs):
    try:
        client = InsecureClient('http://hdfs-namenode:9870', user='airflow')
        
        client.upload('/user/airflow/staging/empleados.csv', '/usr/local/airflow/ingesta/empleados.csv', overwrite=True)
        print("File uploaded to HDFS successfully.")
        
    except Exception as e:
        print(f"Failed to upload file to HDFS: {str(e)}")
        raise

dag = DAG(
    'ingesta_postgres',
    default_args=default_args,
    description='Extract data from PostgreSQL and load to HDFS',
    schedule_interval=None,
)

extract_task = PythonOperator(
    task_id='extract_data_from_postgres',
    python_callable=extract_data_from_postgres,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_hdfs',
    python_callable=load_data_to_hdfs,
    dag=dag,
)

extract_task >> load_task
