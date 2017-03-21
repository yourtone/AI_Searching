from Search import *
import numpy as np

PZ3SZ = (2,2)
PZ8SZ = (3,3)

class State: # [problem specified]
    def __init__(self, SIZE):
        self.SIZE = SIZE
    def create(self, arr):
        return np.uint8(np.resize(np.array(arr),self.SIZE))

'''
def create_state(arr, size=PZ8SZ):
    return np.uint8(np.resize(np.array(arr),size))
'''

class Problem:
    def __init__(self, INITIAL_STATE, GOAL_STATE, ALL_ACTIONS, **OPTIONS):
        self.INITIAL_STATE = INITIAL_STATE
        self.GOAL_STATE = GOAL_STATE
        self.ALL_ACTIONS = ALL_ACTIONS
        if 'size' in OPTIONS.keys(): # [problem specified]
            self.SIZE = OPTIONS['size']
    def ACTIONS(self, state): # [problem specified]
        l1  = np.where(state==0) # l1: location
        # TODO: assert l1 has values
        l1 = np.array([l1[0][0],l1[1][0]])
        feaaction = [] # feasible actions
        for action, actposi in self.ALL_ACTIONS.iteritems():
            l2 = l1 + actposi # l2: new_location
            if l2[0] in range(self.SIZE[0]) and l2[1] in range(self.SIZE[1]):
                feaaction.append(action)
        if len(feaaction)==0:
            return []
        else:
            return feaaction
    def RESULT(self, p_state, action): # [problem specified]
        l1 = np.where(p_state==0) # l1: location
        # TODO: assert l1 has values
        l1 = np.array([l1[0][0],l1[1][0]])
        l2 = l1 + self.ALL_ACTIONS[action] # l2: new_location
        if l2[0] not in range(self.SIZE[0]) or l2[1] not in range(self.SIZE[1]):
            return None
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
#init_state = state3.create([1,0,2,3]) # BFS & DFS need 1 step, DLS needs 11 steps
#init_state = state3.create([0,2,3,1]) # BFS & DFS need 4 steps, DLS needs 8 steps
#init_state = state3.create([1,3,0,2]) # BFS & DLS need 3 steps, DFS needs 9 steps
#init_state = state3.create([3,1,2,0]) # failure
#init_state = state3.create([3,0,1,2])
init_state = state3.create(np.random.permutation(np.arange(np.prod(size))))
goal_state = state3.create(np.arange(np.prod(size)))

puzzle3 = Problem(init_state, goal_state, actions, size=size)

### ================ ###
###      Search      ###
### ================ ###
'''
print '===Puzzle 3==='
print '---BFS---'
solution = BREADTH_FIRST_SEARCH(puzzle3)
PRINT_SOLUTION(solution)

print '---DFS---'
solution = DEPTH_FIRST_SEARCH(puzzle3)
PRINT_SOLUTION(solution)

print '---DLS---'
solution = DEPTH_LIMITED_SEARCH_2(puzzle3, 15) # compare BFS and DLS for [3,0,1,2]
PRINT_SOLUTION(solution, True)
'''

'''
state_list = []
totalNum = np.prod(size)
for l1 in range(totalNum):
    state_list.append(l1)
    for l2 in range(totalNum):
        if l2 in state_list:
            continue
        state_list.append(l2)
        for l3 in range(totalNum):
            if l3 in state_list:
                continue
            state_list.append(l3)
            for l4 in range(totalNum):
                if l4 in state_list:
                    continue
                state_list.append(l4)
                init_state = state3.create([l1,l2,l3,l4])
                print init_state
                puzzle3 = Problem(init_state, goal_state, actions, size=size)
                print '---BFS---'
                solution = BREADTH_FIRST_SEARCH(puzzle3)
                PRINT_SOLUTION(solution)

                print '---DFS---'
                solution = DEPTH_FIRST_SEARCH(puzzle3)
                PRINT_SOLUTION(solution)

                print '---DLS---'
                solution = DEPTH_LIMITED_SEARCH_2(puzzle3, 15)
                PRINT_SOLUTION(solution, True)
                raw_input()
                state_list.pop()
            state_list.pop()
        state_list.pop()
    state_list.pop()
'''


### ================ ###
### Prepare problems ###
### ================ ###
# puzzle 8
size = PZ8SZ
state8 = State(size)
#init_state = state8.create([7,2,4,5,0,6,8,3,1])
#init_state = state8.create([1,2,0,3,4,5,6,7,8]) # 2 steps
#init_state = state8.create([1,2,5,3,4,0,6,7,8]) # 3 steps
init_state = state8.create([3,1,2,4,5,8,6,0,7]) # 5 steps
#init_state = state8.create([3,1,2,6,4,8,0,5,7]) # 8 steps
#init_state = state8.create([3,2,5,4,1,0,6,7,8]) # 5 steps
#init_state = state8.create([1,0,2,6,4,8,7,5,3]) # 11 stesp
#init_state = state8.create([0,2,7,3,8,1,4,6,5]) # 14 steps
#init_state = state8.create([1,0,3,2,4,8,7,5,6]) #  steps
#init_state = state8.create(np.random.permutation(np.arange(np.prod(size))))
goal_state = state8.create(np.arange(np.prod(size)))

puzzle8 = Problem(init_state, goal_state, actions, size=size)

### ================ ###
###      Search      ###
### ================ ###
print '===Puzzle 8==='
print '---BFS---'
solution = BREADTH_FIRST_SEARCH(puzzle8)
PRINT_SOLUTION(solution)

#print '---DFS---'
#solution = DEPTH_FIRST_SEARCH(puzzle8)
#PRINT_SOLUTION(solution)

print '---DLS---'
solution = DEPTH_LIMITED_SEARCH_2(puzzle8, 12) #compare 10 and 8 for [3,1,2,6,4,8,0,5,7]
PRINT_SOLUTION(solution, True)


'''
print '---A*---'

'''