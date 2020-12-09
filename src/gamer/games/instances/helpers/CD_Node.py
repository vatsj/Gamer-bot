"""
Cardinal Direction - Node

Class describing a component node of CD_Linkedlist
Links in cardinal directions (North South East West)
Go board formed as a grid of CD_Node-s
"""

class CD_Node:

    # directions in which nodes can be adjacent
    ADJACENCY_DIRS = ["north", "east", "south", "west"]

    # constructs a new node
    def __init__(self, value = None):

        # value of the node, can be arbitrary type
        self.value = value

        # dict of pointers to adjacent CD_nodes
        # initialized to none, can be linked up via helper methods
        adjacent = {}
        for dir in ADJACENCY_DIRS:
            adjacent[dir] = None

        self.adjacent = adjacent

    # gets node adjacent to self in direction dir
    def getAdjacent(self, dir):

        if dir in ADJACENCY_DIRS:
            adj_node = self.adjacent[dir]
            return adj_node
        # if dir is invalid direction, throw an error
        else:
            print("games.instances.Go error: invalid adjacency direction!")

    # sets self adjacent to target_node in direction dir
    def setAdjacent(self, dir, target_node):

        if dir in ADJACENCY_DIRS:
            self.adjacent[dir] = target_node
        # if dir is invalid direction, throw an error
        else:
            print("games.instances.Go error: invalid adjacency direction!")
