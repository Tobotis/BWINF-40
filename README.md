# BWINF-40
Bearbeitung der 2. Runde des 40. Bundeswettbewerb für Informatik (2022)
## Bearbeitung: Aufgabe 3:
Severin hat heute in der Schule das Hexadezimalsystem kennengelernt. Er verwendet nun kurze
Stäbchen, um die sechzehn Ziffern darzustellen, wie in einer Siebensegmentanzeige. Für die
Darstellung einer Ziffer stehen also sieben Positionen zur Verfügung; jede Position ist entweder
durch ein Stäbchen belegt oder sie ist frei. Severin will nun das folgende, von der Lehrerin gestellte Rätsel lösen: Gegeben ist eine Hexadezimalzahl (kurz: Hex-Zahl) mit n Ziffern. Gesucht ist die größte Hex-Zahl mit der gleichen
Anzahl an Ziffern, die aus der gegebenen Zahl durch eine zusätzlich gegebene Maximalzahl an
Umlegungen erzeugt werden kann. „Umlegung“ bedeutet, ein Stäbchen von seiner bisherigen
Position an eine andere, bislang freie Position zu bewegen.
Eine einzelne Umlegung muss noch keine gültige Hex-Zahl ergeben, aber das Ergebnis nach
allen Umlegungen muss eine gültige Hex-Zahl in der Siebensegmentdarstellung sein. Zu keiner
Zeit darf die Darstellung einer Ziffer komplett „geleert“ werden. Die gegebene Maximalzahl an
Umlegungen muss nicht ausgeschöpft werden.
Hier ein Beispiel: Gegeben sind die Zahl D24 und die Maximalzahl an Umlegungen 3. Die
gesuchte Hex-Zahl ist EE4.
### Aufgabe
Schreibe ein Programm, das eine Hex-Zahl sowie die Maximalzahl m an Umlegungen einliest
und die größte Hexadezimalzahl ermittelt, die mit höchstens m Umlegungen erzeugt werden
kann. Das Programm soll nach jeder Umlegung den Zwischenstand, also die aktuelle Belegung
der Positionen ausgeben.
Wende dein Programm mindestens auf alle Beispiele an, die du auf den BWINF-Webseiten
findest, und dokumentiere die Ergebnisse.
## Bearbeitung: Aufgabe 4:
Zara Zackig hat inzwischen große Karriere gemacht und ihre eigene Informatikfirma aufgebaut,
wobei sie ihre Leidenschaft zur Kryptographie erfolgreich einsetzen konnte. Diese beschäftigt
sie auch privat, was ihr folgendes Problem bereitete:
Zara besitzt jetzt zehn Ferienhäuser die sie zyklisch jedes Wochenende aufsucht. Zur Zugangskontrolle verwendet sie ein selbstentworfenes System, das Lochkarten mit 128 Positionen verwendet. Jede Lochkarte kann also ein beliebiges 128 Bits umfassendes Codeword darstellen.
Für ihre zehn Häuser stellte sie zehn Karten mit zufällig generierten Codewörten her, sortierte
sie anschließend aufsteigend als w1,...,w10 und codierte die Schlösser der zehn Häuser, wobei
Haus k das Codewort wk erhielt.
Nach einiger Zeit bekam Zara aber Angst, dass eine Karte auf dem Weg verloren gehen könnte.
Die meisten Menschen hätten jetzt wahrscheinlich einfach Kopien der Karten an einem sicheren Platz hinterlegt. Nicht so Zara! Sie stellte nur eine zusätzliche Karte her, deren Bitmuster
das exklusive Oder aller zehn Karten enthält. Mithilfe dieser Sicherungskarte kann sie jetzt im
Notfall eine verlorene Karte rekonstruieren.
So weit so gut. Leider sind Zaras Freunde ebenso verrückt wie sie selbst und spielten ihr einen
Streich: Sie erstellten weitere 100 Karten mit zufälligen Codewörtern und mischten sie mit
Zaras elf Karten in einem großen Stapel, den dann Zara so vorfand. Dummerweise sind die
elektronischen Schlösser in Zaras Häusern so konstruiert, dass sie nach drei fehlerhaften Zugangsversuchen das Haus für 24 Stunden verriegeln. Zara konnte das Dilemma allerdings lösen
indem sie ein Programm schrieb, das die 111 Karten einlas und dann herausfand, welche 11
Karten die echten waren.
### Aufgabe
1. Tu es Zara gleich und schreibe ein Programm, das diese Aufgabenstellung bewältigt.
Wende es auf die 111 Karten an, die du auf den BWINF-Webseiten findest. Welche Karten
sind die richtigen und welche wurden durch die „Freunde“ hinzugefügt?
2. Wie kann nun Zara mithilfe der 11 gefundenen Karten am nächsten Wochenende das
nächste Haus aufsperren, ohne dafür mehr als zwei Fehlversuche zu benötigen?
3. Auf den BWINF-Webseiten findest du weitere Beispielaufgaben, an denen du dein Können demonstrieren kannst. Einige davon sind sehr schwer

