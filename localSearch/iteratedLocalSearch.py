"""
 Iterated Local Search using the Fast Local Search as a subroutine.
 Initial Values generated randomly at each iteration.
 Writes results to csv in the form (iteration,value obtained, best value obtained so far)
"""

import os
import importlib.util
### Relative imports from parent directory  ### 
from localSearchFast import LocalSearchFast
from generateRandomSolution import generateRandomSolution
from processData import getAndProcessData

    ### End of copied code ###
### Data Selection and processing ### 

facilitynumber,customernumber,distances,openingcosts = getAndProcessData()
### Run Fast Local Search Procedure n times descending to Local Optimum and recording best obtained value at each procedure ### 
iter = 1
f = open("resultsILS.csv","w")
bestVal= None
n = 50 #adjust this to change the number of iterations of ILS
while(iter <= n):
    initSol = generateRandomSolution(facilitynumber,customernumber,distances)
    try:
        thisVal = LocalSearchFast(initSol,customernumber,openingcosts,distances).run()
        f.write("\n")
        f.write(str(iter))
        f.write(",")
        f.write(str(thisVal))
        f.write(",")
        f.write(str(bestVal))
        if bestVal == None:
            bestVal = thisVal
        elif thisVal < bestVal:
            bestVal = thisVal
        print("best value is ", bestVal," at iteration " , iter)
        iter = iter +1
    except:
        pass
f.write("\n")
f.write("best result is: ")
f.write(str(bestVal))
print("finished")


