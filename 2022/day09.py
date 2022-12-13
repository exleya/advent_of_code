import sys
from collections import defaultdict

class RopeGrid:
    def __init__(self, knots = 2):
        self.hloc = (0,0)
        self.tloc = (0,0)
        self.knotloc = [(0,0) for i in range(knots)]
        self.tailvisit = set()

    def print_grid(self):
        for row in range(5, -1, -1):
            for col in range(7):
                if (col,row) in self.knotloc:
                    print(self.knotloc.index((col,row)), end ='')
                else:
                    print('.', end='')
            print()


    def run_movement(self, movement):
        dir, num = movement.split()
        num = int(num)
        dir_dict = {'R':(1,0), 'U':(0,1), 'L':(-1,0), 'D':(0,-1) }
        dir_vec = dir_dict[dir]
        for i in range(num):
            self.knotloc[0] = self.knotloc[0][0] + dir_vec[0], self.knotloc[0][1] + dir_vec[1]
            for j in range(1, len(self.knotloc)):
                dx, dy = self.knotloc[j-1][0] - self.knotloc[j][0], self.knotloc[j-1][1] - self.knotloc[j][1]
                if abs(dx) > 1 and dy == 0:
                    self.knotloc[j] = self.knotloc[j][0] + dx//abs(dx), self.knotloc[j][1]
                elif abs(dy) > 1 and dx == 0:
                    self.knotloc[j] = self.knotloc[j][0], self.knotloc[j][1] + dy // abs(dy)
                elif abs(dx) > 1 and abs(dy) == 1:
                    self.knotloc[j] = self.knotloc[j][0] + dx // abs(dx), self.knotloc[j][1] + dy // abs(dy)
                elif abs(dx) == 1 and abs(dy) > 1:
                    self.knotloc[j] = self.knotloc[j][0] + dx // abs(dx), self.knotloc[j][1] + dy // abs(dy)
                elif abs(dx) > 1 and abs(dy) > 1:
                    self.knotloc[j] = self.knotloc[j][0] + dx // abs(dx), self.knotloc[j][1] + dy // abs(dy)
            self.tailvisit.add(self.knotloc[-1])

                # self.hloc = self.hloc[0] + dir_vec[0], self.hloc[1] + dir_vec[1]
                # dx, dy = self.hloc[0] - self.tloc[0], self.hloc[1] - self.tloc[1]
                # if abs(dx) > 1 and dy == 0:
                #     self.tloc = self.tloc[0] + dx//abs(dx), self.tloc[1]
                # elif abs(dy) > 1 and dx == 0:
                #     self.tloc = self.tloc[0], self.tloc[1] + dy // abs(dy)
                # elif abs(dx) > 1 and abs(dy) == 1:
                #     self.tloc = self.tloc[0] + dx // abs(dx), self.tloc[1] + dy // abs(dy)
                # elif abs(dx) == 1 and abs(dy) > 1:
                #     self.tloc = self.tloc[0] + dx // abs(dx), self.tloc[1] + dy // abs(dy)
                # self.tailvisit.add(self.tloc)

def part1(fname):
    with open(fname) as fp:
        r = RopeGrid()
        for line in fp:
            #print(line.strip())
            r.run_movement(line.strip())
            #print(r.tailvisit)
        return len(r.tailvisit)


def part2(fname):
    with open(fname) as fp:
        r = RopeGrid(10)
        for line in fp:
            #print(line.strip())
            r.run_movement(line.strip())
            #print(r.tailvisit)
            #r.print_grid()
            #print()
        return len(r.tailvisit)

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
