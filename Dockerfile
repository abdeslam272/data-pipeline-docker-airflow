FROM python:3

WORKDIR /app

COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

CMD ["python", "api_handler.py", "&&", "python", "data_transformer.py", "&&", "python", "db_loader.py"]
