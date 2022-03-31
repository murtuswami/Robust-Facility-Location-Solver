#Worst case realizations
#Calculates worst case realizations of the problems starting from 0 up to p 


import os
import tkinter
from tkinter import filedialog
import os

import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.environ import *
import math
from model import make_model


print("converting data ... ")
arr = []
tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
print("Please select file with input data")
inputdatapath = filedialog.askopenfilename()
print(inputdatapath)
filename = os.path.basename(inputdatapath)
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
        



dp = 50 #deviation percentage, will generate multiple deviations up to and include this percentage 
f = open("worstcaserealizations.csv","w")
averages = [] 
for x in arrRepresentation:
    averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
deviations = []
#Solve dp problems incrementing p by one 
p=0
while p <= dp:
    #deviations is in the form [cust][fac]
    #we want to transform into average accross customer 
 

    #Get the deviation by taking a percentage of the average for each customer 
    for count,x in enumerate(averages):
        deviations.append((count+1,(x/100)* p))

    devDict = {} # create dictionary of deviations for each customer 
    for d in deviations:   
        devDict.update({d[0]:d[1]})

    opt = SolverFactory('cplex')
    

    #make a dictionary for input when all values take on their worst case realization
    worstCaseDistances = {}
    worstCaseDistancesBox = {} 

    for key in paramd:
        worstCaseDistances.update({key: paramd.get(key)+ devDict.get(key[1])})
    for key in paramd:
        box_dist = math.sqrt(   math.pow( paramd.get(key) + devDict.get(key[1]),2)   + math.pow(devDict.get(key[1]),2 ))
        worstCaseDistancesBox.update({key: box_dist})

    worstCaseModel = make_model(worstCaseDistances,paramo,setN,setM)
    worstCaseBoxModel = make_model(worstCaseDistancesBox,paramo,setN,setM)
    opt.solve(worstCaseModel)
    opt.solve(worstCaseBoxModel)
    print("Worst Case Realization", pyo.value(worstCaseModel.obj),"Box Worst Case:" ,pyo.value(worstCaseBoxModel.obj))
    f.write(str(p))
    f.write(",")
    f.write(str(pyo.value(worstCaseModel.obj)))
    f.write(",")
    f.write("interval")
    f.write("\n")

    f.write(str(p))
    f.write(",")
    f.write(str(pyo.value(worstCaseBoxModel.obj)))
    f.write(",")
    f.write("box")
    f.write("\n")

   
   
    p = p + 1
