<?php

// Verbindungsinformationen für die MySQL-Datenbank
$host = "localhost";
$port = 6035;
$user = "admin";
$password = "admin";
$database = "app_db";

// Pfad zur CSV-Datei
$csvFilePath = "./Personio_dwl-rheine_employees_2023-12-12.csv";

// Verbindung zur MySQL-Datenbank herstellen
$mysqli = new mysqli($host, $user, $password, $database, $port);

// Überprüfe die Verbindung
if ($mysqli->connect_error) {
    die("Verbindung zur MySQL-Datenbank fehlgeschlagen: " . $mysqli->connect_error);
}

// CSV-Datei öffnen und Daten in die Datenbank einfügen
if (($handle = fopen($csvFilePath, "r")) !== false) {
    // Lese den Header der CSV-Datei
    $header = fgetcsv($handle);

    // Erstelle die Tabelle basierend auf dem Header der CSV-Datei
    $tableCreationQuery = "CREATE TABLE IF NOT EXISTS data (";

    foreach ($header as $field) {
        $tableCreationQuery .= "`$field` VARCHAR(255), ";
    }

    $tableCreationQuery = rtrim($tableCreationQuery, ", ") . ")";
    $mysqli->query($tableCreationQuery);

    // Füge Daten in die Tabelle ein
    while (($data = fgetcsv($handle)) !== false) {
        $insertQuery = "INSERT INTO data (`" . implode("`, `", $header) . "`) VALUES ('" . implode("', '", $data) . "')";
        $mysqli->query($insertQuery);
    }

    fclose($handle);
    echo "Daten erfolgreich in die MySQL-Datenbank eingefügt.";
} else {
    echo "Fehler beim Öffnen der CSV-Datei.";
}

// Schließe die Verbindung zur Datenbank
$mysqli->close();

?>