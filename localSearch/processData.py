""" Creates a file dialog window for selecting data for a UFLP instances. 
    Processes data returns in format appropriate for solving with Local Search Method
"""


import tkinter                  # For data file select
from tkinter import filedialog  # For filedialog 
tkinter.Tk().withdraw() 
"""
Parameters
    n/a
Returns 
    facilitynumber: Number of facilities in problem
    customernumber : Number of customers in problem
    distances : 2D array Where entries reflect distances between cities and customers
    openingcosts: 1D array where entries reflect opening costs 
Description 
    Captures parameters as global variables and initializes instance LocalSearchFast
"""

def getAndProcessData() : 
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
    return facilitynumber,customernumber,distances,openingcosts
