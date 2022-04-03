"""
Calculates the average descent time to local optimum over n descents for a chosen data set and writes value to a csv file.
"""

import time 
from localSearchFast import LocalSearchFast
from generateRandomSolution import generateRandomSolution
from processData import getAndProcessData


### Data Selection and processing ### 

facilitynumber,customernumber,distances,openingcosts = getAndProcessData()

### Run Fast Local Search to descent 50 times, recording total time taken for each descent ###
times = []
n = 50 # Adjust this to change the number of local optimum descents
i=1
while(i <= n):
    try:
        initsol = generateRandomSolution(facilitynumber,customernumber,distances)
        startTime = time.process_time()
        fast = LocalSearchFast(initsol,customernumber,openingcosts,distances)
        fast.run()
        endTime = time.process_time()
        times.append(endTime-startTime)
        print("-------")
        i = i+1
    except:
        pass
print(times)

### Get Average times and write to file ###
print(sum(times)/len(times))
f = open("resultsAvgDescent.csv" , "w")
f.write(str(sum(times)/len(times)))
