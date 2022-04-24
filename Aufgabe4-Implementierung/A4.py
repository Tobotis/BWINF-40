# Für Messung der Laufzeit
from time import time
# Zum Überprüfen ob Dateien exisitieren
from os.path import exists
# Zur Übergabe von Argumenten im Terminal
from sys import argv
# Zum Berechnen von Fakultäten und Auf-/Abrundungen
from math import comb, ceil, floor
from typing import final

# Funktion zum Anwenden von Brute Force auf das Gesamtproblem (Kombination aller n Karten)
# n: Gesamtzahl an Karten
# k: Anzahl an gesuchten Karten (inkl. Sicherungskarte)
# m: Anzahl Bits pro Karte
# karten: Liste aller Karten (Strings)
def bfAll(n, k, m, karten):
    # Berechnen der beiden Längen
    # => welche die Listen haben müssen, welche kombiniert werden
    längeA = ceil(k/2)
    längeB = floor(k/2)
    # Liste aller Kombinationen der Karten (Zwischenspeicherung)
    kombinationen = []
    # Liste der Kombination mit Länge A oder B
    finalKombinationen = []
    # Iteration über alle Karten
    for i in range(n):
        print(i,n,len(kombinationen))
        # Iteration über alle bisherigen Kombinationen (+1 extra Iteration für eine vollständig neue Kombination)
        for j in range(len(kombinationen), -1, -1):
            # Überprüfung ob es sich um die erste Iteration handelt
            if j == len(kombinationen):
                # Hinzufügen einer neuen Kombination für die Karte i
                neueKombination = [[i], karten[i]]
            else:
                # Erweitern von Kombination j um die Karte i
                neueKombination = [kombinationen[j][0] + [i], ("{0:b}".format(int(kombinationen[j][1], 2) ^ int(karten[i], 2))).zfill(m)] 
            if len(neueKombination[0]) == längeA or len(neueKombination[0]) == längeB:
                finalKombinationen.append(neueKombination)
            if len(neueKombination[0]) < längeA:
                kombinationen.append(neueKombination)

    # Sortieren der Listen nach dem Wert des XORS
    finalKombinationen.sort(key=lambda x: int(x[1], 2))

    # print(finalKombinationen)
    # Suchen nach Duplikaten in den/der Liste/-n
    letzteKombination = finalKombinationen[0]
    for kombination in finalKombinationen[1:]:
        if kombination[1] == letzteKombination[1] and len(kombination[0])+len(letzteKombination[0]) == längeA+längeB:
            if len(list(set(kombination[0]) & set(letzteKombination[0]))) == 0:
                return [kombination[0]+letzteKombination[0]]
        letzteKombination = kombination
    print("Nothing Found")
    return []

# rekursive Funktion zum Anwenden von Brute Force auf das Restproblem (Kombination der Variablen nach dem Gauss-Algorithmus)
# => nur bei unterdeterminierten Eingaben/Matrizen (wenn n>m)
# k: Anzahl an gesuchten Karten (inkl Öffnungskarte)
# variablen: Liste der Bitstrings der Variablen (Auswirkung auf das Ergebnis des Gauss-Algorithmus)
# index: Index der aktuellen Variable
# zweig: [Anzahl an benutzten Variablen, Bitstring (XOR der in diesem Zweig benutzten Variablen)]
# n: Gesamtanzahl an Karten
def bfVars(k, variablen, index, zweig, n):
    # Überprüfung ob der aktuelle Zweig einer Lösung entspricht (Anzahl an 1 = Anzahl an zu benutzenden Karten)
    if zweig[1].count("1") == k:
        return zweig[1]
    # Abbrechen, wenn bereits mehr Variablen genutzt wurden, als es Karten gesucht sind
    elif zweig[0] > k:
        # print("breaking",index,zweig)
        return None
    else:
        # Überprüfung, ob bereits keine Variablen mehr übrig sind
        if index > len(variablen)-1:
            return None
        # Festlegen des Wertes (Bitstings) der aktuellen Variable
        wert = variablen[index]
        # Berechnen (XOR) für den neuen Zweig
        neuerZweig = [zweig[0]+1,("{0:b}".format(int(zweig[1], 2) ^ int(wert, 2))).zfill(n)]
        # Erweitern des neuen Zweiges
        result = bfVars(k, variablen, index+1, neuerZweig, n)
        # Bei Fehlschlagen mit Wahl der Variable, wird ohne die Variable fortgefahren
        if result is None:
            return bfVars(k, variablen, index+1, zweig, n)
        else:
            # Andernfalls wird das Ergebnis zurückgegeben
            return result

