#Worst case realizations
#Calculates worst case realizations of the problems starting from 0 up to p 

import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.environ import *
from  processRobustPyomoData import processRobustPyomoData
import math
from model import make_model

n,m,dist,o,arr,N,M = processRobustPyomoData()

averages = [] 
for x in arr:
    averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
deviations = []
#Solve dp problems incrementing p by one  

dp = 50 #deviation percentage, will generate multiple deviations up to and include this percentage 
f = open("worstCaseRealisations.csv","w")

p=0
while p <= dp:
    #deviations is in the form [cust][fac]
    #we want to transform into average accross customer 
    #Get the deviation by taking a percentage of the average for each customer 
    #dont use calculateDeviations.py as it returns sorted dictionary

    for count,x in enumerate(averages):
        deviations.append((count+1,(x/100)* p))
    devDict = {} # create dictionary of deviations for each customer 
    for d in deviations:   
        devDict.update({d[0]:d[1]})
    opt = SolverFactory('cplex')
    #make a dictionary for input when all values take on their worst case realization
    worstCaseDistances = {}
    worstCaseDistancesBox = {} 

    for key in dist.keys():
        worstCaseDistances.update({key: dist.get(key)+ devDict.get(key[1])})
    for key in dist.keys() :
        box_dist = math.sqrt(   math.pow( dist.get(key) + devDict.get(key[1]),2)   + math.pow(devDict.get(key[1]),2 ))
        worstCaseDistancesBox.update({key: box_dist})

    worstCaseModel = make_model(worstCaseDistances,o,N,M)
    worstCaseBoxModel = make_model(worstCaseDistancesBox,o,N,M)
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
