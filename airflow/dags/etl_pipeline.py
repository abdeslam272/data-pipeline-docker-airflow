from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configuration du DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "simple_weather_pipeline",
    default_args=default_args,
    description="Exécuter api_handler.py avec Airflow",
    schedule_interval=timedelta(hours=1),  # Exécution toutes les heures
    start_date=datetime(2024, 12, 14),
    catchup=False,
) as dag:

    run_script = BashOperator(
        task_id="run_api_handler",
        bash_command="python /app/api_handler.py",
    )
