# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 17:02:27 2014
Python 2.7
@author: Tim Tufts

Priority Queue implementation used from
https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes

I added some customization to make it work better with my node implementation
"""
import heapq, itertools

class PriorityQueue:
    def __init__(self):
        self.pq = []                                    # list of entries arranged in a heap
        self.entry_finder = {}                          # mapping of nodes to entries
        self.REMOVED = '<removed-task>'                 # placeholder for a removed task
        self.counter = itertools.count()                # unique sequence count, used in tie breakers

    def add_node(self, node, priority=0):
        'Add a new node or update the priority of an existing node'
        if node.name in self.entry_finder:              # I use node.name as a standard implementation to allow for looking up a node
            if self.entry_finder[node.name][0] < priority:  # we only want to update the priority if we found a better path
                #print "{} already in queue with lower priority: {} vs {}".format(node.name, self.entry_finder[node.name][0], priority)
                return
            self.remove_node(node.name)                 # mark the old node as removed
        count = next(self.counter)
        entry = [priority, count, node]
        self.entry_finder[node.name] = entry
        heapq.heappush(self.pq, entry)                  # enter the new node with the better priority

    def remove_node(self, nodename):
        'Mark an existing node as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(nodename)
        entry[-1] = self.REMOVED

    def pop_node(self):
        'Remove and return the lowest priority node. Raise KeyError if empty.'
        while self.pq:                                  # this loop removes marked nodes as it finds them and returns the lowest valid node
            priority, count, node = heapq.heappop(self.pq)
            if node is not self.REMOVED:
                del self.entry_finder[node.name]
                return node
        raise KeyError('pop from an empty priority queue')