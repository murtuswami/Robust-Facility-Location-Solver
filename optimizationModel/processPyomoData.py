
import tkinter
from tkinter import filedialog

"""
Takes Data from file and converts into into solveable form for Pyomo model 

Parameters
    n/a 
Returns 
   n: number of facilities
   m: number of customers 
   d: dictionary of distances in form (Facilty,Customer): Distance 
   o: dictionary of opening costs in the form  Facility : Cost
   arrRepresentation: A 2D representation of d (for calculating deviations )
   N: Array containing facility identities
   M Array containing customer identities

   
Description 
    Creates an Pyomo model object for solving a given Uncapacitated Facility Location Problem instance 
"""

def processPyomoData():
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

    M = [*range(1,m+1)]
    N = [*range(1,n+1)]
    o ={}
    d={}
    arrRepresentation = [[] for _ in range(0,m)]

    for x in arr:
        fac = x[0] # first entry is the facility identifier 
        cost = x[1] # second entry is the cost of opening said facility 
        o.update({int(fac):int(cost)})
        del x[:2]
            
        for index, c in enumerate(x): # all other entries are cost of connecting to customer number, counting starts from 1 
            d.update({(int(fac),index+1):int(c)})
            arrRepresentation[index].append(int(c))
    return n,m,d,o,arrRepresentation,N,M