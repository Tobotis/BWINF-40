# Zur Übergabe von Argumenten in der Kommandozeile
from sys import argv
# Zum Überprüfen ob Files exisitieren
from os.path import exists
# Zeitmessung der Execution-Time
import time

# Dictinoary mit den Segmenten des Sieben-Segment-Displays
# Zum Konvertieren einer Hexadezimalzahl (Key) in eine Liste mit den Segmenten, die "leuchten" (Value)
# 1: Segment ist an; 2: Segment ist aus
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

# Die Umwandlung einer Hexadezimalzahl im Sieben-Segment-Display kann ausgeführt werden
# übrigerUmsatz = Segemnte, die nach dem umwandeln übrig sind
# übrigeUmelgungen = Umlegungen, die maximal getätigt werden dürfen
# index = Index der aktuellen Ziffer in der Hexadezimalzahl
# hexZahl = Hexadezimalzahl, die umwandelt werden soll
# nurErhöhung = True, wenn die eingebene Ziffer nur erhöht werden darf
# schritte = Liste der Schritte/Umlegungen, die getätigt wurden


def umwandeln(übrigerUmsatz, übrigeUmlegungen, index, hexZahl, nurErhöhung=False, schritte=[]):
    # Check ob zu viele Segmente übrig sind (die Segemente können keines Falls in den "hinteren" Ziffern untergebracht werden)
    # => Check ob der Umsatz größer ist, als es freie Segmente gibt
    if übrigerUmsatz > (7 * len(hexZahl[index:]))-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]):
        return []
    # Check ob zu viele Segement im voraus verwendet wurden (die Segemnte können keines Falls in den "hinteren" Ziffern gewonnen werden)
    # => Check ob der Umsatz kleiner ist (große negative Zahl), als es gefüllte Segmente gibt, wenn in jeder Ziffer noch mindestens zwei Segmente sein müssen (=1)
    if übrigerUmsatz < (-sum([sum(hexInSSD[i]) for i in hexZahl[index:]]) + 2*len(hexZahl[index:])):
        return []
    # Check ob alle Ziffern umwandelt wurden => man ist am Ende der Hexzahl angekommen
    if index >= len(hexZahl):
        # Check ob Segmente übrig sind => Die Lösung ist nich valid
        if übrigerUmsatz != 0:
            return []
        # Die Lösung ist valid und die Schritte können zurückgegeben werden
        return [schritte, übrigeUmlegungen]
    # Festlegen der aktuellen Ziffer
    ziffer = hexZahl[index]
    # TODO REMOVE
    # print("Ziffer", ziffer, "Schritte", schritte, "Übrig",
    #     übrigerUmsatz, "Umlegungen", übrigeUmlegungen)
    # Iteration über alle anderen Hexziffern von F bis 0
    for i in hexInSSD.keys():
        # Check ob man bei der aktuellen Ziffen angekommen ist
        # Es folgen somit niedrigere Hexziffern
        if i == ziffer and nurErhöhung:
            # Falls nur höhere Hexziffern überprüft werden sollten, wird die Schleife verlassen
            break
        # Die übrigenSegmente entsprechen dem übrigen Umsatz
        übrigeSegemente = übrigerUmsatz
        # Anzahl der Umlegungen nach i wird mit 0 initialisiert
        anzahlUmlegungen = 0
        # Iteration über alle Segmente der Ziffern
        for segment in range(7):
            # Check ob das Segment von i in der Ausgangsziffer fehlt
            if hexInSSD[i][segment] > hexInSSD[ziffer][segment]:
                # Es wird nur eine neue Umlegung durchgeführt, wenn es keine übrigen Segmente gibt
                anzahlUmlegungen += 1 if übrigeSegemente <= 0 else 0
                # Ein "übrigesSegment" wird verwendet (selbst wenn keine übrig sind =>
                # möglicherweise kann es in der nächsten Ziffer erzeugt werden)
                übrigeSegemente -= 1
            # Check ob ein Segment von i in der Ausgangsziffer zu viel ist
            elif hexInSSD[i][segment] < hexInSSD[ziffer][segment]:
                # Es wird nur eine neue Umlegung durchgeführt, wenn es woanders kein "Bedarf" gibt
                anzahlUmlegungen += 0 if übrigeSegemente < 0 else 1
                # Ein "übrigesSegment" wird hinzugefügt
                übrigeSegemente += 1
            # Die Umformung ist nicht möglich, wenn die übrige Umlegungen nicht genug sind
            if anzahlUmlegungen > übrigeUmlegungen:
                break
        else:
            # Wenn nicht aus der for-Loop gebreakt wurde, kann die Ziffer offensichtlich un Ziffer i umwandelt werden
            # Darauf basierend, werden die Schritte für die nächste Ziffer erzeugt
            result = umwandeln(übrigeSegemente, übrigeUmlegungen -
                               anzahlUmlegungen, index+1, hexZahl, False, schritte+[[ziffer, i]])
            # Wenn eine Lösung gefunden wurde, wird diese zurückgegeben
            # Es ist die größtmögliche, da von F nach 0 iteriert wird
            if len(result) > 0:
                return result
    # Es wurde keine Lösung gefunden
    return []


def solve(hexZahl, maxUmlegungen):
    for index in range(len(hexZahl)):
        result = umwandeln(0, maxUmlegungen, index,
                           hexZahl, nurErhöhung=True, schritte=[[i, i]for i in hexZahl[:index]])
        if len(result) > 0 or index == len(hexZahl)-1:
            if result == []:
                print("No solution found")
            else:
                ergebnis = ""
                for ziffer in result[0]:
                    ergebnis += ziffer[1]
                print(ergebnis, "mit", maxUmlegungen-result[1], "Umlegungen")
                return




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
        print("SOLVING:", i)
        solve(i[0], int(i[1]))


if __name__ == "__main__":  # Das ist Python :)
    start_time = time.time()  # Messung der Start-Zeit
    main()
    print("--- %s Sekunden ---" %
          round(time.time() - start_time, 4))  # Ausgeben der Execution-Time
