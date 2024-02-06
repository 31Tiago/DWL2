import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import time
import glob
import re

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

# Function to get the latest CSV file in the directory
def get_latest_csv(directory):
    list_of_files = glob.glob(os.path.join(directory, '*.csv'))
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Directory where the CSV files are stored
csv_directory = '/app/data'

# Get the latest CSV file
csv_file = get_latest_csv(csv_directory)

# CSV file reading
try:
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

# MySQL database connection
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
mysql_db = os.getenv('MYSQL_DATABASE')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')

# Create the SQLAlchemy engine
engine = create_engine(f'mysql+mysqldb://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}')
Base.metadata.create_all(engine)

# Create the session
Session = sessionmaker(bind=engine)
session = Session()

# Delete all existing records in the table
session.query(Employee).delete()

# Reset the Auto-Increment value to 1
session.execute(text('ALTER TABLE Mitarbeiterdaten AUTO_INCREMENT = 1'))

# Regular expression to match various date formats
date_formats = ['%d.%m.%Y', '%d-%m-%Y', '%Y-%m-%d', '%Y.%m.%d']


# Iterate through the DataFrame and insert data into the database
for index, row in df.iterrows():
    Vorname = str(row.get('Vorname', '')).strip()
    Nachname = str(row.get('Nachname', '')).strip()
    Anstelldatum_str = row.get('Anstelldatum', '')
    Anstelldatum = None
    Geburtstag_str = row.get('Geburtstag', '')
    Geburtstag = None

    try:
        if not Vorname or not Nachname:  # Check if Vorname or Nachname is empty
            raise ValueError("Vorname or Nachname is empty")

        if not Anstelldatum_str:
            raise ValueError("Anstelldatum is empty")

        # Try to parse Anstelldatum with different date formats
        for date_format in date_formats:
            try:
                Anstelldatum = datetime.strptime(Anstelldatum_str, date_format).date()
                break  # Stop trying once a valid date format is found
            except ValueError:
                continue  # Try the next date format

        if not Anstelldatum:
            raise ValueError("Invalid Anstelldatum format")

        if not Geburtstag_str:
            raise ValueError("Geburtsdatum is empty")

        # Try to parse Geburtstag with different date formats
        for date_format in date_formats:
            try:
                Geburtstag = datetime.strptime(Geburtstag_str, date_format).date()
                break  # Stop trying once a valid date format is found
            except ValueError:
                continue  # Try the next date format

        if not Geburtstag:
            raise ValueError("Invalid Geburtsdatum format")

        employee = Employee(
            Vorname=Vorname,
            Nachname=Nachname,
            Anstelldatum=Anstelldatum,
            Geburtstag=Geburtstag
        )
        
        session.add(employee)

    except ValueError as e:
        error_message = f"Error processing line {index + 2}: {e}"
        send_error_email(error_message)

# Commit the changes to the database
session.commit()
session.close()
