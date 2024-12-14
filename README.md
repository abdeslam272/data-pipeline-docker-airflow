# data-pipeline-docker-airflow

.gitignore : Empêche d'ajouter des fichiers inutiles, tels que des fichiers temporaires ou des clés API, au dépôt Git. Cela réduit le risque de partager des informations sensibles et garde votre dépôt propre.

.dockerignore : Lors de la construction de l'image Docker, cette liste exclut des fichiers qui ne sont pas nécessaires dans l'image, ce qui rend l'image plus légère et plus rapide à construire. Cela vous évite également d'inclure des fichiers inutiles qui n’ont pas de place dans l’image, comme les fichiers de configuration locaux.

# Structure du projet
``` plaintext
data-pipeline-docker-airflow/
│
├── airflow/
│   ├── dags/
│   │   ├── etl_pipeline.py  # Le DAG Airflow pour orchestrer l'ETL
│   │
│   ├── docker-compose.yml   # Fichier Docker-Compose pour configurer Airflow
│   └── requirements.txt     # Dépendances Python pour Airflow
│
├── app/
│   ├── api_handler.py       # Script Python pour extraire des données depuis l'API
│   ├── data_transformer.py  # Script pour transformer les données
│   ├── db_loader.py         # Script pour charger les données dans PostgreSQL
│   └── tests/
│       ├── test_api_handler.py  # Tests pour la récupération des données API
│       └── test_transformer.py  # Tests pour les transformations de données
│
├── docker-compose.yml       # Orchestration multi-services (Airflow + PostgreSQL)
├── Dockerfile               # Conteneur principal pour vos scripts Python
└── README.md                # Documentation du projet
```


# Sécurisation de la clé API
Pour éviter d'exposer des informations sensibles, comme la clé API, ne la codez jamais directement dans le fichier source. Stockez-la plutôt dans une variable d'environnement ou un fichier .env, et chargez-la à l'aide d'une bibliothèque comme python-dotenv. Assurez-vous que le fichier .env est ajouté à .gitignore pour éviter tout upload accidentel sur GitHub. Cette pratique protège vos identifiants et renforce la sécurité de votre application.

# Que doit contenir un fichier docker-compose.yml ?
Un fichier docker-compose.yml définit les services, réseaux et volumes de votre application. Chaque service spécifie un conteneur, son image ou le contexte de build, les ports, les variables d'environnement et les dépendances. Les réseaux permettent la communication entre les services, et les volumes assurent la persistance des données. Il simplifie la gestion des configurations multi-conteneurs et le déploiement des applications.
 
# Configure une tâche Airflow pour appeler api_handler.py périodiquement.
This Airflow DAG, named simple_weather_pipeline, is scheduled to run every hour starting from December 14, 2024. It uses the BashOperator to execute a Python script (api_handler.py) located at /app/api_handler.py. The DAG is configured with retry logic (1 retry after a 5-minute delay) and catchup=False to avoid backfilling past runs. Default arguments specify that tasks do not depend on previous runs, and the workflow is suitable for automating API data collection or similar periodic tasks.
