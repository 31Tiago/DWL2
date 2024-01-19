# Dockerfile
FROM python:3.8

WORKDIR /app

COPY csv_to_db.py /app/

# Verwenden Sie 'mysqlclient' anstelle von 'MySQLdb'
RUN pip install pandas sqlalchemy mysqlclient

CMD ["python", "csv_to_db.py"]