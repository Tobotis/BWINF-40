# Zur Übergabe von Argumenten in der Kommandozeile
from sys import argv
# Zum Überprüfen ob Files exisitieren
from os.path import exists
# Zeitmessung der Execution-Time
import time


hexInSSD = {
    "0": [1, 1, 1, 1, 1, 1, 0],
    "1": [0, 1, 1, 0, 0, 0, 0],
    "2": [1, 1, 0, 1, 1, 0, 1],
    "3": [1, 1, 1, 1, 0, 0, 1],
    "4": [0, 1, 1, 0, 0, 1, 1],
    "5": [1, 0, 1, 1, 0, 1, 1],
    "6": [1, 0, 1, 1, 1, 1, 1],
    "7": [1, 1, 1, 0, 0, 0, 0],
    "8": [1, 1, 1, 1, 1, 1, 1],
    "9": [1, 1, 1, 1, 0, 1, 1],
    "A": [1, 1, 1, 0, 1, 1, 1],
    "B": [0, 0, 1, 1, 1, 1, 1],
    "C": [1, 0, 0, 1, 1, 1, 0],
    "D": [0, 1, 1, 1, 1, 0, 1],
    "E": [1, 0, 0, 1, 1, 1, 1],
    "F": [1, 0, 0, 0, 1, 1, 1],
}
def umwandlungen(übrigerUmsatz, übrigeUmlegungen, ziffer):
    # Umformungen der Ziffern in eine andere Ziffer
    # [Anzahl der Umlegungen, Umsatz (wie viele Stäbchen bleiben insgesamt über/werde insegesamt abgegeben)]
    umwandlungen = {
        ziffer: (0, 0),
    }
    for i in hexInSSD.keys():
        if i != ziffer:
            übrigeSegemente = übrigerUmsatz
            anzahlUmlegungen = 0
            for segment in range(7):
                # Check ob das Segment in der Ausgangsziffer fehlt
                if hexInSSD[i][segment] > hexInSSD[ziffer][segment]:
                    # Es wird nur eine neue Umlegung durchgeführt, wenn es keine übrigen Segmente gibt
                    anzahlUmlegungen += 1 if übrigeSegemente <= 0 else 0
                    # Ein "übrigesSegment" wird verwendet (selbst wenn keine übrig sind)
                    übrigeSegemente -= 1
                # Check ob ein Segment in der Ausgangsziffer zu viel ist
                elif hexInSSD[i][segment] < hexInSSD[ziffer][segment]:
                    # Es wird nur eine neue Umlegung durchgeführt, wenn es woanders kein "Bedarf" gibt
                    anzahlUmlegungen += 0 if übrigeSegemente < 0 else 1
                    # Ein "übrigesSegment" wird hinzugefügt
                    übrigeSegemente += 1
                # Die Umformung ist nicht möglich, wenn die übrige Umlegungen nicht genug sind
                if anzahlUmlegungen > übrigeUmlegungen:
                    break
            else:
                # Wenn nicht aus der for-Loop gebreakt wurde
                umwandlungen[i] = (anzahlUmlegungen, übrigeSegemente)

    return umwandlungen



def solve(hexZahl):
    for ziffer in hexZahl:
        umwandlungen(0,3,ziffer)


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
        return inhalt


def main():  # Startpunkt des Programmes
    input = parseInput()  # Lesen des Inputs
    if(input is None):
        return
    # Lösen des Problems
    for i in input:
        solve(i)


if __name__ == "__main__":  # Das ist Python :)
    start_time = time.time()  # Messung der Start-Zeit
    main()
    print("--- %s Sekunden ---" %
          round(time.time() - start_time, 4))  # Ausgeben der Execution-Time
