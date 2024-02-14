<?php
$host = 'db';
$user = 'admin';
$pass = 'admin';
$dbname = 'app_db'; // Ersetzen Sie dies durch den tatsächlichen Namen Ihrer Datenbank

$conn = mysqli_connect($host, $user, $pass, $dbname);
if (!$conn) {
    exit('Connection failed: '.mysqli_connect_error().PHP_EOL);
}
mysqli_set_charset($conn, 'utf8');

// SQL-Befehl mit dem erhaltenen Geburtsdatum ausführen (parametrisierte Abfrage)
$sql = "SELECT * FROM Mitarbeiterdaten";
$result = mysqli_query($conn, $sql);

if ($result) {
    while ($row = mysqli_fetch_assoc($result)) {
        echo "<p>" . $row['MitarbeiterID']." ".$row['Vorname']." ".$row['Nachname']." ".$row['Anstelldatum']." ".$row['Geburtstag'] . "</p>";
    }
} else {
    echo "Fehler bei der Abfrage: ".mysqli_error($conn);
}
?>
