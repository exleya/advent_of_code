import sys
from collections import defaultdict


class Grid:
    def __init__(self):
        self.mincol = 0
        self.maxcol = -1
        self.minrow = 0
        self.maxrow = -1
        self.vertices = {}

    def set(self, label, height, dist = 9999):
        self.maxcol = max(label[0], self.maxcol)
        self.maxrow = max(label[1], self.maxrow)
        self.vertices[label] = height, dist

    def get_neighbors(self, label):
        n = []
        myh = self.vertices[label][0]
        for d in ((0,1), (1,0), (-1,0), (0,-1)):
            ln = (label[0]+d[0], label[1]+d[1])
            if (self.mincol <= label[0]+d[0] <= self.maxcol and
                self.minrow <= label[1]+d[1] <= self.maxrow and
                myh - self.vertices[ln][0] <= 1):
                n.append(ln)
        return n

    #def get(self, label)

def setvals(g, queue):
    while len(queue) > 0:
        location = queue.pop(0)
        mydist = g.vertices[location][1]
        for n in g.get_neighbors(location):
            if g.vertices[n][1] > mydist+1:
                g.vertices[n] = (g.vertices[n][0], mydist+1)
                queue.append(n)

def part1(fname):
    g = Grid()
    with open(fname) as fp:
        lines = fp.readlines()
        #print(lines)
        for col in range(len(lines[0]) - 1):
            for row in range(len(lines)):
                #print(col,row)
                if lines[row][col] == 'S':
                    start = (col, row)
                    g.set((col,row), ord('a'))
                elif lines[row][col] == 'E':
                    end = (col, row)
                    g.set((col,row), ord('z'), 0)
                else:
                    g.set((col,row), ord(lines[row][col]))

        setvals(g, [end])
    #print(g.vertices)
    return g.vertices[start][1]

def part2(fname):
    g = Grid()
    with open(fname) as fp:
        lines = fp.readlines()
        #print(lines)
        for col in range(len(lines[0]) - 1):
            for row in range(len(lines)):
                #print(col,row)
                if lines[row][col] == 'S':
                    start = (col, row)
                    g.set((col,row), ord('a'))
                elif lines[row][col] == 'E':
                    end = (col, row)
                    g.set((col,row), ord('z'), 0)
                else:
                    g.set((col,row), ord(lines[row][col]))

        setvals(g, [end])
    mina = start
    for a in g.vertices:
        if g.vertices[a][0] == ord('a'):
            if g.vertices[a][1]< g.vertices[mina][1]:
                mina = a

    return g.vertices[mina][1]

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
