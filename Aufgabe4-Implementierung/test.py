import time
# Python3
t1 = time.process_time()
a = 100234555
b = 22333335
c = 341500
for i in range(1, 1000000000):
    if i % 100000000 == 0:
        print(i)
    a = a - (b % 2)
    b = b - (c % 2)
print("Sum is", a+b)
t2 = time.process_time()
print(t2-t1, "Seconds")
