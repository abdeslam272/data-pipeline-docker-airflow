from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define the DAG
with DAG(
    dag_id="simple_weather_pipeline",  # Identifiant unique du DAG
    description="This is my DAG to orchestrate the data from API to PostgreSQL",
    start_date=datetime(2025, 1, 12, 0, 0),  # Date et heure de début
    schedule_interval="0 */3 * * *",  # Toutes les 3 heures
    catchup=False,  # Éviter l'exécution rétroactive
    dagrun_timeout=timedelta(minutes=45),  # Timeout pour chaque run
    tags=["hourly", "weather"],  # Tags pour le classement
) as dag:

    # Exemple de tâche pour exécuter un script Python
    run_api_handler = BashOperator(
        task_id="run_api_handler",
        bash_command="python /app/api_handler.py",
    )