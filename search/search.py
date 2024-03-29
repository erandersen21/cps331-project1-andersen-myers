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
import searchAgents

class Node:

    def __init__(self, state, parent, action, pathCost):
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost

    def returnState(self):
        return self.state

    def returnParent(self):
        return self.parent
    
    def returnAction(self):
        return self.action
    
    def returnPathCost(self):
        return self.pathCost

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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    currNode = Node(problem.getStartState(), None, None, 0)
    actionList = []
    if problem.isGoalState(currNode.returnState()):
        return actionList
    fringe = util.Stack()
    fringe.push(currNode)
    visitedStates = []

    while not fringe.isEmpty():
        currNode = fringe.pop()
        state = currNode.returnState()
        if state not in visitedStates:
            visitedStates.append(state)
            if problem.isGoalState(state):
                while currNode.returnParent() != None:
                    actionList.insert(0, currNode.returnAction())
                    currNode = currNode.returnParent()
                return actionList
            for successor in expand(problem, currNode):
                fringe.push(successor)
    return None

def expand(problem, node):
    state = node.returnState()
    for triple in problem.getSuccessors(state):
        nextState = triple[0]
        action = triple[1]
        pathCost = triple[2] + node.returnPathCost()
        yield Node(nextState, node, action, pathCost)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    currNode = Node(problem.getStartState(), None, None, 0)
    actionList = []
    if problem.isGoalState(currNode.returnState()):
        return actionList
    fringe = util.Queue()
    fringe.push(currNode)
    visitedStates = [currNode.returnState()]

    while not fringe.isEmpty():
        currNode = fringe.pop()
        for successor in expand(problem, currNode):
            state = successor.returnState()
            if problem.isGoalState(state):
                node = successor
                while node.returnParent() != None:
                    actionList.insert(0, node.returnAction())
                    node = node.returnParent()
                return actionList
            if state not in visitedStates:
                visitedStates.append(state)
                fringe.push(successor)
    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    currNode = Node(problem.getStartState(), None, None, 0)
    actionList = []
    fringe = util.PriorityQueue()
    fringe.push(currNode, 0)
    visitedStates = []
    while not fringe.isEmpty():
        currNode = fringe.pop()
        if currNode.returnState() not in visitedStates:
            visitedStates.append(currNode.returnState())
            if problem.isGoalState(currNode.returnState()):
                while currNode.returnParent() != None:
                    actionList.insert(0, currNode.returnAction())
                    currNode = currNode.returnParent()
                return actionList
            for successor in expand(problem, currNode):
                fringe.push(successor, successor.returnPathCost())
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    currNode = Node(problem.getStartState(), None, None, 0)
    actionList = []
    fringe = util.PriorityQueue()
    fringe.push(currNode, heuristic(currNode.returnState(), problem))
    visitedStates = []
    while not fringe.isEmpty():
        currNode = fringe.pop()
        if currNode.returnState() not in visitedStates:
            visitedStates.append(currNode.returnState())
            if problem.isGoalState(currNode.returnState()):
                while currNode.returnParent() != None:
                    actionList.insert(0, currNode.returnAction())
                    currNode = currNode.returnParent()
                return actionList
            for successor in expand(problem, currNode):
                fringe.push(successor, successor.returnPathCost() + heuristic(successor.returnState(), problem))
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
