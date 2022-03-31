 # uflp _abstract.py:  \

from pyomo.environ import *

model = AbstractModel(name="(uflp_rob)")
model.N = Set()  # facilities
model.M = Set()  # customers



model.d = Param(model.N,model.M) # distances 
model.o = Param(model.N) # opening costs 
model.dc = Param(model.N) #deviation coefficients 
model.dconst = Param()


model.x = Var(model.N, model.M, bounds=(0,1)) # (selected routes )
model.y = Var(model.N, within=Binary)       #selected facilities 
def obj_rule(model):
    return sum(model.d[n,m]*model.x[n,m] for n in model.N for m in model.M) + sum(model.o[n]*model.y[n] for n in model.N ) + sum( (model.dc[n] - model.dconst)for n in model.N)
model.obj = Objective(rule=obj_rule)

def single_demand_rule(model, m):
    return sum(model.x[n,m] for n in model.N) == 1
model.single_demand = Constraint(model.M,rule=single_demand_rule)

def fac_act_rule(model, n, m):
    return model.x[n,m] <= model.y[n]
model.warehouse_active = Constraint(model.N, model.M, rule=fac_act_rule)
