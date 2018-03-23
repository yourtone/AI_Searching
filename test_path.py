#!/usr/bin/env python
__author__  = "Yuetan Lin"
__version__ = "1.1.0"

from Search import *
import numpy as np
from scipy.spatial.distance import cityblock

class Problem:
    def __init__(self, INITIAL_STATE, GOAL_STATE, ALL_ACTIONS, SIZE):
        self.INITIAL_STATE = np.uint8(np.array(INITIAL_STATE))
        self.GOAL_STATE = np.uint8(np.array(GOAL_STATE))
        self.ALL_ACTIONS = ALL_ACTIONS
        self.SIZE = SIZE
        self.WALLS = []
    def IN_BOUNDS(self, id):
        (x, y) = id
        return 0 <= x < self.SIZE[0] and 0 <= y < self.SIZE[1]
    def PASSABLE(self, id):
        (x, y) = id
        return (x, y) not in self.WALLS
    def ACTIONS(self, state): # [problem specified]
        feaaction = [] # feasible actions
        for action, actdirection in self.ALL_ACTIONS.iteritems():
            new_location = state + actdirection
            if self.IN_BOUNDS(new_location) and self.PASSABLE(new_location):
                feaaction.append(action)
        return feaaction
    def RESULT(self, p_state, action): # [problem specified]
        l2 = p_state + self.ALL_ACTIONS[action] # l2: new_location
        #if not (self.IN_BOUNDS(l2) and self.PASSABLE(new_location)):
        #    print 'Never go through'
        #    return None
        return l2
    def STEP_COST(self, p_state, action): # [problem specified]
        return 1 # cost 1 per move
    def GOAL_TEST(self, state): # [problem specified]
        return np.array_equal(state, self.GOAL_STATE)
    def HEURISTIC(self, state): # [problem specified]
        return cityblock(np.int8(state),np.int8(self.GOAL_STATE))

def PRINT_SOLUTION(problem, solution, hascutoff=False):
    if solution:
        infos = {}
        for i in xrange(problem.SIZE[0]):
            for j in xrange(problem.SIZE[1]):
                infos[(i,j)] = '-' # init
        for w in problem.WALLS:
            infos[w] = '*' # walls
        n_step = -1 # since the first one is root node
        for node in solution:
            n_step+=1
            infos[(node.STATE[0],node.STATE[1])] = '%d'%n_step
        s = ''
        for i in xrange(problem.SIZE[0]):
            for j in xrange(problem.SIZE[1]):
                s+=infos.get((i,j)).rjust(3)
            s+='\n'
        print s+ 'Finished in %d steps' % n_step
    elif hascutoff and (solution == cutoff):
        print 'Cutoff'
    else: # None
        print 'Failure'


### ================ ###
### Prepare problems ###
### ================ ###
actions = {'up':(-1,0), 'right':(0,1), 'down':(1,0), 'left':(0,-1)}
size = (15,15)
init_state = (12,0)
goal_state = (7,14)

path = Problem(init_state, goal_state, actions, size)
path.WALLS = [(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11),(2,12),
              (3,12),(4,12),(5,12),(6,12),(7,12),(8,12),(9,12),(10,12),(11,12),(12,12),
              (12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),(12,9),(12,10),(12,11)]

import time
### ================ ###
###      Search      ###
### ================ ###
print '===Path Finding==='
'''
start_time = time.time()
print '---BFS---'
solution = BREADTH_FIRST_SEARCH(path)
PRINT_SOLUTION(path, solution)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print '---UCS---'
solution = UNIFORM_COST_SEARCH(path)
PRINT_SOLUTION(path, solution)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print '---DFS---'
solution = DEPTH_FIRST_SEARCH(path)
PRINT_SOLUTION(path, solution)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print '---DLS---'
solution = DEPTH_LIMITED_SEARCH(path, 30)
PRINT_SOLUTION(path, solution, True)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print '---DLS1---'
solution = DEPTH_LIMITED_SEARCH_1(path, 30)
PRINT_SOLUTION(path, solution, True)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print '---DLS2---'
solution = DEPTH_LIMITED_SEARCH_2(path, 30)
PRINT_SOLUTION(path, solution, True)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print '---IDS---'
solution = ITERATIVE_DEEPENING_SEARCH(path)
PRINT_SOLUTION(path, solution, True)
print("--- %s seconds ---" % (time.time() - start_time))
'''

start_time = time.time()
print '---GBFS---'
solution = GREEDY_BEST_FIRST_SEARCH(path)
PRINT_SOLUTION(path, solution)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print '---AStar---'
solution = A_STAR_SEARCH(path)
PRINT_SOLUTION(path, solution)
print("--- %s seconds ---" % (time.time() - start_time))
