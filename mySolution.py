import sys
from math import ceil

def secToBoom(line: str):
    rates = [float(obj) for obj in line.rstrip().split(' ')]
    storage = rates.pop(0)
    rates = [1.0/r for r in rates]
    rate = sum(rates)
    ETA = ceil(storage/rate)
    print(ETA)


for line in sys.stdin:
    secToBoom(line)
    
    