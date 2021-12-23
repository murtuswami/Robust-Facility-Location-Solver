from localSearchSlow import LocalSearchSlow
from localSearchFast import LocalSearchFast
import tkinter
from tkinter import filedialog
import random

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


#generate number_open facilties to open

def generate_random_solution():
    number_open = random.randint(1,facilitynumber) 
    opened = []
    for _ in range(number_open):
        open_this = random.randrange(facilitynumber)
        while open_this in opened:
         open_this = random.randrange(facilitynumber)
        opened.append(open_this)
    #calculate solution 
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

instance =  LocalSearchFast(generate_random_solution(),customernumber,openingcosts,distances)
bestVal = instance.run()
iter = 1
while(iter < 50):
    iter = iter +1
    print("Best Value is" ,bestVal)
    print(iter)
    thisVal = LocalSearchFast(generate_random_solution(),customernumber,openingcosts,distances).run()
    if thisVal < bestVal:
        bestVal = thisVal
f = open("iterated_local_search.txt","a")
f.write("\n")
f.write(datafile.name)
f.write(" ")
f.write(str(bestVal))

print("finished")


