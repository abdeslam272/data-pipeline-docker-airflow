# data-pipeline-docker-airflow

.gitignore : Empêche d'ajouter des fichiers inutiles, tels que des fichiers temporaires ou des clés API, au dépôt Git. Cela réduit le risque de partager des informations sensibles et garde votre dépôt propre.

.dockerignore : Lors de la construction de l'image Docker, cette liste exclut des fichiers qui ne sont pas nécessaires dans l'image, ce qui rend l'image plus légère et plus rapide à construire. Cela vous évite également d'inclure des fichiers inutiles qui n’ont pas de place dans l’image, comme les fichiers de configuration locaux.

# Structure du projet
``` plaintext
project-root/
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
