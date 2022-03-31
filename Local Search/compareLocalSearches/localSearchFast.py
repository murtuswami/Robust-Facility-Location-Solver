"""
Fast Local Search procedure with modified file writing to collect information on time between neighbour generation
Modified sections highlighted below 
Detailed comments ommited, see  /localSearch/localSearchFast.py for detailed documentation 
"""


import copy
import time 
class LocalSearchFast:
    def __init__(self, init,custs,facilsOpenCost,distances):
        self.cSol = init
        self.bSol = init
        self.custs = custs 
        self.facilsOpenCost = facilsOpenCost 
        self.distances = distances

    def run(self):
        ### Modification from original file starts here ###
        f = open("fastTimes.csv","a")
        while True:
            f.write(str(time.process_time()))
            f.write(",")
            f.write(str(self.objectiveValue(self.bSol)))
            f.write("\n ")
            print(time.process_time(),self.objectiveValue(self.bSol))
        ### Modification from original file ends here ###
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
    
    def best_neighbour(self,cur):
        highest_neighbour = None 
        highest_neighbour_profit = None
        opened = [] 
        closed = [] 
        second_closest_values = []

        for x in cur:
            if x not in opened:
                opened.append(x)
        
        for x in range(len(self.facilsOpenCost)):
            if not x in opened:
                closed.append(x)


        for i,x in enumerate(cur):
            second_best = None
            city_number = None
            for n in opened: 
                dist = self.distances[n][i]
                if n != x and (second_best == None or dist < second_best):
                    city_number = n
            second_closest_values.append(city_number)

        best_swaps = []
        for x in closed:
            ret = copy.copy(cur)
            gain = 0
            loss = {}
            for n in opened:

                diff = self.facilsOpenCost[x] - self.facilsOpenCost[n] 
                loss.update({n:diff})
            for i,n in enumerate(cur):
                if self.distances[x][i]<= self.distances[n][i]:
                        gain = gain + self.distances[n][i] - self.distances[x][i] 

                else:
                    current_loss = loss.get(n)
                    new_loss =   min(self.distances[x][i],self.distances[second_closest_values[i]][i]) - self.distances[n][i] 
                    loss.update({n:current_loss + new_loss})
         
            best = min(loss, key=loss.get)

            profit = gain - loss.get(best)
            best_swaps.append((x,best,profit))

        best_swaps.sort(key=lambda tup: tup[2],reverse= True) 

        highest_neighbour_profit = best_swaps[0][2]
        swap = best_swaps[0][1]
        swapwith = best_swaps[0][0]
 
        cop = copy.copy(cur) 
        for i,n in enumerate(cur):
            if n != swap:  
                if self.distances[swapwith][i]< self.distances[n][i]:
                    cop[i] = swapwith

            else:
                if self.distances[swapwith][i] < self.distances[second_closest_values[i]][i]: 
                        cop[i] = swapwith 
                else:
                    cop[i] = second_closest_values[i]

        highest_neighbour = cop

        for x in opened:
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): 
                if n == x:             
                    profit = profit + self.distances[x][i] - self.distances[second_closest_values[i]][i] 
                    ret[i] = second_closest_values[i] 
            profit = profit + self.facilsOpenCost[x] 
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret 
                highest_neighbour_profit = profit 

        for x in closed:
            ret = copy.copy(cur)
            profit = 0 
            for i,n in enumerate(cur): 
                if self.distances[x][i] < self.distances[n][i]:        
                    profit = profit  + self.distances[n][i] - self.distances[x][i]
                    ret[i] = x  
            profit = profit - self.facilsOpenCost[x]
            if  highest_neighbour_profit == None or profit > highest_neighbour_profit:
                highest_neighbour = ret 
                highest_neighbour_profit = profit 

        return highest_neighbour

    def objectiveValue(self,n):
        val = 0 
        opening = []
        for i,x in enumerate(n): 
            val = val + self.distances[x][i] 
            if x not in opening:
                opening.append(x)
        for x in opening:
            val  = val + self.facilsOpenCost[x]
        return val



