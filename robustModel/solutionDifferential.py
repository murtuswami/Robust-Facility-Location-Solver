"""
Calculates the solution differential between sets of solutions to the UFLP

Parameters
    s: Array of solutions to the UFLP, where solutions are arrays containing tuples of assignments in the form (facility:value {1,0})
Returns 
    Returns an Integer corresponding to the number of assignment changes between all solutions in the set 
Description 
   Takes set of solutions and iterates over them pairwise, counting the number of differences in assignment
"""

def solutionDifferential(s):
    s1= 0
    s2 =1 
    delta = 0
    while s2 < len(s):
        difference_count = 0
        for n,x in enumerate(s[s1]):
            if x[1] != s[s2][n][1]:
                difference_count = difference_count+ 1 # differences between pairwise arrays
        delta = delta + difference_count               # differences between all arrays summed 
        s1 = s1 +1
        s2 = s2 +1
    return delta 