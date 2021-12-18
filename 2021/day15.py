import sys
from collections import defaultdict
import queue as Q
import heapq

'''
Node, memoize, PriorityQueue and search blatantly stolen from
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
        return self.state < node.state

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



def neighbors(location):
    x,y = location
    rlist = []
    if x > 0:
        rlist.append((x-1, y))
    if x < Cave.mx:
        rlist.append((x+1, y))
    if y > 0:
        rlist.append((x, y-1))
    if y < Cave.my:
        rlist.append((x, y+1))
    return rlist

class Cave2:
    mx = 0
    my = 0

    def __init__(self):
        self.map = {}
        self.riskmap = {}

    def addloc(self, x, y, val):
        self.map[(x,y)] = val
        Cave2.mx = max(Cave2.mx, x)
        Cave2.my = max(Cave2.my, y)

    def expand(self):
        self.newmap = {}
        for i in range(5):
            for j in range(5):
                for k,v in self.map.items():
                    v = v + i + j
                    if v > 9: v -= 9
                    #print((k[0] * j, k[1] * i))
                    self.newmap[(k[0] + (Cave2.mx+1)*j, k[1] + (Cave2.my+1)*i)] = v
        self.map = self.newmap
        Cave2.mx = Cave2.mx * 5 + 4
        Cave2.my = Cave2.my * 5 + 4

    def __repr__(self):
        s = ''
        for y in range(Cave2.my+1):
            for x in range(Cave2.mx+1):
                s += str(self.map[(x,y)])
            s += '\n'
        return s

    def h(self, loc):
        return (Cave2.mx - loc[0]) + (Cave2.my - loc[1])

    def neighbors(self,location):
        x,y = location
        rlist = []
        if x > 0:
            rlist.append((x-1, y))
        if x < Cave2.mx:
            rlist.append((x+1, y))
        if y > 0:
            rlist.append((x, y-1))
        if y < Cave2.my:
            rlist.append((x, y+1))
        return rlist

    def findpath(self):
        queue = PriorityQueue()
        queue.put((0,0,0,0,[0,0]))
        visited = set()
        inqmap = {(0,0) : self.h((0,0))}

        while not queue.empty():
            node = queue.get()
            loc = node[1], node[2]
            if loc == (Cave2.mx, Cave2.my):
                return node[3]
            else:
                visited.add(loc)
                for neighbor in self.neighbors(loc):
                    g = self.map[neighbor] + node[3]
                    f = self.h(neighbor) + g
                    if neighbor not in visited or f < inqmap[neighbor]:
                        #print(f)
                        queue.put((f,
                            neighbor[0],
                            neighbor[1], g, node[4] + [neighbor]))
                        inqmap[neighbor] = f

    def xymonotonicpath(self):
        self.hmap = {}
        self.hmax = 0
        self.hmap[(0,0)] = 0
        for i in range(1, Cave2.my+1):
            self.hmap[(0,i)] = self.map[(0,i)] + self.hmap[(0,i-1)]
        for j in range(1, Cave2.mx+1):
            self.hmap[(j,0)] = self.map[(j,0)] + self.hmap[(j-1,0)]

        for i in range(1, Cave2.my+1):
            for j in range(1, Cave2.my+1):
                self.hmap[(j,i)] = self.map[(j,i)] + min(
                    self.hmap[(j-1, i)], self.hmap[(j, i-1)])

        for val in self.hmap.values():
            self.hmax = max(val, self.hmax)

    def findpathbh(self):
        f = lambda n: n.path_cost
        f = memoize(f, 'f')
        node = Node((0,0))
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        while frontier:
            node = frontier.pop()
            if node.state == (Cave2.mx, Cave2.my):
                return node.path_cost
            explored.add(node.state)
            for neighbor in self.neighbors(node.state):
                child = Node(neighbor, path_cost = node.path_cost + self.map[neighbor])
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                # elif child in frontier:
                #     if f(child) < frontier[child]:
                #         del frontier[child]
                #         frontier.append(child)
        return None


class Cave:
    mx = 0
    my = 0

    def __init__(self):
        self.map = {}
        self.riskmap = {}

    def addloc(self, x, y, val):
        self.map[(x,y)] = val
        Cave.mx = max(Cave.mx, x)
        Cave.my = max(Cave.my, y)

    def h(self, loc):
        return (Cave.mx - loc[0]) + (Cave.my - loc[1])


    def findpath(self):
        queue = Q.PriorityQueue()
        queue.put((0,0,0,0))
        visited = set()
        inqmap = {(0,0) : 0}

        while not queue.empty():
            node = queue.get()
            loc = node[1], node[2]
            if loc == (Cave.mx, Cave.my):
                return node[3]
            else:
                visited.add(loc)
                for neighbor in neighbors(loc):
                    g = self.map[neighbor] + node[3]
                    f = self.h(neighbor) + g
                    if neighbor not in visited or f < inqmap[neighbor]:
                        queue.put((f,
                            neighbor[0],
                            neighbor[1], g))
                        inqmap[neighbor] = f



    def __repr__(self):
        s = ''
        for y in range(Cave.my+1):
            for x in range(Cave.mx+1):
                s += str(self.map[(x,y)])
            s += '\n'
        return s

def part1(fname):
    with open(fname) as fp:
        c = Cave()
        linelist = fp.readlines()
        for y in range(len(linelist)):
            for x in range(len(linelist[y])-1):
                c.addloc(x,y,int(linelist[y][x]))
        return c.findpath()

def part2(fname):
    with open(fname) as fp:
        c = Cave2()
        linelist = fp.readlines()
        for y in range(len(linelist)):
            for x in range(len(linelist[y])-1):
                c.addloc(x,y,int(linelist[y][x]))
        c.expand()
        #print('a*:')
        #print(c.findpath())
        #c.xymonotonicpath()
        #print('a* bh:')
        return c.findpathbh()



def main():
    'main function'
    #print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
