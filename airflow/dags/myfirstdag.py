from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable



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
        sql='/sql/create_customer.sql'
    )

    insert_values=PostgresOperator(
        task_id="insert_values",
        postgres_conn_id="postgres_conn",
        sql='/sql/insert.sql',
    )

    select_values=PostgresOperator(
        task_id="select_values",
        postgres_conn_id="postgres_conn",
        sql=''' select * from customers where birth_date between %(start_date)s and %(end_date)s ''',
        parameters={
            "start_date" : "{{var.value.start_date}}", "end_date" : "{{var.value.end_date}}"
        }
    )

    create_table >> insert_values >> select_values