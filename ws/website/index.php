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
    echo "<!DOCTYPE html>";
    echo "<html lang=\"de\">";
    echo "<head>";
    echo "<meta charset=\"UTF-8\">";
    echo "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">";
    echo "<title>Geburtstagsliste</title>";
    echo "<style>";
    echo ".teil-1 {";
    echo "background-color: white;";
    echo "color: white;";
    echo "text-align: center;";
    echo "padding: 50px;";
    echo "}";
    echo ".teil-2 {";
    echo "background-color: #A5BCD4;";
    echo "color: white;";
    echo "text-align: center;";
    echo "padding: 50px;";
    echo "}";
    echo "</style>";
    echo "</head>";
    echo "<body>";
    echo "<div class=\"teil-1\">";
    echo "<center>";
    echo "<img src=\"background.png\" width=\"400\" height=\"\" alt=\"Hintergrundbild\">";
    echo "</center>";
    echo "</div>";
    echo "<hr>";
    echo "<div class=\"teil-2\">";
    echo "<h1> Herzlichen Glückwunsch zum Geburtstag ...🎉 </h1>";
    while ($row = mysqli_fetch_assoc($result)) {
        echo "<p>" . $row['MitarbeiterID']." ".$row['Vorname']." ".$row['Nachname']." ".$row['Anstelldatum']." ".$row['Geburtstag'] . "</p>";
    }
    echo "</div>";
    echo "</body>";
    echo "</html>";
} else {
    echo "Fehler bei der Abfrage: ".mysqli_error($conn);
}
?>
