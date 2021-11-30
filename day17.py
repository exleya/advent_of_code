import sys

class TimeCube:
    '''no longer a lifecube it is a TIMECUBE
    see timecube.com for details
    '''
    OFFSETS = []

    def __init__(self, initmap):
        lines = initmap.split()

        self.xrange = range(0, len(lines[0]))
        self.yrange = range(0, len(lines))
        self.zrange = range(0,1)
        self.wrange = range(0,1)

        self.lcdict = {}
        for i in self.xrange:
            for j in self.yrange:
                self.lcdict[(i, j, 0, 0)] = lines[j][i]

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for k in (-1, 0, 1):
                    for l in (-1, 0, 1):
                        TimeCube.OFFSETS.append((i,j,k,l))
        TimeCube.OFFSETS.remove((0,0,0,0))

    def print(self):
        for l in self.wrange:
            for k in self.zrange:
                print(f"z={k}, w={l}")

                for i in self.xrange:
                    for j in self.yrange:
                        print(self.lcdict[(i, j, k, l)], end ='')
                    print()

    def active_count(self):
        return list(self.lcdict.values()).count('#')

    def nextpop(self, location):
        activecount = 0
        for off in TimeCube.OFFSETS:
            x = location[0] + off[0]
            y = location[1] + off[1]
            z = location[2] + off[2]
            w = location[3] + off[3]
            if self.lcdict.get((x,y,z,w), None) == '#':
                activecount += 1
        if self.lcdict.get(location, '.') == '#' and (activecount == 2 or activecount == 3):
            return '#'
        elif self.lcdict.get(location, '.') == '.' and activecount == 3:
            return '#'
        else:
            return '.'

    def step(self):
        nextlc = {}
        nxrange = range(self.xrange.start - 1, self.xrange.stop + 1)
        nyrange = range(self.yrange.start - 1, self.yrange.stop + 1)
        nzrange = range(self.zrange.start - 1, self.zrange.stop + 1)
        nwrange = range(self.wrange.start - 1, self.wrange.stop + 1)
        
        xch = set()
        ych = set()
        zch = set()
        wch = set()
        for i in nxrange:
            for j in nyrange:
                for k in nzrange:
                    for l in nwrange:
                        newch = self.nextpop((i,j,k,l))
                        nextlc[(i,j,k,l)] = newch
                        if newch == '#':
                            xch.add(i)
                            ych.add(j)
                            zch.add(k)
                            wch.add(l)
                         

        self.xrange = range(min(xch), max(xch)+1)
        self.yrange = range(min(ych), max(ych)+1)
        self.zrange = range(min(zch), max(zch)+1)
        self.wrange = range(min(wch), max(wch)+1)
        
        self.lcdict = nextlc

class LifeCube:
    OFFSETS = []

    def __init__(self, initmap):
        lines = initmap.split()

        self.xrange = range(0, len(lines[0]))
        self.yrange = range(0, len(lines))
        self.zrange = range(0,1)

        self.lcdict = {}
        for i in self.xrange:
            for j in self.yrange:
                self.lcdict[(i, j, 0)] = lines[j][i]

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for k in (-1, 0, 1):
                    LifeCube.OFFSETS.append((i,j,k))
        LifeCube.OFFSETS.remove((0,0,0))

    def print(self):
        for k in self.zrange:
            print(f"z={k}")

            for i in self.xrange:
                for j in self.yrange:
                    print(self.lcdict[(i, j, k)], end ='')
                print()

    def active_count(self):
        return list(self.lcdict.values()).count('#')

    def nextpop(self, location):
        activecount = 0
        for off in LifeCube.OFFSETS:
            x = location[0] + off[0]
            y = location[1] + off[1]
            z = location[2] + off[2]
            if self.lcdict.get((x,y,z), None) == '#':
                activecount += 1
        if self.lcdict.get(location, '.') == '#' and (activecount == 2 or activecount == 3):
            return '#'
        elif self.lcdict.get(location, '.') == '.' and activecount == 3:
            return '#'
        else:
            return '.'

    def step(self):
        nextlc = {}
        nxrange = range(self.xrange.start - 1, self.xrange.stop + 1)
        nyrange = range(self.yrange.start - 1, self.yrange.stop + 1)
        nzrange = range(self.zrange.start - 1, self.zrange.stop + 1)
        
        xch = set()
        ych = set()
        zch = set()
        for i in nxrange:
            for j in nyrange:
                for k in nzrange:
                    newch = self.nextpop((i,j,k))
                    nextlc[(i,j,k)] = newch
                    if newch == '#':
                        xch.add(i)
                        ych.add(j)
                        zch.add(k)

        self.xrange = range(min(xch), max(xch)+1)
        self.yrange = range(min(ych), max(ych)+1)
        self.zrange = range(min(zch), max(zch)+1)
        
        self.lcdict = nextlc

def main():
    with open(sys.argv[1], 'r') as fp:
        txt = fp.read()

    lc = LifeCube(txt.strip())
    for i in range(6):
        lc.step()

    print(lc.active_count())

    lc = TimeCube(txt.strip())
    for i in range(6):
        lc.step()

    print(lc.active_count())

if __name__ == '__main__':
    main()
