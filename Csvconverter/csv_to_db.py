import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, ARRAY, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta
from dateutil.easter import easter
import smtplib
from email.mime.text import MIMEText
import time
import glob

# Warte 10 Sekunden
time.sleep(10)

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Funktion zum Senden einer E-Mail mit einem Fehlerbericht
def send_error_email(error_message):
    # Gmail-Kontozugangsdaten
    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    # Empfänger-E-Mail-Adresse
    to_email = os.getenv('TO_EMAIL')

    # Einrichten des MIME
    message = MIMEText(error_message)
    message['Subject'] = 'Fehler im CSV-Konvertierungsskript'
    message['From'] = gmail_user
    message['To'] = to_email
    
    # Verbindung zum Gmail-Server herstellen
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Anmeldung am Gmail-Konto
    server.login(gmail_user, gmail_password)

    # E-Mail senden
    server.sendmail(gmail_user, to_email, message.as_string())

    # Server beenden
    server.quit()

# Funktion, um die neueste CSV-Datei im Verzeichnis zu erhalten
def get_latest_csv(directory):
    list_of_files = glob.glob(os.path.join(directory, '*.csv'))
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Verzeichnis, in dem die CSV-Dateien gespeichert sind
csv_directory = '/app/data'

# Die neueste CSV-Datei abrufen
csv_file = get_latest_csv(csv_directory)

# CSV-Datei lesen
try:
    df = pd.read_csv(csv_file, sep=';', quotechar='"', skiprows=1 , na_filter=False)
except Exception as e:
    # Wenn ein Fehler auftritt, sende eine E-Mail mit dem Fehlerbericht
    error_message = f"Fehler beim Lesen der CSV-Datei:\n{str(e)}"
    send_error_email(error_message)
    # Skript beenden oder Fehler entsprechend behandeln
    exit()

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'Mitarbeiterdaten'
    id = Column(Integer, primary_key=True)
    Vorname = Column(String(255))
    Nachname = Column(String(255))
    Anstelldatum = Column(Date)
    Geburtstag = Column(Date)
    NextBirthdayWorkday = Column(Date)
    NextHireDateWorkday = Column(Date)

# MySQL-Datenbankverbindung
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
mysql_db = os.getenv('MYSQL_DATABASE')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')

# SQLAlchemy-Engine erstellen
engine = create_engine(f'mysql+mysqldb://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}')
Base.metadata.create_all(engine)

# Sitzung erstellen
Session = sessionmaker(bind=engine)
session = Session()

# Alle vorhandenen Datensätze in der Tabelle löschen
session.query(Employee).delete()

# Setzen des Auto-Increment-Werts auf 1 zurück
session.execute(text('ALTER TABLE Mitarbeiterdaten AUTO_INCREMENT = 1'))

# Regulärer Ausdruck zum Abgleichen verschiedener Datumsformate
date_formats = ['%d.%m.%Y', '%d-%m-%Y', '%Y-%m-%d', '%Y.%m.%d']

# Beispiel für Feiertage
def calculate_holidays():
    # Aktuelles Jahr ermitteln
    current_year = datetime.now().year
    
    # Berechnen von Ostern
    easter_date = easter(current_year)
    
    # Ableitung anderer Feiertage
    karfreitag = easter_date - timedelta(days=2)
    ostermontag = easter_date + timedelta(days=1)
    christi_himmelfahrt = easter_date + timedelta(days=39)
    pfingstmontag = easter_date + timedelta(days=50)
    fronleichnam = easter_date + timedelta(days=60)

    # Festlegung der Feiertage in NRW, an denen nicht gearbeitet wird
    nrw_feiertage = [
        datetime(current_year, 1, 1).date(),  # Neujahr
        karfreitag,                    # Karfreitag
        ostermontag,                   # Ostern - Ostermontag
        datetime(current_year, 5, 1).date(),  # 1. Mai - Tag der Arbeit
        christi_himmelfahrt,          # Christi Himmelfahrt
        pfingstmontag,                # Pfingsten - Pfingstmontag
        fronleichnam,                 # Fronleichnam
        datetime(current_year, 10, 3).date(), # Tag der Deutschen Einheit
        datetime(current_year, 12, 25).date(),# 1. Weihnachtsfeiertag
        datetime(current_year, 12, 26).date() # 2. Weihnachtsfeiertag


        #datetime(current_year, ?, ?).date() # selbst Feiertag einstellen
    ]

    # Liste der Feiertage zurückgeben
    return nrw_feiertage
feiertage = calculate_holidays()

def is_weekend(date):
    return date.weekday() >= 5

def next_workday(date, holidays):
    current_year = datetime.now().year  # Aktuelles Jahr
    current_date = datetime(current_year, date.month, date.day).date()  # Aktuelles Datum mit dem gleichen Tag und Monat, aber im aktuellen Jahr
    if not is_weekend(current_date) and current_date not in holidays:
        return current_date
    
    next_day = current_date + timedelta(days=1)
    while True:
        if not is_weekend(next_day) and next_day not in holidays:
            return next_day
        next_day += timedelta(days=1)

# Iteriere durch das DataFrame und füge Daten in die Datenbank ein
for index, row in df.iterrows():
    Vorname = str(row.get('Vorname', '')).strip()
    Nachname = str(row.get('Nachname', '')).strip()
    Anstelldatum_str = row.get('Anstelldatum', '')
    Anstelldatum = None
    Geburtstag_str = row.get('Geburtstag', '')
    Geburtstag = None

    try:
        if not Vorname or not Nachname:  # Überprüfe, ob Vorname oder Nachname leer sind
            raise ValueError("Vorname oder Nachname ist leer")

        if not Anstelldatum_str:
            raise ValueError("Anstelldatum ist leer")

        # Versuche, Anstelldatum mit verschiedenen Datumsformaten zu parsen
        for date_format in date_formats:
            try:
                Anstelldatum = datetime.strptime(Anstelldatum_str, date_format).date()
                break  # Sobald ein gültiges Datumsformat gefunden ist, aufhören zu versuchen
            except ValueError:
                continue  # Das nächste Datumsformat versuchen

        if not Anstelldatum:
            raise ValueError("Ungültiges Anstelldatum-Format")

        if not Geburtstag_str:
            raise ValueError("Geburtsdatum ist leer")

        # Versuche, Geburtstag mit verschiedenen Datumsformaten zu parsen
        for date_format in date_formats:
            try:
                Geburtstag = datetime.strptime(Geburtstag_str, date_format).date()
                break  # Sobald ein gültiges Datumsformat gefunden ist, aufhören zu versuchen
            except ValueError:
                continue  # Das nächste Datumsformat versuchen

        if not Geburtstag:
            raise ValueError("Ungültiges Geburtsdatum-Format")

        # Berechnung des nächsten Arbeitstags für Geburtstag und Anstellungsdatum
        
        next_birthday_workday = next_workday(Geburtstag, feiertage)
        next_hiredate_workday = next_workday(Anstelldatum, feiertage)
        
        # Mitarbeiterobjekt erstellen und hinzufügen
        employee = Employee(
            Vorname=Vorname,
            Nachname=Nachname,
            Anstelldatum=Anstelldatum,
            Geburtstag=Geburtstag,
            NextBirthdayWorkday=next_birthday_workday,
            NextHireDateWorkday=next_hiredate_workday
        )
        
        session.add(employee)

    except ValueError as e:
        error_message = f"Fehler beim Verarbeiten von Zeile {index + 2}: {e}"
        send_error_email(error_message)

# Änderungen an der Datenbank bestätigen
session.commit()
session.close()
