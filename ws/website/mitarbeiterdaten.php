<?php
$host = 'db';
$user = 'admin';
$pass = 'admin';
$dbname = 'app_db';

$conn = mysqli_connect($host, $user, $pass, $dbname);
if (!$conn) {
    exit('Connection failed: '.mysqli_connect_error().PHP_EOL);
}
mysqli_set_charset($conn, 'utf8');

// SQL-Befehl, um nur die Mitarbeiter mit heutigem Geburtstag abzurufen
$today = date('m-d'); // Das aktuelle Datum im Format MM-DD
$sql_birthday = "SELECT * FROM Mitarbeiterdaten WHERE DATE_FORMAT(Geburtstag, '%m-%d') = '$today'";
$result_birthday = mysqli_query($conn, $sql_birthday);

// SQL-Befehl, um nur die Mitarbeiter mit heutigem Anstellungsdatum abzurufen
$sql_start_today = "SELECT * FROM Mitarbeiterdaten WHERE DATE_FORMAT(Anstelldatum, '%m-%d') = '$today'";
$result_start_today = mysqli_query($conn, $sql_start_today);

if (!$result_birthday || !$result_start_today) {
    echo "Fehler bei der Abfrage: ".mysqli_error($conn);
    exit();
}

// Schriftstil für die Mitarbeiter, die heute angestellt wurden
$font_style = "font-family: Arial, sans-serif;";

// Liste von Geburtstagswünschen
$birthday_quotes = array(
    "Herzlichen Glückwunsch zum Geburtstag! 🎉",
    "Alles Gute zum Geburtstag! 🎂",
    "Ein weiteres Jahr älter, ein weiteres Jahr weiser! Happy Birthday! 🥳"
);

// Liste von Sprüchen für neue Mitarbeiter
$start_quotes = array(
    "Happy Jahrestag im Team! 🎉 Ein Jahr großartiger Zusammenarbeit und Erfolge!",
    "Herzlichen Glückwunsch zum Firmenjubiläum im Team! 🌟",
    "Ein Jahr voller wertvoller Beiträge und Engagement! Herzlichen Glückwunsch zum Jahrestag im Team! 🎈"
);

// Wähle einen zufälligen Geburtstagsspruch aus
$random_birthday_quote = $birthday_quotes[array_rand($birthday_quotes)];

// Wähle einen zufälligen Spruch für neue Mitarbeiter aus
$random_start_quote = $start_quotes[array_rand($start_quotes)];

// Nachricht für Geburtstagswünsche
$birthday_message = "";

if(mysqli_num_rows($result_birthday) > 0) {
    $birthday_message = "<p style='$font_style;font-size: 18px;'>🎉 $random_birthday_quote 🎉:</p>";
    while ($row = mysqli_fetch_assoc($result_birthday)) {
        $birthday_message .= "<p style='$font_style;font-size: 16px;'>" . $row['MitarbeiterID']." ".$row['Vorname']." ".$row['Nachname'] . "</p>";
    }
}

// Ausgabe der Geburtstagsnachricht, falls vorhanden
echo $birthday_message;

// Nachricht für neue Mitarbeiter am heutigen Tag
if(mysqli_num_rows($result_start_today) > 0) {
    echo "<p style='$font_style;font-size: 16px;'>🎉 $random_start_quote 🎉:</p>";
    while ($row = mysqli_fetch_assoc($result_start_today)) {
        echo "<p style='$font_style;font-size: 16px;'>" . $row['MitarbeiterID']." ".$row['Vorname']." ".$row['Nachname'] . "</p>";
    }
}

// Ausgabe, falls heute weder Geburtstag noch Einstellungstag ist
if (empty($birthday_message) && mysqli_num_rows($result_start_today) == 0) {
    echo "<p style='$font_style;font-size: 16px;'>Heute hat niemand Geburtstag und es wurden auch keine Mitarbeiter eingestellt.</p>";
}
?>
