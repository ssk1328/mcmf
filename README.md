# mcmf

Various python scripts, that use solvers like gurobi and qap to get optimum pacement flow routing of packets on a Network on Chip for a Matrix Vector Multiplication application

The tasks can be broken down in to the following

- Python script lp_qap.py generates text files, which serve as data files for quadratic assignment problem solver
- sa_qap.cpp files takes the data from text file to generate a optimum placement on the mesh
- mcmf.py uses the placment and using the flow information models this as a multi commodity flow problem
- mcmf.py further generates the Lookup.bsv for logic to store this routing information


Shashank Gangrade
High Performance Computing Lab
EE, IITB
