import sys
from collections import defaultdict

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    
    pthash = defaultdict(int)

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.pset = set()
        if p1.x == p2.x:
            for j in range(min(p1.y,p2.y), max(p1.y,p2.y)+1):
                self.pset.add((p1.x, j))
                Line.pthash[(p1.x, j)] += 1
        elif p1.y == p2.y:
            for i in range(min(p1.x,p2.x), max(p1.x,p2.x)+1):
                self.pset.add((i, p1.y))
                Line.pthash[(i, p1.y)] += 1
        else:
            if p1.x < p2.x:
                xstep = 1
            else:
                xstep = -1
            if p1.y < p2.y:
                ystep = 1
            else:
                ystep = -1
            x = p1.x
            y = p1.y
            while x != p2.x:
                Line.pthash[(x,y)] += 1
                x += xstep
                y += ystep
            Line.pthash[(x,y)] += 1


def part1(fname):
    with open(fname) as fp:
        linelist = []
        for line in fp:
            pt1,pt2 = line.split('->')
            p1 = Point(int(pt1.split(',')[0]), int(pt1.split(',')[1]))
            p2 = Point(int(pt2.split(',')[0]), int(pt2.split(',')[1]))
            if p1.x == p2.x or p1.y == p2.y:
                linelist.append(Line(p1, p2))
        counter = 0
        alist = list(Line.pthash.values())
        for val in alist:
            if val > 1:
                counter += 1

        return counter
                
            


def part2(fname):
    Line.pthash.clear()
    with open(fname) as fp:
        linelist = []
        for line in fp:
            pt1,pt2 = line.split('->')
            p1 = Point(int(pt1.split(',')[0]), int(pt1.split(',')[1]))
            p2 = Point(int(pt2.split(',')[0]), int(pt2.split(',')[1]))
            linelist.append(Line(p1, p2))
        counter = 0
        alist = list(Line.pthash.values())
        for val in alist:
            if val > 1:
                counter += 1

        return counter

def main():
    'main function'    
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
