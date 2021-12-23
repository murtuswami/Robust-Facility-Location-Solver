from localSearchSlow import LocalSearchSlow
from localSearchFast import LocalSearchFast
import tkinter
from tkinter import filedialog
import random
import time 

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

#generate number_open facilties to open
for _ in range(number_open):
    open_this = random.randrange(facilitynumber)
    while open_this in opened:
       open_this = random.randrange(facilitynumber)
    opened.append(open_this)
print(opened)
#calculate solution 
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


slow = LocalSearchSlow(initsol,customernumber,openingcosts,distances)
ss =time.process_time()
f = open("slowtimes.txt","a")
f.write(str(ss))
f.write(" ")
valueslow = slow.run()
print("obtained local optimum of:", valueslow)

print("\n\n\n")

print("starting fast search" )
fs = time.process_time()
f = open("fasttimes.txt","a")
f.write(str(fs))
f.write(" ")
fast = LocalSearchFast(initsol,customernumber,openingcosts,distances)
valuefast = fast.run()

print("obtained local optimum of:", valuefast)
print("\n\n\n")
