# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class Node:
    PRV = []

    def __init__(self, state, direction='', parent=None, cost=0):
        Node.PRV.append(state)
        self.state = state
        self.parent = parent
        self.children = []
        self.direction = direction
        self.cost = cost

    def add_child(self, child):
        new_child = Node(child[0], child[1], self, self.cost + child[2])
        self.children.append(new_child)
        return new_child

    @classmethod
    def clear(cls):
        cls.PRV = []


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""

    def helper(state, path, visited):
        if state in visited:
            return []
        else:
            visited.append(state)
        if problem.isGoalState(state):
            return path
        all_paths = []
        for suc in problem.getSuccessors(state):
            all_paths.append(helper(suc[0], path + [suc[1]], visited[:]))
        paths = filter(len, all_paths)
        if paths:
            return min(paths, key=len)
        return []

    return helper(problem.getStartState(), [], [])


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    root = Node(problem.getStartState())
    laye = [root]
    while laye:
        temp = []
        for r in laye:
            for child in problem.getSuccessors(r.state):
                if child[0] not in Node.PRV:
                    temp.append(r.add_child(child))
                    if problem.isGoalState(child[0]):
                        node = temp[-1]
                        path = []
                        while node.parent:
                            path.append(node.direction)
                            node = node.parent
                        Node.clear()
                        return path[::-1]
        laye = temp
    Node.clear()
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    import heapq
    COSTS = {}
    heap = [(0, Node(problem.getStartState()))]
    while heap:
        cost, node = heapq.heappop(heap)
        if node.state in COSTS and COSTS[node.state] < cost:
            continue
        COSTS[node.state] = cost
        if problem.isGoalState(node.state):
            path = []
            while node.parent:
                path.append(node.direction)
                node = node.parent
            Node.clear()
            return path[::-1]
        for child in problem.getSuccessors(node.state):
            heapq.heappush(heap, (cost + child[2], node.add_child(child)))
    Node.clear()
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    import heapq
    root = Node(problem.getStartState())
    heap = [(heuristic(root.state, problem), root)]
    while heap:
        _, node = heapq.heappop(heap)
        if problem.isGoalState(node.state):
            path = []
            while node.parent:
                path.append(node.direction)
                node = node.parent
            Node.clear()
            return path[::-1]
        for child in problem.getSuccessors(node.state):
            if child[0] not in Node.PRV:
                heapq.heappush(heap, (node.cost + child[2] + heuristic(child[0], problem), node.add_child(child)))
    Node.clear()
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
