# Zur Übergabe von Argumenten in der Kommandozeile
from logging import info
import time
from os.path import exists
from sys import argv
import matplotlib.pyplot as plt
# Für sehr große Eingaben, muss das Rekursionslimit hochgestellt werden
from sys import setrecursionlimit
setrecursionlimit(1500)
# Zum Überprüfen ob Files exisitieren
# Zeitmessung der Execution-Time

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


def brute_all_possiblities():
    anzahlZiffern = 3
    possibilites = set()
    umsätze = set()
    u = set()
    for ziffer in hexInSSD.keys():
        for zielZiffer in hexInSSD.keys():
            übrigeSegmente = 0
            umlegungen = 0
            for segment in range(7):
                # Segment muss weggenommen werden
                if hexInSSD[ziffer][segment] > hexInSSD[zielZiffer][segment]:
                    if übrigeSegmente >= 0:
                        umlegungen += 1
                    übrigeSegmente += 1
                # Segment muss eingesetzt werden
                elif hexInSSD[ziffer][segment] < hexInSSD[zielZiffer][segment]:
                    if übrigeSegmente <= 0:
                        umlegungen += 1
                    übrigeSegmente -= 1
            zielWert = list(hexInSSD.keys()).index(zielZiffer)
            zifferWert = list(hexInSSD.keys()).index(ziffer)
            wertsteigerung = (zielWert-zifferWert)
            possibilites.add(
                (umlegungen, übrigeSegmente, wertsteigerung, zifferWert, sum(hexInSSD[ziffer])))
            umsätze.add(übrigeSegmente)
            u.add(umlegungen)

    print(possibilites, len(possibilites))
    print(umsätze, len(umsätze))
    print(u, len(u))

    x = list(zip(*possibilites))[4]
    y = list(zip(*possibilites))[0]
    plt.scatter(x, y)
    plt.show()
# solve-Funktion => initialisierung des Lösungsprozesses und Ausgabe der Lösung


def solve(hexZahl, maxUmlegungen, zwischenstandAnzeige=False):
    umlegeOptionen = {}
    for i in range(len(hexZahl)):
        ziffer = hexZahl[i]
        for zielZiffer in hexInSSD.keys():
            übrigeSegmente = 0
            umlegungen = 0
            for segment in range(7):
                # Segment muss weggenommen werden
                if hexInSSD[ziffer][segment] > hexInSSD[zielZiffer][segment]:
                    if übrigeSegmente >= 0:
                        umlegungen += 1
                    übrigeSegmente += 1
                # Segment muss eingesetzt werden
                elif hexInSSD[ziffer][segment] < hexInSSD[zielZiffer][segment]:
                    if übrigeSegmente <= 0:
                        umlegungen += 1
                    übrigeSegmente -= 1
            information = (umlegungen, übrigeSegmente)
            if information in umlegeOptionen.keys():
                umlegeOptionen[information].add(i)
            else:
                umlegeOptionen[information] = {i}
    print(umlegeOptionen)


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
                  for i in inhalt]  # Zeilenumbrüche entfernen
        hexZahl = inhalt[0]  # Die Hexzahl befindet sich in der ersten Zeile
        # Die Maximalzahl an Umlegungen m befindet sich in der zweiten Zeile
        m = int(inhalt[1])
        # Zurückgeben der gelesenen Daten (...und File, für Benennung der Ergebnisdatei)
        return hexZahl, m, file


def main():  # Startpunkt des Programmes
    input = parseInput()  # Lesen des Inputs
    if(input is None):
        return
    # Lesen der Flagge -z für Zwischenstand anzeigen
    zwischenstandAnzeige = False
    if len(argv) >= 3:
        zwischenstandAnzeige = argv[2] == "-z"
    # Lösen des Problems
    ergebnis, umlegungen = solve(input[0], input[1], zwischenstandAnzeige)
    # Ausgabe der Lösungszahl
    print("Lösung:", ergebnis)
    print(umlegungen, "Umlegungen benötigt")
    # Schreiben der Lösungsdatei
    with open("ergebnis_" + input[2], "w") as f:
        f.write(ergebnis)


if __name__ == "__main__":  # Das ist Python :)
    start_time = time.time()  # Messung der Start-Zeit
    # main()
    brute_all_possiblities()
    print("--- %s Sekunden ---" %
          round(time.time() - start_time, 4))  # Ausgeben der Execution-Time
