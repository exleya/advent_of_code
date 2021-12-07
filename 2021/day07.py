import sys
from collections import defaultdict


def part1(fname):
    with open(fname) as fp:
        line = fp.readline()
        nums = line.split(',')
        nmin, nmax = int(nums[0]), int(nums[0])
        counter = defaultdict(int)
        for i in range(len(nums)):
            nums[i] = int(nums[i])
            counter[nums[i]] += 1
            nmax = max(nums[i], nmax)
            nmin = min(nums[i], nmin)

        totals = {}
        minval = nmin
        for i in range(nmin, nmax+1):
            total = 0
            for val, count in counter.items():
                total += abs(i - val) * count
            totals[i] = total
            if totals[i] < totals[minval]:
                minval = i
        return totals[minval]

def part2(fname):
    with open(fname) as fp:
        line = fp.readline()
        nums = line.split(',')
        nmin, nmax = int(nums[0]), int(nums[0])
        counter = defaultdict(int)
        for i in range(len(nums)):
            nums[i] = int(nums[i])
            counter[nums[i]] += 1
            nmax = max(nums[i], nmax)
            nmin = min(nums[i], nmin)

        totals = {}
        minval = nmin
        for i in range(nmin, nmax+1):
            total = 0
            for val, count in counter.items():
                n = abs(i - val)
                total += ((n * (n+1)) // 2) * count
            totals[i] = total
            if totals[i] < totals[minval]:
                minval = i
        return totals[minval]

def main():
    'main function'    
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
