# Zeitmessung der Execution-Time
import time
# Zum Überprüfen ob Files exisitieren
from os.path import exists
# Zur Übergabe von Argumenten in der Kommandozeile
from sys import argv
import math


def gaussianElimination(n, k, m, karten):
    # Transponieren der Matrix
    tMatrix = [[0 for _ in range(n+1)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            tMatrix[j][i] = int(karten[i][j])
    # Eliminierungsverfahren
    for r1 in range(len(tMatrix)):
        for c1 in range(len(tMatrix[r1])):
            if tMatrix[r1][c1] == 1:
                for r2 in range(len(tMatrix)):
                    if r1 != r2 and tMatrix[r2][c1] == 1:
                        for c2 in range((len(tMatrix[r2]))):
                            tMatrix[r2][c2] = (tMatrix[r2][c2] +
                                               tMatrix[r1][c2]) % 2
                break
    # print(tMatrix)
    # print(sum([sum(i)-1 if sum(i)-1 > 0 else 0 for i in transponierteMatrix]))
    lösungen = []
    # Herausfinden von Variablen
    variablen = []
    for i in range(len(tMatrix)):
        leading1 = False
        for j in range(len(tMatrix[i])):
            if tMatrix[i][j] == 1:
                if not leading1:
                    leading1 = True
                else:
                    if j not in variablen:
                        variablen.append(j)

    print(variablen)
    if True:
        print("BRUTE", 2**len(variablen))
        # Brute Force der Variablen
        for i in range(2**len(variablen)):
            # Bestimmen der Werte für alle Variablen
            variablenWerte = str(bin(i)[2:].zfill(len(variablen)))
            #print("VARS", variablenWerte[::-1])
            lösung = [(0 if col not in variablen else int(
                variablenWerte[variablen.index(col)])) for col in range(n)]
            # print(lösung)
            for r in range(len(tMatrix)):
                summe = 0
                index = 0
                leading1 = False
                for c in range(len(tMatrix[r])-1):
                    if tMatrix[r][c] == 1:
                        if leading1:
                            summe = (
                                int(variablenWerte[variablen.index(c)]) + summe) % 2
                        else:
                            index = c
                            leading1 = True
                lösung[index] = summe
            indizes = []
            for l in range(len(lösung)):
                if lösung[l] == 1:
                    indizes.append(l)
            if len(indizes) == k+1:
                lösungen.append(indizes)
    print(lösungen)
    return lösungen

# Funktion zum Lesen des Inputs


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
        # Gesamtzahl an Karten
        n = int(inhalt[0].split(" ")[0])
        # Anzahl Öffnungskarten
        k = int(inhalt[0].split(" ")[1])
        # Anzahl der Bits
        m = int(inhalt[0].split(" ")[2])
        # Karten
        karten = inhalt[1:]
        # Zurückgeben der gelesenen Daten (...und File, für Benennung der Ergebnisdatei)
        return n, k, m, karten, file


def main():  # Startpunkt des Programmes
    input = parseInput()  # Lesen des Inputs
    if(input is None):
        return
    # Lösen des Problems
    lösungen = gaussianElimination(input[0], input[1], input[2], input[3])
    # Ausgabe der Lösungszahl
    # Schreiben der Lösungsdatei
    with open("ergebnis_" + input[4], "w") as f:
        for lösung in lösungen:
            for index in lösung:
                print(input[3][index])
                f.write(input[3][index] + "\n")
            f.write("\n")
            print()


if __name__ == "__main__":
    start_time = time.time()  # Startzeit des Programmes
    main()
    # Ausgeben der Execution-Time
    print("--- %s Sekunden ---" % round(time.time() - start_time, 4))
