import sys
from collections import defaultdict

# witness my embarassing code!
class SeaFloor:
    def __init__(self, fname):
        self.vset = set()
        self.rset = set()
        with open(fname) as fp:
            lines = fp.readlines()
            self.ymax = len(lines)
            self.xmax = len(lines[0].strip())
            for j in range(len(lines)):
                for i in range(len(lines[j].strip())):
                    if lines[j][i] == 'v':
                        self.vset.add((i,j))
                    elif lines[j][i] == '>':
                        self.rset.add((i,j))


    def __repr__(self):
        s = ''
        for j in range(self.ymax):
            for i in range(self.xmax):
                if (i,j) in self.vset:
                    s += 'v'
                elif (i,j) in self.rset:
                    s += '>'
                else:
                    s += '.'
            s+= '\n'
        return s

    def step(self):
        '''return True if changed'''
        changed = False
        occupiedset = self.vset | self.rset
        newvset = set()
        newrset = set()
        for loc in self.rset:
            x = (loc[0] + 1) % self.xmax
            if (x, loc[1]) in occupiedset:
                newrset.add(loc)
            else:
                changed = True
                newrset.add((x, loc[1]))

        occupiedset = self.vset | newrset
        for loc in self.vset:
            y = (loc[1] + 1) % self.ymax
            if (loc[0], y) in occupiedset:
                newvset.add(loc)
            else:
                changed = True
                newvset.add((loc[0], y))

        self.vset = newvset
        self.rset = newrset
        return changed


def part1(floor):
    i = 1
    while floor.step():
        i += 1
    return i

def part2(floor):

    pass



def main():
    'main function'
    floor = SeaFloor(sys.argv[1])
    print(part1(floor))
    print(part2(floor))

if __name__ == '__main__':
    main()
