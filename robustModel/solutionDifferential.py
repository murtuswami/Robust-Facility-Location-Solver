

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