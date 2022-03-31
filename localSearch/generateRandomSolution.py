"""
Generates a random solution to to a given instance of a uncapacitated facility location problem 
First select and open a random number of facilities 
Then extract a solution array from the open set of facilities
"""
import random 
import tkinter                  # For data file select
from tkinter import filedialog  # For filedialog 

def generateRandomSolution(f,c,d):
    #Open a random number of facilities 
    number_open = random.randint(1,f) 
    open = []
    for _ in range(number_open):
        open_this = random.randrange(f)
        while open_this in open:
         open_this = random.randrange(f)
        open.append(open_this)
    #calculate solution array under this open set of facilities 
    sol = []
    for x in range(c):
        best = None
        best_val= None
        for y in open:
            val = d[y][x]
            if best == None or val < best_val:
                best = y
                best_val = val
        sol.append(best)
    return sol