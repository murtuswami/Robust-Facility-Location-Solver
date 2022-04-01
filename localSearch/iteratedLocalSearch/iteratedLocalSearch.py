"""
 Iterated Local Search using the Fast Local Search as a subroutine.
 Initial Values generated randomly at each iteration.
 Writes results to csv in the form (iteration,value obtained, best value obtained so far)
"""

import os
import importlib.util
### Relative imports from parent directory  ### 
path = os.getcwd()
parent = os.path.abspath(os.path.join(path, os.pardir)) 

    ### taken from https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path ###
spec = importlib.util.spec_from_file_location("LocalSearchFast", parent + "/localSearchFast.py")
spec2 = importlib.util.spec_from_file_location("generateRandomSolution", parent + "/generateRandomSolution.py")
spec3 = importlib.util.spec_from_file_location("getAndProcessData", parent + "/processData.py")
localSearchFast = importlib.util.module_from_spec(spec)
generateRandomSolution = importlib.util.module_from_spec(spec2)
processData = importlib.util.module_from_spec(spec3)
spec.loader.exec_module(localSearchFast)
spec2.loader.exec_module(generateRandomSolution)
spec3.loader.exec_module(processData)
    ### End of copied code ###

### Data Selection and processing ### 

facilitynumber,customernumber,distances,openingcosts = processData.getAndProcessData()
### Run Fast Local Search Procedure n times descending to Local Optimum and recording best obtained value at each procedure ### 
iter = 1
f = open("resultsILS.csv","w")
bestVal= None
n = 10 #adjust this to change the number of iterations of ILS
while(iter <= n):
    initSol = generateRandomSolution.generateRandomSolution(facilitynumber,customernumber,distances)
    thisVal = localSearchFast.LocalSearchFast(initSol,customernumber,openingcosts,distances).run()
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
f.write("\n")
f.write("best result is: ")
f.write(str(bestVal))
print("finished")


