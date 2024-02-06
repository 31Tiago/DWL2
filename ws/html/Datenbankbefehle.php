<?php
// Verbindung zur Datenbank herstellen (hier mit PDO)
$dsn = 'lockalhost:3306';
$username = 'admin';
$password = 'admin';

try {
    $pdo = new PDO($dsn, $username, $password);
    echo "Datenbankverbindung hergestellt!";
} catch (PDOException $e) {
    die("Verbindung zur Datenbank fehlgeschlagen: " . $e->getMessage());
}

// Beispiel-SQL-Befehl: Daten aus einer Tabelle abfragen
$sql = "SELECT * FROM MItarbeiterdaten";
$result = $pdo->query($sql);

// Überprüfen, ob Ergebnisse vorhanden sind
if ($result->rowCount() > 0) {
    // Ergebnisse ausgeben
    while ($row = $result->fetch(PDO::FETCH_ASSOC)) {
        echo "ID: " . $row
?>