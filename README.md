# Robust Uncapcaitated Facility Location Solver

This project implements methods for solving Uncapcaitated Facility Location(UFLP) nominally and under data uncertainty.

Can be used for solving the UFLP approximately and to optimality and to produce robust solutions to the UFLP under spatial demand uncertainty. 

## Description

The project implements two methods for solving the UFLP a Local Search Algorithm and an Optimization model written in Pyomo. The optimization model is configured to run with CPLEX but can be reconfigured for use with any MIP solver with Pyomo Interface. 

The Robust Solver implements Cardinality Constrained Robustness, where each demand node in the UFLP has an uncertain interval. It solves the problem with an input parameter gamma which corresponds to the number of demand nodes taking on their worst case realization within their demand interval. The solution is produced by solving nominal instances of the UFLP to optimality using the Pyomo model. 


## Getting Started

### Dependencies

* Python 3.8.8 + 
* Pyomo 6.1.2 +
* IBM ILOG CPLEX Interactive Optimizer 20.1.0.0 +
 
### Recommended Installation 

* Install the latest Anaconda distribution https://www.anaconda.com/
* From the Anaconda CLI install Pyomo with 
    ```
    conda install -c conda-forge pyomo
    ```
* If using CPLEX for the optimization model install from https://www.ibm.com/analytics/cplex-optimizer
* If using another Optimzation solver with a Pyomo interface update the SolverFactory object parameters in 
        - optimizationModel/solver.py
        - robustModel/robustModelVaryGamma.py
        - robustModel/worstCaseRealizations.py
        - robustModel/robustSingleSolve.py

## Execution 

Each folder contains a single dataset to run and produce output on.
A more detailed exploration can be done by running on instances in the /Data directory
All algorithms can accept datasets in the input format specified in 
https://resources.mpi-inf.mpg.de/departments/d1/projects/benchmarks/UflLib/data-format.html

### Running Local Search 

* 

### Running Optimization Solver

### Running Robust Model 


## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Harsha Ramachandran

## Version History

* 1.0 
    * Initial Release 

### Data 
Contains extracts from the two data sets from the Max Planck Institute For Informatics
Access at  https://resources.mpi-inf.mpg.de/departments/d1/projects/benchmarks/UflLib/packages.html

* Euclidian Benchmarks 
* Koerkel-Ghosh Asymmetric Benchmarks 


Data folder contains data sets and their optimal/best known solutions 
https://resources.mpi-inf.mpg.de/departments/d1/projects/benchmarks/UflLib/data-format.html

Data is Seperated into folders based on report section they appear in 

### Results 


