# take a sum of the distance to all facilites average it then take percentage of that value as radius or deviation constant 
#percentage is same for all nodes but since the distnaces are all different the deviations change 

#deviations is in the form [cust][fac]
#we want to transform into average accross customer 

def calculateDeviations(dp,arrRepresentation,n):
    averages = [] 
    for x in arrRepresentation:
        averages.append(sum(x)/n) # sum of facility costs for a customer divided by number of facilities 
    deviations = []
    dp = 50
    for count,x in enumerate(averages):
        deviations.append((count+1,round((x/100)* dp,2)))
    #sort by deviations 
    sortByDeviation = sorted(deviations,key = lambda tup:tup[1],reverse=True)
    devDict = {} # create dictionary 
    for d in sortByDeviation:   
        devDict.update({d[0]:d[1]})
    return devDict