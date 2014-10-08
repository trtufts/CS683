Problem 5.3 is the Knight's Shortest Path Problem
There are two ways to run this code with command line arguments.
The first is a single coordinate pair mode which looks like this:
  Prob_5_3.py Single x y
  where x and y are the target coordinates.
This will output the path taken, the number of moves in the path, 
the number of states explored to find this path and the computation time.

The second way runs a suite of random coordinates and is run like this:
  Prob_5_3.py Suite
This will create two graphs that show the number of states expanded and the computation time
both as functions of the number of steps in the solution.
This method requires matplotlib.pyplot and will tell you if it cannot be found.
