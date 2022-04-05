"""
Class representing Faster Local Search implementation as described in report section 4.3 
"""

import copy
class LocalSearchFast:


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
        return None
        


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
        opened = [] #open facilities in the current solution 
        closed = [] #closed facilities in the current solution
        second_closest_values = [] #Second closest facility to each customer

        #Enumerate open facilities in current solution 
        for x in cur:
            if x not in opened:
                opened.append(x)

         #Enumerate closed facilities in current solution
        for x in range(len(self.facilsOpenCost)):
            if not x in opened:
                closed.append(x)
        
        #Calculate second closest facility for each customer
        for i,x in enumerate(cur):
            second_best = None
            city_number = None
            for n in opened: 
                dist = self.distances[n][i]
                if n != x and (second_best == None or dist < second_best): # row X column, iterate to find the second highest
                    second_best = dist
                    city_number = n
            second_closest_values.append(city_number)

        

        #swap open facilities with closed facilities or S = S + s' - s''
        #record the best neighbour and its profit from each this procedure 
    
        best_swaps = []
        for x in closed: #loop through each facility and calculate the best swap to make 
            ret = copy.copy(cur) # make a copy of current solution 
            gain = 0
            loss = {} 
            for n in opened: #loss from opening x and closing n
               
                # if x costs more our loss will be positive, if we save by closing facility n then the loss will have a negative value so be a gain 
                # Therefore prefactor opening costs into loss map
                diff = self.facilsOpenCost[x] - self.facilsOpenCost[n] 
                loss.update({n:diff})
            for i,n in enumerate(cur):
                if self.distances[x][i]<= self.distances[n][i]: #if the replacement distance to this customer is less than its current replace it 
                        gain = gain + self.distances[n][i] - self.distances[x][i] # profit  is (current - new )  for this customer
                else:  #else ( it reduces it ), add to the netloss for replacing with this facility 
                    current_loss = loss.get(n)
                    new_loss =   min(self.distances[x][i],self.distances[second_closest_values[i]][i]) - self.distances[n][i] 
                    loss.update({n:current_loss + new_loss})

            best = min(loss, key=loss.get) # get the best facility to swap the current one with 
            profit = gain - loss.get(best) 
            best_swaps.append((x,best,profit)) #append the best swap for this facility and the profit 

        #from array containing the best facility to swap each facility with, get the one with the highest profit
        best_swaps.sort(key=lambda tup: tup[2],reverse= True)  
        highest_neighbour_profit = best_swaps[0][2] # record profit from this neighbour swap 
        swap = best_swaps[0][1]
        swapwith = best_swaps[0][0]

      # need to swap facility 'swap' with facility 'swapwith' 
      # perform swap and record solution 
        cop = copy.copy(cur) #copy current solution 
        for i,n in enumerate(cur):
            if n != swap: #if the current city is not the one we are replacing         
                if self.distances[swapwith][i]< self.distances[n][i]: #if the replacement distance to this customer is less than its current we will replace it 
                    cop[i] = swapwith
                #else do nothing to it
            else:
                if self.distances[swapwith][i] < self.distances[second_closest_values[i]][i]: #if distance of customer to replacement is better than second closest value 
                        cop[i] = swapwith # set replacement
                else:
                    cop[i] = second_closest_values[i]

        highest_neighbour = cop

        #remove one facility or S = s - s' 
        #remove each facility 
        for x in opened:
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): # for each customer calculate the new value 
                if n == x:             #if the current city is not the one we are closing , then there is no change
                    profit = profit + self.distances[x][i] - self.distances[second_closest_values[i]][i] #If customer was served by this
                    ret[i] = second_closest_values[i]                            #Minus from profit difference between best and second best 
                                                                                                  
            profit = profit + self.facilsOpenCost[x] # We gain profit of the cost of opening x since we are not opening it 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit: # if produces a better neighbour that previous steps record 
                highest_neighbour = ret 
                highest_neighbour_profit = profit 
    


        #Add one facility or S = s +s' 
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


