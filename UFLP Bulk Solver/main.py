

import data_convertor
import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import uflp

directory = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir)) +"/data"
filenames = os.listdir("data/raw")
  
optdict = {}
for f in filenames:
    try:
        optfile = open("data/opt/" + f +".opt",'r')
        optval = optfile.readline().split()[-1]
        print("optimal value for file " + f + "is " + optval)
        optdict.update({f:int(optval)})
    except:
        print("no opt file found for "+ f)
    try:
        optfile = open("data/opt/" + f +".bub",'r')
        optval = optfile.readline().split()[-1]
        print("optimal value for file " + f + "is " + optval)
        optdict.update({f:int(optval)})
    except:
        print("no bub file found for "+ f)

print(optdict)
for f in filenames:
    try:
        
        data_convertor.convert(f)
    except:
        print("unable to parse filename : " + f)

total = 0
correct = 0
for f in filenames: 
    opt = SolverFactory('cplex')
    opt.options['timelimit'] = 30
    instance = uflp.model.create_instance("data/converted/"+f+".dat")
    opt.solve(instance,tee = True)
    total+=1
    deltapercent = ((pyo.value(instance.obj) - optdict.get(f) ) / pyo.value(instance.obj) ) * 100
    print ( "percentage difference from best value : " + str(deltapercent))
    print( pyo.value(instance.obj) )

    if int(pyo.value(instance.obj)) == optdict.get(f):
        correct+=1
    print(".", end =" ")
print ("total: " + str(total))
print ("correct: " + str(correct)) 
print((correct/total) * 100)
    


