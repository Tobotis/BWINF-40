# Zur Übergabe von Argumenten in der Kommandozeile
from sys import argv
# Zum Überprüfen ob Files exisitieren
from os.path import exists
# Zeitmessung der Execution-Time
import time

# Dictinary mit den Segmenten des Sieben-Segment-Displays
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
# umwandeln-Funktion => rekursives Vorgehen zum maximieren einer Hexadezimalzahl im SSD
# übrigerUmsatz => Segemnte, die nach dem umwandeln übrig sind
# übrigeUmelgungen => Umlegungen, die maximal getätigt werden dürfen
# index => Index der aktuellen Ziffer in der Hexadezimalzahl
# hexZahl => Hexadezimalzahl, die umwandelt werden soll
# schritte => Liste der Schritte/Umlegungen, die getätigt werden. Element := [IndexAlt, SegmentIndexAlt, IndexNeu, SegmentIndexNeu]


def umwandeln(maxUmlegungen, hexZahl, index=0, übrigerUmsatz=0, schritte=[]):
    # Check ob zu viele Segmente übrig sind (die Segemente können keines Falls in den "hinteren" Ziffern untergebracht werden)
    # => Check ob der Umsatz größer ist, als es freie Segmente gibt
    if übrigerUmsatz > (7 * len(hexZahl[index:]))-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]):
        return []
    # Check ob zu viele Segement im voraus verwendet wurden (die Segmente können keines Falls von den "hinteren" Ziffern genommen werden)
    # => Check ob der Umsatz kleiner ist (negative Zahl), als es gefüllte Segmente gibt, wenn in jeder Ziffer am Ende noch mindestens zwei Segmente sein müssen (=1)
    if übrigerUmsatz < (-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]) + 2*len(hexZahl[index:])):
        return []
    # Check ob alle Ziffern umwandelt wurden => man ist am Ende der Hexzahl angekommen
    if index >= len(hexZahl):
        # Check ob Segmente übrig sind => Die Lösung ist nicht valid
        # => Es müssen alle Segmente verwendet werden
        if übrigerUmsatz != 0:
            return []
        # Die Lösung ist valid und die Schritte können zurückgegeben werden
        return schritte
    # Festlegen der aktuellen Ziffer
    ziffer = hexZahl[index]
    # TODO REMOVE
    #print("Ziffer", ziffer, "Schritte", schritte, "Übrig", übrigerUmsatz,)
    # Iteration über alle anderen Hexziffern von F bis 0
    for i in hexInSSD.keys():
        # Check ob man bei der aktuellen Ziffer angekommen ist
        # Es folgen somit niedrigere Hexziffern
        if i == ziffer and len(schritte) == 0:
            return umwandeln(maxUmlegungen, hexZahl,
                             index+1, übrigerUmsatz, schritte)
        übrigeSegmente = übrigerUmsatz
        schritteNeu = schritte.copy()
        # Iteration über alle Segmente der Ziffern
        for segment in range(7):
            # Check ob das Segment von i in der Ausgangsziffer fehlt
            if hexInSSD[i][segment] > hexInSSD[ziffer][segment]:
                # Check ob Segmente übrigt sind
                if übrigeSegmente > 0:
                    schritteNeu[len(schritteNeu)-übrigeSegmente][2] = index
                    schritteNeu[len(schritteNeu)-übrigeSegmente][3] = segment
                else:
                    schritteNeu.append([None, None, index, segment])
                # Ein "übrigesSegment" wird verwendet (selbst wenn keine übrig sind =>
                # möglicherweise kann es in der nächsten Ziffer erzeugt werden)
                übrigeSegmente -= 1
            # Check ob ein Segment von i in der Ausgangsziffer zu viel ist
            elif hexInSSD[i][segment] < hexInSSD[ziffer][segment]:
                if übrigeSegmente < 0:
                    schritteNeu[len(schritteNeu)+übrigeSegmente][0] = index
                    schritteNeu[len(schritteNeu)+übrigeSegmente][1] = segment
                else:
                    schritteNeu.append([index, segment, None, None])
                # Ein "übrigesSegment" wird hinzugefügt
                übrigeSegmente += 1
            # Die Umformung ist nicht möglich, wenn die übrige Umlegungen nicht genug sind
            if len(schritteNeu) > maxUmlegungen:
                break
        else:
            result = umwandeln(maxUmlegungen, hexZahl,
                               index+1, übrigeSegmente, schritte=schritteNeu)

            # Wenn eine Lösung gefunden wurde, wird diese zurückgegeben
            # Es ist die größtmögliche, da von F nach 0 iteriert wird
            if len(result) > 0:
                return result
    # Es wurde keine Lösung gefunden
    return []


def solve(hexZahl, maxUmlegungen):
    ergebnis = umwandeln(maxUmlegungen, hexZahl)
    if len(ergebnis) > 0:
        # Es wurde eine Lösung gefunden
        ssd = [hexInSSD[i].copy() for i in hexZahl]
        printSSD(ssd)
        for schritt in ergebnis:
            ssd[schritt[0]][schritt[1]] = 0
            ssd[schritt[2]][schritt[3]] = 1
            printSSD(ssd)
        ergebnis = ""
        for anzeige in ssd:
            ergebnis += list(hexInSSD.keys()
                             )[list(hexInSSD.values()).index(anzeige)]
        print("Lösung:", ergebnis)
    else:
        print("KEINE LÖSUNG GEFUNDEN")


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
        data = [i.split(" ") for i in inhalt]
        return data


def main():  # Startpunkt des Programmes
    input = parseInput()  # Lesen des Inputs
    if(input is None):
        return
    # Lösen des Problems
    for i in input:
        solve(i[0], int(i[1]))


if __name__ == "__main__":  # Das ist Python :)
    start_time = time.time()  # Messung der Start-Zeit
    main()
    print("--- %s Sekunden ---" %
          round(time.time() - start_time, 4))  # Ausgeben der Execution-Time
