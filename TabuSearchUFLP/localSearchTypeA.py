# lets first try and just iterate through solutions picking the next lowest solution 

import tkinter
from tkinter import filedialog
import random
import copy

class LocalSearchTypeA:
    def __init__(self, init,custs,facilsOpenCost,distances):
        self.cSol = init
        self.bSol = init
        self.custs = custs # integer
        self.facilsOpenCost = facilsOpenCost # integer array of opening costs
        self.distances = distances # custs x facils indexed such that cust x = index [x-1] & same for facils 
        
    def terminate(self):
        # can add more termination criteria
        return False
    
    def run(self):
        print(self.objectiveValue(self.cSol))
        while not self.terminate():
            # get all of the neighbors
            neighbours = self.neighbours(self.cSol)
            # pick the best neighbor solution
            neighbours.sort(key=lambda n: self.objectiveValue(n))
          #  print("\n")
          #  print(self.objectiveValue(neighbours[0]), self.objectiveValue(neighbours[1]))
            # get the cost between the two solutions
            cost = self.objectiveValue(self.bSol) - self.objectiveValue(neighbours[0])
            if cost >= 0:
                self.bSol = copy.copy(neighbours[0])
            self.cSol = copy.copy(neighbours[0])

            print(self.objectiveValue(self.bSol))
        # return best solution found
        return self.bSol
        
    
    def neighbours(self,cur):
        #Generate neighbours from current solution 
        #Define a neighbour as pick one customer. For the customer if it has a connector a facility with a lower value set that to its one 
        #return a list of solutions 
        #we can define a neighbour as for each facility swap with a closed one 
        #remove one facility from open 
        #add one facility from closed

        opened = [] #our open faciltiies 
        closed = [] #our not-open facilities set difference open with facilities 

        for x in cur:
            if x not in opened:
                opened.append(x)
        
        for x in range(len(self.facilsOpenCost)):
            if not x in opened:
                closed.append(x)
        
        neighbours = [] 
     

        for i,x in enumerate(cur):
            neigh = copy.copy(cur)
            neigh[i] = random.choice(closed)
            neighbours.append(neigh)
        for i,x in enumerate(cur):
            neigh = copy.copy(cur)
            neigh[i] = random.randrange(0,len(self.facilsOpenCost))
            neighbours.append(neigh)

        return neighbours 

    def objectiveValue(self,n):
        #given a candidate solution n, generate its objective function value 
        val = 0 
        opening = set()
        for i,x in enumerate(n): #index is customers , x is the city its connected to
            val = val + self.distances[x][i] 
            opening.add(x)
        for x in opening:
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

instance = LocalSearchTypeA(initsol,customernumber,openingcosts,distances)
instance.run()



