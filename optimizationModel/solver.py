""" Imports data file, processes it, define a Pyomo model for solving the UFLP and solve with processed data as input"""

import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.environ import *
from processPyomoData import processPyomoData
from model import make_model

### Get Data from file and convert it into format appropriate for Pyomo Model ### 


n,m,d,o,arrRepresentation,N,M = processPyomoData()

### Solve Model and write results to file ###

opt = SolverFactory('cplex') 
opt.options['timelimit'] = 180 #3 mins time limit 
model = make_model(d,o,N,M)
opt.solve(model,tee = True,logfile ="results.txt") #Solve model with verbose settings 
print( pyo.value(model.obj) )


