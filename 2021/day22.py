import sys
from collections import defaultdict
import re

def inbounds(v):
    return -50 <= v <= 50

def linear_overlap(a1, a2, b1, b2):
    '''return value where a1..a2 overlaps b1..b2
    return tuple of start, end
    otherwise return False
    '''
    if a2 < b1 or b2 < a1:
        return False
    else:
        if b1 <= a1 <= b2:
            start = a1
        elif a1 <= b1 <= a2:
            start = b1

        if b1 <= a2 <= b2:
            end = a2
        elif a1 <= b2 <= a2:
            end = b2
        return (start,end)
    return 'oops!'

def overlap(cuboida, cuboidb):
    '''each region is a 6-tuple
    if overlap occurs, return the overlap cuboid
     as a 6-tuple
    it begins at
    '''
    ax1, ax2, ay1, ay2, az1, az2 = cuboida
    bx1, bx2, by1, by2, bz1, bz2 = cuboidb
    xlimits = linear_overlap(ax1, ax2, bx1, bx2)
    if xlimits != False:
        ylimits = linear_overlap(ay1, ay2, by1, by2)
        if ylimits != False:
            zlimits = linear_overlap(az1, az2, bz1, bz2)
            if zlimits != False:
                return Cuboid(xlimits[0], xlimits[1], ylimits[0], ylimits[1], zlimits[0], zlimits[1], None)
    return False


