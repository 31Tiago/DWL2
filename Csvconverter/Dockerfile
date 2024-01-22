# Dockerfile
FROM python:3.8

WORKDIR /app
RUN pip install pandas sqlalchemy mysqlclient

COPY csv_to_db.py /app/
RUN mkdir /app/data  # Make sure this directory matches the one you are mounting

# Verwenden Sie 'mysqlclient' anstelle von 'MySQLdb'
RUN pip install pandas sqlalchemy mysqlclient

CMD ["python", "csv_to_db.py"]