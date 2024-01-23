document.addEventListener("DOMContentLoaded", function () {
    // DOM ist vollständig geladen

    // Feiertage von der PHP-Datei abrufen
    fetch('feiertage.php')
        .then(response => response.text())
        .then(data => {
            // Daten in den Container einfügen
            document.getElementById('feiertageContainer').innerHTML = data;
        })
        .catch(error => console.error('Fehler beim Abrufen der Feiertage:', error));
});
