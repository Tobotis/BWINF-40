# BWINF-40
2. Runde des 40. Bundeswettbewerb für Informatik (2022)
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


