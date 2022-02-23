#The purpose of this file is to convert data to .dat format for the Uncapacitated Facility Location Problem
#For the model file see AbstractWarehouse.py 
#The data to be processed is in the simple FILE type from http://resources.mpi-inf.mpg.de/departments/d1/projects/benchmarks/UflLib/data-format.html
import os
import tkinter
from tkinter import filedialog
def convert():
    print("converting data ... ")
    arr = []
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    print("Please select file with input data")
    inputdatapath = filedialog.askopenfilename()
    print(inputdatapath)
    filename = os.path.basename(inputdatapath)
    file = open(inputdatapath)
    for line in file:
        arr.append(line.rstrip().split())

    initVals = arr[1]
    del arr[:2]
    m = int(initVals[1])
    n = int(initVals[0])
    setM = [*range(1,m+1)]
    setN = [*range(1,n+1)]
    paramo =[]
    paramd=[]

    for x in arr:
        fac = x[0]
        cost = x[1]
        paramo.append((fac,cost))
        del x[:2]
        
        for index, c in enumerate(x):
            paramd.append( (fac,index+1,c ) )

    try:
        f = open(filename+".dat", "x")
        s = "set N := "
        for x in setN:
            s += str(x)
            s += " "
        s += ";"
        f.write(s + "\n")

        s = "set M := "
        for x in setM:
            s += str(x)
            s += " "
        s += ";"

        f.write(s + "\n")

        s= "param d :=" 
        for x in paramd:
            s += "\n" +  str(x[0]) + " " + str(x[1]) + " " + str(x[2]) 
        s += ";"

        f.write(s + "\n")

        s= "param o :=" 
        for x in paramo:
            s += "\n" +  str(x[0]) + " " + str(x[1])
        s += ";"
        f.write(s + "\n")
    except:
       
        pass
    print("finished data conversion")
    return filename
    





 


        