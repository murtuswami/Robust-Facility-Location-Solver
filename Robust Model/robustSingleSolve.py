
import os
import tkinter
from tkinter import filedialog
import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
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
        

# take a sum of the distance to all facilites average it then take percentage of that value as radius or deviation constant 
#percentage is same for all nodes but since the distnaces are all different the deviations change 

#deviations is in the form [cust][fac]
#we want to transform into average accross customer 
averages = [] 
for x in arrRepresentation:
    averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
deviations = []
dp = 50
for count,x in enumerate(averages):
    deviations.append((count+1,round((x/100)* dp,2)))
#sort by deviations 
sortByDeviation = sorted(deviations,key = lambda tup:tup[1],reverse=True)

print(sortByDeviation)
devDict = {} # create dictionary 
for d in sortByDeviation:   
    devDict.update({d[0]:d[1]})



    
# this is not used in modelling but is included to show what a more production friendly alternative might look like 
def make_robust_model(dis,op,N,M,d,dc):
 
    model = ConcreteModel(name="(uflp_robust)")
    model.x = Var(N, M, bounds=(0,1)) # (selected routes )
    model.y = Var(N, within=Binary)       #selected facilities

    def obj_rule(model):    
        return sum( (dis[n,m] +max((d[m]- dc),0))*model.x[n,m] for n in N for m in M) + sum(op[n]*model.y[n] for n in N ) 
    model.obj = Objective(rule=obj_rule)

    def restrict_cust(model, m):
        return sum(model.x[n,m] for n in N) == 1
    model.one_per_cust = Constraint(M,rule=restrict_cust)

    def must_be_active(model, n, m):
        return model.x[n,m] <= model.y[n]
    model.warehouse_active = Constraint(N, M, rule=must_be_active)
    
    return model
def make_model(dis,op,N,M):

    model = ConcreteModel(name="(uflp)")


    model.x = Var(N, M, bounds=(0,1)) 
    model.y = Var(N, within=Binary)      

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

wc = 75
f1 = open("vary_gamma.csv","a")
f2 = open("wc_" + str(wc) + ".csv","w" )
opt = SolverFactory('cplex')
solutions = []
solution_values= []
for l in devDict.keys():    
    dc = devDict.get(l)
    distances = paramd.copy()
    for node in distances.keys():
        distances.update({node:(distances.get(node) + (max(devDict.get(node[1]) - dc,0)))})
    model = make_model(distances,paramo,setN,setM)
    opt.solve(model)
    print(dc*wc +pyo.value(model.obj) )
    sol_arr = []
    for i in model.y:
        sol_arr.append( (i, model.y[i].value))
    
    f2.write(str(dc*wc + pyo.value(model.obj)))
    f2.write("\n")
    solutions.append(dc*wc + pyo.value(model.obj))
    solution_values.append(sol_arr)

#solve l+1th = 0 nominal problem this corresponds to the worst case realization 
dc = 0 
distances = paramd.copy()
for node in distances.keys():
    distances.update({node:(distances.get(node) + (max(devDict.get(node[1]) - dc,0)))})
model = make_model(distances,paramo, setN,setM)
opt.solve(model)
print("dc= 0 ", dc *wc + pyo.value(model.obj))
solutions.append(dc *wc + pyo.value(model.obj))
f2.write(str(dc*wc + pyo.value(model.obj)))
f2.write("\n")

solutions.append(dc*wc + pyo.value(model.obj))
solution = min ( solutions )
#make a dictionary for input when all values take on their worst case realization , equivalent to dc = 0 

worstCaseDistances = {}
for key in paramd:
    worstCaseDistances.update({key: paramd.get(key)+ devDict.get(key[1])})

worstCaseModel = make_model(worstCaseDistances,paramo,setN,setM)
opt.solve(worstCaseModel)
f1.write(str(wc))
f1.write(",")
f1.write(str(solution))
f1.write("\n")
print("Robust Solution:", solution)
print("Worst Case Realaization", pyo.value(worstCaseModel.obj))
print(solution_values)

x1= 0
x2 = 1 

while x2 < len(solution_values):
    difference_count = 0
    for n,x in enumerate(solution_values[x1]):
        if x[1] != solution_values[x2][n][1]:
            difference_count = difference_count+ 1
    print(difference_count)
    x1 = x1 +1
    x2 = x2 +1

    





