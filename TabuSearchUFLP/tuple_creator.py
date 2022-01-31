import tkinter
from tkinter import filedialog
f = open("tuples.txt","w")
tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
print("Please select file with input data")
inputdatapath = filedialog.askopenfilename()
datafile = open(inputdatapath)
arr =[]
count = 0
for line in datafile:
    arr.append(((str(count),line.rstrip().split()[0])))
    count = count + 1
print(arr)

for x in arr:
    f.write("(")
    f.write(x[0])
    f.write(",")
    f.write(x[1])
    f.write(")" )

    
  
