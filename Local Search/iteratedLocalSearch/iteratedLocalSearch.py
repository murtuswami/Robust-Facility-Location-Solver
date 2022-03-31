"""Iterated Local Search using the Fast Local Search as a subroutine. Initial Values generated randomly at each iteration. Writes results to csv in the form (iteration,value obtained, best value obtained so far)"""
from localSearchFast import LocalSearchFast
import tkinter
from tkinter import filedialog
import random


### Open File and process data ###
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


#### Generates Random Initial Solution for use at each local optimum descent ###
def generate_random_solution():
    #Open a random number of facilities 
    number_open = random.randint(1,facilitynumber) 
    opened = []
    for _ in range(number_open):
        open_this = random.randrange(facilitynumber)
        while open_this in opened:
         open_this = random.randrange(facilitynumber)
        opened.append(open_this)
    #calculate solution array under this open set of facilities 
    sol = []
    for x in range(customernumber):
        best = None
        best_val= None
        for y in opened:
            val = distances[y][x]
            if best == None or val < best_val:
                best = y
                best_val = val
        sol.append(best)
    return sol

### Run Fast Local Search Procedure 50 times descending to Local Optimum and recording best obtained value at each procedure ### 
iter = 1
f = open("resultsILS.csv","w")
while(iter <= 50):
    print("Best Value is" ,bestVal, "Iteration: ", iter)
    thisVal = LocalSearchFast(generate_random_solution(),customernumber,openingcosts,distances).run()
    f.write("\n")
    f.write(str(iter))
    f.write(",")
    f.write(str(thisVal))
    f.write(",")
    f.write(str(bestVal))
    if thisVal < bestVal:
        bestVal = thisVal
    iter = iter +1
f.write("\n")
f.write("best result is: ")
f.write(str(bestVal))

print("finished")


