import sys
from collections import defaultdict


def part1(fname):
    with open(fname) as fp:
        fish = fp.readline().split(',')
        for i in range(len(fish)):
            fish[i] = int(fish[i])

        for i in range(80):
            newfish = []
            for j in range(len(fish)):
                if fish[j] == 0:
                    fish[j] = 6
                    newfish.append(8)
                else:
                    fish[j] -= 1
            fish += newfish
        return len(fish)       


def part2(fname):
    numcount = [0] * 9
    with open(fname) as fp:
        fish = fp.readline().split(',')
        for i in range(len(fish)):
            numcount[int(fish[i])] += 1

        print(numcount)
        for i in range(256):
            newcount = [0] * 9
            for j in range(8,0,-1):
                newcount[j-1] = numcount[j]
            newcount[8] = numcount[0]
            newcount[6] += numcount[0]
            numcount = newcount
        return sum(numcount)       

def main():
    'main function'    
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
