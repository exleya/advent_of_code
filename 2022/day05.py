import sys
from collections import defaultdict
STACKS = 9
STACKHEIGHT = 8

def part1(fname):

    boxlist = [[] for i in range(STACKS)]
    with open(fname) as fp:
        text = fp.readlines()
        for i in range(STACKHEIGHT):
            line = text[i]
            #print(line)
            for j in range(1, STACKS*4, 4):
                if line[j] != ' ':
                    boxlist[(j-1)//4].append(line[j])
        print(boxlist)
        for i in range(STACKHEIGHT + 2, len(text)):
            line = text[i][5:]
            count, locs = line.split('from')
            count = int(count)
            src, dst = locs.split('to')
            src = int(src) - 1
            dst = int(dst) - 1
            for i in range(count):
                boxlist[dst].insert(0,boxlist[src].pop(0))
        msg = ""
        for i in range(STACKS):
            msg += boxlist[i][0]
        return msg

def part2(fname):

    boxlist = [[] for i in range(STACKS)]
    with open(fname) as fp:
        text = fp.readlines()
        for i in range(STACKHEIGHT):
            line = text[i]
            #print(line)
            for j in range(1, STACKS*4, 4):
                if line[j] != ' ':
                    boxlist[(j-1)//4].append(line[j])
        print(boxlist)
        for i in range(STACKHEIGHT + 2, len(text)):
            line = text[i][5:]
            count, locs = line.split('from')
            count = int(count)
            src, dst = locs.split('to')
            src = int(src) - 1
            dst = int(dst) - 1
            tmp = []
            for i in range(count):
                tmp.insert(0,boxlist[src].pop(0))
            for i in range(count):
                boxlist[dst].insert(0, tmp.pop(0))
        msg = ""
        for i in range(STACKS):
            msg += boxlist[i][0]
        return msg

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
