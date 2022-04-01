

import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from model import make_model

def robustSolver(wc,paramd,paramo,setN,setM,devDict): 
    opt = SolverFactory('cplex')
    solutions = [] # array of n nominal solution values 

#solve l nominal problems with modified deviations 
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
        solutions.append( (dc*wc + pyo.value(model.obj),sol_arr ) ) 

#solve l+1th nominal problem set dc to 0 
    dc = 0 
    distances = paramd.copy()
    for node in distances.keys():
        distances.update({node:(distances.get(node) + (max(devDict.get(node[1]) - dc,0)))})
    model = make_model(distances,paramo, setN,setM)
    opt.solve(model)
    
 
    sol_arr = [] 
    for i in model.y:
        sol_arr.append( (i, model.y[i].value))
    solutions.append( (dc*wc + pyo.value(model.obj),sol_arr ) )
    solution = min ( solutions ,key = lambda t:t[0]) # extract robust solution 


#make a dictionary for input when all values take on their worst case realization , equivalent to dc = 0 
    worstCaseDistances = {}
    for key in paramd:
        worstCaseDistances.update({key: paramd.get(key)+ devDict.get(key[1])})

    worstCaseModel = make_model(worstCaseDistances,paramo,setN,setM)
    opt.solve(worstCaseModel)
    print("finished solving nominal instances")
    print("Robust Solution:", solution[0])
    print("when dc = 0 objective value is  ", dc *wc + pyo.value(model.obj))
    print("Worst Case Realaization is ", pyo.value(worstCaseModel.obj))
    return solution
    



    





