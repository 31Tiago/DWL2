document.addEventListener('DOMContentLoaded', function () {
    const animationContainer = document.getElementById('animation-container');

    // Simuliere das Einlesen der CSV-Daten (ersetze dies durch den tatsächlichen Ladevorgang)
    const csvData = `Name,Geburtsdatum
                     Max,Muster,01.01.1990
                     Maria,Muster,15.05.1985
                     John,Doe,20.11.2000`;

    // Funktion zum Parsen der CSV-Daten
    function parseCSV(csv) {
        const lines = csv.split('\n');
        const headers = lines[0].split(',');
        const data = [];

        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',');
            const entry = {};

            for (let j = 0; j < headers.length; j++) {
                entry[headers[j]] = values[j];
            }

            data.push(entry);
        }

        return data;
    }

    // Funktion zum Anzeigen der animierten Texte
    function displayAnimatedText(data) {
        data.forEach((entry, index) => {
            const animatedText = document.createElement('div');
            animatedText.classList.add('animated-text');
            animatedText.innerHTML = `<p>Name: ${entry.Name}</p><p>Geburtsdatum: ${entry.Geburtsdatum}</p>`;
            animationContainer.appendChild(animatedText);

            // Verzögere die Animation jedes Textelements
            setTimeout(() => {
                animatedText.style.opacity = '1';
                animatedText.style.transform = 'translateY(0)';
            }, index * 1000);
        });
    }

    // Daten parsen und anzeigen
    const parsedData = parseCSV(csvData);
    displayAnimatedText(parsedData);
});
