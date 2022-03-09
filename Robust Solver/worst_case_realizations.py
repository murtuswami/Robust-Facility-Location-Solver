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

import functools

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
        

# take a sum of the distance to all facilites average it then take percentage of that value as radius or deviation constant 
#percentage is same for all nodes but since the distnaces are all different the deviations change 

def make_model(dis,op,N,M):
    #distance is distances
    #op is opening costs 
    #n is a set containing the customers identity 
    #m is a set containing the demand nodes identity 
    model = ConcreteModel(name="(uflp)")


    model.x = Var(N, M, bounds=(0,1)) # (selected routes )
    model.y = Var(N, within=Binary)       #selected warehouses 

    def obj_rule(model):
        return sum(dis[n,m]*model.x[n,m] for n in N for m in M) + sum(op[n]*model.y[n] for n in N )
    model.obj = Objective(rule=obj_rule)

    def restrict_cust(model, m):
        return sum(model.x[n,m] for n in N) == 1
    model.one_per_cust = Constraint(M,rule=restrict_cust)

    def must_be_active(model, n, m):
        return model.x[n,m] <= model.y[n]
    model.warehouse_active = Constraint(N, M, rule=must_be_active)
    return model

dp = 51 #deviation percentage, will generate multiple deviations up to and include this percentage 
f = open("worstcaserealizations.csv","w")

"""
#Solve dp problems incrementing p by one 
for p in range(0,dp):
    #deviations is in the form [cust][fac]
    #we want to transform into average accross customer 
    averages = [] 
    for x in arrRepresentation:
        averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
    deviations = []

    #Get the deviation by taking a percentage of the average for each customer 
    for n,x in enumerate(averages):
        deviations.append((n+1,(x/100)* p))

    devDict = {} # create dictionary of deviations for each customer 
    for d in deviations:   
        devDict.update({d[0]:d[1]})

    opt = SolverFactory('cplex')
    opt.options['timelimit'] = 30

    #make a dictionary for input when all values take on their worst case realization
    worstCaseDistances = {}

    for key in paramd:
        worstCaseDistances.update({key: paramd.get(key)+ devDict.get(key[1])})


    worstCaseModel = make_model(worstCaseDistances,paramo,setN,setM)
    opt.solve(worstCaseModel)
    print("Worst Case Realaization", pyo.value(worstCaseModel.obj))
    f.write(str(p))
    f.write(",")
    f.write(str(pyo.value(worstCaseModel.obj)))
    f.write("\n")
"""
#solve dp = 5,start from 0 and increment by 0.1 
dec = 0 
while dec <= 5:
    averages = [] 
    for x in arrRepresentation:
        averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
    deviations = []

    #Get the deviation by taking a percentage of the average for each customer 
    for n,x in enumerate(averages):
        deviations.append((n+1,(x/100)* dec))

    devDict = {} # create dictionary of deviations for each customer 
    for d in deviations:   
        devDict.update({d[0]:d[1]})

    opt = SolverFactory('cplex')
    opt.options['timelimit'] = 30

    #make a dictionary for input when all values take on their worst case realization
    worstCaseDistances = {}

    for key in paramd:
        worstCaseDistances.update({key: paramd.get(key)+ devDict.get(key[1])})


    worstCaseModel = make_model(worstCaseDistances,paramo,setN,setM)
    opt.solve(worstCaseModel)
    print("Worst Case Realaization", pyo.value(worstCaseModel.obj))
    f.write(str(dec))
    f.write(",")
    f.write(str(pyo.value(worstCaseModel.obj)))
    f.write("\n")
    dec = dec + 0.1




 