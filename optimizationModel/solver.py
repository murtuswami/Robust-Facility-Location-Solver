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

### Create and solve Model  ###
"""
Parameters
    dis: Dictionary of distances in the form ( (facility,customer ) : distance )
    op: Dictionary of opening costs 
    N:  Array of Facility
    M:  Array of Customer Identities
Returns 
    Model ( not solved ) representing the given instance of the Uncapacitated Facility Location Problem 
Description 
    Creates an Pyomo model object for solving a given Uncapacitated Facility Location Problem instance 
"""

def make_model(dis,op,N,M):

    model = ConcreteModel(name="(uflp)")

    model.x = Var(N, M, bounds=(0,1))   #Decision Variable for selected routes 
    model.y = Var(N, within=Binary)     #Decision variables for opened facilities 

    #Objective function, sum of selected distances and open facilities opening costs 
    def obj_rule(model):
        return sum(dis[n,m]*model.x[n,m] for n in N for m in M) + sum(op[n]*model.y[n] for n in N )
    model.obj = Objective(rule=obj_rule)

    #Each customer is served by only one facility, 
    def restrict_cust(model, m):
        return sum(model.x[n,m] for n in N) == 1
    model.one_per_cust = Constraint(M,rule=restrict_cust)

    #Each customer must have their demand met by some facility 
    def must_be_active(model, n, m):
        return model.x[n,m] <= model.y[n]
    model.warehouse_active = Constraint(N, M, rule=must_be_active)
    return model

opt = SolverFactory('cplex') 
opt.options['timelimit'] = 180 #3 mins time limit 
model = make_model(paramd,paramo,setN,setM)
opt.solve(model,tee = True,logfile ="results.txt") #Solve model with verbose settings 
print( pyo.value(model.obj) )


