#Superficial Ghosts: Collective Bayesian Decision-Making in Pacman

This project was developed in Python 3.10, hence it is recommended 
(but not required) to use a virtual environment like anaconda. To install anaconda,
check:

Then create a conda environment with Python 3.10:
conda create -n pac-man python=3.10

Install required packages:
pip install -r requirements

Run the bayesian algorithm:
python pacman.py bayesian

Run the benchmark algorithm:
python pacman.py benchmark

Commands:
--n         Number of runs
--ratio     Ratio of colours, should be n-1 for n colours
--map       Name of map
--ghosts    Number of agents
--colours   Number of colours

Examples:
Run algorithm 10 times:
python pacman.py bayesina --n=10

Run with 5 agents:
python pacman.py benchmark --ghosts=5

Run with ratio of 0.6
python pacman.py bayesian --ratio=0.6

Run the extended bayesian algorithm in environment with 3 colours:
python pacman.py bayesian --ratio=0.6,0.2 --colour=3

To run the algorithm for ten times with a ratio 0.53 in the line map:
python pacman.py bayesian --n=10 --ratio=0.53 --map=line