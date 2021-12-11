import sys
from collections import defaultdict

class Grid:
    neighbors = [(-1,-1), (-1,0), (-1,1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)]



    def __init__(self, lines):
        self.grid = {}
        for row in range(len(lines)):
            for col in range(10):
                self.grid[(row,col)] = int(lines[row][col])
        self.flashcount = 0

    def __repr__(self):
        s = ''
        for row in range(10):
            for col in range(10):
                s += str(self.grid[(row,col)])
            s+= '\n'
        return s

    def step(self):
        for k in self.grid:
            self.grid[k] += 1

        flash = True
        while flash == True:
            flash = False
            for k, v in self.grid.items():
                if 20 > v > 9:
                    self.flashcount += 1
                    self.grid[k] = 20
                    flash = True
                    for n in Grid.neighbors:
                        x, y = k[0] + n[0], k[1] + n[1]
                        if (x,y) in self.grid:
                            self.grid[(x,y)] += 1

        for k in self.grid:
            if self.grid[k] > 9:
                self.grid[k] = 0


def part1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        g = Grid(linelist)
        for i in range(100):
            g.step()
        return g.flashcount


def part2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        g = Grid(linelist)
        i = 1
        while True:
            g.step()
            if g.flashcount == 100:
                return i
            g.flashcount = 0
            i += 1

        print(g.flashcount)

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
