from infrastructure import *
import numpy as np

'''
def STATE_TO_STR(state):
    return ''.join([str(x) for x in state.flatten().tolist()]) # [problem specified]
def NODE_TO_STR(node):
    return STATE_TO_STR(node.STATE)
'''

def CHILD_NODE(problem, parent, action):
    state = problem.RESULT(parent.STATE, action)
    if state == None:
        return None
    else:
        return Node(state, parent, action, parent.PATH_COST+problem.STEP_COST(parent.STATE, action))

def SOLUTION(node):
    current = node
    path = [current]
    while current.PARENT:
        current = current.PARENT
        path.append(current)
    path.reverse() # optional
    return path

def A_IN_B(A, B): # [problem specified]
    # state A in node list B
    if isinstance(B,list): # B is [explored]
        if len(B) == 0:
            return False
        return np.any([np.array_equal(A,x) for x in B])
    elif isinstance(B, QueueFIFO) or isinstance(B, QueueLIFO): # B is [frontier]
        if B.EMPTY():
            return False
        return np.any([np.array_equal(A,x.STATE) for x in B.GETALL()])
    elif isinstance(B, PriorityQueue): # B is [frontier]
        if B.EMPTY():
            return False
        return np.any([np.array_equal(A,x[1].STATE) for x in B.GETALL()])
    else: # Error
        print '*** Undefined type of B ***'
        return False

def GET_A_IN_B(A, B): # [problem specified]
    # TODO assert: isinstance(B, PriorityQueue)
    # TODO assert: not B.EMPTY()
    return B.GETALL()[np.where([np.array_equal(A,x[1].STATE) for x in B.GETALL()])[0]]

def REPLACE_A_IN_B(A, B): # [problem specified]
    # TODO assert: isinstance(B, PriorityQueue)
    # TODO assert: not B.EMPTY()
    (priority, A) = A
    B.GETALL()[np.where([np.array_equal(A.STATE,x[1].STATE) for x in B.GETALL()])[0]] = (priority, A)



def BREADTH_FIRST_SEARCH(problem):
    node = Node(problem.INITIAL_STATE, None, 'Start', 0) # root node
    if problem.GOAL_TEST(node.STATE):
        return SOLUTION(node)
    frontier = QueueFIFO()
    frontier.INSERT(node)
    explored = []

    while not frontier.EMPTY():
        node = frontier.POP()
        explored.append(node.STATE)
        for action in problem.ACTIONS(node.STATE):
            child = CHILD_NODE(problem, node, action)
            if not A_IN_B(child.STATE, explored) and not A_IN_B(child.STATE, frontier):
                if problem.GOAL_TEST(child.STATE):
                    return SOLUTION(child)
                frontier.INSERT(child)

    return None # failure

def UNIFORM_COST_SEARCH(problem):
    node = Node(problem.INITIAL_STATE, None, 'Start', 0) # root node
    frontier = PriorityQueue()
    frontier.INSERT(node.PATH_COST, node)
    explored = []

    while not frontier.EMPTY():
        node = frontier.POP()
        if problem.GOAL_TEST(node.STATE):
            return SOLUTION(node)
        explored.append(node.STATE)
        for action in problem.ACTIONS(node.STATE):
            child = CHILD_NODE(problem, node, action)
            if not A_IN_B(child.STATE, explored) and not A_IN_B(child.STATE, frontier):
                frontier.INSERT(child.PATH_COST, child)
            elif A_IN_B(child.STATE, frontier) and child.PATH_COST < GET_A_IN_B(child.STATE, frontier)[0]:
                REPLACE_A_IN_B((child.PATH_COST, child), frontier)

    return None # failure

def DEPTH_FIRST_SEARCH(problem):
    node = Node(problem.INITIAL_STATE, None, 'Start', 0) # root node
    if problem.GOAL_TEST(node.STATE):
        return SOLUTION(node)
    frontier = QueueLIFO()
    frontier.INSERT(node)
    explored = []

    while not frontier.EMPTY():
        node = frontier.POP()
        explored.append(node.STATE)
        for action in problem.ACTIONS(node.STATE):
            child = CHILD_NODE(problem, node, action)
            if not A_IN_B(child.STATE, explored) and not A_IN_B(child.STATE, frontier):
                if problem.GOAL_TEST(child.STATE):
                    return SOLUTION(child)
                frontier.INSERT(child)

    return None # failure

def DEPTH_LIMITED_SEARCH(problem, limit):
    node = Node(problem.INITIAL_STATE, None, 'Start', 0) # root node
    return RECURSIVE_DLS(node, problem, limit)

def DEPTH_LIMITED_SEARCH_2(problem, limit):
    node = Node(problem.INITIAL_STATE, None, 'Start', 0) # root node
    explored = []
    return RECURSIVE_DLS_2(node, problem, limit, explored)

cutoff = 0
def RECURSIVE_DLS(node, problem, limit):
    if problem.GOAL_TEST(node.STATE):
        return SOLUTION(node)
    elif limit == 0:
        return cutoff
    else:
        cutoff_occurred = False
        for action in problem.ACTIONS(node.STATE):
            child = CHILD_NODE(problem, node, action)
            result = RECURSIVE_DLS(child, problem, limit-1)
            if result == cutoff:
                cutoff_occurred = True
            elif result: # not result == None
                return result
        if cutoff_occurred:
            return cutoff
        else:
            return None # failure

def RECURSIVE_DLS_2(node, problem, limit, explored):
    explored.append(node.STATE)
    if problem.GOAL_TEST(node.STATE):
        return SOLUTION(node)
    elif limit == 0:
        return cutoff
    else:
        cutoff_occurred = False
        for action in problem.ACTIONS(node.STATE):
            child = CHILD_NODE(problem, node, action)
            if not A_IN_B(child.STATE, explored):
                result = RECURSIVE_DLS_2(child, problem, limit-1, explored)
                if result == cutoff:
                    cutoff_occurred = True
                elif result: # not result == None
                    return result
        if cutoff_occurred:
            return cutoff
        else:
            return None # failure

def ITERATIVE_DEEPENING_SEARCH(problem):
    depth = 0
    while True:
        print 'Current depth: ', depth
        result = DEPTH_LIMITED_SEARCH_2(problem, depth)
        if not result == cutoff:
            return result
        depth+=1
