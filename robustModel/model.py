

from pyomo.environ import *
def make_model(dis,op,N,M):
    #distance is distances
    #op is opening costs 
    #n is a set containing the customers identity 
    #m is a set containing the demand nodes identity 
    model = ConcreteModel(name="(uflp)")


    model.x = Var(N, M, bounds=(0,1)) # (selected routes )
    model.y = Var(N, within=Binary)       #selected warehouses 

    def obj_rule(model):
        return sum(dis[n,m]*model.x[n,m] for n in N for m in M) + sum(op[n]*model.y[n] for n in N )
    model.obj = Objective(rule=obj_rule)

    def restrict_cust(model, m):
        return sum(model.x[n,m] for n in N) == 1
    model.one_per_cust = Constraint(M,rule=restrict_cust)

    def must_be_active(model, n, m):
        return model.x[n,m] <= model.y[n]
    model.warehouse_active = Constraint(N, M, rule=must_be_active)
    return model