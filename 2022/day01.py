import sys
from collections import defaultdict

def part1(fname):
    with open(fname) as fp:
        max = 0
        total = 0
        for line in fp:
            if len(line) > 1:
                total += int(line)
            else:
                if total > max:
                    max = total
                total = 0
        return max

def part2(fname):
    with open(fname) as fp:
        loads = []
        max = 0
        total = 0
        for line in fp:
            if len(line) > 1:
                total += int(line)
            else:
                loads.append(total)
                if total > max:
                    max = total
                total = 0
        loads.sort()
        return loads[-1] + loads[-2] + loads[-3]

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
