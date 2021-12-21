import sys
from collections import defaultdict

class Die:
    def __init__(self):
        self.rollcount = 0
        self.val = 1

    def roll3(self):
        self.rollcount += 3
        val = 3 * (self.val + 1)
        self.val += 3
        return val

class DiracDie:

    def roll3(self, startloc):
        return {
            ((startloc + 3) % 10):1,
            ((startloc + 4) % 10):3,
            ((startloc + 5) % 10):6,
            ((startloc + 6) % 10):7,
            ((startloc + 7) % 10):6,
            ((startloc + 8) % 10):3,
            ((startloc + 9) % 10):1
        }

class MV:
    def __init__(self, p1loc, p2loc):
        # counter: 4-tuple of p1loc,p1score,p2loc,p2score: count
        self.counter = {(p1loc-1, 0, p2loc-1, 0): 1}
        self.turn = 1
        self.p1wins = 0
        self.p2wins = 0

    def take_turn(self):
        newc = {}
        d = DiracDie()
        if self.turn == 1:
            for universe, count in self.counter.items():
                p1loc = universe[0]
                result = d.roll3(p1loc)
                for newloc, count2 in result.items():
                    newscore = universe[1] + newloc+1
                    if newscore >= 21:
                        self.p1wins += (count2*count)
                    else:
                        newtup = (newloc, newscore, universe[2], universe[3])
                        newc[newtup] = newc.get(newtup, 0) + (count2*count)
        else:
            for universe, count in self.counter.items():
                p2loc = universe[2]
                result = d.roll3(p2loc)
                for newloc, count2 in result.items():
                    newscore = universe[3] + newloc+1
                    if newscore >= 21:
                        self.p2wins += (count2*count)
                    else:
                        newtup = (universe[0], universe[1], newloc, newscore)
                        newc[newtup] = newc.get(newtup, 0) + (count2*count)

        self.counter = newc
        self.turn = 3 - self.turn

def part1(p1start, p2start):
    p1score, p2score = 0,0
    p1loc, p2loc = p1start-1, p2start-1
    d = Die()
    while True:
        p1loc = (p1loc + d.roll3()) % 10
        p1score += (p1loc+1)
        if p1score >= 1000:
            return p2score * d.rollcount

        p2loc = (p2loc + d.roll3()) % 10
        p2score += (p2loc+1)
        if p2score >= 1000:
            return p1score * d.rollcount


def part2(p1start, p2start):
    multiverse = MV(p1start, p2start)
    multiverse.take_turn()
    while len(multiverse.counter) > 0:
        multiverse.take_turn()
    return max(multiverse.p1wins, multiverse.p2wins)

def main():
    'main function'
    #print(part1(4,8))
    print(part1(9,3))
    #print(part2(4,8))
    print(part2(9,3))

if __name__ == '__main__':
    main()
