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
│   ├── Dockerfile           # Conteneur principal pour Airflow
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

# Erreurs d'Airflow :
Après avoir lancé les conteneurs à l'aide du fichier docker-compose situé dans le dossier airflow :
![image](https://github.com/user-attachments/assets/eef376f6-16ca-4868-90ca-2dd84569dff7)

J'observe une erreur récurrente dans les deux conteneurs suivants : airflow-scheduler-1 et airflow-webserver-1.
L'erreur est la suivante : ![image](https://github.com/user-attachments/assets/975b4058-4860-4717-9941-4ede319739e1)

Solution: J'utilise pgAdmin pour intéragir avec la base de données, pas de naviguer en port 5432.


# Erreurs de conteneur postgres :
On a une erreur qui se répéte liée au container postgres : 
![image](https://github.com/user-attachments/assets/2a19fe93-9f43-461d-8ada-7ce73de5c5ff)


# le fonctionnement pour voir les données en pgadmin
### Étape 1 : Ouvrir pgAdmin
1. Accédez à [http://localhost:5050](http://localhost:5050) dans votre navigateur.
2. Connectez-vous avec les identifiants suivants :
   - **Email** : `admin@example.com`
   - **Mot de passe** : `admin`

### Étape 2 : Connectez-vous à votre serveur PostgreSQL
1. Dans le panneau de gauche, faites un clic droit sur **Servers** et sélectionnez **Create → Server...**.
2. Remplissez les informations suivantes :
   - **Onglet General** : Donnez un nom à votre serveur, par exemple : `Postgres`.
   - **Onglet Connection** :
     - **Hostname/Address** : `postgres` (correspond au nom de service dans votre fichier `docker-compose.yml`).
     - **Port** : `5432`.
     - **Maintenance Database** : `mydatabase`.
     - **Username** : `myuser`.
     - **Password** : `mypassword`.
3. Cliquez sur **Save**.

### Étape 3 : Naviguez vers la base de données
1. Dans le panneau de gauche, développez l’arborescence **Servers** :
   - Cliquez sur votre serveur (par exemple : `Postgres`).
   - Développez **Databases**.
   - Sélectionnez votre base de données : `mydatabase`.

### Étape 4 : Ouvrir l’outil de requêtes
1. Développez **Schemas → public → Tables**.
2. Vous devriez voir votre table `weather_data` dans la liste.
3. Faites un clic droit sur `weather_data` et sélectionnez **Query Tool**.
   - Vous pouvez également cliquer sur le menu **Tools** en haut, puis choisir **Query Tool**.

### Étape 5 : Exécuter une requête pour voir les données
1. Dans l’éditeur de requêtes, saisissez la commande SQL suivante :
   ```sql
   SELECT * FROM weather_data;
   ```
2. Cliquez sur l'icône en forme d'éclair (ou appuyez sur F5) pour exécuter la requête.
### Étape 6 : Vérifier les résultats
Les résultats de la requête apparaîtront dans le panneau de sortie en bas.
Vous devriez voir les données insérées, par exemple
   ```plaintext
   time                  | temperature | humidity | weather
----------------------+-------------+----------+--------
2024-12-21 11:00:00  | 25.3        | 60       | Sunny
   ```

# Airflow
Apache Airflow is a platform to programmatically author, schedule, and monitor workflows.

## Features:
Define task dependencies.
Configure task retries in case of failures.
Integrate with other tools through Connections.

## Core Components
### Webserver
Provides the Airflow UI.
Enables monitoring and troubleshooting of data pipelines.
### Scheduler
Determines when tasks should run based on dependencies and schedules.
### Metadata Database
Serves as the memory of Airflow, storing workflow states and metadata.
Commonly uses PostgreSQL or MySQL.
### Executor
Defines how tasks are executed (e.g., locally, in a cluster, or via Kubernetes).
### Worker
Executes tasks assigned by the Scheduler through the Executor.
### Triggers
Manages tasks that wait for external events to complete before continuing.

## Core Components
### DAG
Directed Acyclic graph
Aucun cycle
Une seule direction
### Operator
Les opérateurs encapsulent les tâches et permettent de définir les actions à effectuer
Permet d'écrire de nombreuses tâches sans coder
#### Action Operator
Exécutent une action spécifique
#### Transfom Operator
Effectuent le transfert de données entre systèmes
#### sensor opertors 
Attendent une certaine condition
#### Trigger-Deferrable Operators 
Capteurs qui ne bloquent pas un worker
#### Custom Operatos
Créés pour des besoins spécifiques
