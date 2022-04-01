
import tkinter
from tkinter import filedialog

def processRobustPyomoData():
    arr = []
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    print("Please select file with input data")
    inputdatapath = filedialog.askopenfilename()

    file = open(inputdatapath)
    for line in file:
        arr.append(line.rstrip().split())

    initVals = arr[1]
    del arr[:2]
    m = int(initVals[1])
    n = int(initVals[0]) 
    print(m)
    setM = [*range(1,m+1)]
    setN = [*range(1,n+1)]
    paramo ={}
    paramd={}
    arrRepresentation = [[] for _ in range(0,m)]
    print(arrRepresentation)

    print(m)
    for x in arr:
        fac = x[0] # first entry is the facility identifier 
        cost = x[1] # second entry is the cost of opening said facility 
        paramo.update({int(fac):int(cost)})
        del x[:2]
            
        for index, c in enumerate(x): # all other entries are cost of connecting to customer number, counting starts from 1 
            paramd.update({(int(fac),index+1):int(c)})
            arrRepresentation[index].append(int(c))
    return n,m,paramd,paramo,arrRepresentation,setN,setM