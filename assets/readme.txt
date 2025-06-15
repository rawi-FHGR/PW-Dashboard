*************************************************
PERSONENWAGEN-DASHBOARD
Web: https://pw-dashboard.onrender.com
Github: https://github.com/rawi-FHGR/PW-Dashboard
*************************************************


## PROJEKTBESCHREIBUNG

Bereitstellung eines interaktiven Dashboards zur Visualisierung und Analyse der Bestände und der Inverkehrsetzungen von Personenwagen nach Treibstoffarten, absolut und pro 1000 Personen. Für alle Gemeinden und Kantone der Schweiz im Zeitraum zwischen 2010 und 2024. Erstellt mit **Python** und **Dash** unter Verwendung von **plotly.express** zur Visualisierung der Daten.

Autoren: Ralph Wildhaber, Lukas Temperli, Raphael Weiss


## ZIELGRUPPE DES DASHBOARDS

Das Dashboard richtet sich an Behörden, Forschende, Unternehmen sowie die interessierte Öffentlichkeit. Es dient der Planung, Analyse und Information in den Bereichen Mobilität, Verkehr, Umwelt und Wirtschaft.


## DATENQUELLEN / DATENBERECHNUNG 

Bundesamt für Statistik (BFS), bfs.admin.ch
1) Daten zu den eingelösten Strassenfahrzeugen, 2010-2024
** BFS-Nummer: px-x-1103020100_111 (Bestand), px-x-1103020200_121 (Neue Inverkehrsetzungen) **
2) Ständige Wohnbevölkerung auf Gemeindeebene, 2010-2023 (!) 
** BFS-Nummer:px-x-0102010000_101 **
3) Basisgeometrien (für Kantons- und Gemeindegrenzen)
** Link: https://www.bfs.admin.ch/bfs/de/home/statistiken/regionalstatistik/kartengrundlagen/basisgeometrien.html (Kartenset 2024) **

(!) Um die Personenwagendichte zu rechnen, wird die Berechnungsweise vom Bundesamt für Statistik verwendet:
Die Personenwagendaten (Stand jeweils Ende September) werden mit der letztjährigen ständigen Wohnbevölkerung (Stand jeweils Ende Dezember des Vorjahres) dividiert. 

(!) Folgende Gemeindefusionen von 2024 müssen beim Bevölkerungsdatensatz vorgenommen werden, damit er mit den Personenwagendaten zusammengeführt werden kann:
- 947 Zwieselberg fusionierte mit 767 Reutigen
- 2456 Lüterswil-Gächliwil fusionierte mit 2465 Buchegg
- 4042 Turgi fusionierte mit 4021 Baden
- 993 Wangenried fusionierte mit 992 Wangen an der Aare
- 6773 Beurnevésin und 6775 Bonfol fusionierten zur neuen Gemeinde 6812 Basse-Vendline (Jura)


## DATENAUSWAHL

Folgende Daten werden im Dashboard berücksichtigt:

Fahrzeuggruppen nach BFS        | Im Dashboard enthalten
--------------------------------|-------------------------
Personenwagen                   | JA 
Personentransportfahrzeuge      | -
Sachentransportfahrzeuge        | -
Landwirtschaftsfahrzeuge        | -
Industriefahrzeuge              | -
Motorräder                      | -
Anhänger                        | -

Personenwagen machen den grössten Teil des Fahrzeugbestands aus und sind für Trends in Motorisierung und Antriebsarten besonders relevant. Daher konzentriert sich das Dashboard auf diese Fahrzeuggruppe.

Treibstoffarten nach BFS:
Code  | Bezeichnung
------|----------------------------------------------------
1     | Andere
2     | Benzin
3     | Benzin-elektrisch: Normal-Hybrid
4     | Benzin-elektrisch: Plug-in-Hybrid
5     | Diesel
6     | Diesel-elektrisch: Normal-Hybrid
7     | Diesel-elektrisch: Plug-in-Hybrid
8     | Elektrisch
9     | Gas (mono- und bivalent)
10    | Ohne Motor
11    | Wasserstoff

Aggregierte Treibstoffkategorien für Dashboard:
Kategorie   | Umfassende Codes
------------|-------------------------
Benzin      | 2
Diesel      | 5
Hybrid      | 3, 4, 6, 7
Elektrisch  | 8
Andere      | 1, 9, 10, 11


## VISUALISIERUNGEN MIT ZIEL

