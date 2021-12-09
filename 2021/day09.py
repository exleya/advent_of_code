import sys
from collections import defaultdict

def part1(fname):
    with open(fname) as fp:
        lpsum = 0
        linelist = fp.readlines()
        for i in range(len(linelist)):
            linelist[i] = linelist[i].strip()
        for row in range(1,len(linelist)-1):
            for col in range(1,len(linelist[row])-1):
                ch = linelist[row][col]
                if (ch < linelist[row][col+1] and
                        ch < linelist[row][col-1] and
                        ch < linelist[row-1][col] and
                        ch < linelist[row+1][col]):
                    #print(ch)
                    lpsum += int(ch) + 1

        for col in range(1, len(linelist[row])-1):
            chtop = linelist[0][col]
            chbot = linelist[-1][col]
            if (chtop < linelist[0][col+1] and
                    chtop < linelist[0][col-1] and
                    chtop < linelist[1][col]):
                #print(chtop)
                lpsum += int(chtop) + 1
            if (chbot < linelist[-1][col+1] and
                    chbot < linelist[-1][col-1] and
                    chbot < linelist[-2][col]):
                #print(chbot)
                lpsum += int(chbot) + 1

        for row in range(1, len(linelist)-1):
            chleft = linelist[row][0]
            chright = linelist[row][-1]
            if (chleft < linelist[row-1][0] and
                    chleft < linelist[row+1][0] and
                    chleft < linelist[row][1]):
                lpsum += int(chleft) + 1
            if (chright < linelist[row-1][-1] and
                    chright < linelist[row+1][-1] and
                    chright < linelist[row][-2]):
                lpsum += int(chright) + 1

        if (linelist[0][0] < linelist[0][1] and
            linelist[0][0] < linelist[1][0]):
            lpsum += int(linelist[0][0])
        if (linelist[0][-1] < linelist[0][-2] and
            linelist[0][-1] < linelist[1][-1]):
            #print(linelist[0][-1])
            lpsum += int(linelist[0][-1]) + 1
        if (linelist[-1][-1] < linelist[-1][-2] and
            linelist[-1][-1] < linelist[-2][-1]):
            #print(linelist[-1][-1])
            lpsum += int(linelist[-1][-1]) + 1
        if (linelist[-1][0] < linelist[-1][1] and
            linelist[-1][0] < linelist[-2][0]):
            #print(linelist[-1][0])
            lpsum += int(linelist[-1][0]) + 1
        return lpsum

def is_lp(lplocdict, row, col, height, width):
    return ((row == 0 or lplocdict[(row, col)] < lplocdict[(row-1, col)]) and
        (row == height-1 or lplocdict[(row,col)] < lplocdict[(row+1, col)]) and
        (col == 0 or lplocdict[(row,col)] < lplocdict[(row, col-1)]) and
        (col == width-2 or lplocdict[(row,col)] < lplocdict[(row,col+1)]))

def rec_findsize(ldict, lp):
    if lp not in ldict:
        return 0
    elif ldict[lp] == 9:
        return 0
    else:

        ldict[lp] = 9
        sum = 0
        for adj in [(-1,0), (1, 0), (0, 1), (0, -1)]:
            sum += rec_findsize(ldict, (lp[0] + adj[0], lp[1] + adj[1]))
        return sum + 1


def part2(fname):

    with open(fname) as fp:
        linelist = fp.readlines()
        locdict = {}
        for row in range(len(linelist)):
            line = linelist[row].strip()
            for col in range(len(line)):
                locdict[(row,col)] = int(line[col])

        lplist = []
        for k in locdict:
            if is_lp(locdict, k[0], k[1], len(linelist), len(linelist[0])):
                lplist.append(k)

        sizelist = []
        for lp in lplist:
            sizelist.append(rec_findsize(locdict, lp))

        sizelist.sort()
        return sizelist[-1] * sizelist[-2] * sizelist[-3]

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
