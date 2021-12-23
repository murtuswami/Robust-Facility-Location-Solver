
import tkinter
from tkinter import filedialog
import random
import copy
from queue import Queue
class TabuSearch:
    def __init__(self, init,custs,facilsOpenCost,distances,tt,limit):
        self.cSol = init
        self.bSol = init
        self.custs = custs # integer
        self.facilsOpenCost = facilsOpenCost # integer array of opening costs
        self.distances = distances # custs x facils indexed such that cust x = index [x-1] & same for facils 
        self.iter = 0
        self.tabu = Queue(maxsize = tt)
        self.iterlimit = limit

        
    def terminate(self):
        if self.iter == self.iterlimit:
            return True
        return False
    
    def run(self):
       
        while not self.terminate():
            print(self.objectiveValue(self.bSol))
            hn = self.best_neighbour(self.cSol)
            hn_op = hn[1]
            hn = hn[0]
            cost = self.objectiveValue(self.bSol) - self.objectiveValue(hn)
            if cost >= 0:
                self.bSol = copy.copy(hn)
            self.cSol = copy.copy(hn)
            if self.tabu.full():
                self.tabu.get()
            self.tabu.put(hn_op)
            self.iter = self.iter +1 
           
        return self.bSol
        
    
    def best_neighbour(self,cur):
        highest_neighbour = None 
        highest_neighbour_profit = None
        neighbour_operation = None
        opened = [] #our open faciltiies 
        closed = [] #our not-open facilities set difference open with facilities 
        second_closest_values = []

        for x in cur:
            if x not in opened:
                opened.append(x)
        
        for x in range(len(self.facilsOpenCost)):
            if not x in opened:
                closed.append(x)
        #generate the second closest values for each 
        for i,x in enumerate(cur):
         
            second_best = None
            city_number = None
            for n in opened: 
                dist = distances[n][i]

                if n != x and (second_best == None or dist < second_best): # row X column, We iterate to find the second highest
                    second_best = dist
                    city_number = n
            second_closest_values.append(city_number)

        
        #0 = swap
        #1 = add
        #2 = remove

        #swap opened with closed 
        for y in opened: # replace y 
            for x in closed: # with x 
                if (y,x) in self.tabu.queue:
                    continue
                ret = copy.copy(cur)
                profit = 0 
                for i,n in enumerate(cur): # for each customer calculate the new value 
                    if n != y: #if the current city is not the one we are replacing         
                        if distances[x][i]< distances[n][i]: #if the replacement distance to this customer is less than its current we will replace it 
                            ret[i] = x
                            profit = profit + distances[y][i] - distances[x][i] # profit  is (current - new )  for this customer
                        
                    else:
                            if distances[x][i] < distances[second_closest_values[i]][i]: #if distance of customer to replacement is better than second closest value 
                                ret[i] = x # set replacement
                                profit = profit + distances[n][i]- distances[x][i] # add replacement to profit 
                            else:
                                ret[i] = second_closest_values[i]
                                profit = profit + distances[n][i] - distances[second_closest_values[i]][i] # accounts for negative profit from moving to second best value 
                profit = profit + self.facilsOpenCost[y] - self.facilsOpenCost[x] #We gain in profit the opening cost of y since we are not going to open it  
                                                                                  #We lose x since we are opeining it 
                if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                    highest_neighbour = ret
                    highest_neighbour_profit = profit 
                    neighbour_operation = (y,x) #swap y with x
                    
       
        #remove one facility 

        for x in opened:
            if -x in self.tabu.queue:
                    continue
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): # for each customer calculate the new value 
                if n == x:             #if the current city is not the one we are closing , then there is no change
                    profit = profit + distances[x][i] - distances[second_closest_values[i]][i] #If customer was served by this
                    ret[i] = second_closest_values[i]                            #Minus from profit difference between best and second best 
                                                                                                   #Since we will switch to second best
            profit = profit + self.facilsOpenCost[x] # We gain profit of the cost of opening x since we are not opening it 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret 
                highest_neighbour_profit = profit 
                neighbour_operation = -x 
        
        #Open a new facility 
        for x in closed:
            if x in self.tabu.queue:
                    continue
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): # for each customer calculate the new value 
                if distances[x][i] < distances[n][i]:             #so if the new city is closer for this customer set it 
                    profit = profit  + distances[n][i] - distances[x][i] #Minus from profit difference between best and second best       
                    ret[i] = x                                                      # since we will switch to second best
            profit = profit - self.facilsOpenCost[x] # We lose the profit of the cost of opening x since we are opening it 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret #swap y with x 
                highest_neighbour_profit = profit 
                neighbour_operation = x
              
       

        #get the new solution with swap (x,y) by generating it with a variant on the above method and return it 
        return (highest_neighbour,neighbour_operation)

    def objectiveValue(self,n):
        val = 0 
        opening = []
        for i,x in enumerate(n): #index is customers , x is the city its connected to
            val = val + self.distances[x][i] 
            if x not in opening:
                opening.append(x)
        for x in opening:
            val  = val + self.facilsOpenCost[x]
        
        return val

