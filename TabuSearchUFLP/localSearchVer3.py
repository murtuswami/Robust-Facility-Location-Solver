import tkinter
from tkinter import filedialog
import random
import copy


class LocalSearchVer3:
    def __init__(self, init,custs,facilsOpenCost,distances):
        self.cSol = init # set of open facilities 
        self.bSol = init
        self.custs = custs # integer
        self.facilsOpenCost = facilsOpenCost # integer array of opening costs
        self.distances = distances # custs x facils indexed such that cust x = index [x-1] & same for facils 
        
    def terminate(self):
        return False
    
    def run(self):
       # print(self.objectiveValue(self.cSol))
        #return
        while not self.terminate():
            neighbours = self.neighbours(self.cSol)                # get all of the neighbors
            print("Generated Neighbours")
            neighbours.sort(key=lambda n: self.objectiveValue(n))  # pick the best neighbor solution
            print("Sorted Neighbours")
            cost = self.objectiveValue(self.bSol) - self.objectiveValue(neighbours[0]) # get the cost between the two solutions
            if cost >= 0:
                self.bSol = copy.copy(neighbours[0])
            self.cSol = copy.copy(neighbours[0])
            print(self.objectiveValue(self.bSol))
        return self.bSol
        
    
    def neighbours(self,cur):
        opened = [] #our open faciltiies 
        closed = [] #our not-open facilities set difference open with facilities 

        neighbour_open_facilities = [] 
        
        for x in cur:
            if x not in opened:
                opened.append(x)
        for x in range(len(self.facilsOpenCost)):
            if not x in opened:
                closed.append(x)
        for x in closed:
            nopen = copy.copy(opened)
            nopen.append(x)
            neighbour_open_facilities.append(nopen)
        for x in opened:
            nopen = copy.copy(opened)
            nopen.remove(x)
            neighbour_open_facilities.append(nopen)
        for i,x in enumerate(opened):
            for y in closed:
                nopen = copy.copy(opened)
                nopen[i] = y 
                neighbour_open_facilities.append(nopen)
        return neighbour_open_facilities

    def objectiveValue(self,s):
     
        val = 0 
        for m in range(self.custs):
            lowest = None
            for n in s:
                dist = distances[n][m]
                if lowest == None or dist < lowest: # row X column 
                    lowest = dist
            val = val + lowest
        for x in s:
            val  = val + self.facilsOpenCost[x]
        
        return val



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



"""
print("Please select file with starting solution")
startingsolpath = filedialog.askopenfilename()
solfile = open(startingsolpath)
solarr = []
for line in solfile:
    solarr.append(line.rstrip().split())
initsol = []
for x in solarr:
    for y in x:
        initsol.append(int(y))

"""
        
initsol = []
for x in range(customernumber):
    initsol.append(random.randrange(0,facilitynumber))
initopen = []
for x in initsol:
    if x not in initopen:
        initopen.append(x)
print("starting with" , initopen)


instance = LocalSearchVer3(initopen,customernumber,openingcosts,distances)
instance.run()




