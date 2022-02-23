
import os
import tkinter
from tkinter import filedialog
import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.environ import *
import uflp

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
setM = [*range(1,m+1)]
setN = [*range(1,n+1)]
paramo ={}
paramd={}

for x in arr:
    fac = x[0]
    cost = x[1]
    paramo.update({int(fac):int(cost)})
    del x[:2]
        
    for index, c in enumerate(x):
        paramd.update({(int(fac),index+1):int(c)})

print(paramd)

print(paramo)

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


opt = SolverFactory('cplex')
opt.options['timelimit'] = 30
model = make_model(paramd,paramo,setN,setM)
print(model)
opt.solve(model,tee = True)
print( pyo.value(model.obj) )


