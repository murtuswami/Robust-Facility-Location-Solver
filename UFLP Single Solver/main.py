

import data_convertor
import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import uflp

filename = data_convertor.convert()
opt = SolverFactory('cplex')
opt.options['timelimit'] = 30
instance = uflp.model.create_instance(filename+".dat")
opt.solve(instance,tee = True)
deltapercent = ((pyo.value(instance.obj) - optdict.get(f) ) / pyo.value(instance.obj) ) * 100
print ( "percentage difference from best value : " + str(deltapercent))
print( pyo.value(instance.obj) )


