import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import time

time.sleep(5)
# Load environment variables from .env file
load_dotenv()

# Function to send an email with an error report
def send_error_email(error_message):
    
    # Gmail account credentials
    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    # Recipient email address
    to_email = os.getenv('TO_EMAIL')

    # Setup the MIME
    message = MIMEText(error_message)
    message['Subject'] = 'Error in CSV Converter Script'
    message['From'] = gmail_user
    message['To'] = to_email

    # Connect to the Gmail server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to the Gmail account
    server.login(gmail_user, gmail_password)

    # Send the email
    server.sendmail(gmail_user, to_email, message.as_string())

    # Quit the server
    server.quit()

# CSV-Datei einlesen
csv_file = '/app/data/Personio_dwl-rheine_employees_2023-12-12.csv'
#csv_file = '/app/data/Personio_dwl-rheine_employees_2023-12-12 (Kopie).csv'

try:
    # Try reading the CSV file
   
    df = pd.read_csv(csv_file, sep=';', quotechar='"', skiprows=1 , na_filter=False)
    
except Exception as e:
    # If an error occurs, send an email with the error report
    error_message = f"Error reading CSV file:\n{str(e)}"
    send_error_email(error_message)
    # Exit the script or handle the error as needed
    exit()

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
    Vorname = str(row.get('Vorname', '')).strip()
    Nachname = str(row.get('Nachname', '')).strip()
    Anstelldatum_str = row.get('Anstelldatum', '')
    Anstelldatum = None
    Geburtstag_str = row.get('Geburtstag', '')
    Geburtstag = None

    try:
        if not Vorname or not Nachname:  # Überprüfen Sie, ob Vorname oder Nachname leer sind
            raise ValueError("Vorname oder Nachname ist leer")

        if not Anstelldatum_str:
            raise ValueError("Anstelldatum ist leer")

        Anstelldatum = datetime.strptime(Anstelldatum_str, '%d.%m.%Y').date()

        if not Geburtstag_str:
            raise ValueError("Geburtsdatum ist leer")

        Geburtstag = datetime.strptime(Geburtstag_str, '%d.%m.%Y').date()

        employee = Employee(
            Vorname=Vorname,
            Nachname=Nachname,
            Anstelldatum=Anstelldatum,
            Geburtstag=Geburtstag
        )
        
        session.add(employee)

    except ValueError as e:
        error_message = f"Fehler beim Verarbeiten der Zeile {index + 2}: {e}"
        send_error_email(error_message)


# Commit the changes to the database
session.commit()
session.close()