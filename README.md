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
Fournit l'interface utilisateur d'Airflow.
Permet de surveiller et de résoudre les problèmes des pipelines de données.
### Scheduler
Détermine quand les tâches doivent être exécutées en fonction des dépendances et des calendriers.
### Metadata Database
Sert de mémoire à Airflow, stockant les états des workflows et les métadonnées.
Utilise fréquemment PostgreSQL ou MySQL.
### Executor
Définit comment les tâches sont exécutées (par exemple : localement, dans un cluster ou via Kubernetes).
### Worker
Exécute les tâches assignées par le Planificateur via l'Exécuteur.
### Triggers
Gère les tâches qui attendent la réalisation d'événements externes avant de continuer.

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

## Airflow & Docker 
To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml.
   ```
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'
   ```
the command is to start the container:
   ```
   docker-compose up airflow-init
   docker-compose up -d
   ```

https://devblogit.com/apache-airflow-tutorial-architecture-concepts-and-how-to-run-airflow-locally-with-docker

## Créer notre premier DAG

### Paramètres du DAG
- **dag_id** : Identifiant unique pour votre DAG. S'il est dupliqué, Airflow en attribuera un aléatoire sans afficher d'erreur.  
- **description** : Une courte description de l'objectif de votre DAG pour une meilleure compréhension.  
- **start_date** : La date et l'heure à partir desquelles le DAG commencera à s'exécuter.  
- **schedule_interval** : Détermine la fréquence d'exécution du DAG (par exemple, quotidien, horaire).  
- **catchup** :  
  - `True` : Airflow exécutera toutes les exécutions manquées depuis la `start_date`.  
  - `False` : Airflow ignorera les exécutions manquées et ne lancera que l'instance la plus récente.  

## Points importants à connaître

1. **Fuseau horaire par défaut** :  
   Le fuseau horaire par défaut dans Airflow est **UTC**. Vous pouvez ajuster ce paramètre dans le fichier `airflow.cfg` ou par DAG selon vos besoins.

2. **Comprendre l'exécution des tâches** :  
   Dans Airflow, l'exécution des tâches est planifiée en fonction de la **date de début** (*start date*) et de l'**intervalle de planification** (*schedule interval*). Notez que l'exécution réelle d'une tâche correspond à la **date de début plus l'intervalle de planification**.  
   Par exemple, si un DAG a une date de début fixée au `2024-01-01` et un intervalle quotidien, la première exécution aura lieu pour la date **2024-01-02**.

3. **Intervalle de planification : `timedelta` vs. expressions Cron (`* * * * *`)** :  
   - **`timedelta`** : Cet objet Python permet de définir des intervalles de temps de manière programmatique (par exemple, `schedule_interval=timedelta(days=1)` pour une planification quotidienne).  
   - **Expressions Cron** : Elles offrent un moyen plus flexible de définir des plannings grâce à une syntaxe spécifique (par exemple, `schedule_interval="0 0 * * *"` pour une exécution quotidienne à minuit).  
   - Le choix entre ces deux méthodes dépend de la complexité de votre planification. Utilisez `timedelta` pour des intervalles simples et les expressions Cron pour des plannings plus complexes.

## Création d'un DAG et d'une tâche

J'ai créé un DAG nommé `myfirstdag.py` avec une tâche pour créer une table dans PostgreSQL :

```python
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Définir le DAG
with DAG(
    dag_id="myfirstdag",
    description="C'est mon premier DAG",
    start_date=datetime(2024, 12, 27, 10, 0),
    schedule_interval="*/5 * * * *",
    catchup=False,
    dagrun_timeout=timedelta(minutes=45),
    tags=["sales", "monthly"]
) as dag:
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_conn",
        sql='''
        CREATE TABLE IF NOT EXISTS customers(
        customer_id VARCHAR(50) NOT NULL,
        customer_name VARCHAR NOT NULL,
        address VARCHAR NOT NULL,
        birth_date DATE NOT NULL
        );
        '''
    )
```
Une fois que vous avez créé le fichier, ouvrez Command Prompt ou PowerShell, puis lancez le planificateur Airflow avec la commande suivante :
```Powershell
docker exec -it airflow-airflow-scheduler-1 /bin/bash
```

Ensuite, vous pouvez tester la tâche en exécutant la commande suivante :

```Powershell
airflow tasks test myfirstdag create_table 2024-12-31
```
Cela exécutera la tâche create_table pour le DAG myfirstdag à la date spécifiée (ici le 31 décembre 2024).


## Problème de Configuration 

### Description de l'erreur
Lors de l'accès à l'interface utilisateur d'Airflow, l'erreur suivante apparaît : 

> **Airflow Configuration**  
> Your Airflow administrator chose not to expose the configuration, most likely for security reasons.

### Capture d'écran de l'erreur
![Configuration Error](https://github.com/user-attachments/assets/510491f0-dc4e-4200-9801-eb43725bb6b8)

---

### Solution
Pour résoudre ce problème et exposer la configuration dans l'interface web d'Airflow, vous devez définir la variable d'environnement `AIRFLOW__WEBSERVER__EXPOSE_CONFIG` à `True`. Voici les étapes pour y parvenir : 

1. Créez un fichier `.env` dans le répertoire contenant votre fichier `docker-compose.yml` et ajoutez la variable suivante :
   ```env
   AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True
   ```

2. Modifiez le fichier docker-compose.yml pour inclure ce fichier .env dans la configuration du service airflow-webserver :
 ```
 services:
  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - "8080:8080"
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully
 ```
3. Redémarrez vos conteneurs Docker pour appliquer les modifications :

```bash
docker-compose down
docker-compose up -d
 ```
Après ces étapes, la configuration d'Airflow devrait être visible depuis l'interface web.

## Sensors dans Apache Airflow

Les **Sensors** dans Apache Airflow sont des opérateurs spéciaux qui permettent de surveiller et d'attendre qu'un événement particulier se produise. Une fois l'événement détecté, le capteur déclenche l'exécution de la tâche suivante dans le DAG.

### Types de Sensors
1. **File Sensor**  
   Ce capteur vérifie si un fichier spécifique est disponible dans un dossier donné. Par exemple, lorsqu'un fichier attendu arrive dans le répertoire cible, le capteur déclenche l'exécution de la prochaine tâche.

2. **SQL Sensor**  
   Ce capteur surveille une base de données pour vérifier si un enregistrement particulier existe. Par exemple, dans un scénario où vous chargez des données quotidiennement, le capteur peut vérifier si un enregistrement attendu est arrivé. En cas d'absence de données, il peut émettre une alerte ou effectuer une autre action.

### Utilisation
Les Sensors sont particulièrement utiles dans les workflows dépendant d'événements externes, comme l'arrivée de fichiers ou la disponibilité de données spécifiques dans une base de données.



# Unification de projet 
Avec un contenu de fichier .env:
DB_HOST=postgres
DB_PORT=5432
DB_NAME=my_database
DB_USER=my_user
DB_PASSWORD=my_password
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

j'arrive pas a voir la table Weather_data
Avec 
.env :
DB_HOST=postgres
DB_PORT=5432
DB_NAME=my_database
DB_USER=my_user
DB_PASSWORD=my_password

je peux voir la data dans de la table Weather_data in pgadmin

## Command
 ```bash
docker-compose -f docker-compose.yaml up --build
 ```