| Visualisierung                  | Ziel                                                                  |
|---------------------------------|-----------------------------------------------------------------------|
| 1) Schweizerkarte               | 1) Übersicht nach Kantonen                                            |
| 2) Kantonskarten mit Gemeinden  | 2) Ermöglicht Analyse auf Gemeindeebene                               |
| 3) Barchart: Anteil Treibstoffe | 3) Zeitlicher Verlauf für die Schweiz bzw. für den ausgewählten Kanton|
| 4) Piechart: Anteil Treibstoffe | 4) Prozentuale Verteilung nach Treibstoffart für das ausgewählte Jahr |
| 5) Textblock/Tabelle            | 5) Absolute Werte nach Treibstoffart, inkl. Total                     |
|---------------------------------|-----------------------------------------------------------------------|


## LAYOUT MIT ERLÄUTERUNGEN

| Ebene | Erläuterungen zum Inhalt, inkl. Funktionalitäten                                                     |
|-------|------------------------------------------------------------------------------------------------------|
| Tab   | Auswahl-Möglichkeit zwischen Bestandeszahlen (Default) oder Zahlen zu den neu Inverkehrsetzungen     |
|       | Tab 1: Bestand / Tab 2: Inverkehrsetzungen; die beiden Tabs sind identisch aufgebaut.                |
|       | Dies ermöglicht eine schnelle Orientierung und einfache Vergleichsmöglichkeit.                       |
|-------|------------------------------------------------------------------------------------------------------|
| Oben  | Zusätzliche Interaktionsmöglichkeit: Home-Button (Defaulteinstellungen), Jahresslider (Default: 2024)|
|       | und Auswahl "absolut" oder "relativ(pro 1000 Personen)" (Default)                                    |
|-------|------------------------------------------------------------------------------------------------------|
| Mitte | Schweizerkarte mit **Hover- und Klickfunktionalität** und allgemeine Hinweise zur Benutzung          |
|       | (Default) bzw. Kantonskarte mit Gemeinden mit **Hoverfunktionalität**, zoombar                       |
|-------|------------------------------------------------------------------------------------------------------|
| Unten | Diagramme (Barchart): Auffschlüsselung nach Treibstoffart mit **Hoverfunktionalität**                |
|       | Diagramme (Piechart): Historisch (Default: Schweiz) und für das ausgewählte Jahr (Default: 2024)     |
|       | Textblock/Tabelle: Übersicht mit den absolute Werten, inkl. Total (Default: Schweiz)                 |
|-------|------------------------------------------------------------------------------------------------------|

Dieses Layout führt entsprechend der gewohnten Leserichtung vom Allgemeinen oben links (Schweizerkarte mit Totalwerten nach Kanton) zu den Detaildaten unten (Aufschlüsselung nach Treibstoffarten und Kanton) und seitlich rechts (Aufschlüsselung nach Gemeinden). 

Das Layout besitzt ein responsive Design, wurde jedoch primär für den Desktop konzipiert.


## Interaktionen

- Klickfunktionalität: Schweizerkarte, Homebutton, Umstellung absolut/relativ (pro 1000 Einwohner), Tab (Bestand, Inverkehrsetzungen)
- Hoverfunktionalität: Schweizerkarte, Kantonskarte, Barchart, Piechart
- Sliderfunktionalität: Jahreszahlen


## Farbwahl

- Karten: monochromer Farbskala, sequentielle Daten (Viridis, barrierefrei) 
- Treibstoff-Diagramme: diskrete Farbskala, kategoriale Daten (barrierefrei) 


## METADATEN IM DASHBOARD

Im Dashboard sind folgende Metainformationen sichtbar:
- Datenquelle
- Hinweise zu Auffälligkeiten (Tooltips bei Diagrammen)


## Limitationen in der Dateninterpretation

Die Fahrzeugstatistik basiert auf dem sogenannten Halteradressenprinzip. Das Bundesamt für Statistik ordnet ein Fahrzeug der Gemeinde zu, in der die Halterin oder der Halter gemeldet ist. Diese Adresse entspricht nicht zwangsläufig dem tatsächlichen Standort des Fahrzeugs. Gerade bei Unternehmen wird oft der Hauptsitz als Halteradresse erfasst – unabhängig davon, wo die Fahrzeuge tatsächlich unterwegs sind und in welchem Kanton das Kontrollschild ausgestellt wurde.


## Technische Limitationen 

