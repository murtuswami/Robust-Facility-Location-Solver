"""
Runs the Slow Local Search and Fast Local Search on the same data set with the same initial value. 
Writes the times between each neighbourhood generation step to two different csv files 
Both Procedures always descend in the same way to the same local optimum value. 
Uses a modified Local Search Class in order to capture the time between each neighbourhood generation step

Outputs four files

resultsFast.csv and resultsSlow.csv contain the the time in seconds 
required to run the local Search descents for fast and slow respectively.

slowTimes and fastTimes output the time at which best neighbour was generated and its value along the Local Search descent
for the fast and slow local search descents respectively 

Use this file to capture data on times between local search descents 
and the values produced at each step of a the local search
"""


from localSearchSlowMod import LocalSearchSlowMod
from localSearchFastMod import LocalSearchFastMod
import time 
import os
import importlib.util

### Relative imports from parent directory  ### 
path = os.getcwd()
parent = os.path.abspath(os.path.join(path, os.pardir)) 
    ### taken from https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path ###

spec2 = importlib.util.spec_from_file_location("generateRandomSolution", parent + "/generateRandomSolution.py")
spec3 = importlib.util.spec_from_file_location("getAndProcessData", parent + "/processData.py")

generateRandomSolution = importlib.util.module_from_spec(spec2)
processData = importlib.util.module_from_spec(spec3)

spec2.loader.exec_module(generateRandomSolution)
spec3.loader.exec_module(processData)
    ### End of copied code ###


### Data Selection and processing ### 

facilitynumber,customernumber,distances,openingcosts = processData.getAndProcessData()
initsol =generateRandomSolution.generateRandomSolution(facilitynumber,customernumber,distances)



### Descend to local optimum from initial solution using slow method with modified time capturing ###
print("starting slow search")
slow = LocalSearchSlowMod(initsol,customernumber,openingcosts,distances)
f = open("resultsSlow.csv","w")
fs = time.process_time()
valueslow = slow.run()
print("obtained local optimum of:", valueslow)
f.write(str(time.process_time() - fs)) #write time for running in seconds to file 
print("\n\n\n")

### Descend to local optimum from initial solution using Fast method with modified time capturing ###
print("starting fast search" )
f = open("resultsFast.csv","w")
fs = time.process_time()
fast = LocalSearchFastMod(initsol,customernumber,openingcosts,distances)
valuefast = fast.run()
f.write(str(time.process_time() - fs)) #write time for running in seconds to file 
print("obtained local optimum of:", valuefast)
print("\n\n\n")
