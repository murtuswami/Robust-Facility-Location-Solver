"""
Calculates the worst case realisations for a UFLP problem set under box and interval uncertainty 
Varies the realisations by increasing the deviation percentage from 0% to 50%

Output:
worstCaseRealizations.csv contains entries in the form (Deviation Percentage, Solution Objective Value,Type of uncertainty {box,interval})
"""

import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.environ import *
from  processRobustPyomoData import processRobustPyomoData
import math
from model import make_model

n,m,dist,o,arr,N,M = processRobustPyomoData()

# get averages of distances to all facilities for each customer 
averages = [] 
for x in arr:
    averages.append(sum(x)/n) 
deviations = []


dp = 50 #deviation percentage, will generate multiple deviations up to and include this percentage 
#f = open("worstCaseRealisations.csv","w")

p=0
while p <= dp:
    #deviations is in the form [cust][fac]
    #we want to transform into average accross customer 
    #Get the deviation by taking a percentage of the average for each customer 
    #dont use calculateDeviations.py as it returns sorted dictionary

    #Calculate deviations for customers under current p
    for count,x in enumerate(averages):
        deviations.append((count+1,(x/100)* p)) #1D array index is customer entry deviation 
    devDict = {} # Dictionary of deviations for each customer 
    for d in deviations:   
        devDict.update({d[0]:d[1]})
    opt = SolverFactory('cplex')

    #make a dictionary for input when all values take on their worst case realization
    worstCaseDistances = {}
    worstCaseDistancesBox = {} 

    #Interval uncertainty deviation added to distance
    for key in dist.keys():
        worstCaseDistances.update({key: dist.get(key)+ devDict.get(key[1])})
    #Box uncertainty deviation is taken as  half length of box , pythogras used to calculate worst case realisation
    for key in dist.keys() :
        box_dist = math.sqrt(   math.pow( dist.get(key) + devDict.get(key[1]),2)   + math.pow(devDict.get(key[1]),2 ))
        worstCaseDistancesBox.update({key: box_dist})

    #Solve model for box and interval 
    worstCaseModel = make_model(worstCaseDistances,o,N,M)
    worstCaseBoxModel = make_model(worstCaseDistancesBox,o,N,M)

    opt.solve(worstCaseModel)
    opt.solve(worstCaseBoxModel)
    
    print("Worst Case Realization", pyo.value(worstCaseModel.obj),"Box Worst Case:" ,pyo.value(worstCaseBoxModel.obj))

    f = open("interval.csv","a")
    f.write(str(p))
    f.write(",")
    f.write(str(pyo.value(worstCaseModel.obj)))
    f.write(",")
    f.write("\n")
    f = open("box.csv","a")
    f.write(str(p))
    f.write(",")
    f.write(str(pyo.value(worstCaseBoxModel.obj)))
    f.write(",")
    f.write("\n")
    p = p + 1