Die Quellendaten werden vom BFS als px-Dateien bereitgestellt. Die Überführung in das für die Datenverarbeitung etwas handlichere csv-Format erfolgt ausserhalb des Dashboards. Zudem wäre es in einer weiteren Ausbaustufe sinnvoll, die Quelldaten direkt in einer Datenbank abzulegen.


## Mögliche Ausbauschritte

- Diagramme für jede Gemeinde (untere Ebene): Die Aufschlüsselung nach der Treibstoffart auf Gemeindeebene könnte beispielsweise Unterschiede im Elektrifizierungsgrad nach Siedlungsstruktur aufzeigen. 
- Weitere Fahrzeugkategorien (als zusätzliches Auswahlelement): Allerdings fraglicher Zusatznutzen im Hinblick auf das Ziel des Dashboards (siehe oben) 


## Feedback/Verbesserungsideen aus der Demo/Tag 7

a) Der Jahresslider zeigte keine Ticks, was die Auswahl eines bestimmten Jahres erschwerte. Zudem erzeugte die farbliche Hervorhebung des linken Bereichs den Eindruck einer kumulierten Darstellung.
b) Die Kantonskarte war bei vielen Gemeinden zu klein, nicht zoombar und die Grenzen schwer erkennbar – insbesondere bei ähnlichen Farbwerten.
c) Die zentrale Platzierung von Home-Button, Jahresslider und der Auswahl „absolut/relativ“ wurde hinterfragt.
d) Die Farbwahl für Treibstoffe wurde kritisiert: Zwar barrierefrei, aber ohne assoziativen Bezug zu den Treibstoffarten.
e) Texte, inkl. Metainformationen, waren teils zu klein und wenig aussagekräftig.
f) Der verfügbare Platz würde zusätzliche Informationen wie Tendenzen (z. B. mit Pfeilen) erlauben.
g) Es wurde vorgeschlagen, beim Jahresslider ein individuelles Startjahr wählen zu können.


## Umsetzung Feedback aus der Demo/Tag 7

a) Jahresticks wurden ergänzt und die Flächenfärbung entfernt.
b) Die Karte ist nun zoombar; Gemeindegrenzen werden durch weisse Linien hervorgehoben.
c) Eine Platzierung unterhalb der Tabs wurde auf Basis des Feedbacks geprüft und mehrheitlich als intuitiver bewertet. Der zunächst befürchtete Verlust der visuellen Trennung zur detaillierten Treibstoffauswertung hat sich aufgrund der klaren visuellen Struktur als unbegründet erwiesen.
d) Die Farbpalette wurde angepasst, um stärkeren Bezug zu den Treibstoffarten herzustellen, ohne die Barrierefreiheit aufzugeben:   
   - Benzin: Hellgrau (Assoziation: Technisch, traditionell, veraltet)
   - Diesel: Dunkelbraun (Assoziation: Schwer, schmutzig) 
   - Hybrid: Olivgelb (Assoziation: Mischung aus Grün (Nachhaltigkeit) und Gelb (Vorsicht, nur Teilumstieg)) 
   - Elektro: Türkis (Assoziation: Mischung aus Blau (Technologie) und Grün (Nachhaltigkeit), frisch, sauber, modern)
   - Andere: Blau (Assoziation: Wasser, Reinheit, Hightech)
e) Texte wurden teils vergrössert und inhaltlich präzisiert.
f) Die Darstellung von Tendenzen wird als klarer Mehrwert gesehen und wäre wünschenswert. Die technische Umsetzung ist jedoch mit grösserem Aufwand verbunden und wurde daher noch nicht realisiert.
g) Aus Zeitgründen nicht umgesetzt. Zudem ist der Mehrwert begrenzt, da lediglich einzelne Jahre aus der Darstellung ausgeschlossen würden. Nur bei kumulierten Werten über mehrere Jahre ergäbe es einen Mehrwert. Das Dashboard zeigt jedoch nur immer die Daten des aktuellen Jahres.


## Source Code
Der Source Code für diese Dashboard ist in einem privaten Repository verwaltet: https://github.com/rawi-FHGR/PW-Dashboard.git
Im Abgabe-Bereich innerhalb des Moodle-Moduls 'Dashboard-Design' wurde der Source-Code in einem zip-Paket hochgeladen.

## Publiziertes Dashboard
Das Personenwagen-Dashboard wurde publiziert und ist öffentlich zugänglich: https://pw-dashboard.onrender.com/

Viel Spass!
