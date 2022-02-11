# wl_abstract.py: AbstractModel version of warehouse \

from pyomo.environ import *

model = AbstractModel(name="(WL)")
model.N = Set()  # warehouses / supply
model.M = Set()  # cities / demand

model.d = Param(model.N,model.M)

model.o = Param(model.N)

model.x = Var(model.N, model.M, bounds=(0,1)) # (selected routes )
model.y = Var(model.N, within=Binary)       #selected warehouses 

def obj_rule(model):
    return sum(model.d[n,m]*model.x[n,m] for n in model.N for m in model.M) + sum(model.o[n]*model.y[n] for n in model.N )
model.obj = Objective(rule=obj_rule)

def one_per_cust_rule(model, m):
    return sum(model.x[n,m] for n in model.N) == 1
model.one_per_cust = Constraint(model.M,rule=one_per_cust_rule)

def warehouse_active_rule(model, n, m):
    return model.x[n,m] <= model.y[n]
model.warehouse_active = Constraint(model.N, model.M, rule=warehouse_active_rule)
