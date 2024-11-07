# distributed-epidemic-prediction-large-scale-graph

This is the source code repo for the paper "Accurate and Efficient Distributed COVID-19 Spread Prediction based on a Large-Scale Time-Varying People Mobility Graph'' accepted at IEEE International Parallel and Distributed Processing Symposium (IPDPS 2023).

All codes are written in python. Tested in Python3. Command to run a file: python3 filename.py

initial_static_graph_partitioning.py has the codes for initial graph partitioning and replication

worker.py is the code for SIR calculation

next_iteration has the codes for repartitioning

Mobility prediction has the codes for the ML model to predict mobiility between grids

Graph alignment has the codes for aligning partition graph and server graph

analysis_codes.rar has the codes for the data analyses described in the paper
