# Für Messung der Laufzeit
from time import time
# Zum Überprüfen ob Dateien exisitieren
from os.path import exists
# Zur Übergabe von Argumenten im Terminal
from sys import argv
# Für sehr große Eingaben, muss das Rekursionslimit hochgestellt werden (Maximale Rekursionstiefe)
# => Entspricht im Sachzusammenahang der Anzahl an Ziffern in der Eingabedatei
from sys import setrecursionlimit
setrecursionlimit(1200)


# Dictionary den Segmenten des Sieben-Segment-Displays (SSD) (von F bis 0)
# Zum Konvertieren einer Hexadezimalzahl (Key) in eine Liste mit den Segmenten, welche vorhanden sind (Value)
# => 1: Segment ist an; 0: Segment ist aus
# Indizes starten beim obersten Segment (0) und folgen dem Urzeigersinn => Index 6 ist das mittlere Segement (siehe Dokumentation)
hexInSSD = {
    "F": [1, 0, 0, 0, 1, 1, 1],
    "E": [1, 0, 0, 1, 1, 1, 1],
    "D": [0, 1, 1, 1, 1, 0, 1],
    "C": [1, 0, 0, 1, 1, 1, 0],
    "B": [0, 0, 1, 1, 1, 1, 1],
    "A": [1, 1, 1, 0, 1, 1, 1],
    "9": [1, 1, 1, 1, 0, 1, 1],
    "8": [1, 1, 1, 1, 1, 1, 1],
    "7": [1, 1, 1, 0, 0, 0, 0],
    "6": [1, 0, 1, 1, 1, 1, 1],
    "5": [1, 0, 1, 1, 0, 1, 1],
    "4": [0, 1, 1, 0, 0, 1, 1],
    "3": [1, 1, 1, 1, 0, 0, 1],
    "2": [1, 1, 0, 1, 1, 0, 1],
    "1": [0, 1, 1, 0, 0, 0, 0],
    "0": [1, 1, 1, 1, 1, 1, 0],
}
# Das Äquivalent für das Binärsystem
binInSSD = {
    "1": [0, 1, 1, 0, 0, 0, 0],
    "0": [1, 1, 1, 1, 1, 1, 0],
}

