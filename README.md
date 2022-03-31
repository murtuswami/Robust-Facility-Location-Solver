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

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)