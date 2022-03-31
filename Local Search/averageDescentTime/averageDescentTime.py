"""
Calculates the average descent time to local optimum over 50 descents for a chosen data set and writes value to a csv file.
"""


#from localSearchFast import LocalSearchFast
import tkinter
from tkinter import filedialog
import random
import time 
from .. import localSearchFast

### Data Selection and processing ### 
tkinter.Tk().withdraw() 
print("Please select file with input data")
inputdatapath = filedialog.askopenfilename()
datafile = open(inputdatapath)
arr =[]
for line in datafile:
    arr.append(line.rstrip().split())

initVals = arr[1]
del arr[:2]
customernumber = int(initVals[1])
facilitynumber = int(initVals[0]) 
openingcosts = []
distances = []  #Each subarray represents city i and its cost of connecting to j denoted by internal index 

for x in arr:
    oc = x[1]
    openingcosts.append(int(oc)) # index i correspondes to facility i +1 
    del x[:2]
    cityarr = []
    for y in x:
        #each y entry is the cost of connecting the city represented by x to customer represented by index in y 
        cityarr.append(int(y))
    distances.append(cityarr)


#### Generates Random Initial Solution for use at each local optimum descent ###
def generate_random_solution():
    #Open a random number of facilities 
    number_open = random.randint(1,facilitynumber) 
    open = []
    for _ in range(number_open):
        open_this = random.randrange(facilitynumber)
        while open_this in open:
         open_this = random.randrange(facilitynumber)
        open.append(open_this)
    #calculate solution array under this open set of facilities 
    sol = []
    for x in range(customernumber):
        best = None
        best_val= None
        for y in open:
            val = distances[y][x]
            if best == None or val < best_val:
                best = y
                best_val = val
        sol.append(best)
    return sol

### Run Fast Local Search to descent 50 times, recording total time taken for each descent ###
times = []
for _ in range(50):
    initsol = generate_random_solution()
    startTime = time.process_time()
    fast = LocalSearchFast(initsol,customernumber,openingcosts,distances)
    fast.run()
    endTime = time.process_time()
    times.append(endTime-startTime)
    print("-------")
print(times)

### Average times and write to file ###
print(sum(times)/len(times))
f = open("resultsAvgDescent.csv" , "w")
f.write(sum(times)/len(times))