# Funktion für das Gausssche Eliminationsverfahren und Brute-Force der Variabalen-Kombinationen
# n: Anzahl an Gesamtkarten (int)
# m: Anzahl an Bits pro Karte (int)
# k: Anzahl an gesuchten Karten (inkl. Sicherungskarte)
# karten: Liste an Karten (Strings)
def gaussElim(n, k, m, karten):
    # Anlegen einer Matrix (transponierte Matrix => m und n sind vertauscht) 
    tMatrix = [[0 for _ in range(n+1)] for _ in range(m)]
    # Füllen der transponierten Matrix (Iteration über alle Reihen der ursprünglichen Matrix)
    for i in range(n):
        # Iteration über alle Spalten der ursprünglichen Matrix
        for j in range(m):
            # Einsetzen des Wertes in die transponierte Matrix
            tMatrix[j][i] = int(karten[i][j])
    # Hinzufügen einer Zeile für die Parität von k
    # tMatrix.append([1 for _ in range(n)]+[k % 2])
    # Eliminationsverfahren
    # Iteration über alle Reihen der transponierten Matrix (O(m))
    for r1 in range(len(tMatrix)):
        # Iteration über alle Spalten der transponierten Matrix (O(n))
        for c1 in range(len(tMatrix[r1])):
            # Überprüfung, ob es sich um die erste Eins in dieser Reihe handelt
            if tMatrix[r1][c1] == 1:
                # r1 muss auf alle anderen Reihen xored werden
                # => Iteration über alle anderen Reihen (O(m))
                for r2 in range(len(tMatrix)):
                    # Nur wenn eine 1 vorhanden ist und es sich nicht um die selbe Reihe handelt
                    if r1 != r2 and tMatrix[r2][c1] == 1:
                        # Die XOR-Operation muss auf jede Spalte angewendet werden O(m)
                        for c2 in range((len(tMatrix[r2]))):
                            # Anwenden der XOR Operation bzw. Addition in Z2
                            tMatrix[r2][c2] = (tMatrix[r2][c2] +
                                               tMatrix[r1][c2]) % 2
                # Dieser Prozess soll nur für die erste Eins in der Reihe durchgeführt werden
                break
    # Ausgabe der transponierten und eliminierten Matrix
    # for r in tMatrix:
    #   print(r)
    # Dictionary
    # (key: Index der Spalte bzw. Karte der Variable
    #  value: Liste an Indizes der Karten, welche von der Variable beeinflusst werden)
    variablen = {}
    # Iteration über alle Reihen der transponierten Matirx
    for i in range(len(tMatrix)):
        # Setzen des Indexes auf die Spalte, in welcher die erste 1 der Reihe vorkommt
        index = None
        # Iteration über alle (bis auf die letzte => ist überall 0) Spalte
        for j in range(len(tMatrix[i])-1):
            if tMatrix[i][j] == 1:
                # Überprüfung, ob es sich um die erste Eins handelt
                if index is None:
                    # Setzen des Indexes für die erste Eins
                    index = j
                else:
                    # Es handelt sich nicht um die erste Eins
                    # => Es ist eine unabhängige Variable
                    # Überprüfung ob diese Variable bereits aufgenommen wurde
                    if j not in variablen.keys():
                        # Hinzufügen einer neuen Variable
                        variablen[j] = [index]
                    else:
                        # Hinzufügen des Indexes in die beeinflussten Variablen
                        variablen[j].append(index)

    # Liste von Bitstrings der Länge n für jede Variable
    # => 1, wenn die Karte i von der Variable beeinflusst wird
    processedVariablen = []
    # Iteration über alle Variablen
    for variable in variablen.keys():
        processedVariablen.append("")
        # Iteration über alle Karten
        for i in range(n):
            # Hinzufügen einer "1", wenn die Karte von der Variable beeinflusst wird
            if i in variablen[variable] or i == variable:
                processedVariablen[-1] += "1"
            else:
                # Andernfalls muss ein "0" eingefügt werden
                processedVariablen[-1] += "0"
    # Brute forcen der Variablen Kombination
    print(len(processedVariablen))
    lösungen = []

    lösungen = [bfVars(k, processedVariablen, 0, [0,"0"], n)]
    processedLösungen = []
    for lösung in lösungen:
        processedLösungen.append([])
        for i in range(len(lösung)):
            if lösung[i] == "1":
                processedLösungen[-1].append(i)
    return processedLösungen

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
    lösungen = (bfAll(n, k+1, m, karten) if comb(n,ceil((k+1)/2)) < (0 if m > n else comb(n-m,k+1)) else gaussElim(n, k+1, m, karten))
    # Schreiben der Lösungsdatei
    with open("ergebnis_" + file, "w") as f:
        # Iteration über alle Lösungen
        for lösung in lösungen:
            # Itearation über alle Kartenindizes der Lösung
            for index in lösung:
                # Ausgabe der Lösung
                print(karten[index])
                # Schreiben der Kartenwerte in die Datei
                f.write(karten[index] + "\n")
            # Trennung der Lösungen über ein \n
            f.write("\n")
            print()


# Startpunkt des Programms
if __name__ == "__main__":
    # Aufnahme der Startzeit
    startTime = time()
    # Ausführung
    main()
    # Aufnhame der Endzeit
    endTime = time()
    # Ausgabe der Laufzeit
    print("--- {:.4f} Sekunden ---".format(endTime - startTime))
