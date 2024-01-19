# csv_to_db.py
import os
import pandas as pd
from sqlalchemy import create_engine

# CSV-Datei einlesen
csv_file = 'db/Personio_dwl-rheine_employees_2023-12-12.csv'
df = pd.read_csv(csv_file)

# Verbindung zur MySQL-Datenbank herstellen
mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
mysql_port = os.environ.get('MYSQL_PORT', '3306')
mysql_db = os.environ.get('MYSQL_DATABASE', 'app_db')
mysql_user = os.environ.get('MYSQL_USER', 'admin')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'admin')

engine = create_engine(f'mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}')

# Datenframe in die Datenbank schreiben
df.to_sql('deine_tabelle', con=engine, if_exists='replace', index=False)
