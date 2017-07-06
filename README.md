NoC mapping and routing flow
============================

Various python scripts, that use solvers like gurobi and qap to get optimum pacement flow routing of packets on a Network on Chip running a matrix product application.

## Dependencies: ##

- Python 2.7
- g++ 
- Gurobi Optimiser LP Solver

Install gurobi following the steps mentioned here https://www.gurobi.com/documentation/6.5/quickstart_mac/quickstart_mac.html
- Free academic license valid for a year can be obtained from here https://user.gurobi.com/download/licenses/free-academic
- Get Gurobi Optimizer for your system from here https://www.gurobi.com/downloads/gurobi-optimizer
- Follow the steps to untar and setup library paths in .bashrc
- Validate the license key
- Open gurobi shell to verify installation by $ gurobi.sh

## Makefile ##
`$ make help`

To see all possible targets for makefile 

`$ make`

The default will clean all and generate a fresh mapping and routing solution and resultant bluespec files in /bsv

## Generating Mapping results ##

`$ make map`

This will do the following 
- Python script qap_lp_algo.py generates the initial data files of the form qap_data_pg\<x\>.txt
- sa_qap_mandar.cpp is quadratic assigment problem solver using simulated annealing with hardcoded iteration and revision count
- g++ to compile the .cpp solver file
- Run the generated output a.out for all qap_data_pg\<x\>.txt files
- Result placement is stored in qap_sol_pg\<x\>.txt files to be read by mcmf solvers later
- For example for p=2, qap_data_pg2.txt has the data and qap_sol_pg2.txt has the solved location info

## Generating Routing results ##

`$ make route`

This will do the following
- Read data flow graph to setup initial data structure for multi commodity solver
- Formulates this as LP with cost and constraint, solved using Gurobi Optimiser
- Gurobi solutions are used to generate all possible arc-path using min flow recursive cut
- Generate bsc readable bluespec files in /bsv folder

## Get simulation results ##

- Uncomment lines for runtime in mcflow and runtime for that run will append in /data/Optimize_Runtimes.txt 
- Run scripts/mcflow_gencongestion.py to get model simulated congestion values for arc-path and XY routing

## Input for the flow

- Input data flow graph is specified as the dependency variable in mcflow.py python script, generated for the pg matrix product application

Shashank Gangrade  
High Performance Computing Lab  
Department of Electrical Engineering  
IIT Bombay
