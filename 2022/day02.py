import sys
from collections import defaultdict

def part1(fname):
    with open(fname) as fp:
        score = 0
        for line in fp:
            op, me = line.split()
            if 'X' in me:
                score += 1
                if 'A' in op:
                    score += 3
                elif 'B' in op:
                    score += 0
                elif 'C' in op:
                    score += 6
            elif 'Y' in me:
                score += 2
                if 'A' in op:
                    score += 6
                elif 'B' in op:
                    score += 3
                elif 'C' in op:
                    score += 0
            elif 'Z' in me:
                score += 3
                if 'A' in op:
                    score += 0
                elif 'B' in op:
                    score += 6
                elif 'C' in op:
                    score += 3
    return score
          

def part2(fname):
    with open(fname) as fp:
        score = 0
        for line in fp:
            op, me = line.split()
            if 'X' in me:
                if 'A' in op:
                    score += 3
                elif 'B' in op:
                    score += 1
                elif 'C' in op:
                    score += 2
            elif 'Y' in me:
                score += 3
                if 'A' in op:
                    score += 1
                elif 'B' in op:
                    score += 2
                elif 'C' in op:
                    score += 3
            elif 'Z' in me:
                score += 6
                if 'A' in op:
                    score += 2
                elif 'B' in op:
                    score += 3
                elif 'C' in op:
                    score += 1
    return score
          

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
