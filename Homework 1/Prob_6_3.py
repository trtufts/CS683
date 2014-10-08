# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 20:14:26 2014
Python 2.7
@author: Tim Tufts

CS 683
HW 1
Problem 6.2 and 6.3

6.2
Generates problems for instances of Travelling Salesman Problem,
Takes number of cities as a parameter and generates them as random points in the unit square

6.3
Solves generated TSP problems

Inspiration for Prim's came from:
http://interactivepython.org/runestone/static/pythonds/Graphs/graphshortpath.html
but was written from scratch with my implementation of cities, roads, and PriorityQueue
"""
import random, math, PriorityQueue, time, sys
from collections import OrderedDict
try:
    import matplotlib.pyplot as plt
    importFlag = True
except:
    importFlag = False

# Problem generator for Problem 6.2, takes in number of cities,
# returns the city coords, the paths between them
# the cities will be named with numbers, the paths between them keyed with a_b where a and b are the start and end numbers
# given the random nature of generation, the first city will always be considered the origin city without much lose of problem diversity
def TSP_Generator(numCities):
    cities = OrderedDict()
    roads = OrderedDict()
    for city in range(numCities):                       # creates the desired number of cities, named as numbers, 0 indexed
        # random.random generates a float in the range of 0.0 to 1.0
        x = random.random()
        y = random.random()
        if cities:                                      # if there are already cities, i.e. this is not the first
            roads.update(                               # add roads connecting this city to each other by the Euclidean Distance
                {'{}_{}'.format(source,city):
                math.sqrt( (cities[source][0]-x)**2 + (cities[source][1]-y)**2 )
                for source in cities})
        cities[city] = (x,y)
    print cities
    print roads

    return cities, roads                                # return the cities and roads to be solved as a TSP

# used as a quick dirty fix to use priorityQueue with basic elements in the heurFunc
class cityObject:
    def __init__(self, name, prevNode):
        self.name = name
        self.prevNode = prevNode

# define a node that stores all relevant info
class node:
    # heuristic function, takes the unconnected cities, the entire road dict and the starting city as inputs to get the sum of the MST edge weights
    def heurFunc(self, cities, roads, start):
        MSTsum = 0
        lowestRoadCosts = PriorityQueue.PriorityQueue()
        Cities = list(cities)                           # we copy the list from the pointer since we are going to edit it

        # with my implementation of PriorityQueue, add_node only puts the new instance on if the path is shorter than the current shortest path
        for city in Cities:                             # iterate over every city we still need to add and take the path cost to it
            if city < start: lowestRoadCosts.add_node(cityObject(city, start), roads['{}_{}'.format(city,start)])  # key strings are ordered with the smaller value first
            else: lowestRoadCosts.add_node(cityObject(city, start), roads['{}_{}'.format(start, city)])

        while lowestRoadCosts.pq:                       # pop off the cheapest connection and update all the previous connections
            try: nextCity = lowestRoadCosts.pop_node()
            except KeyError: break                      # catch when the queue is full of removed nodes
            if nextCity.name < nextCity.prevNode: MSTsum += roads['{}_{}'.format(nextCity.name,nextCity.prevNode)]
            else: MSTsum += roads['{}_{}'.format(nextCity.prevNode,nextCity.name)]
            Cities.remove(nextCity.name)
            for city in Cities:                         # iterate over every city we still need to add and take the path cost to it
                if city < nextCity.name: lowestRoadCosts.add_node(cityObject(city, nextCity.name), roads['{}_{}'.format(city,nextCity.name)])  # key strings are ordered with the smaller value first
                else: lowestRoadCosts.add_node(cityObject(city, nextCity.name), roads['{}_{}'.format(nextCity.name, city)])

        return MSTsum

    # initialization function to set instance level values and compute the f value
    def __init__(self, previousCity, currentCity, prevPath, visitedCities, cities, roads):
        # City that the salesman is in, origin node for the MST
        self.currentCity = currentCity

        # list of cities the salesman has already visited
        if visitedCities: self.visitedCities = list(visitedCities)
        else: self.visitedCities = []
        self.visitedCities.append(currentCity)

        # name of the node, used as a standard for nodes in my priorityqueue
        self.name = "{}".format(','.join([str(cityInt) for cityInt in self.visitedCities]))

        # path taken to this node
        if previousCity != -1:  # if the city was not the origin city, format what to add to the path list
            if previousCity < currentCity: newPath = '{}_{}'.format(previousCity, currentCity)
            else: newPath = '{}_{}'.format(currentCity, previousCity)
        if previousCity == 0: self.path = [newPath]     # if this is the first step, initialize the path list
        elif prevPath:                                  # if there is already a previous path, add the new path part to it
            self.path = list(prevPath)
            self.path.append(newPath)
        else: self.path = []                            # if this is the origin city, there is no path so far

        # the distance traveled in this state is the sum of the road costs along the path
        self.pathCost = 0
        for step in self.path:
            self.pathCost += roads[step]

        # create the list of cities left by removing all the visited cities from the full city list
        self.citiesLeft = list(cities)
        for city in self.visitedCities:
            try: self.citiesLeft.remove(city)
            except ValueError:
                if city == 0: break                     # if it encounters city 0 for a second time, break out of the loop and leave an empty city list
                else: raise('Duplicate City')

        # estimated f-value for this state
        self.fValue = self.pathCost + self.heurFunc(self.citiesLeft, roads, currentCity)

# performs A* search on the generated cities, origin is always 0
def A_star(cities, roads):
    startPos = node(-1, 0, [], [], cities, roads)       # initializes the start state
    frontier = PriorityQueue.PriorityQueue()            # initializes my custom priority queue
    frontier.add_node(startPos,startPos.fValue)         # adds the start position to the priority queue with its f-value as the priority
    explored = {}                                       # initialize the set of explored states

    # metrics
    nodesExpanded = 0
    timestart = time.clock()

    while(frontier.pq):                                 # explore nodes until the frontier comes back empty
        curPos = frontier.pop_node()                    # pop a node off of the frontier
        nodesExpanded += 1
        if not curPos.citiesLeft and not curPos.currentCity: # if the state is a goal state, return the path to it and its cost, and other metrics. This check says no cities are left and we are in the origin city 0
            return curPos.path, curPos.pathCost, nodesExpanded, (time.clock() - timestart)
        explored[curPos.name] = curPos.pathCost         # add the state the explored states with its path cost
        actions = curPos.citiesLeft                     # the available actions are to go to any of the remaining cities
        if not actions: actions = [0]                   # if there are no cities left, the available action is to go to the origin, so we put that option onto the frontier (not it is not automatically picked)
        for action in actions:                          # perform every action on the current state
            child = node(curPos.currentCity,            # the previous city of the next city is the current city
                action,                                 # action represents the next city
                curPos.path,                            # pass the path to the child so it can add itself to the path
                curPos.visitedCities,                   # pass in the previous visited cities and the new one gets added during initialization
                cities, roads)                          # pass the city and road dictionaries
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
        cities, roads = TSP_Generator(int(sys.argv[2]))
        print A_star(cities, roads)

    elif sys.argv[1].lower() == 'suite' and importFlag:
        numcities = []
        numnodes = []
        comptime = []
        for a in range(100):
            numCities = random.randint(0, 15)
            cities, roads = TSP_Generator(numCities)
            path, steps, nodes, time = A_star(cities, roads)
            numcities.append(numCities)
            numnodes.append(nodes)
            comptime.append(time)

        plt.figure(1)
        plt.subplot(121)
        plt.scatter(numcities, numnodes)
        plt.xlabel('Number of Cities in Problem')
        plt.ylabel('Number of Nodes expanded')

        plt.subplot(122)
        plt.scatter(numcities, comptime)
        plt.xlabel('Number of Cities in Problem')
        plt.ylabel('Computation Time')
        plt.show()
    elif sys.argv[1].lower() == 'suite' and not importFlag:
        print 'Failed to load matplotlib.pyplot'

    raw_input("")
if __name__ == "__main__":
    main()