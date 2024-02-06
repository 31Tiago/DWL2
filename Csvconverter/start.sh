#!/bin/bash
# Füge den initialen Startbefehl hier ein, falls benötigt
/usr/local/bin/python /app/csv_to_db.py

# Füge den Cron-Job für alle 12 Stunden hinzu und leite die Ausgabe in eine Datei
echo "* */12 * * * root /usr/local/bin/python /app/csv_to_db.py > /app/data/cron.log 2>&1" > /etc/cron.d/csv-cron

# Starte den Cron-Daemon
cron && tail -f /app/data/cron.log
