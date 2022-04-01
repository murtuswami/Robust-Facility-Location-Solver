from robustSolver import robustSolver
from processRobustPyomoData import processRobustPyomoData
from calculateDeviations import calculateDeviations

"""
Loads UFLP Data
Calculates Deviations 
Computes robust solution for  wc values at their worst case realisation 

Output:
singleRobustSolution.txt single value with the robust solution 
"""

n,m,d,o,arr,N,M = processRobustPyomoData()
devDict = calculateDeviations(5,arr,n)
wc = round ( (m/100) * 75 )  # gamma, number of solutions at their worst case realization currently set to 75% 
robustSolution = robustSolver(wc,d,o,N,M,devDict)
print("-----")
print(robustSolution)   
f = open("singleRobustSolution.txt","w")
f.write("Robust Solution Objective Value:" + str(robustSolution[0]))