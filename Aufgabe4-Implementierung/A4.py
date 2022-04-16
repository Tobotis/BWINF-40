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
    # tMatrix.append([1 for _ in range(n)]+[k % 2])
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
    # for r in tMatrix:
     #   print(r)
    # print(sum([sum(i)-1 if sum(i)-1 > 0 else 0 for i in transponierteMatrix]))
    lösungen = []
    # Herausfinden von Variablen
    variablen = {}
    for i in range(len(tMatrix)):
        index = None
        for j in range(len(tMatrix[i])-1):
            if tMatrix[i][j] == 1:
                if index is None:
                    index = j
                else:
                    if j not in variablen.keys():
                        variablen[j] = [index]
                    else:
                        variablen[j].append(index)

    processedVariablen = {}
    anzahl1 = []
    for variable in variablen.keys():
        processedVariablen[variable] = ""
        anzahlVar = 0
        for i in range(n-len(variablen)):
            if i in variablen[variable]:
                processedVariablen[variable] += "1"
                anzahlVar += 1
            else:
                processedVariablen[variable] += "0"
        anzahl1.append([variable, anzahlVar])
    anzahl1.sort(key=lambda x: x[1], reverse=True)
    for r in processedVariablen.keys():
        print(r, processedVariablen[r])

    print(len(processedVariablen))

    kombinationen = []
    overallIterations = 0
    for i in range(len(processedVariablen)):
        variable = list(processedVariablen.keys())[i]
        for j in range(len(kombinationen), -1, -1):
            overallIterations += 1
            if j == len(kombinationen):
                neueKombination = [[variable], processedVariablen[variable]]
            else:
                neueKombination = [kombinationen[j][0] + [variable],
                                   "{0:b}".format(int(processedVariablen[variable], 2) ^ int(kombinationen[j][1], 2))]

            if neueKombination[1].count("1")+len(neueKombination[0]) == k+1:
                print("FOUND")
                print(neueKombination)
                lösungen.append(neueKombination)
            möglich = len(neueKombination[0]) < k+1  # math.ceil((k+1)/2)+1
            if möglich:
                übrigeVariablen = k+1 - len(neueKombination[0])
                maximalAnzahl1 = 0
                benutzt = 0
                for p in range(len(anzahl1)):
                    if anzahl1[p][0] not in neueKombination[0]:
                        maximalAnzahl1 += anzahl1[p][1]
                        benutzt += 1
                        if benutzt == übrigeVariablen:
                            break
                if neueKombination[1].count("1")+len(neueKombination[0]) - (maximalAnzahl1+benutzt) > k+1:
                    möglich = False

            if möglich:
                kombinationen.append(neueKombination)
        print(i, len(kombinationen), overallIterations)

    # Fusionieren der Lösungskombinationen
    '''for i in range(len(kombinationen)):
        if i % 1000 == 0:
            print(i)
        for j in range(i+1, len(kombinationen)):
            for element in kombinationen[i][0]:
                if element in kombinationen[j][0]:
                    break
            else:

                neueKombination = [kombinationen[j][0] + kombinationen[i][0],
                                   "{0:b}".format(int(kombinationen[i][1], 2) ^ int(kombinationen[j][1], 2))]
                if neueKombination[1].count("1")+len(neueKombination[0]) == k+1:
                    lösungen.append(neueKombination)'''

    processedLösungen = []
    for lösung in lösungen:
        lösung[1] = lösung[1].zfill(n-len(processedVariablen))
        processedLösungen.append(lösung[0])
        for i in range(len(lösung[1])):
            if lösung[1][i] == "1":
                processedLösungen[-1].append(i)
    print(processedLösungen)
    return processedLösungen

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