class Cuboid:
    xmin = float('inf')
    xmax = 0
    ymin = float('inf')
    ymax = 0
    zmin = float('inf')
    zmax = 0

    def __init__(self, x1, x2, y1, y2, z1, z2, type):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.type = type
        Cuboid.xmin = min(x1, Cuboid.xmin)
        Cuboid.ymin = min(y1, Cuboid.ymin)
        Cuboid.zmin = min(z1, Cuboid.zmin)
        Cuboid.xmax = max(x1, Cuboid.xmax)
        Cuboid.ymax = max(y1, Cuboid.ymax)
        Cuboid.zmax = max(z1, Cuboid.zmax)
        self.overlaplist = []

    def __repr__(self):
        return "({}, {}, {}, {}, {}, {}, {}, {})".format(
            self.x1,self.x2, self.y1,self.y2,
            self.z1,self.z2,self.type, self.size()
        )

    def size(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def overlap(self, other):
        result = overlap((self.x1, self.x2,
                self.y1, self.y2,
                self.z1, self.z2),
                (other.x1, other.x2,
                other.y1, other.y2,
                other.z1, other.z2))
        if result != False:
            return result


    def translate(self):
        '''translates so that the min is 0,0,0'''
        self.x1 -= Cuboid.xmin
        self.x2 -= Cuboid.xmin
        self.y1 -= Cuboid.ymin
        self.y2 -= Cuboid.ymin
        self.z1 -= Cuboid.zmin
        self.z2 -= Cuboid.zmin

    def reassert_min_max(self):
        Cuboid.xmin = 0
        Cuboid.xmax -= Cuboid.xmin
        Cuboid.ymin = 0
        Cuboid.ymax -= Cuboid.ymin
        Cuboid.zmin = 0
        Cuboid.zmax -= Cuboid.zmin

    def linearize(self):
        if (Cuboid.xmin, Cuboid.ymin, Cuboid.zmin) != (0,0,0):
            print('nope!')
            return
        else:
            linear_segment_list = []
            for z in range(self.z1, self.z2+1):
                for y in range(self.y1, self.y2+1):
                    linear_segment_list.append((
                        z*Cuboid.zmax*Cuboid.zmax + y*Cuboid.ymax + self.x1,
                        z*Cuboid.zmax*Cuboid.zmax + y*Cuboid.ymax + self.x2))
            return linear_segment_list


def combine(sl, c):
    '''combine segment list and cuboid c'''
    csegs = c.linearize()
    # print('trying to combine: ')
    # print('      ' + str(csegs))
    # print(' into ' + str(sl))

    ci = 0
    si = 0

    while ci < len(csegs):
        # iterate forward in sl
        while si < len(sl) and sl[si][0] < csegs[ci][0] :
            si += 1
        # now, sl[si-1][0] <= csegs[ci][0] <= sl[si][0]
        # or si is at the end of the list.
        if si == len(sl):
            if c.type == 'on':
                if len(sl) == 0:
                    sl.insert(si, csegs[ci])
                elif csegs[ci][0] <= sl[si-1][1]:
                    sl[si-1] = (sl[si-1][0], csegs[ci][1])
                else:
                    sl.insert(si, csegs[ci])
        elif si == 0:
            #print('--------',csegs[ci],sl[si])
            # so in here,
            # csegs[ci][0] <= sl[si][0]
            if c.type == 'on':
                while si < len(sl) and csegs[ci][1] >= sl[si][1]:
                    del sl[si]
                if sl[si][0] <= csegs[ci][1]:
                    sl[si] = (csegs[ci][0], sl[si][1])
                else:
                    sl.insert(si, csegs[ci])
            else:
                while si < len(sl) and csegs[ci][1] >= sl[si][1]:
                    del sl[si]
                if  sl[si][0] <= csegs[ci][1] <= sl[si][1]:
                    sl[si] = (csegs[ci][1]+1,sl[si][1])
        else:
            #print(sl[si-1], csegs[ci], sl[si])
            # now, sl[si-1][0] < csegs[ci][0] < sl[si][0]
            if c.type == 'on':
                if csegs[ci][0] <= sl[si-1][1]:
                    sl[si-1] = (sl[si-1][0], csegs[ci][1])
                while si < len(sl) and csegs[ci][1] >= sl[si][1]:
                    del sl[si]
                if si<len(sl) and sl[si][0] <= csegs[ci][1]:
                    if sl[si-1][1] == csegs[ci][1]:
                        sl[si-1] == (sl[si-1][0], sl[si][1])
                        del sl[si]
                    else:
                        sl[si] = (csegs[ci][0], sl[si][1])
                else:
                    if sl[si-1][1] != csegs[ci][1]:
                        sl.insert(si, csegs[ci])
            else:
                if csegs[ci][0] <= sl[si-1][1]:
                    sl[si-1] = (sl[si-1][0], csegs[ci][0] - 1)
                while si < len(sl) and csegs[ci][1] >= sl[si][1]:
                    del sl[si]
                if sl[si][0] <= csegs[ci][1]:
                    sl[si] = (csegs[ci][1]+1, sl[si][1])


        ci += 1


    #
    #
    # while ci < len(csegs):
    #     if si >= len(sl):
    #         sl.insert(si, csegs[ci])
    #     else:
    #         while si < len(sl) and csegs[ci][0] < sl[si][0]:
    #             si += 1
    #         if si < len(sl) and sl[si][0] <= csegs[ci][0] <= sl[si][1]:
    #             if c.type == 'on':
    #                 sl[si] = (sl[si][0], csegs[ci][1])
    #                 while si+1 < len(sl) and csegs[ci][1] >= sl[si+1][1]:
    #                     del sl[si+1]
    #                 if si+1 < len(sl) and sl[si+1][0] <= csegs[ci][1] <= sl[si+1][1]:
    #                     sl[si] = (sl[si][0], sl[si+1][1])
    #                     del sl[si+1]
    #             else:
    #                 print('case 1:' + str(csegs[ci]))
    #                 sl[si] = (sl[si][0], csegs[ci][0]-1)
    #                 while csegs[ci][1] >= sl[si+1][1]:
    #                     del sl[si+1]
    #                 if sl[si+1][0] <= csegs[ci][1] <= sl[si+1][1]:
    #                     sl[si+1] = (csegs[ci][1]+1, sl[si+1][1])
    #         else:
    #             if c.type == 'on':
    #                 while si+1 < len(sl) and csegs[ci][1] >= sl[si+1][1]:
    #                     del sl[si+1]
    #                 if si+1 < len(sl) and sl[si+1][0] <= csegs[ci][1] <= sl[si+1][1]:
    #                     sl[si+1] = (csegs[ci][0], sl[si+1][1])
    #                 elif si+1 < len(sl) and csegs[ci][1] < sl[si][0]:
    #                     sl.insert(si, csegs[ci])
    #                 else:
    #                     sl.insert(si+1, csegs[ci])
    #             else:
    #                 print('case 2:'+ str(csegs[ci]) + ' ' + str(sl[si]))
    #                 while si+1 < len(sl) and csegs[ci][1] >= sl[si+1][1]:
    #                     print('del!')
    #                     del sl[si+1]
    #                 if si < len(sl) and sl[si][0] <= csegs[ci][1] <= sl[si][1]:
    #                     print('update!')
    #                     sl[si] = (csegs[ci][1]+1, sl[si][1])
    #                     #si+=1
    #     ci += 1

def total(seglist):
    tot = 0
    for seg in seglist:
        tot += seg[1] - seg[0] + 1
    return tot


def part2(fname):
    clist = []
    with open(fname, 'r') as fp:
        for line in fp:
            pat = re.compile('([a-z]*) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')
            match = pat.search(line.strip())
            x1 = int(match.group(2))
            x2 = int(match.group(3))
            y1, y2 = int(match.group(4)), int(match.group(5))
            z1, z2 = int(match.group(6)), int(match.group(7))
            clist.append(Cuboid(x1,x2,y1,y2,z1,z2,match.group(1)))
    for c in clist:
        c.translate()
        print(c)

    clist[0].reassert_min_max()
    #
    # totalon = 0
    # for i in range(len(clist)):
    #     for j in range(i+1, len(clist)):
    #         res = clist[i].overlap(clist[j])
    #         if res:
    #             clist[i].overlaplist.append(res)
    #
    #
    #
    # print(clist[0].overlaplist)
    # print(clist[1].overlaplist)
    # print(clist[2].overlaplist)
    # print(clist[3].overlaplist)
    #
    #
    # totalon = 0
    # for i in range(len(clist)):
    #     if clist[i].type == 'on':
    #         totalon += clist[i].size()
    #     print(totalon)
    #     for j in range(i):
    #         if clist[j].type == 'on':
    #             res = clist[i].overlap(clist[j])
    #             if res:
    #                 print(res)
    #                 print(str(j)+' overlaps on ' + str(i))
    #                 totalon -= res.size()
    #                 print(totalon)
    #     #print(i)
    #     #print(linear_segments)
    #     #print(total(linear_segments))
    #     #combine(linear_segments, c)
    # print(totalon)
    # #print(linear_segments)
    # print('hmm')
    return totalon



def part1(fname):
    settings = {}
    with open(fname, 'r') as fp:
        for line in fp:
            if 'on' in line:
                pat = re.compile('x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')
                match = pat.search(line.strip())
                x1 = int(match.group(1))
                x2 = int(match.group(2))
                y1, y2 = int(match.group(3)), int(match.group(4))
                z1, z2 = int(match.group(5)), int(match.group(6))
                if (inbounds(x1) and inbounds(x2) and
                    inbounds(y1) and inbounds(y2) and
                    inbounds(z1) and inbounds(z2)):
                    for i in range(x1,x2+1):
                        for j in range(y1,y2+1):
                            for k in range(z1,z2+1):
                                settings[(i,j,k)] = True
            elif 'off' in line:
                pat = re.compile('x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')
                match = pat.search(line.strip())
                x1 = int(match.group(1))
                x2 = int(match.group(2))
                y1, y2 = int(match.group(3)), int(match.group(4))
                z1, z2 = int(match.group(5)), int(match.group(6))
                if (inbounds(x1) and inbounds(x2) and
                    inbounds(y1) and inbounds(y2) and
                    inbounds(z1) and inbounds(z2)):
                    for i in range(x1,x2+1):
                        for j in range(y1,y2+1):
                            for k in range(z1,z2+1):
                                if (i,j,k) in settings:
                                    del settings[(i,j,k)]

    return len(settings)




def main():
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
