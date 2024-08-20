from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

def test_postgres_connection():
    try:
        postgres_hook = PostgresHook(postgres_conn_id='postgres_dev')
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"Connection test successful, result: {result}")
    except Exception as e:
        print(f"Connection test failed: {str(e)}")
        raise

dag = DAG(
    'test_postgres_dag',
    default_args=default_args,
    description='Test PostgreSQL connection using Airflow',
    schedule_interval=None,
)

test_conn_task = PythonOperator(
    task_id='test_postgres_connection',
    python_callable=test_postgres_connection,
    dag=dag,
)

test_conn_task
