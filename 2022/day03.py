import sys
from collections import defaultdict

def part1(fname):
    with open(fname) as fp:
        priosum = 0
        for line in fp:
            line = line.strip()
            first = line[:len(line)//2]
            second = line[len(line)//2:]
            ind = 0
            while ind < len(first):
                ch = first[ind]
                if ch in second:
                    if 'a' <= ch <= 'z':
                        prio = ord(ch) - 96
                    else:
                        prio = ord(ch) - 38
                    priosum += prio
                    ind = len(first)
                ind+= 1
        return priosum

def findcommonletter(s1,s2,s3):
    for ch in s1:
        if ch in s2 and ch in s3:
            return ch

def part2(fname):
    with open(fname) as fp:
        priosum = 0
        text = fp.read().split()
        i = 0
        while i < len(text):
            ch = findcommonletter(text[i], text[i+1], text[i+2])
            if 'a' <= ch <= 'z':
                 prio = ord(ch) - 96
            else:
                 prio = ord(ch) - 38
            priosum += prio
            i += 3
    return priosum

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
