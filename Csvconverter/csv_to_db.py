import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# CSV-Datei einlesen
csv_file = '/app/data/Personio_dwl-rheine_employees_2023-12-12.csv'
#csv_file = '/app/data/Personio_dwl-rheine_employees_2023-12-12 (Kopie).csv'
df = pd.read_csv(csv_file, sep=';', quotechar='"', skiprows=1)

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'Mitarbeiterdaten'
    id = Column(Integer, primary_key=True)
    Vorname = Column(String(255))  # Specify a length for VARCHAR
    Nachname = Column(String(255))  # Specify a length for VARCHAR
    Anstelldatum = Column(Date)
    Geburtstag = Column(Date)

# Verbindung zur MySQL-Datenbank herstellen
mysql_host = 'db'
mysql_port = '3306'
mysql_db = 'app_db'
mysql_user = 'admin'
mysql_password = 'admin'

# Create the SQLAlchemy engine
engine = create_engine(f'mysql+mysqldb://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}')
Base.metadata.create_all(engine)

# Create the session
Session = sessionmaker(bind=engine)
session = Session()

# Lösche alle vorhandenen Datensätze in der Tabelle
session.query(Employee).delete()

# Setze den Auto-Increment-Wert auf 1 zurück
session.execute(text('ALTER TABLE Mitarbeiterdaten AUTO_INCREMENT = 1'))

# Iteriere durch das DataFrame und füge Daten in die Datenbank ein
for index, row in df.iterrows():
    Vorname = row.get('Vorname', '')
    Nachname = row.get('Nachname', '')
    Anstelldatum_str = row.get('Anstelldatum', '')
    Anstelldatum = datetime.strptime(Anstelldatum_str, '%d.%m.%Y').date() if Anstelldatum_str else None
    Geburtstag_str = row.get('Geburtstag', '')
    Geburtstag = datetime.strptime(Geburtstag_str, '%d.%m.%Y').date() if Geburtstag_str else None

    employee = Employee(
        Vorname=Vorname,
        Nachname=Nachname,
        Anstelldatum=Anstelldatum,
        Geburtstag=Geburtstag
    )
    
    session.add(employee)

# Commit the changes to the database
session.commit()
session.close()
