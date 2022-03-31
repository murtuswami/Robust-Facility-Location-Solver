
"""
Class representing Slower local search implementation as described in report section 4.2
"""

import copy

class LocalSearchSlow:

    """
    Parameters
        init : Initial Solution, 1D array of facility numbers where index corresponds to a customer
        custs: Integer value reflecting number of customers 
        facilsOpenCost: Integer Array of opening costs, index corresponds to facility 
        distances: 2D array of where entries reflect distances between facilities and customers. Indexed in form [customer][facility]
    Returns 
        n/a
    Description 
        Captures parameters as global variables and initializes instance LocalSearchFast
    """
    def __init__(self, init,custs,facilsOpenCost,distances):
        self.cSol = init
        self.bSol = init
        self.custs = custs
        self.facilsOpenCost = facilsOpenCost 
        self.distances = distances 


    """
    Parameters
        n/a
    Returns 
        Best Solution obtained from Local Search Descent 
    Description 
        Runs until local optima is reached and returns the best value obtained. 
    """
    def run(self):
        while True:
            hn = self.best_neighbour(self.cSol)
            bSol_value = self.objectiveValue(self.bSol)
            hn_value = self.objectiveValue(hn)
            if bSol_value <= hn_value:
                return bSol_value
            cost = bSol_value - hn_value
            if cost >= 0:
                self.bSol = copy.copy(hn)
                self.cSol = copy.copy(hn)
        return self.bSol
        
    """
    Parameters
        cur : Current solution 
    Returns 
        The neighbour of current solution with best objective value 
    Description 
        Takes current solution, generates all neighbours to current solution and returns the neighbour with the best objective value 
    """
    def best_neighbour(self,cur):
        highest_neighbour = None 
        highest_neighbour_profit = None

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
                dist = self.distances[n][i]

                if n != x and (second_best == None or dist < second_best): # row X column, We iterate to find the second highest
                    second_best = dist
                    city_number = n
            second_closest_values.append(city_number)

        #swap opened with closed 
        for y in opened: # replace y 
            for x in closed: # with x 
                ret = copy.copy(cur)
                profit = 0 
                for i,n in enumerate(cur): # for each customer calculate the new value 
                    if n != y: #if the current city is not the one we are replacing         
                        if self.distances[x][i]< self.distances[n][i]: #if the replacement distance to this customer is less than its current we will replace it 
                            ret[i] = x
                            profit = profit + self.distances[n][i] - self.distances[x][i] # profit  is (current - new )  for this customer
                        
                    else:
                            if self.distances[x][i] < self.distances[second_closest_values[i]][i]: #if distance of customer to replacement is better than second closest value 
                                ret[i] = x # set replacement
                                profit = profit + self.distances[n][i]- self.distances[x][i] # add replacement to profit 
                            else:
                                ret[i] = second_closest_values[i]
                                profit = profit + self.distances[n][i] - self.distances[second_closest_values[i]][i] # accounts for negative profit from moving to second best value 
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
                    profit = profit + self.distances[x][i] - self.distances[second_closest_values[i]][i] #If customer was served by this
                    ret[i] = second_closest_values[i]                            #Minus from profit difference between best and second best 
                                                                                                   #Since we will switch to second best
            profit = profit + self.facilsOpenCost[x] # We gain profit of the cost of opening x since we are not opening it 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret 
                highest_neighbour_profit = profit 
                
       
        #Open one facility 
        for x in closed:
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): # for each customer calculate the new value 
                if self.distances[x][i] < self.distances[n][i]:             #so if the new city is closer for this customer set it 
                    profit = profit  + self.distances[n][i] - self.distances[x][i] #Minus from profit difference between best and second best       
                    ret[i] = x                                                      # since we will switch to second best
            profit = profit - self.facilsOpenCost[x] # We lose the profit of the cost of opening x since we are opening it 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret #swap y with x 
                highest_neighbour_profit = profit 
              
              
    
        #get the new solution with swap (x,y) by generating it with a variant on the above method and return it 
    
      
        return highest_neighbour
    
    """
    Parameters
        n: A 1D Solution array where the assumption that each assigned facility is the closest one holds 
    Returns 
        Objective Function Value 
    Description 
        Iterates through solution, summing distances of routes used and  opening costs to reach an objective solution value. 
    """
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

