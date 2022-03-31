from pyomo.environ import *
def make_robust_model(dis,op,N,M,d,dc):
 
    model = ConcreteModel(name="(uflp_robust)")
    model.x = Var(N, M, bounds=(0,1)) # (selected routes )
    model.y = Var(N, within=Binary)       #selected facilities

    def obj_rule(model):    
        return sum( (dis[n,m] +max((d[m]- dc),0))*model.x[n,m] for n in N for m in M) + sum(op[n]*model.y[n] for n in N ) 
    model.obj = Objective(rule=obj_rule)

    def restrict_cust(model, m):
        return sum(model.x[n,m] for n in N) == 1
    model.one_per_cust = Constraint(M,rule=restrict_cust)

    def must_be_active(model, n, m):
        return model.x[n,m] <= model.y[n]
    model.warehouse_active = Constraint(N, M, rule=must_be_active)
    
    return model