# Zeitmessung der Execution-Time
import time
# Zum Überprüfen ob Files exisitieren
from os.path import exists
# Zur Übergabe von Argumenten in der Kommandozeile
from sys import argv

# Funktion für das Lösen des Problems
def solve(n,anzahl,m,karten):
    lösungen = []
    for i in range(n):
        print ("NEW SICHERUNGSKARTE ============>>>>")
        sicherungsKarte = karten[i]
        # Liste an zunächst möglichen Gruppen, nur beim ersten Bit relevant
        möglicheGruppen = []
        # Liste an Gruppen, welche die Kriterien erfüllen
        abgeschlosseneGruppen = []
        # Für jedes Bit von rechts nach links
        for b in range(m-1,-1,-1):
            # Beim ersten Bit sollen die möglichen Gruppen erstellt werden
            if b == m-1:
                # Für jede andere Karte im Stapel
                for j in range(n):
                    if j != i:
                        # Bildung der Gruppen
                        for gruppe in möglicheGruppen:
                            neueGruppe = [gruppe[0] + [j], gruppe[1]+int(karten[j][b])]
                            if len(neueGruppe[0]) == anzahl:
                                if neueGruppe[1]%2 == int(sicherungsKarte[b]):
                                    abgeschlosseneGruppen.append(neueGruppe[0])
                            else:
                                möglicheGruppen.append(neueGruppe)
                        if n-j >= anzahl:
                            möglicheGruppen.append([[j],int(karten[j][b])])
            else:
                print(len(abgeschlosseneGruppen))
                # Anwendung der Gruppen
                for gruppe in abgeschlosseneGruppen:
                    summe = 0
                    for index in gruppe:
                        summe += int(karten[index][b])
                    if summe % 2 != int(sicherungsKarte[b]):
                        abgeschlosseneGruppen.remove(gruppe) 

        print(abgeschlosseneGruppen)
        if len(abgeschlosseneGruppen) != 0:
            for gruppe in abgeschlosseneGruppen:
                lösung = gruppe + [i]
                lösungen.append(lösung)
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
        return n,k,m,karten,file


def main():  # Startpunkt des Programmes
    input = parseInput()  # Lesen des Inputs
    if(input is None):
        return
    # Lösen des Problems
    lösungen = solve(input[0], input[1], input[2], input[3])
    # Ausgabe der Lösungszahl
    # Schreiben der Lösungsdatei
    with open("ergebnis_" + input[4], "w") as f:
        for lösung in lösungen:
            for index in lösung:
                f.write(input[3][index] + "\n")
            f.write("\n")


if __name__ == "__main__":
    start_time = time.time()  # Startzeit des Programmes
    main()
    # Ausgeben der Execution-Time
    print("--- %s Sekunden ---" % round(time.time() - start_time, 4))
