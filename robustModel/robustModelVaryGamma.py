from robustSolver import robustSolver
from processRobustPyomoData import processRobustPyomoData
from calculateDeviations import calculateDeviations
from solutionDifferential import solutionDifferential

n,m,d,o,arr,N,M = processRobustPyomoData()
devDict = calculateDeviations(5,arr,n) # dev dict is constant when varying gamma 
solAssignments = [] 
f = open("varyGamma.csv","w")

for wc in range(4):
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

    