class LocalSearch:
    def __init__(self, init,custs,facilsOpenCost,distances):
        self.cSol = init
        self.bSol = init
        self.custs = custs # integer
        self.facilsOpenCost = facilsOpenCost # integer array of opening costs
        self.distances = distances # custs x facils indexed such that cust x = index [x-1] & same for facils 
        
    def terminate(self):

        return False
    
    def run(self):
       
        while not self.terminate():
            print(self.objectiveValue(self.cSol))
            hn = self.best_neighbour(self.cSol)
            cost = self.objectiveValue(self.bSol) - self.objectiveValue(hn)
            if cost >= 0:
                self.bSol = copy.copy(hn)
                self.cSol = copy.copy(hn)
        return self.bSol
        
    
    def best_neighbour(self,cur):
        highest_neighbour = None 
        highest_neighbour_profit = None
        highest_neighbour_type = None
        opened = [] #our open faciltiies 
        closed = [] #our not-open facilities set difference open with facilities 
        second_closest_values = []

        for x in cur:
            if x not in opened:
                opened.append(x)
        
        for x in range(len(self.facilsOpenCost)):
            if not x in opened:
                closed.append(x)
        #generate the second closest values for each 
        for i,x in enumerate(cur):
         
            second_best = None
            city_number = None
            for n in opened: 
                dist = distances[n][i]

                if n != x and (second_best == None or dist < second_best): # row X column, We iterate to find the second highest
                    second_best = dist
                    city_number = n
            second_closest_values.append(city_number)

        
        #0 = swap
        #1 = add
        #2 = remove

        #swap opened with closed 
        for y in opened: # replace y 
            for x in closed: # with x 
                ret = copy.copy(cur)
                profit = 0 
                for i,n in enumerate(cur): # for each customer calculate the new value 
                    if n != y: #if the current city is not the one we are replacing         
                        if distances[x][i]< distances[n][i]: #if the replacement distance to this customer is less than its current we will replace it 
                            ret[i] = x
                            profit = profit + distances[y][i] - distances[x][i] # profit  is (current - new )  for this customer
                        
                    else:
                            if distances[x][i] < distances[second_closest_values[i]][i]: #if distance of customer to replacement is better than second closest value 
                                ret[i] = x # set replacement
                                profit = profit + distances[n][i]- distances[x][i] # add replacement to profit 
                            else:
                                ret[i] = second_closest_values[i]
                                profit = profit + distances[n][i] - distances[second_closest_values[i]][i] # accounts for negative profit from moving to second best value 
                profit = profit + self.facilsOpenCost[y] - self.facilsOpenCost[x] #We gain in profit the opening cost of y since we are not going to open it  
                                                                                  #We lose x since we are opeining it 
                if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                    highest_neighbour = ret
                    highest_neighbour_profit = profit 
       
        #remove one facility 

        for x in opened:
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): # for each customer calculate the new value 
                if n == x:             #if the current city is not the one we are closing , then there is no change
                    profit = profit + distances[x][i] - distances[second_closest_values[i]][i] #If customer was served by this
                    ret[i] = second_closest_values[i]                            #Minus from profit difference between best and second best 
                                                                                                   #Since we will switch to second best
            profit = profit + self.facilsOpenCost[x] # We gain profit of the cost of opening x since we are not opening it 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret 
                highest_neighbour_profit = profit 
           
        for x in closed:
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): # for each customer calculate the new value 
                if distances[x][i] < distances[n][i]:             #so if the new city is closer for this customer set it 
                    profit = profit  + distances[n][i] - distances[x][i] #Minus from profit difference between best and second best       
                    ret[i] = x                                                      # since we will switch to second best
            profit = profit - self.facilsOpenCost[x] # We lose the profit of the cost of opening x since we are opening it 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret #swap y with x 
                highest_neighbour_profit = profit 
              
       

        #get the new solution with swap (x,y) by generating it with a variant on the above method and return it 
        return highest_neighbour

    def objectiveValue(self,n):
        val = 0 
        opening = []
        for i,x in enumerate(n): #index is customers , x is the city its connected to
            val = val + self.distances[x][i] 
            if x not in opening:
                opening.append(x)
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

instance = TabuSearch(initsol,customernumber,openingcosts,distances,100,500)
instance.run()



