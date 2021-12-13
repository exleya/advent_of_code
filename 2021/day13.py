import sys
from collections import defaultdict

class Paper:
    mx = 0
    my = 0

    def __init__(self):
        self.coordset = set()

    def add(self,x,y):
        self.coordset.add((x,y))
        Paper.mx = max(x, Paper.mx)
        Paper.my = max(y, Paper.my)

    def foldx(self, xval):
        toremove = []
        for point in self.coordset:
            if point[0] > xval:
                toremove.append(point)

        for point in toremove:
            self.coordset.remove(point)
            self.coordset.add((Paper.mx - point[0], point[1]))

        Paper.mx = Paper.mx // 2 - 1

    def foldy(self, yval):
        if Paper.my//2 != yval:
            print('sus')
            print(yval, Paper.my//2)
        else:
            toremove = []
            for point in self.coordset:
                if point[1] > yval:
                    toremove.append(point)

            for point in toremove:
                self.coordset.remove(point)
                self.coordset.add((point[0], Paper.my - point[1]))

            Paper.my = Paper.my // 2 - 1

    def __repr__(self):
        s = ''
        for j in range(Paper.my+1):
            for i in range(Paper.mx+1):
                if (i,j) in self.coordset:
                    s += '#'
                else:
                    s += '.'
            s += '\n'
        return s

def part1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        tp = Paper()
        for line in linelist:
            if ',' in line:
                pt = line.strip().split(',')
                tp.add(int(pt[0]), int(pt[1]))
            elif 'fold along x=' in line:
                xval = line.strip().split('=')[1]
                tp.foldx(int(xval))
                return len(tp.coordset)
            elif 'fold along y=' in line:
                yval = line.strip().split('=')[1]
                tp.foldy(int(yval))
                return len(tp.coordset)
        print(tp)

def part2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        tp = Paper()
        for line in linelist:
            if ',' in line:
                pt = line.strip().split(',')
                tp.add(int(pt[0]), int(pt[1]))
            elif 'fold along x=' in line:
                xval = line.strip().split('=')[1]
                tp.foldx(int(xval))
                #return len(tp.coordset)
            elif 'fold along y=' in line:
                yval = line.strip().split('=')[1]
                tp.foldy(int(yval))
                #return len(tp.coordset)
        print(tp)

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
