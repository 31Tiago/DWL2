$aHolidayList = [
    '01.01.' => 'Neujahr',
    '06.01.' => 'Hl. drei Könige',
    'E-1'    => 'Test -1',
    'E+0'    => 'Ostersonntag',
    'E+1'    => 'Ostermontag',
    '01.05.' => 'Staatsfeiertag',
    'E+39'   => 'Christi Himmelfahrt',
    'E+50'   => 'Pfingstmontag',
    'E+60'   => 'Fronleichnam',
    '15.08.' => 'Maria Himmelfahrt',
    '26.10.' => 'Nationalfeiertag',
    '01.11.' => 'Allerheiligen',
    '08.12.' => 'Maria Empfängnis',
    '24.12.' => 'Heilig Abend',
    '25.12.' => 'Christtag',
    '26.12.' => 'Stefanitag',
    '31.12.' => 'Silvester'
 ];

date_default_timezone_set('Europe/Berlin');
$dtEaster = new DateTime();
$year = $dtEaster->format('Y'); // aktuelles jahr
$dtEaster = $dtEaster->setTimestamp( easter_date($year) ); // ostersonntag heuer 27.03.2016

$format = 'd.m.Y';

foreach ($aHolidayList as $dateExpr => $desc) {
    if ( strpos($dateExpr, 'E') === 0 ) {
        $dateExpr = ltrim($dateExpr, 'E');
        $dtCurr = clone $dtEaster;
        echo $dtCurr->modify($dateExpr.' day')->format($format). " -- " . $desc . "<br>";
    } else {
        echo (new DateTime($dateExpr.$year))->format($format). " -- " . $desc . "<br>";
    }
} 