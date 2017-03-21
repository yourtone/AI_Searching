#!/usr/bin/env python
__author__  = "Yuetan Lin"
__version__ = "1.2.1"

from Search import *
import numpy as np

PZ3SZ = (2,2)
PZ8SZ = (3,3)

class State: # [problem specified]
    def __init__(self, SIZE):
        self.SIZE = SIZE
    def create(self, arr):
        return np.uint8(np.resize(np.array(arr),self.SIZE))

class Problem:
    def __init__(self, INITIAL_STATE, GOAL_STATE, ALL_ACTIONS, SIZE):
        self.INITIAL_STATE = INITIAL_STATE
        self.GOAL_STATE = GOAL_STATE
        self.ALL_ACTIONS = ALL_ACTIONS
        self.SIZE = SIZE
    def IN_BOUNDS(self, id):
        (x, y) = id
        return 0 <= x < self.SIZE[0] and 0 <= y < self.SIZE[1]
    def FIND_ZERO(self, state):
        location = np.where(state==0)
        # TODO: assert location has values
        return np.array([location[0][0],location[1][0]])
    def ACTIONS(self, state): # [problem specified]
        l1 = self.FIND_ZERO(state)
        feaaction = [] # feasible actions
        for action, actdirection in self.ALL_ACTIONS.iteritems():
            if self.IN_BOUNDS(l1 + actdirection):
                feaaction.append(action)
        return feaaction
    def RESULT(self, p_state, action): # [problem specified]
        l1 = self.FIND_ZERO(p_state)
        l2 = l1 + self.ALL_ACTIONS[action] # l2: new_location
        #if not self.IN_BOUNDS(l2):
        #    print 'Never go through'
        #    return None
        state = np.copy(p_state)
        state[l1[0],l1[1]],state[l2[0],l2[1]]=state[l2[0],l2[1]],state[l1[0],l1[1]]
        return state
    def STEP_COST(self, p_state, action): # [problem specified]
        return 1 # cost 1 per move
    def GOAL_TEST(self, state): # [problem specified]
        return np.array_equal(state, self.GOAL_STATE)

def PRINT_SOLUTION(solution, hascutoff=False):
    if solution:
        n_step = -1 # since the first one is root node
        for node in solution:
            print node.ACTION
            print node.STATE
            n_step+=1
        print 'Finished in %d steps' % n_step
    elif hascutoff and (solution == cutoff):
        print 'Cutoff'
    else: # None
        print 'Failure'


### ================ ###
### Prepare problems ###
### ================ ###
actions = {'up':(-1,0), 'right':(0,1), 'down':(1,0), 'left':(0,-1)}
# puzzle 3
size = PZ3SZ
state3 = State(size)
init_state = state3.create(np.random.permutation(np.arange(np.prod(size))))
goal_state = state3.create(np.arange(np.prod(size)))

puzzle3 = Problem(init_state, goal_state, actions, size)

### ================ ###
###      Search      ###
### ================ ###
print '===Puzzle 3==='
print '---BFS---'
solution = BREADTH_FIRST_SEARCH(puzzle3)
PRINT_SOLUTION(solution)

print '---DFS---'
solution = DEPTH_FIRST_SEARCH(puzzle3)
PRINT_SOLUTION(solution)

print '---DLS---'
solution = DEPTH_LIMITED_SEARCH_2(puzzle3, 10)
PRINT_SOLUTION(solution, True)


### ================ ###
### Prepare problems ###
### ================ ###
# puzzle 8
size = PZ8SZ
state8 = State(size)
init_state = state8.create([1,0,2,6,4,8,7,5,3]) # 11 stesp
init_state = state8.create([7,2,4,5,0,6,8,3,1])
#init_state = state8.create(np.random.permutation(np.arange(np.prod(size))))
goal_state = state8.create(np.arange(np.prod(size)))

puzzle8 = Problem(init_state, goal_state, actions, size)

### ================ ###
###      Search      ###
### ================ ###
print '===Puzzle 8==='
#print '---BFS---'
#solution = BREADTH_FIRST_SEARCH(puzzle8)
#PRINT_SOLUTION(solution)

#print '---UCS---'
#solution = UNIFORM_COST_SEARCH(puzzle8)
#PRINT_SOLUTION(solution)

#print '---DFS---'
#solution = DEPTH_FIRST_SEARCH(puzzle8)
#PRINT_SOLUTION(solution)

#print '---DLS---'
#solution = DEPTH_LIMITED_SEARCH_2(puzzle8, 12)
#PRINT_SOLUTION(solution, True)

print '---IDS---'
solution = ITERATIVE_DEEPENING_SEARCH(puzzle8)
PRINT_SOLUTION(solution, True)
