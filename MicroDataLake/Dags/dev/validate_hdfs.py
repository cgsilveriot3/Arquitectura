from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from hdfs import InsecureClient
import os

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

def validate_hdfs_connection(**kwargs):
    try:
        
        client = InsecureClient('http://hdfs-namenode:9870', user='airflow')

        test_file_path = '/usr/local/airflow/test/dag_test_hdfs.txt'
        with open(test_file_path, 'w') as f:
            f.write("HDFS connection test desde dag")

        print(f"Test file created at {test_file_path}")

        client.upload('/user/airflow/', test_file_path, overwrite=True)
        print("File uploaded to HDFS successfully.")

    except Exception as e:
        print(f"Failed to connect to HDFS or upload file: {str(e)}")
        raise

dag = DAG(
    'validate_hdfs',
    default_args=default_args,
    description='Validate connection and access to HDFS',
    schedule_interval=None,
)

validate_hdfs_task = PythonOperator(
    task_id='validate_hdfs_connection_task',
    python_callable=validate_hdfs_connection,
    dag=dag,
)
