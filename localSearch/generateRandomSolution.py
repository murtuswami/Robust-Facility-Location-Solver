"""
Generates a random solution to to a given instance of a uncapacitated facility location problem 
First select and open a random number of facilities 
Then extract a solution array from the open set of facilities
"""
import random 

"""
Parameters
    f: Number of facilities in problem
    c: Number of customers in problem
    d: 2D Array of distances 
Returns 
    Array of length c with entries in range f. Corresponds to selected facility for customer
Description 
    Takes problem input instances and randomly generates a feasible solution 
"""
def generateRandomSolution(f,c,d):
    #Open a random number of facilities 
    number_open = random.randint(1,f) 
    open = []
    for _ in range(number_open):
        open_this = random.randrange(f)
        while open_this in open:        #If facility is already open, keep randomly selecting until it is not
         open_this = random.randrange(f)
        open.append(open_this)
    #calculate solution array under this open set of facilities 
    sol = []
    for x in range(c):
        best = None
        best_val= None
        #Calculate best open facility for customer x
        for y in open:
            val = d[y][x]
            if best == None or val < best_val:
                best = y
                best_val = val
        sol.append(best)
    return sol