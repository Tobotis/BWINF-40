# Zur Übergabe von Argumenten in der Kommandozeile
from sys import argv
# Zum Überprüfen ob Files exisitieren
from os.path import exists
# Zeitmessung der Execution-Time
import time

# Dictinary mit den Segmenten des Sieben-Segment-Displays (SSD)
# Zum Konvertieren einer Hexadezimalzahl (Key) in eine Liste mit den Segmenten, die "leuchten" (Value)
# 1: Segment ist an; 0: Segment ist aus
# Indizes starten beim obersten Segment (0) und folgen dem Urzeigersinn => Index 6 ist das mittlere Segement
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
# umwandeln-Funktion => rekursives Vorgehen zum Maximieren einer Hexadezimalzahl im SSD
# maxUmlegungen => Umlegungen, die maximal getätigt werden dürfen
# hexZahl => Hexadezimalzahl, die umwandelt werden soll
# index => Index der aktuellen Ziffer in der Hexadezimalzahl (Standardmäßig 0)
# übrigerUmsatz => Segemnte, die nach dem umwandeln übrig sind (Standardmäßig 0)
# schritte => Liste der Schritte/Umlegungen, die getätigt werden. Element := [IndexAlt, SegmentIndexAlt, IndexNeu, SegmentIndexNeu] (Standardmäßig leer)


def umwandeln(maxUmlegungen, hexZahl, index=0, übrigerUmsatz=0, schritte=[]):
    # Check ob zu viele Segmente übrig sind (die Segemente können keines Falls in den "hinteren" Ziffern untergebracht werden)
    # => Check ob der Umsatz größer ist, als es freie Segmente gibt
    if übrigerUmsatz > (7 * len(hexZahl[index:]))-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]):
        # Dieser Weg ist nicht möglich => Abbruch
        return []
    # Check ob zu viele Segement im Voraus verwendet wurden (die Segmente können keines Falls von den "hinteren" Ziffern genommen werden)
    # => Check ob der Umsatz kleiner ist (negative Zahl), als es gefüllte Segmente gibt, wenn in jeder Ziffer am Ende noch mindestens zwei Segmente sein müssen (=1)
    if übrigerUmsatz < (-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]) + 2*len(hexZahl[index:])):
        # Dieser Weg ist nicht möglich => Abbruch
        return []
    # Check ob alle Ziffern umwandelt wurden => man ist am Ende der Hexzahl angekommen
    if index >= len(hexZahl):
        # Check ob Segmente übrig sind => Die Lösung ist nicht valide
        # => Es müssen alle Segmente verwendet werden
        if übrigerUmsatz != 0:
            return []
        # Die Lösung ist valide und die Schritte können zurückgegeben werden
        return schritte
    # Festlegen der aktuellen Ziffer der Hexzahl
    ziffer = hexZahl[index]
    # TODO REMOVE
    # print("Ziffer", ziffer, "Schritte", schritte, "Übrig", übrigerUmsatz,)

    # Iteration über alle anderen Hexziffern von F bis 0
    for i in hexInSSD.keys():
        # Check ob man bei der aktuellen Ziffer angekommen ist
        # Es folgen somit niedrigere Hexziffern
        # => nur fortfahren, wenn bereits Umlegungen getätigt worden sind
        # Die erste Ziffer, die umgelegt wird, darf nicht verringert werden,
        # sonst wird die gesamte Hexadezimalziffer verringert (siehe Stellenwertsystem)
        if i == ziffer and len(schritte) == 0:
            # Die aktuelle Ziffer bleibt unverändert ... es wird mit der nächsten fortgefahren
            return umwandeln(maxUmlegungen, hexZahl,
                             index+1, übrigerUmsatz, schritte)
        # Die aktuell übrigen Segmente entsprechen dem Segmentumsatz
        übrigeSegmente = übrigerUmsatz
        # Kopie der schritte um Mutation zu vermeiden
        schritteNeu = schritte.copy()
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
                break
        else:
            # Wird ausgeführt wenn nicht gebreakt wurde
            # Es kann mit der nächsten Ziffer fortgefahren werden
            result = umwandeln(maxUmlegungen, hexZahl,
                               index+1, übrigeSegmente, schritte=schritteNeu)

            # Wenn eine Lösung gefunden wurde, wird diese zurückgegeben
            # Es ist die größtmögliche, da von F nach 0 iteriert wird
            if len(result) > 0:
                return result
            # Andernfalls wird mit der nächsten Ziffer fortgefahren
    # Es wurde keine Lösung gefunden
    return []

# solve-Funktion => initialisierung des Lösungsprozesses und Ausgabe der Lösung


def solve(hexZahl, maxUmlegungen):
    # Ermitteln der Lösung mithilfe von "umwandeln"
    ergebnis = umwandeln(maxUmlegungen, hexZahl)
    # Check ob Umlegungen getätigt wurden
    if len(ergebnis) > 0:
        # Es wurde eine Lösung gefunden
        # Initialisierung der SSA (Liste von Datstellungen von Ziffern)
        ssd = [hexInSSD[i].copy() for i in hexZahl]
        # Ausagbe der Starthexzahl in der SSA
        printSSD(ssd)
        # Iteraion über die ermittleten Umlegungen
        for schritt in ergebnis:
            # Durchführen der Umlegung
            ssd[schritt[0]][schritt[1]] = 0
            ssd[schritt[2]][schritt[3]] = 1
            # Ausgabe der SSA
            printSSD(ssd)
        # Ermitteln der Lösungszahl
        # (Umformen von der SSA-Darstellung in einen String)
        ergebnisString = ""
        # Iteration über alle Ziffern in der SSA
        for anzeige in ssd:
            # Hinzufügen der Ziffer im Stringformat (Umformung über die Dictionary s.o.)
            ergebnisString += list(hexInSSD.keys()
                                   )[list(hexInSSD.values()).index(anzeige)]
        # Ausgabe der Lösungszahl
        print("Lösung:", ergebnisString)
    else:
        # Es wurden keine Umformungen getätigt
        # Es ist bereits die maximale Hexadezimalzahl
        print("KEINE UMLEGUNGEN NÖTIG")
        print("Lösung:", hexZahl)


def printSSD(SSD,):
    # Iteration über alle Segmente der Ziffern des SSD
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


def parseInput():
    if(len(argv) == 1):  # Es wurde kein extra Argument angegeben
        file = input("Eingabedatei eingeben:")
    else:  # Es wurde ein extra Argument angegeben
        file = argv[1]
    if(not exists(file)):  # Check ob die angegebene Datei nicht existiert
        print("\033[1;31mDatei nicht gefunden\033[0m")
        return None
    with open(file=file, mode="r") as data:  # Öffnen der angegebenen Datei
        inhalt = data.readlines()  # Lesen der Zeilen
        inhalt = [i.replace("\n", "")
                  for i in inhalt[1:]]  # Zeilenumbrüche entfernen
        # Aufteilen der Hexzahl und der maximalen Umlegungen
        data = [i.split(" ") for i in inhalt]
        return data  # Zurückgeben der gelesenen Daten


def main():  # Startpunkt des Programmes
    input = parseInput()  # Lesen des Inputs
    if(input is None):
        return
    # Lösen des Problems
    for i in input:
        # [Hexzahl] : string
        # [maximaleUmlegungen] : int
        solve(i[0], int(i[1]))


if __name__ == "__main__":  # Das ist Python :)
    start_time = time.time()  # Messung der Start-Zeit
    main()
    print("--- %s Sekunden ---" %
          round(time.time() - start_time, 4))  # Ausgeben der Execution-Time
