from pyomo.environ import *
"""
Creates a Pyomo model for solving UFLP with input data 

Parameters
    dis: Dictionary of distances in the form ( (facility,customer ) : distance )
    op: Dictionary of opening costs 
    N:  Array of Facility
    M:  Array of Customer Identities
Returns 
    Model ( not solved ) representing the given instance of the Uncapacitated Facility Location Problem 
Description 
    Creates an Pyomo model object for solving a given Uncapacitated Facility Location Problem instance 
"""

def make_model(dis,op,N,M):

    model = ConcreteModel(name="(uflp)")

    model.x = Var(N, M, bounds=(0,1))   #Decision Variable for selected routes 
    model.y = Var(N, within=Binary)     #Decision variables for opened facilities 

    #Objective function, sum of selected distances and open facilities opening costs 
    def obj_rule(model):
        return sum(dis[n,m]*model.x[n,m] for n in N for m in M) + sum(op[n]*model.y[n] for n in N )
    model.obj = Objective(rule=obj_rule)

    #Each customer is served by only one facility, 
    def restrict_cust(model, m):
        return sum(model.x[n,m] for n in N) == 1
    model.one_per_cust = Constraint(M,rule=restrict_cust)

    #Each customer must have their demand met by some facility 
    def must_be_active(model, n, m):
        return model.x[n,m] <= model.y[n]
    model.warehouse_active = Constraint(N, M, rule=must_be_active)
    return model