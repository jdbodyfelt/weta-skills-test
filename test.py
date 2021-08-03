import sys



for line in sys.stdin:
    data =  [float(obj) for obj in line.rstrip().split(' ')]
    print(data)
    