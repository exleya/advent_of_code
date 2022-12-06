import sys
from collections import defaultdict

import queue as Q
import heapq

'''
Node, PriorityQueue and search blatantly stolen from
AI: A Modern Approach
Python code
(aima.cs.berkeley.edu)
'''


def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.path_cost + h(self.state) < node.path_cost +h(node.state)

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)



class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)



def legit_dest(mover, room, roomindex):
    #print(mover, room, roomindex)
    #print(len(room))
    answer = ('ABCD'.index(mover) == roomindex and
            (len(room) == 0 or
                (len(room) == 1 and room[0] == mover)))
    #print(answer)
    return answer

class State:
    stepcost = {'A':1, 'B':10,'C':100,'D':1000}

    def __hash__(self):
        return hash(self.__repr__())

    def __init__(self, room1, room2, room3, room4):
        # each room is a string of two things
        self.rooms = [None] * 4
        # self.rooms[0] = Room(room1[0], room1[1])
        # self.rooms[1] = Room(room2[0], room2[1])
        # self.rooms[2] = Room(room3[0], room3[1])
        # self.rooms[3] = Room(room4[0], room4[1])
        self.rooms[0] = room1
        self.rooms[1] = room2
        self.rooms[2] = room3
        self.rooms[3] = room4
        self.hallway = '.' * 11

    def solution(self):
        return (self.rooms[0] == 'AA' and
                self.rooms[1] == 'BB' and
                self.rooms[2] == 'CC' and
                self.rooms[3] == 'DD')

    def __repr__(self):
        s = '#############\n'
        s += '#' + self.hallway + '#\n'
        s += '###'
        for i in range(len(self.rooms)):
            if len(self.rooms[i]) == 2:
                s += self.rooms[i][0] + '#'
            else:
                s += '.#'
        s += '##\n  #'
        for i in range(len(self.rooms)):
            if len(self.rooms[i]) == 2:
                s += self.rooms[i][1] + '#'
            elif len(self.rooms[i]) == 1:
                s += self.rooms[i][0] + '#'
            else:
                s += '.#'
        s += '\n'
        s += '  #########\n'
        return s

class AmphipodProblem:
    def actions(foo, self):
        '''actions from current state'''
        actions = []
        # first check hallway locations
        for i in range(len(self.hallway)):
            if self.hallway[i] != '.':
                mover = self.hallway[i]
                #print(mover)
                pathleft = range(i-1,1,-1)
                pathright = range(i+1,9)
                for j in pathleft:
                    if self.hallway[j] != '.':
                        break
                    if j in [2,4,6,8] and legit_dest(mover, self.rooms[j//2-1], j//2-1):
                        steps = abs(i - j) + 2 - len(self.rooms[j//2-1])
                        actions.append((i, 20 + j//2 - 1, steps * self.stepcost[self.hallway[i]]))
                for j in pathright:
                    if self.hallway[j] != '.':
                        break
                    if j in [2,4,6,8] and legit_dest(mover, self.rooms[j//2-1], j//2-1):
                        steps = abs(i - j) + 2 - len(self.rooms[j//2-1])
                        actions.append((i, 20 + j//2 - 1, steps * self.stepcost[self.hallway[i]]))
        # then check rooms
        for i in range(len(self.rooms)):
            if len(self.rooms[i]) > 0:
                mover = self.rooms[i][0]
                if 'ABCD'.index(mover) == i and len(self.rooms[i]) == 1:
                    break
                if ('ABCD'.index(mover) == i and len(self.rooms[i]) == 2 and
                    self.rooms[i][0] == self.rooms[i][1]):
                    break
                roomexit = (i + 1) * 2
                #print(roomexit)
                pathleft = range(roomexit,-1,-1)
                pathright = range(roomexit,11)
                for j in pathleft:
                    if self.hallway[j] != '.':
                        break
                    if j not in [2,4,6,8]:
                        steps = abs(roomexit-j) + 2 - len(self.rooms[i])
                        actions.append((20 + i, j, steps*self.stepcost[mover]))
                    else:
                        roomeindex = (j // 2) - 1
                        steps = abs(roomexit-j) + 2 - len(self.rooms[i]) + 2 - len(self.rooms[roomeindex])
                        if legit_dest(mover, self.rooms[roomeindex], roomeindex):
                            actions.append((20+i, 20+roomeindex, steps*self.stepcost[mover]))
                for j in pathright:
                    if self.hallway[j] != '.':
                        break
                    if j not in [2,4,6,8]:
                        steps = abs(roomexit-j) + 2 - len(self.rooms[i])
                        actions.append((20 + i, j, steps*self.stepcost[self.rooms[i][0]]))
                    else:
                        roomeindex = (j - 1) // 2
                        steps = abs(roomexit-j) + 2 - len(self.rooms[i]) + 2 - len(self.rooms[roomeindex])
                        if legit_dest(mover, self.rooms[roomeindex], roomeindex):
                            actions.append((20+i, 20+roomeindex, steps*self.stepcost[mover]))
        return actions

    def result(foo, self, action):
        s2 = State(self.rooms[0], self.rooms[1], self.rooms[2], self.rooms[3])
        if action[0] >= 20:
            roomfrom = action[0] - 20
            mover = s2.rooms[roomfrom][0]
            s2.hallway = self.hallway[:action[1]] + mover + self.hallway[action[1]+1:]
            s2.rooms[roomfrom] = s2.rooms[roomfrom][1:]
        else:
            roomto = action[1] - 20
            mover = self.hallway[action[0]]
            s2.hallway = self.hallway[:action[0]] + '.' + self.hallway[action[0]+1:]
            s2.rooms[roomto] = mover + s2.rooms[roomto]
        return s2

    def path_cost(self, prev_path_cost, cur_state, action, next_state):
        return prev_path_cost + action[2]


def h(state):
    '''heuristic for given state'''

    return 0

def part1():
    ap = AmphipodProblem()
    f = lambda n: n.path_cost + h(n.state)
    f = memoize(f, 'f')
    b = State('BA', 'CD', 'BC', 'DA')
    init = Node(b)
    frontier = PriorityQueue('min', f)
    frontier.append(init)
    explored = set()
    while frontier:
        # print(frontier.heap)
        # input()
        node = frontier.pop()
        if node.state.solution():
            return node.path_cost, node.solution()
        explored.add(node.state)
        for child in node.expand(ap):
            #child = Node(neighbor, path_cost = node.path_cost + self.map[neighbor])
            if child.depth < 11 and child.state not in explored and child not in frontier:
                frontier.append(child)


    # print(b)
    # print(b.actions())
    # c = b.result(b.actions()[-1])
    # print(c)
    # d = c.result(c.actions()[-3])
    # print(d)
    # print(d.actions())
    # for a in d.actions():
    #     f = d.result(a)
    #     print(f)
    #     input()


def part2():
    pass

def main():
    'main function'
    print(part1())
    print(part2())

if __name__ == '__main__':
    main()
