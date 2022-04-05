# Zur Übergabe von Argumenten in der Kommandozeile
from logging import info
import time
from os.path import exists
from A3 import *
from sys import argv
import matplotlib.pyplot as plt
import random as r
# Für sehr große Eingaben, muss das Rekursionslimit hochgestellt werden
from sys import setrecursionlimit
setrecursionlimit(1500)
# Zum Überprüfen ob Files exisitieren
# Zeitmessung der Execution-Time

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

def testTime():
    m = 100
    times = []
    for i in range(1, 10):
        hx = ""
        s = time.time() 
        for _ in range(i):
            hx += list(hexInSSD.keys())[r.randint(0, len(hexInSSD.keys())-1)]
        solve(hx, m)
        e = time.time()
        times.append([i,e-s])
    plt.plot(list(zip(*times))[0], list(zip(*times))[1])
    plt.show()

if __name__ == "__main__":  
    testTime()

