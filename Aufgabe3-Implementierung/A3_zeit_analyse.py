### Dieses Programm dient zur Messung der Entwicklung der Reallaufzeit von A3.py
import time
from A3 import *
import matplotlib.pyplot as plt
import random as r
from sys import setrecursionlimit
setrecursionlimit(1500)

# Funktion zum Herausfinden von allen Tripel
def bruteAllPossiblities():
    possibilites = set()
    umsätze = set()
    u = set()
    tripel = set()
    for ziffer in hexInSSD.keys():
        for zielZiffer in hexInSSD.keys():
            dS = 0
            m = 0
            for segment in range(7):
                # Segment muss weggenommen werden
                if hexInSSD[ziffer][segment] > hexInSSD[zielZiffer][segment]:
                    m += 1
                    dS += 1
                # Segment muss eingesetzt werden
                elif hexInSSD[ziffer][segment] < hexInSSD[zielZiffer][segment]:
                    dS -= 1

            zielWert = list(hexInSSD.keys()).index(zielZiffer)
            zifferWert = list(hexInSSD.keys()).index(ziffer)
            profit = (zielWert-zifferWert)

            umsätze.add(dS)
            u.add(m)
            tripel.add((profit, dS, m))
            possibilites.add(
                (m, dS, profit, zifferWert, sum(hexInSSD[ziffer])))

    print(possibilites, len(possibilites))
    print(tripel, len(tripel))
    x = list(zip(*possibilites))[1]
    y = list(zip(*possibilites))[0]
    plt.scatter(x, y)
    plt.xlabel("$\Delta S$")
    plt.ylabel("$m'$")
    plt.show()

# Zeit-Testungen
def testTime():
    times = []
    for i in range(1, 1000):
        hx = ""
        s = time()
        for _ in range(i):
            hx += list(hexInSSD.keys())[r.randint(0, len(hexInSSD.keys())-1)]
        result = maximieren(hx, r.randint(int(i*0.5), int(i*1.5)))
        if i%100 == 0:
            #print(hx, result[0], i)
            print(i)
        e = time()
        times.append([i, e-s])
    plt.xlabel("n (Anzahl an Ziffern)")
    plt.ylabel("Reallaufzeit in s")
    plt.plot(list(zip(*times))[0], list(zip(*times))[1])
    plt.show()


if __name__ == "__main__":
    testTime()
