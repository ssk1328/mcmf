# mcmf

# Multi Commodity Max Flow

Various python scripts, that use solvers like gurobi and qap to get optimum pacement flow routing of packets on a Network on Chip running a matrix product application.

To run and files and generate dataf

Dependencies:f

- Python 2.7
- g++ 
- Gurobi Optimiser LP Solver

Install gurobi following the steps mentioned here https://www.gurobi.com/documentation/6.5/quickstart_mac/quickstart_mac.html
- d
d
The tasks can be broken down in to the followingf

- Python script lp_qap.py generates text files, which serve as data files for quadratic assignment problem solver
- sa_qap.cpp files takes the data from text file to generate a optimum placement on the mesh
- mcmf.py uses the placment and using the flow information models this as a multi commodity flow problem
- mcmf.py further generates the Lookup.bsv for logic to store this routing information

In /qap_scripts
---------------
- qap_lp_algo.py generates the initial data files of the form qap_data_pg\<x\>.txt
- sa_qap_mandar.cpp is the modified .cpp solver which uses the network specification from data file and use a simulated anneleaning approach to solve for optimal placement
- iteration and revision count are hardcoded in sa_qap_mandar.cpp file
- Result placement is stored in qap_sol_pg\<x\>.txt files to be read by mcmf solvers later
- For example for p=2, qap_data_pg2.txt has the data and qap_sol_pg2.txt has the solved location info

Shashank Gangrade  
High Performance Computing Lab  
Department of Electrical Engineering  
IIT Bombay
