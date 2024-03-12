# Dockerfile
FROM python:3.8

WORKDIR /app

# Erforderliche Pakete installieren
RUN apt-get update && apt-get -y install cron vim

# Python-Abhängigkeiten installieren
RUN pip install pandas sqlalchemy mysqlclient python-dotenv

COPY data/ /app/data/
COPY csv_to_db.py /app/csv_to_db.py
COPY .env /app/ 
COPY start.sh /app/start.sh
# Das Cron-Verzeichnis erstellen
RUN mkdir -p /etc/cron.d

# Berechtigungen für den Cron-Job festlegen
RUN chmod 0644 /etc/cron.d
CMD ["bash", "/app/start.sh"]
