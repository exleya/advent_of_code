import sys
from collections import defaultdict
import numpy as np

class Scanner:
    def __init__(self, num):
        self.num = num
        self.beacon_set = set()

    def add_beacon(self, x,y,z):
        self.beacon_set.add((x,y,z))

    def set_matrix(self):
        self.b_matrix = np.matrix(list(self.beacon_set))

    def translate_test(self, other):
        '''test if we can translate other scanner
        on to this one, return the translation if so
        '''
        tcount = defaultdict(int)
        for myb in self.b_matrix:
            for otherb in other.b_matrix:
                translation = myb - otherb
                tcount[tuple(translation.tolist()[0])] += 1
                if tcount[tuple(translation.tolist()[0])] >= 12:
                    # print('Scanner ' + other.num + ' maps to ' + self.num)
                    # print(' with translation ' + str(translation))
                    return translation

    def rotate(self, rmatrix):
        '''return a copy of this scanner with
        rotation performed'''
        s = Scanner(self.num)
        s.beacon_set = self.beacon_set.copy()
        s.b_matrix = (rmatrix * self.b_matrix.transpose()).transpose()
        return s

ROTATIONS = None

def rot_list():
    global ROTATIONS
    if ROTATIONS != None:
        return ROTATIONS

    A = [np.matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]]),
        np.matrix([[0, 1, 0],[0, 0, 1],[1, 0, 0]]),
        np.matrix([[0, 0, 1],[1, 0, 0],[0, 1, 0]])]
    B = [np.matrix([[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]]),
        np.matrix([[-1, 0, 0],[ 0,-1, 0],[ 0, 0, 1]]),
        np.matrix([[-1, 0, 0],[ 0, 1, 0],[ 0, 0,-1]]),
        np.matrix([[ 1, 0, 0],[ 0,-1, 0],[ 0, 0,-1]])]
    C = [np.matrix([[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]]),
        np.matrix([[ 0, 0,-1],[ 0,-1, 0],[-1, 0, 0]])]
    ROTATIONS = []
    for a in A:
        for b in B:
            for c in C:
                ROTATIONS.append(a*b*c)
    return ROTATIONS


def part1and2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        scanners = []
        s = None
        for line in linelist:
            if 'scanner' in line:
                if s != None:
                    s.set_matrix()
                    scanners.append(s)
                num = line.split()[2]
                s = Scanner(num)
            elif ',' in line:
                x, y, z = line.strip().split(',')
                s.add_beacon(int(x), int(y), int(z))
        s.set_matrix()
        scanners.append(s)

    transformlist = []
    s0 = scanners.pop(0)

    while len(scanners) > 0:
        #print("current: " + str(current))
        for i in range(len(scanners)-1, -1,-1):
            print(i)
            for r in rot_list():
                rot_s = scanners[i].rotate(r)
                t = s0.translate_test(rot_s)
                if t is not None:
                    for beacon in rot_s.b_matrix:
                        tb = beacon+t
                        s0.add_beacon(tb[0,0], tb[0,1], tb[0,2])
                    transformlist.append(t.tolist()[0])
                    s0.set_matrix()
                    scanners.pop(i)
                    break

    return len(s0.beacon_set), largest_dist(transformlist)

def largest_dist(lst):
    md = 0
    for a in lst:
        for b in lst:
            if a != b:
                dist = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
                md = max(md, dist)
    return md

def main():
    'main function'
    print(part1and2(sys.argv[1]))
    #print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
