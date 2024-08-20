
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

def validate_hdfs_connection(**kwargs):
    try:
        test_file_path = '/usr/local/airflow/test/test_hdfs.txt'

        # Crear un archivo de prueba
        with open(test_file_path, 'w') as f:
            f.write("HDFS connection test")

        print(f"Test file created at {test_file_path}")

        # Ejecutar el comando HDFS en el contenedor de hdfs-namenode
        container_name = 'test-hdfs-namenode-1'  # Nombre del contenedor
        result = os.system(f'docker exec {container_name} hdfs dfs -put -f {test_file_path} /user/airflow/')
        if result == 0:
            print("File uploaded to HDFS successfully.")
        else:
            print(f"Failed to upload file to HDFS, error code: {result}")
            raise Exception("HDFS upload failed")

    except Exception as e:
        print(f"Failed to connect to HDFS or upload file: {str(e)}")
        raise

dag = DAG(
    'validate_hdfs_docker',
    default_args=default_args,
    description='Validate connection and access to HDFS',
    schedule_interval=None,
)

validate_hdfs_task = PythonOperator(
    task_id='validate_hdfs_connection_task',
    python_callable=validate_hdfs_connection,
    dag=dag,
)

