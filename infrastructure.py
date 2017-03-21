class Node:
    def __init__(self, STATE, PARENT, ACTION, PATH_COST):
        self.STATE = STATE
        self.PARENT = PARENT
        self.ACTION = ACTION
        self.PATH_COST = PATH_COST

##
from collections import deque as dq

class QueueFIFO:
    def __init__(self):
        self.elements = dq()
    def EMPTY(self):
        return len(self.elements) == 0
    def INSERT(self, element):
        self.elements.append(element)
    def POP(self):
        return self.elements.popleft() # FIFO
    def LEN(self):
        return len(self.elements)
    def GETALL(self):
        return self.elements

class QueueLIFO:
    def __init__(self):
        self.elements = dq()
    def EMPTY(self):
        return len(self.elements) == 0
    def INSERT(self, element):
        self.elements.append(element)
    def POP(self):
        return self.elements.pop() # LIFO
    def LEN(self):
        return len(self.elements)
    def GETALL(self):
        return self.elements

import heapq as hq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    def EMPTY(self):
        return len(self.elements) == 0
    def INSERT(self, priority, item):
        hq.heappush(self.elements, (priority, item))
    def POP(self):
        return hq.heappop(self.elements)[1]
    def GETALL(self):
        return self.elements