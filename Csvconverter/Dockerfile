# Dockerfile
FROM python:3.8

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get -y install cron vim

# Install Python dependencies
RUN pip install pandas sqlalchemy mysqlclient python-dotenv

COPY data/ /app/data/
COPY csv_to_db.py /app/
COPY .env /app/ 
COPY start.sh /app/start.sh
# Create the cron directory
RUN mkdir -p /etc/cron.d
# Create the log directory and file
RUN mkdir -p /var/log && touch /var/log/cron.log
# Set permissions for the cron job
RUN chmod 0644 /etc/cron.d
CMD ["bash", "/app/start.sh"]