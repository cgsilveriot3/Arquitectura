from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

def test_postgres_connection(**kwargs):
    try:
        postgres_hook = PostgresHook(postgres_conn_id='postgres_dev')
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staging.empleados LIMIT 5")  # Cambia `your_table` por el nombre de tu tabla
        result = cursor.fetchall()
        if result:
            print(f"Data retrieved successfully, number of rows: {len(result)}")
        else:
            print("No data returned from the query.")
        kwargs['ti'].xcom_push(key='query_result', value=result)  # Usar XCom para compartir el resultado
    except Exception as e:
        print(f"Connection test failed: {str(e)}")
        raise

def use_query_result(**kwargs):
    result = kwargs['ti'].xcom_pull(key='query_result', task_ids='test_postgres_connection')
    print(f"Result from previous task: {result}")

dag = DAG(
    'validate_postgres',
    default_args=default_args,
    description='Test PostgreSQL connection using Airflow and pass results between tasks',
    schedule_interval=None,
)

# Tarea para probar la conexión a PostgreSQL y recuperar datos
test_conn_task = PythonOperator(
    task_id='test_postgres_connection',
    python_callable=test_postgres_connection,
    provide_context=True,
    dag=dag,
)

# Tarea para usar el resultado de la consulta de PostgreSQL
use_result_task = PythonOperator(
    task_id='use_query_result',
    python_callable=use_query_result,
    provide_context=True,
    dag=dag,
)

# Define la secuencia de ejecución de las tareas
test_conn_task >> use_result_task
