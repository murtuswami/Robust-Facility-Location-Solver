from robustSolver import robustSolver
from processRobustPyomoData import processRobustPyomoData
from calculateDeviations import calculateDeviations
from solutionDifferential import solutionDifferential
"""
Loads UFLP Data
Calculates Deviations 
Computes robust solutions for 0 - m values at their worst case realisations, writes value to csv file
Computes Solution Differential on solutions and writes value to text file 

Output:
varyGamma.csv containing robust solution at each wc value 
solutionDifferential.txt single value containing solution difference value 

"""

n,m,d,o,arr,N,M = processRobustPyomoData()
devDict = calculateDeviations(5,arr,n) # deviate by 5 %
solAssignments = [] 
f = open("varyGamma.csv","w")
for wc in range(m+1):
    print("solving for " + str(wc) + " customers at worst case realization")
    sol = robustSolver(wc,d,o,N,M,devDict)
    f.write(str(wc))
    f.write(",")
    f.write(str(sol[0]))
    f.write("\n")
    solAssignments.append(sol[1])
f = open("solutionDifferntial.txt","w")
sd = solutionDifferential(solAssignments)
f.write(str(sd))
print("solution differential is " + str(solutionDifferential(solAssignments)))

    
