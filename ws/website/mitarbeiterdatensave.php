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
$sql_birthday = "SELECT *, DATE_FORMAT(Geburtstag, '%m-%d') AS GeburtstagFormatted FROM Mitarbeiterdaten WHERE DATE_FORMAT(NextBirthdayWorkday, '%m-%d') = '$today'";
$result_birthday = mysqli_query($conn, $sql_birthday);

// SQL-Befehl, um nur die Mitarbeiter mit heutigem Anstellungsdatum abzurufen
$sql_start_today = "SELECT *, DATE_FORMAT(Anstelldatum, '%m-%d') AS AnstelldatumFormatted FROM Mitarbeiterdaten WHERE DATE_FORMAT(NextHireDateWorkday, '%m-%d') = '$today'";
$result_start_today = mysqli_query($conn, $sql_start_today);

if (!$result_birthday || !$result_start_today) {
    echo "Fehler bei der Abfrage: ".mysqli_error($conn);
    exit();
}

// Schriftstil für die Mitarbeiter, die heute angestellt wurden
$font_style = "font-family: Arial, sans-serif;";

// Nachricht für Geburtstagswünsche
$birthday_message = "";

if(mysqli_num_rows($result_birthday) > 0) {
    while ($row = mysqli_fetch_assoc($result_birthday)) {
        // Überprüfen, ob der Geburtstag heute ist
        if ($row['GeburtstagFormatted'] == $today) {
            $birthday_message .= "<p style='$font_style;font-size: 20px;'>🎉 Herzlichen Glückwunsch ".$row['Vorname']." ".$row['Nachname']."! 🎉</p>";
        } else {
            // Geburtstag des Mitarbeiters
            $geburtstag = date_create_from_format('m-d', date('m-d', strtotime($row['Geburtstag'])));
            $heute = date_create_from_format('m-d', date('m-d'));
            $tage = $heute->diff($geburtstag)->format('%a');
            $birthday_message .= "<p style='$font_style;font-size: 20px;'>🎉 Herzlichen Glückwunsch nachträglich zu Ihrem Geburtstag, ".$row['Vorname']." ".$row['Nachname']." vor ".$tage." Tagen! 🎉</p>";

        }
    }
}

// Ausgabe der Geburtstagsnachricht, falls vorhanden
echo $birthday_message;

// Ausgabe, falls heute weder Geburtstag noch Einstellungstag ist
if (mysqli_num_rows($result_start_today) == 0 && empty($birthday_message)) {
    echo "<p style='$font_style;font-size: 20px;'>Heute hat niemand Geburtstag und es wurden auch keine Mitarbeiter eingestellt.</p>";
}


// Nachricht für neue Mitarbeiter am heutigen Tag
// Nachricht für neue Mitarbeiter am heutigen Tag
if(mysqli_num_rows($result_start_today) > 0) {
    while ($row = mysqli_fetch_assoc($result_start_today)) {
        // Überprüfen, ob der Anstellungstag heute ist
        if ($row['AnstelldatumFormatted'] == $today) {
            // Berechne die Anzahl der Jahre seit dem Anstellungstag
            $anstelldatum = new DateTime($row['Anstelldatum']);
            $heute = new DateTime('now');
            $jahre = $heute->diff($anstelldatum)->y;
            echo "<p style='$font_style;font-size: 20px;'>🎉 Herzlichen Glückwunsch zu Ihrem $jahre jährigen Betriebsjubiläum in unserem Unternehmen, ".$row['Vorname']." ".$row['Nachname']."! Danke für Ihre Arbeit seit dem: ".$anstelldatum->format('d.m.Y')."! 🎉</p>";
        } else {
            // Berechne die Anzahl der Jahre seit dem Anstellungstag
            $anstelldatum = new DateTime($row['Anstelldatum']);
            $heute = new DateTime('now');
            $jahre = $heute->diff($anstelldatum)->y;
            echo "<p style='$font_style;font-size: 20px;'>🎉 Herzlichen Glückwunsch nachträglich zu Ihrem $jahre jährigen Betriebsjubiläum ".$row['Vorname']." ".$row['Nachname'].". Danke für Ihre Arbeit seit dem: ".$anstelldatum->format('d.m.Y')."! 🎉</p>";
        }
    }
}
?>
