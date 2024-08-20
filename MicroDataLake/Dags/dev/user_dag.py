import os
import pwd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

def check_user(**kwargs):
    user_id = os.getuid()
    user_name = pwd.getpwuid(user_id).pw_name
    print(f"The DAG is running under the user: {user_name}")

dag = DAG(
    'check_user_dag',
    default_args=default_args,
    description='Check the user running the DAG',
    schedule_interval=None,
)

check_user_task = PythonOperator(
    task_id='check_user_task',
    python_callable=check_user,
    dag=dag,
)
