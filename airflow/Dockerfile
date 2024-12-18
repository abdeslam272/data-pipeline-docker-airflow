FROM apache/airflow:2.7.2

# Installer les dépendances Python
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Commande par défaut
CMD ["airflow", "webserver"]
