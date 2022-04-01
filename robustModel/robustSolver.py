
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from model import make_model

"""
Cardinality Constrained Robustness model produces a robust solution to the UFLP with Spatial Demand Uncertainty
solves l+1 nominal problems with solutions modified by constant to produce a robust solution  

Parameters
    wc: Integer number of parameters at their worst case realisation
    dist: Dictionary of distances in the form (Facilty,Customer): Distance 
    o: Dictionary of opening costs in the form Facility: Cost 
    N: Array containing facility identities
    M Array containing customer identities
    devDict:  A Sorted dictionary  of deviations in the form  (customer,deviation) 

Returns  
    Robust solution value and Robust Solution Assignment
Description 
    Uses Cardinality Constrained Robustness model to solve the UFLP with wc customers at their worst case spatial realization
    Iterates over deviation dictionary,at each iteration
         Modifies the distances by dl -dc 
         Solves model with modified distances 
         Modifies solution by dc * wc where dc is the deviation in said iteration 
    Returns solution with minimum value 

"""


def robustSolver(wc,dist,o,N,M,devDict): 
    opt = SolverFactory('cplex')
    solutions = [] # array of n nominal solution values, populated during iterations 

 #solve l nominal problems with modified deviations 
    for l in devDict.keys():    #dictionary is sorted  so d1 >= d2 ... >= dl holds 
        dc = devDict.get(l)     #constant for this iteration
        # Copy dictionary and update for this iteration 
        distances = dist.copy()
        for node in distances.keys(): 
            distances.update({node:(distances.get(node) + (max(devDict.get(node[1]) - dc,0)))})
        # Solve model with updated distances 
        model = make_model(distances,o,N,M)
        opt.solve(model)
        print(dc*wc +pyo.value(model.obj) )
        sol_arr = []
        #Capture assignment 
        for i in model.y:
            sol_arr.append( (i, model.y[i].value))
        solutions.append( (dc*wc + pyo.value(model.obj),sol_arr ) ) # capture solution and assignment 

#solve l+1th nominal problem set dc to 0, corresponds to worst case realization 
    dc = 0 
    distances = dist.copy()
    for node in distances.keys():
        distances.update({node:(distances.get(node) + (max(devDict.get(node[1]) - dc,0)))})
    model = make_model(distances,o, N,M)
    opt.solve(model)
    sol_arr = [] 
    for i in model.y:
        sol_arr.append( (i, model.y[i].value))
    solutions.append( (dc*wc + pyo.value(model.obj),sol_arr ) )
    
    
    #get the minimum value from the solutions 
    solution = min ( solutions ,key = lambda t:t[0]) 


#make a dictionary for input when all values take on their worst case realization , equivalent to dc = 0 
    worstCaseDistances = {}
    for key in dist:
        worstCaseDistances.update({key: dist.get(key)+ devDict.get(key[1])})

    worstCaseModel = make_model(worstCaseDistances,o,N,M)
    opt.solve(worstCaseModel)
    print("finished solving nominal instances")
    
    print("Robust Solution:", solution[0])
    #Following two should be equivalent
    print("when dc = 0 objective value is  ", dc *wc + pyo.value(model.obj))
    print("Worst Case realisation is ", pyo.value(worstCaseModel.obj))
    return solution
    



    





