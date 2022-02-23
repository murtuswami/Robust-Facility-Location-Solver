
import os
import tkinter
from tkinter import filedialog
import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.environ import *

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
dp = 5 #deviation percentage


#deviations is in the form [cust][fac]
#we want to transform into average accross customer 
averages = [] 
for x in arrRepresentation:

    averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
deviations = []
dp = 5
for x in averages:
    deviations.append((x/100)* 5)

print(deviations)

def make_model(dis,op,N,M,d,dc):
    #distance is distances dictionary in the form (n,m):d , where n is a customer , m is a demand node, d is distance between both
    #op is opening costs in form n:c , where is facility c is cost 
    #n is a set containing the customers identity [1,..n] starting from 1 
    #m is a set containing the demand nodes identity [1,...m], which have been sorted in order of their deviation constant values in descending order 
    #dev is a set of devation constants (worst case deviation), [(1:d),...(n:d))] 
    #dc is the deviation constant term dl for this particular nominal instance 
    model = ConcreteModel(name="(uflp)")


    model.x = Var(N, M, bounds=(0,1)) # (selected routes )
    model.y = Var(N, within=Binary)       #selected warehouses 

    def obj_rule(model):    
        return sum( (dis[n,m] +max({d[n,m],0}))*model.x[n,m] for n in N for m in M) + sum(op[n]*model.y[n] for n in N ) 
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


