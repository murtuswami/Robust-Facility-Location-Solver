"""
Creates deviations on an input distances to the Facility Location Problem

Parameters
    dp: percentage amount to deviate distances
    dist: 2D Array representation of distances where indices represent customers and facilities
    n: number of facilities 

Returns 
    A Sorted dictionary with values (customer,deviation) 
Description 
    Takes the average of the distances to all facilities for a given customer 
    Multiplies the average by the deviation percentage for the the given customer
    Inserts deviations into dictionary in sorted order so that d1 >= d2 .. >=dl holds 
"""

def calculateDeviations(dp,dist,n):
    averages = [] 
    for x in dist:
        averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
    deviations = []
    for count,x in enumerate(averages):
        deviations.append((count+1,round((x/100)* dp,2)))
    #sort array of deviations and then insert into dictionary in order
    sortByDeviation = sorted(deviations,key = lambda tup:tup[1],reverse=True)
    devDict = {} # create dictionary 
    for d in sortByDeviation:   
        devDict.update({d[0]:d[1]})
    return devDict

