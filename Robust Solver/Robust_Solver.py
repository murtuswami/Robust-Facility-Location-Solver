import tkinter
from tkinter import filedialog


""" Take as input 
    1.Data for a UFLP problem 
    2.Number of customers taking on worst case realization 
    3.Size of box uncertainty as represented by % of distance to facility as length/2 
"""

print("Please select file with input data")
inputdatapath = filedialog.askopenfilename()
datafile = open(inputdatapath)
arr =[]
for line in datafile:
    arr.append(line.rstrip().split())

n = input("Number of customers taking on worst case value ")
p = input("Percent of distance to facility to use as box uncertainty length/2")

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

print(openingcosts)
print(distances)
print(n)
print(p)
