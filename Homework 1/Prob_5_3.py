# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 19:56:33 2014
Python 2.7
@author: Tim Tufts

CS 683
HW 1
Problem 5.3

Solves the Knight's Shortest Path problem with the heuristic function designed in problem 5.2
(For Github: this problem finds the shortest path a knight on a chessboard can
take to go from (0,0) to (x,y) where x and y can be negative.
The heuristic is the maximum of the absolute distance between the current pos
and the target pos for both coordinates, all over two.  i.e from the start it is
max of abs( x/2 ) and abs ( y/2 ).  Please contact me if you would like the
reasoning for this )
"""

import PriorityQueue, random, time, sys
try:
    import matplotlib.pyplot as plt
    importFlag = True
except:
    importFlag = False

# define a node that stores all relevant info
class node:
    # heuristic function, takes the goal coordinates as input
    def heurFunc(self, xg, yg):
        return max(abs((xg- self.xPos)/2), abs((yg- self.yPos)/2))

    # initialization function to set instance level values and compute the f value
    def __init__(self, xPos, yPos, pathCost, prevPath, xg, yg):
        # x and y position of the knight in this state
        self.xPos = xPos
        self.yPos = yPos

        # name of the node, used as a standard for nodes in my priorityqueue
        self.name = "{}_{}".format(xPos,yPos)

        # how many moves it took to get to this state
        self.pathCost = pathCost

        # path taken to this node
        if not prevPath: self.path = [(xPos,yPos)]
        else:
            self.path = list(prevPath)
            self.path.append((xPos, yPos))

        # estimated f-value for this state
        self.fValue = pathCost + self.heurFunc(xg, yg)

# performs A* search on goal coordinates (xg,yg) from (0,0)
def A_star(xg, yg):
    startPos = node(0, 0, 0, [], xg, yg)                # initializes the start state
    frontier = PriorityQueue.PriorityQueue()            # initializes my custom priority queue
    frontier.add_node(startPos,startPos.fValue)         # adds the start position to the priority queue with its f-value as the priority
    explored = {}                                       # initialize the set of explored states
    actions = [(2,1),(-2,1),(-2,-1),(2,-1),(1,2),(-1,2),(-1,-2),(1,-2)] # these are all of the actions that can be made at any point

    # metrics
    nodesExpanded = 0
    timestart = time.clock()

    while(frontier.pq):                                 # explore nodes until the frontier comes back empty
        curPos = frontier.pop_node()                    # pop a node off of the frontier
        nodesExpanded += 1
        if ((curPos.xPos,curPos.yPos) == (xg,yg)):      # if the state is a goal state, return the path to it and its cost, and other metrics
            return curPos.path, curPos.pathCost, nodesExpanded, (time.clock() - timestart)
        explored[curPos.name] = curPos.pathCost         # add the state the explored states with its path cost
        for action in actions:                          # perform every action on the current state
            child = node(curPos.xPos+action[0],         # the child has coordinates change based on the action
                curPos.yPos+action[1],
                curPos.pathCost+1,                      # the path cost is always one more since we are taking one action
                curPos.path,                            # pass the path to the child so it can add itself to the path
                xg, yg)                                 # same goal states for computation of h
            if child.name in explored:                  # before adding the child to the frontier, check if it has been explored
                if explored[child.name] > child.pathCost:   # if it was already explored but with a greater path cost, search it again
                    #print "Node {} already explored but found shorter path, {} vs {}, attempting to add to frontier".format(child.name,child.pathCost,explored[child.name])
                    pass
                else:                                   # if it was already explored at a cheaper or equal cost, don't add it
                    #print "Node {} already explored".format(child.name)
                    continue
            frontier.add_node(child, child.fValue)      # this add checks to see if it is already on the frontier and updates the priority if need be
    return "No path found", 0                           # return if no path

def main():
    if sys.argv[1].lower() == 'single':
        # goal state can be set here.  This state solves in about a second, 1000,1000 solves in about 2 minutes
        xg = int(sys.argv[2])
        yg = int(sys.argv[3])

        # prints the path to the goal and the number of steps to get there
        print A_star(xg, yg)

    elif sys.argv[1].lower() == 'suite' and importFlag:
        numsteps = []
        numnodes = []
        comptime = []
        for a in range(100):
            xg = random.randint(-100, 100)
            yg = random.randint(-100, 100)
            path, steps, nodes, time = A_star(xg,yg)
            numsteps.append(steps)
            numnodes.append(nodes)
            comptime.append(time)

        plt.figure(1)
        plt.subplot(121)
        plt.scatter(numsteps, numnodes)
        plt.xlabel('Number of Steps in Solution')
        plt.ylabel('Number of Nodes expanded')

        plt.subplot(122)
        plt.scatter(numsteps, comptime)
        plt.xlabel('Number of Steps in Solution')
        plt.ylabel('Computation Time')
        plt.show()
    elif sys.argv[1].lower() == 'suite' and not importFlag:
        print 'Failed to load matplotlib.pyplot'

    raw_input("")
if __name__ == "__main__":
    main()
