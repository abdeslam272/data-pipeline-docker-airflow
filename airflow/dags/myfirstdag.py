from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Define the DAG
with DAG(
    dag_id="myfirstdag",
    description="This is my first DAG",
    start_date=datetime(2024, 12, 27,10,00),
    schedule_interval="*/5 * * * *",
    catchup=False,
    dagrun_timeout=timedelta(minutes=45),
    tags=["sales", "monthly"]
) as dag:
    create_table=PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_conn",
        sql='''
        CREATE TABLE IF NOT EXISTS customers(
        customer_id varchar(50) NOT NULL,
        customer_name VARCHAR NOT NULL,
        addres VARCHAR NOT NULL,
        birth_date DATE NOT NULL
        );
        '''
    )

    insert_values=PostgresOperator(
        task_id="insert_values",
        postgres_conn_id="postgres_conn",
        sql='/sql/insert.sql',
    )
