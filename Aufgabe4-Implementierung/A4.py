# Für Messung der Laufzeit
import time
# Zum Überprüfen ob Dateien exisitieren
from os.path import exists
# Zur Übergabe von Argumenten im Terminal
from sys import argv
# Zum Berechnen von Fakultäten und Auf-/Abrundungen
from math import factorial,ceil,floor

# Funktion zum Anwenden von Brute Force auf das Gesamtproblem (Kombination aller n Karten)
# n: Gesamtzahl an Karten
# k: Anzahl an Gesamtkarten! (Öffnungskarten + 1)
# m: Anzahl Bits pro Karte
# karten: Liste aller Karten (Strings)
def bfAll(n, k, m, karten):
    länge = k//2
    if k % 2 == 1:
        längeA = ceil(k/2)
        längeB = floor(k/2)
    # Liste aller Kombinationen der Karten (Zwischenspeicherung)
    kombinationen = []
    # Liste der Kombination mit Länge A
    kombinationenA = []
    # Liste der Kombinationen mit Länge B
    kombinationenB = []
    # Iteration über alle Karten
    for i in range(n):
        # Iteration über alle bisherigen Kombinationen (+1 extra Iteration für eine vollständig neue Kombination)
        for j in range(len(kombinationen), -1, -1):
            # Überprüfung ob es sich um die erste Iteration handelt
            if j == len(kombinationen):
                # Hinzufügen einer neuen Kombination für die Karte i
                kombinationen.append([[i], karten[i]])
            else:
                # Erweitern von Kombination j um die Karte i
                neueKombination = [kombinationen[j][0] + [i], "{0:b}".format(int(kombinationen[j][1], 2) ^ int(karten[i], 2)).zfill(m)]
            # Überprüfung ob es zwei Listen mit verschiedenen Längen gibt
            if k % 2 == 1:
                # Hinzufügen der neuen Kombination in die zugehörige Liste
                if len(neueKombination[0]) == längeA:
                    kombinationenA.append(neueKombination)
                elif len(neueKombination[0]) == längeB:
                    kombinationenB.append(neueKombination)
                elif len(neueKombination[0]) < längeB:
                    # Die neue Kombination kann noch erweitert werden
                    kombinationen.append(neueKombination)
            else:
                # Hinzufügen der neuen Kombination in die Liste A (Es gibt eine einheitliche Länge)
                if len(neueKombination[0]) == länge:
                    kombinationenA.append(neueKombination)
                elif len(neueKombination[0]) < länge:
                    # Die neue Kombination kann noch erweitert werden
                    kombinationen.append(neueKombination)
                
    # Sortieren der Listen nach dem Wert des XORS
    kombinationenA.sort(key= lambda x: int(x[1],2))
    kombinationenB.sort(key= lambda x: int(x[1],2))

    # Suchen nach Duplikaten in den/der Liste/-n
    if k % 2 == 0:
        letzteKombination = kombinationenA[0][1]
        for kombination in kombinationenA[1:]:
            if kombination[1] == letzteKombination:
                print("FOUND SOLUTION:", letzteKombination, kombination)
                break
    else:
        # TODO
        pass

# rekursive Funktion zum Anwenden von Brute Force auf das Restproblem (Kombination der Variablen nach dem Gauss-Algorithmus)
# => nur bei unterdeterminierten Eingaben/Matrizen (wenn n>m)
# k: Anzahl an Gesamtkarten! (Öffnungskarten + 1)
# variablen: Liste der Bitstrings der Variablen (Auswirkung auf das Ergebnis des Gauss-Algorithmus)
# index: Index der aktuellen Variable
# zweig: Bitstring (XOR der in diesem Zweig benutzten Variablen) 
def bfVars(k, variablen, index, zweig):
    # Überprüfung ob der aktuelle Zweig einer Lösung entspricht (Anzahl an 1 = Anzahl an zu benutzenden Karten)
    if zweig.count("1") == k:
        return zweig
    elif len(zweig[0]) > k:
        # print("breaking",index,zweig)
        return None
    else:
        if index > len(variablen)-1:
            return None
        variable = list(variablen.keys())[index]
        wert = variablen[variable]
        neuerZweig = [zweig[0] + [variable],
                      "{0:b}".format(int(zweig[1], 2) ^ int(wert, 2))]
        result = bfVars(k, variablen, index+1, neuerZweig)
        if result is None:
            return bfVars(k, variablen, index+1, zweig)
        else:
            return result


def gaussElim(n, k, m, karten):
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
    lösung = bfVars(k, processedVariablen, 0, [[], "0"])
    print(lösung)
    '''for i in range(len(processedVariablen)):
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
        print(i, len(kombinationen), overallIterations)'''

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
    # for lösung in lösungen:
    lösung[1] = lösung[1].zfill(n-len(processedVariablen))
    processedLösungen.append(lösung[0])
    for i in range(len(lösung[1])):
        if lösung[1][i] == "1":
            processedLösungen[-1].append(i)
    print(processedLösungen)
    return processedLösungen

# Funktion zum Lesen des Inputs
def parseInput():
    # Überprüfung ob ein Argument angegeben wurde
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
    # Öffnen der Eingabedatei (im Lesemodus)
    with open(file=file, mode="r") as data: 
        # Lesen aller Zeilen der Eingabedatei
        inhalt = data.readlines()
        # Bereinigen der Zeilen (Zeilenumbrüche entfernen)
        inhalt = [i.replace("\n", "") for i in inhalt]
        # Gesamtzahl an Karten auslesen
        n = int(inhalt[0].split(" ")[0])
        # Anzahl Öffnungskarten auslesen
        k = int(inhalt[0].split(" ")[1])
        # Anzahl der Bits auslesen
        m = int(inhalt[0].split(" ")[2])
        # Karten auslesen
        karten = inhalt[1:]
        # Zurückgeben der gelesenen Daten (...und File, für Benennung der Ergebnisdatei)
        return n, k, m, karten, file

# Hauptfunktion (Ausführung des Programms)
def main():
    # Sicheres Lesen des Inputs
    try:
        n, k, m, karten, file = parseInput()
    except Exception as e:
        # Ausgabe des Fehlers
        print("Input konnte nicht gelesen werden: {}".format(e))
        return
    # Anwenden des Gauss-Algorithmus auf den gelsenen Input
    # => Übergeben von k+1, da die Gesamtzahl an XOR-Karten = Öffnungskarten + Sicherungskarten
    lösungen = gaussElim(n, k+1, m, karten)
    # Schreiben der Lösungsdatei
    with open("ergebnis_" + file, "w") as f:
        # Iteration über alle Lösungen
        for lösung in lösungen:
            # Itearation über alle Kartenindizes der Lösung
            for index in lösung:
                # Schreiben der Kartenwerte in die Datei
                f.write(input[3][index] + "\n")
            # Trennung der Lösungen über ein \n
            f.write("\n")

# Startpunkt des Programms
if __name__ == "__main__":
    # Aufnahme der Startzeit
    startTime = time.time()
    # Ausführung
    main()
    # Aufnhame der Endzeit
    endTime = time.time()
    # Ausgabe der Zeit
    print("--- {:.4f} Sekunden ---".format(endTime - startTime))
