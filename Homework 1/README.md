Problem 5.3 is the Knight's Shortest Path Problem
There are two ways to run this code with command line arguments.
The first is a single coordinate pair mode which looks like this: <br>
  Prob_5_3.py Single x y<br>
  where x and y are the target coordinates.<br>
This will output the path taken, the number of moves in the path, 
the number of states expanded to find this path and the computation time.

The second way runs a suite of random coordinates and is run like this:<br>
  Prob_5_3.py Suite<br>
This will create two graphs that show the number of states expanded and the computation time
both as functions of the number of steps in the solution.
This method requires matplotlib.pyplot and will tell you if it cannot be found.


Problem 6.3 is the Travelling Salesman Problem
This code is run in the same way as the KSP in Problem 5.3
The single problem mode looks like this:<br>
  Prob_6_3.py Single x<br>
  where x is the number of cities to consider.  In general I avoid going above 15 or 20 because the computation time ramps up significantly<br>
This will output the path taken, the path distance, the number of nodes expanded and the computation time.

The second way is also a suite as before and is run like this:<br>
Prob_6_3.py Suite<br>
This creates the same graphs as above.

Note: The cities are all coordinates in the unit square and the origin city is the first city generated.<br>
When the problem is generated it prints out all the cities and roads.


All of the code ends with a prompt for raw input.  This means you can end the execution by hitting enter when it is done.  I did this in case it is being run in a window that closes out right away so you can control when it will close the window.
