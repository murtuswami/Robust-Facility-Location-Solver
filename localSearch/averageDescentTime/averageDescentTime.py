"""
Calculates the average descent time to local optimum over n descents for a chosen data set and writes value to a csv file.
"""

import time 
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

### Run Fast Local Search to descent 50 times, recording total time taken for each descent ###
times = []
n = 10 # Adjust this to change the number of local optimum descents
for _ in range(n):
    initsol = generateRandomSolution.generateRandomSolution(facilitynumber,customernumber,distances)
    startTime = time.process_time()
    fast = localSearchFast.LocalSearchFast(initsol,customernumber,openingcosts,distances)
    fast.run()
    endTime = time.process_time()
    times.append(endTime-startTime)
    print("-------")
print(times)

### Get Average times and write to file ###
print(sum(times)/len(times))
f = open("resultsAvgDescent.csv" , "w")
f.write(str(sum(times)/len(times)))