# Funktion für rekursives Vorgehen zum Maximieren einer Hexadezimalzahl im SSD
# maxUmlegungen: Umlegungen, die maximal getätigt werden dürfen
# hexZahl: Hexadezimalzahl, die umwandelt werden soll
# index: Index der aktuellen Ziffer in der Hexadezimalzahl (Standardmäßig 0)
# übrigerUmsatz: Segemente, die nach dem umwandeln übrig sind (Standardmäßig 0)
# schritte: Liste der Schritte/Umlegungen, die getätigt werden.
#     Schritt: [IndexAlt, SegmentIndexAlt, IndexNeu, SegmentIndexNeu] (Standardmäßig leer)
# tempOptionen: Liste an Optionen welche bereits ausprobiert wurden und gescheitert sind (für Optimierung) (Standardmäßig leer)
# min: True, wenn die Zahl minimiert werden soll (Standardmäßig False)
def maxZiffer(maxUmlegungen, hexZahl, index=0, übrigerUmsatz=0, schritte=[], tempOptionen=[], min = False):
    # Check ob alle Ziffern umwandelt wurden => man ist am Ende der Hexzahl angekommen
    if index >= len(hexZahl):
        # Check ob Segmente übrig sind => Die Lösung ist nicht valide
        # => Es müssen alle Segmente verwendet werden
        if übrigerUmsatz != 0:
            return []
        # Die Lösung ist valide und die Schritte können zurückgegeben werden
        return schritte
    # Check ob zu viele Segmente übrig sind (die Segemente können keines Falls in den "hinteren" Ziffern untergebracht werden)
    # => Check ob der Umsatz größer ist, als es leere Segmente gibt
    if übrigerUmsatz > (7 * len(hexZahl[index:]))-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]):
        # Die Anzahl der ''Lücken'' in der hinteren Ziffern ist größer als die Anzahl der übrigen Segmente
        return []
    # Check ob zu viele Segement im Voraus verwendet wurden (die Segmente können keines Falls von den "hinteren" Ziffern genommen werden)
    # => Check ob der Umsatz kleiner ist (negative Zahl), als es gefüllte Segmente gibt, wenn in jeder Ziffer am Ende noch mindestens zwei Segmente sein müssen (=1)
    if übrigerUmsatz < (-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]) + 2*len(hexZahl[index:])):
        # Die Anzahl der ''Lücken'' in den bereits umegelegten Ziffern ist größer als die Anzahl der übrigen Segmente in den hinteren Ziffern
        return []
    # Festlegen der aktuellen Ziffer der Hexzahl
    ziffer = hexZahl[index]
    # Iteration über alle anderen Hexziffern von F bis 0
    for i in (reversed(hexInSSD.keys()) if min else hexInSSD.keys()):
        # Check ob man bei der aktuellen Ziffer angekommen ist
        # Es folgen somit niedrigere Hexziffern
        # => nur fortfahren, wenn bereits Umlegungen getätigt worden sind
        # Die erste Ziffer, die umgelegt wird, darf nicht verringert werden,
        # sonst wird die gesamte Hexadezimalziffer verringert (siehe Stellenwertsystem)
        if i == ziffer and (len(schritte) == 0 or übrigerUmsatz == 0):
            # Die aktuelle Ziffer bleibt unverändert ... es wird mit der nächsten fortgefahren
            return maxZiffer(maxUmlegungen, hexZahl,
                             index+1, übrigerUmsatz, schritte)
        # Die aktuell übrigen Segmente entsprechen dem Segmentumsatz
        übrigeSegmente = übrigerUmsatz
        # Kopie der Schritte um Mutation zu vermeiden
        schritteNeu = schritte.copy()
        # Kopie der ausgeschiedenen Optionen um Mutation zu vermeiden
        tempOptionenNeu = tempOptionen.copy()
        # Iteration über alle Segmente der Ziffern
        for segment in range(7):
            # Check ob das Segment von i in der Ausgangsziffer fehlt
            if hexInSSD[i][segment] > hexInSSD[ziffer][segment]:
                # Check ob Segmente übrig sind
                if übrigeSegmente > 0:
                    # Es gibt noch Segmente, die verwendet werden können
                    # die "Zielposition" (Ziffernindex, Segmentindex) der übrigen Segmente wird beim entsprechenden Segment hinzugefügt
                    # (war vorher noch nicht bestimmt) (Siehe Format der schritte-Liste)
                    schritteNeu[len(schritteNeu)-übrigeSegmente][2] = index
                    schritteNeu[len(schritteNeu)-übrigeSegmente][3] = segment
                    # Es wird keine neue Umlegung gebraucht
                else:
                    # Es gibt keine Segmente, die verwendet werden können
                    # Es muss eine neue Umlegung mit unbestimmter Herkunftsposition hinzugefügt werden
                    schritteNeu.append([None, None, index, segment])
                # Ein "übrigesSegment" wird verwendet (selbst wenn keine übrig sind =>
                # möglicherweise kann es in der nächsten Ziffer erzeugt werden)
                übrigeSegmente -= 1
            # Check ob ein Segment von i in der Ausgangsziffer zu viel ist
            elif hexInSSD[i][segment] < hexInSSD[ziffer][segment]:
                # Check ob mehr Segmente verwendet wurden, als frei geworden sind
                if übrigeSegmente < 0:
                    # Es gibt Umlegungen mit unbestimmter Herkunftsposition
                    # Die Herkunftsposition wird auf die aktuelle Position (Ziffernindex, Segmentindex) gesetzt
                    schritteNeu[len(schritteNeu)+übrigeSegmente][0] = index
                    schritteNeu[len(schritteNeu)+übrigeSegmente][1] = segment
                    # Es wird keine neue Umlegung gebraucht
                else:
                    # Es gibt keine Umlegungen mit unbestimmter Herkunftsposition
                    # Es muss eine neue Umlegung mit unbestimmter Zielposition hinzugefügt werden
                    schritteNeu.append([index, segment, None, None])
                # Ein "übrigesSegment" wird hinzugefügt
                übrigeSegmente += 1
            # Die Umformung ist nicht möglich, wenn die übrige Umlegungen nicht genug sind
            # (Es darf nicht mehr schritte als Umlegungen geben)
            if len(schritteNeu) > maxUmlegungen:
                tempOptionenNeu.append([ziffer, i])
                break

        else:
            # Wird ausgeführt wenn nicht gebreakt wurde
            # Es kann mit der nächsten Ziffer fortgefahren werden
            result = maxZiffer(maxUmlegungen, hexZahl,
                               index+1, übrigeSegmente, schritte=schritteNeu)

            # Wenn eine Lösung gefunden wurde, wird diese zurückgegeben
            # Es ist die größtmögliche, da von F nach 0 iteriert wird
            if len(result) > 0:
                return result
            # Andernfalls wird mit der nächsten Ziffer fortgefahren
    # Es wurde keine Lösung gefunden
    return []

