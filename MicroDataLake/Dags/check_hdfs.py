from airflow import DAG
from airflow.providers.apache.hdfs.sensors.hdfs import HdfsSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'hdfs_test',
    default_args=default_args,
    description='Test HDFS connection',
    schedule_interval=None,
)

start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

hdfs_check = HdfsSensor(
    task_id='check_hdfs',
    filepath='/user/airflow/',
    hdfs_conn_id='hdfs_default',
    timeout=300,
    poke_interval=10,
    dag=dag,
)

start_task >> hdfs_check
