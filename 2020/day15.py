import sys

def part1(numlist):
    sd = {}
    for num, i in enumerate(numlist):
        sd[int(i)] = num

    print(sd)
    prevnum = numlist[-1]

    for i in range(len(numlist), 30000000):
        ppnum = prevnum
        if prevnum not in sd:
            prevnum = 0
        else:
            last = sd[prevnum]
            diff = (i - 1) - last
            prevnum = diff
        sd[ppnum] = i - 1
    print(prevnum)

def main():
    with open(sys.argv[1],'r') as fp:
        line = fp.readline()

    line = line.strip()

    part1(line.split(','))

if __name__ == '__main__':
    main()