# Funktion zur Initialisierung des Lösungsprozesses und Anzeige
# hexZahl: Hexadezimalzahl, welche maximiert werden soll (String)
# maxUmlegungen: maximale Anzahl an Umlegungen
# zwischenstandAnzeige: True, wenn die Zwischenstände angezeigt werden sollen
# min: True, wenn die hexZahl minimiert statt maximiert werden soll
def maximieren(hexZahl, maxUmlegungen, zwischenstandAnzeige=False, min=False):
    # Ermitteln der nötigen Umlegungen zur Maximierung der Hexadezimalzahl mithilfe von "maxZiffer"
    ergebnis = maxZiffer(maxUmlegungen, hexZahl, min=min)
    # Maximale Hexadezimalzahl muss aus den Umlegungen "zurückgewonnen" werden
    ergebnisString = ""
    # Check ob überhaupt Umlegungen getätigt wurden
    if len(ergebnis) > 0:
        # Es wurden Umlegungen getätigt
        # Initialisierung der SSA (Liste von Datstellungen von Ziffern)
        ssd = [hexInSSD[i].copy() for i in hexZahl]
        # Ausagbe der Starthexzahl wenn gewünscht
        if zwischenstandAnzeige:
            printSSD(ssd)
        # Iteraion über die ermittleten Umlegungen
        for schritt in ergebnis:
            # Durchführen der Umlegung
            ssd[schritt[0]][schritt[1]] = 0
            ssd[schritt[2]][schritt[3]] = 1
            # Ausgabe der SSA wenn gewünscht
            if zwischenstandAnzeige:
                printSSD(ssd)
        # Iteration über alle Ziffern in der SSA
        for anzeige in ssd:
            # Hinzufügen der Ziffer im Stringformat (Umformung über die Dictionary s.o.)
            ergebnisString += list(hexInSSD.keys())[list(hexInSSD.values()).index(anzeige)]
    else:
        # Es wurden keine Umlegungen getätigt
        # Es ist bereits die maximale Hexadezimalzahl
        ergebnisString = hexZahl

    # Zurückgeben der Lösung und der benötigten umlegungen
    return ergebnisString, len(ergebnis)

# Funktion zur Ausgabe eines SSDs in der Konsole
# SSD := Liste der Darstellungen von Ziffern (Liste von Sublisten mit 7 Elementen := Segmenten)
def printSSD(SSD):
    # Hardcoded Ausgabe der einzelnen Segmente
    lines = ["" for _ in range(5)]
    for ziffer in SSD:
        if ziffer[0] == 1:
            lines[0] += " - "
        else:
            lines[0] += "   "
        if ziffer[5] == 1:
            lines[1] += "| "
        else:
            lines[1] += "  "
        if ziffer[1] == 1:
            lines[1] += "|"
        else:
            lines[1] += " "
        if ziffer[6] == 1:
            lines[2] += " - "
        else:
            lines[2] += "   "
        if ziffer[4] == 1:
            lines[3] += "| "
        else:
            lines[3] += "  "
        if ziffer[2] == 1:
            lines[3] += "|"
        else:
            lines[3] += " "
        if ziffer[3] == 1:
            lines[4] += " - "
        else:
            lines[4] += "   "
    for line in lines:
        print(line)

# Funktion zum Lesen des Inputs
def parseInput():
    # Überprüfung ob kein Argument angegeben wurde
    if(len(argv) == 1):
        # Fragen nach Eingabedatei
        file = input("Eingabedatei eingeben:")
    else:
        # Lesen der Eingabedatei aus den Argumenten
        file = argv[1]
    # Überprüfung ob die Eingabedatei existiert
    if(not exists(file)):
        # Ausgabe eines Fehlers
        print("\033[1;31mDatei nicht gefunden\033[0m")
        return None
    # Öfnnen der Eingabedatei (im Lesemodus)
    with open(file=file, mode="r") as data:
        # Lesen aller Zeilen der Eingabedatei
        inhalt = data.readlines()
        # Bereinigen der Zeilen (Zeilenumbrüche entfernen)
        inhalt = [i.replace("\n", "") for i in inhalt]
        # Hexadezimalzahl
        hexZahl = inhalt[0]
        # Maximalzahl an Umlegungen
        m = int(inhalt[1])
        # Zurückgeben der gelesenen Daten (...und File, für Benennung der Ergebnisdatei)
        return hexZahl, m, file

# Hauptfunktion (Ausführung des Programms)
def main():
    # Sicheres Lesen des Inputs
    try:
        hexZahl, m, file = parseInput()
    except Exception as e:
        # Ausgabe des Fehlers
        print("Input konnte nicht gelesen werden: {}".format(e))
        return
    # Lesen der Flagge -d für Zwischenstand anzeigen
    zwischenstandAnzeige = "-d" in argv
    # Lesen der Flagge -min für Minimierung statt Maximierung
    min = "-min" in argv
    # Maximieren der eingelesenen Hexadezimalzahl mit maximal m Umlegungen
    lösung, umlegungen = maximieren(hexZahl, m, zwischenstandAnzeige, min)
    # Schreiben der Lösungsdatei
    with open("ergebnis_" + file, "w") as f:
        # Ausgabe der Lösungszahl
        print("Lösung:", lösung)
        # Ausgabe der benötigten Umlegungen
        print("{}/{} Umlegungen benötigt".format(umlegungen, m))
        # Schreiben der Lösung
        f.write(lösung + "\n" + "{}/{}".format(umlegungen, m))


# Startpunkt des Programms
if __name__ == "__main__":
    # Aufnahme der Startzeit
    startTime = time()
    # Ausführung
    main()
    # Aufnahme der Endzeit
    endTime = time()
    # Ausgabe der Laufzeit
    print("--- {:.4f} Sekunden ---".format(endTime - startTime))
