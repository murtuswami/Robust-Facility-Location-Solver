"""
Runs the Slow Local Search and Fast Local Search on the same data set with the same initial value. 
Writes the times between each neighbourhood generation step to two different csv files 
Both Procedures always descend in the same way to the same local optimum value. 
"""


from localSearchSlow import LocalSearchSlow
from localSearchFast import LocalSearchFast
import tkinter
from tkinter import filedialog
import random
import time 


### Open File and Process Data ###
tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
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

number_open = random.randint(1,facilitynumber) 
opened = []
print(number_open)

### Randomly generate an initial solution by opening a random number of facilities  ### 
for _ in range(number_open):
    open_this = random.randrange(facilitynumber)
    while open_this in opened:
       open_this = random.randrange(facilitynumber)
    opened.append(open_this)
print(opened)
#calculate solution array under this open set of facilities 
initsol = []
for x in range(customernumber):
    best = None
    best_val= None
    for y in opened:
        val = distances[y][x]
        if best == None or val < best_val:
            best = y
            best_val = val
    initsol.append(best)
print("starting slow search")


### Descend to local optimum from initial solution using slow method with modified time capturing ###
slow = LocalSearchSlow(initsol,customernumber,openingcosts,distances)
f = open("resultsSlow.csv","w")

f.write(str(time.process_time()))
f.write("\n")
valueslow = slow.run()
print("obtained local optimum of:", valueslow)

print("\n\n\n")
### Descend to local optimum from initial solution using Fast method with modified time capturing ###
print("starting fast search" )
fs = time.process_time()
f = open("resultsFast.csv","w")
f.write(str(time.process_time()))
f.write("\n")
fast = LocalSearchFast(initsol,customernumber,openingcosts,distances)
valuefast = fast.run()
print("obtained local optimum of:", valuefast)
print("\n\n\n")
