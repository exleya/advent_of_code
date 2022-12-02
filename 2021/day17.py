import sys
from collections import defaultdict


class Probe:
    txmin = 20
    txmax = 30
    tymin = -10
    tymax = -5

    def __init__(self, xv, yv):
        self.x = 0
        self.y = 0
        self.dx = xv
        self.dy = yv
        self.ymax = 0

    def step(self):
        self.x += self.dx
        self.y += self.dy
        self.ymax = max(self.y, self.ymax)
        self.dx = max(0, self.dx - 1)
        self.dy -= 1

    def in_target(self):
        if Probe.txmin <= self.x <= Probe.txmax and Probe.tymin <= self.y <= Probe.tymax:
            return True
        return False

    def past_target(self):
        if self.x > Probe.txmax or self.y < Probe.tymin:
            return True
        return False

    def __repr__(self):
        return "({x}[{dx}], {y}[{dy}])".format(
            x=self.x,dx=self.dx,y=self.y,dy=self.dy)

def part1():
    xvals = []
    for i in range(Probe.txmax):
        if Probe.txmin <= (i * (i+1) // 2) <= Probe.txmax:
            xvals.append(i)
    y = 0
    hits = []
    while y < 200:
        for x in xvals:
            p = Probe(x,y)
            while not p.past_target():
                if p.in_target():
                    hits.append((p.ymax, x, y))
                p.step()
                #print(p)
                #input()
        y+=1
    return sorted(hits)[-1][0]



def part2():
    xvals = []
    for i in range(Probe.txmax+1):
        xvals.append(i)
    y = Probe.tymin
    hits = set()
    while y < 200:
        for x in xvals:
            p = Probe(x,y)
            while not p.past_target():
                if p.in_target():
                    hits.add((x, y))
                p.step()
                #print(p)
                #input()
        y+=1
    #print(sorted(list(hits)))
    return len(hits)




def main():
    'main function'
    Probe.txmin = 85
    Probe.txmax = 145
    Probe.tymin = -163
    Probe.tymax = -108
    print(part1())
    print(part2())

if __name__ == '__main__':
    main()
