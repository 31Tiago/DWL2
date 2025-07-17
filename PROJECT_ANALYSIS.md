# Project Analysis: Employee Birthday & Anniversary Management System

## Overview
This is a multi-service Docker-based application that manages employee data from CSV files and displays birthday/anniversary notifications on a web interface. The system consists of several containerized services working together to provide a complete employee celebration management solution.

## Architecture

### Services Overview
The application uses Docker Compose to orchestrate 6 services:

1. **CSV Converter Service** (`csv-converter`)
2. **MySQL Database** (`db`)
3. **Nginx Web Server** (`nginx`)
4. **PHP Application** (`php`)
5. **phpMyAdmin** (`phpmyadmin`)
6. **Portainer** (`portainer`)

### Service Details

#### 1. CSV Converter Service
- **Purpose**: Processes CSV files containing employee data and imports them into MySQL database
- **Technology**: Python 3.8
- **Key Features**:
  - Automated CSV processing every 12 hours via cron job
  - Flexible date format parsing (supports multiple date formats)
  - German holiday calculation (NRW holidays)
  - Next workday calculation for birthdays and hire dates
  - Email error notification system
  - Automatic database table reset and re-population

#### 2. MySQL Database
- **Purpose**: Stores employee data
- **Version**: MySQL 5.7
- **Database Structure**:
  - Table: `Mitarbeiterdaten` (Employee Data)
  - Fields: `id`, `Vorname` (First Name), `Nachname` (Last Name), `Anstelldatum` (Hire Date), `Geburtstag` (Birthday), `NextBirthdayWorkday`, `NextHireDateWorkday`

#### 3. Web Interface (Nginx + PHP)
- **Purpose**: Displays birthday and anniversary notifications
- **Features**:
  - Responsive HTML interface with confetti animations
  - Real-time employee celebration notifications
  - Automatic detection of today's birthdays and work anniversaries
  - Multilingual support (German)

## Key Functionality

### Data Processing Pipeline
1. **CSV Import**: Python script reads the latest CSV file from `/app/data/` directory
2. **Data Validation**: Validates employee names, dates, and formats
3. **Date Calculations**: Computes next workday for birthdays and hire dates considering:
   - Weekends (Saturday/Sunday)
   - German public holidays (NRW)
   - Easter-dependent holidays
4. **Database Update**: Clears existing data and imports fresh employee records
5. **Error Handling**: Sends email notifications for processing errors

### Holiday Calculation
The system includes comprehensive German holiday support:
- **Fixed Holidays**: New Year's Day, Labor Day, German Unity Day, Christmas
- **Easter-dependent**: Good Friday, Easter Monday, Ascension Day, Whit Monday, Corpus Christi
- **Automatic Year Calculation**: Updates holidays for current year

### Web Display Logic
- **Birthday Notifications**: Shows congratulations for employees with birthdays on current workday
- **Anniversary Notifications**: Displays work anniversary celebrations with years of service
- **Fallback Message**: Shows default message when no celebrations are due

## Technical Implementation

### CSV Data Structure
Expected CSV format (semicolon-separated):
```csv
sep=;
"Vorname";"Nachname";"Anstelldatum";"Geburtstag"
"Alexander";"Korsch";"02.02.2020";"2020.3.2"
```

### Supported Date Formats
- `%d.%m.%Y` (German format: 02.02.2020)
- `%d-%m-%Y` (Dash format: 02-02-2020)
- `%Y-%m-%d` (ISO format: 2020-02-02)
- `%Y.%m.%d` (Dot format: 2020.02.02)

### Database Schema
```sql
CREATE TABLE Mitarbeiterdaten (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Vorname VARCHAR(255),
    Nachname VARCHAR(255),
    Anstelldatum DATE,
    Geburtstag DATE,
    NextBirthdayWorkday DATE,
    NextHireDateWorkday DATE
);
```

## Configuration

### Environment Variables Required
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`
- `GMAIL_USER`, `GMAIL_PASSWORD`, `TO_EMAIL` (for error notifications)

### Port Mappings
- **Web Interface**: 8080:80
- **Database**: 6036:3306
- **CSV Converter**: 6037:6038
- **phpMyAdmin**: 8085:80
- **Portainer**: 9443:9443

## Strengths

1. **Comprehensive Date Handling**: Supports multiple date formats and German holidays
2. **Automated Processing**: Cron-based CSV processing every 12 hours
3. **Error Handling**: Email notifications for processing failures
4. **User-Friendly Interface**: Clean web interface with visual celebrations
5. **Containerized Architecture**: Easy deployment and scaling
6. **Database Management**: Includes phpMyAdmin for easy data management

## Areas for Improvement

1. **Security**: Database credentials are hardcoded in PHP files
2. **Error Recovery**: Limited error recovery mechanisms in CSV processing
3. **Scalability**: Single CSV file processing approach may not scale
4. **Logging**: Limited logging and monitoring capabilities
5. **Testing**: No apparent unit tests or automated testing
6. **Documentation**: Missing API documentation and deployment guides

## Deployment

The system can be deployed using:
```bash
docker-compose up -d
```

Access points:
- **Main Application**: http://localhost:8080
- **phpMyAdmin**: http://localhost:8085
- **Portainer**: https://localhost:9443

## Data Flow

1. CSV files are placed in `Csvconverter/data/` directory
2. Python script processes latest CSV file every 12 hours
3. Data is validated and imported into MySQL database
4. Web interface queries database for today's celebrations
5. Users see real-time birthday/anniversary notifications

This system provides a complete solution for employee celebration management with automated data processing and an intuitive web interface.