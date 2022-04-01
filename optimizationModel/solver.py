""" Imports data file, processes it, define a Pyomo model for solving the UFLP and solve with processed data as input"""
import os
import tkinter
from tkinter import filedialog
import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.environ import *


### Get Data from file and convert it into format appropriate for Pyomo Model ### 
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
setM = [*range(1,m+1)]
setN = [*range(1,n+1)]
paramo ={} #Opening Costs 
paramd={}  #Distances 

for x in arr:
    fac = x[0]
    cost = x[1]
    paramo.update({int(fac):int(cost)})
    del x[:2]
    for index, c in enumerate(x):
        paramd.update({(int(fac),index+1):int(c)})

opt = SolverFactory('cplex') 
opt.options['timelimit'] = 180 #3 mins time limit 
model = make_model(paramd,paramo,setN,setM)
opt.solve(model,tee = True,logfile ="results.txt") #Solve model with verbose settings 
print( pyo.value(model.obj) )


