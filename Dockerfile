FROM python:3

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application dans le conteneur
COPY app /app

# Spécifier la commande par défaut
CMD ["bash", "-c", "python api_handler.py && python data_transformer.py && python db_loader.py"]