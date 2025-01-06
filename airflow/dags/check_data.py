from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.sql import SqlSensor
from airflow.operators.python import PythonOperator

def proscessing_data():
    print("record exists")

# Define the DAG
with DAG(
    dag_id="check_data",
    description="This is my first DAG",
    start_date=datetime(2024, 12, 27,10,00),
    schedule_interval="*/5 * * * *",
    catchup=False,
    dagrun_timeout=timedelta(minutes=45),
    tags=["sales", "monthly"]
) as dag:
    
    check_records=SqlSensor(
        task_id = "check_records",
        conn_id="postgres_conn",
        sql = ''' select * from customers where customer_ame = 'Adil'; ''',
        poke_interval = 10,
        timeout = 30,
        mode="reschedule",
        soft_fail=True
    )

    proscessing_data = PythonOperator(
        task_id = "proscessing_data",
        python_callable=proscessing_data
    )

    check_records >> proscessing_data