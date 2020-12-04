import sys

def main():
    validcount = 0
    for line in sys.stdin:
        blah = line.split()
        rng = blah[0]
        ch = blah[1][0]
        pwd = blah[2]
        lower, upper = rng.split('-')
        lower = int(lower)
        upper = int(upper)
        count = 0
        if pwd[lower-1] == ch:
            count += 1
        if pwd[upper-1] == ch:
            count += 1
        if count == 1:
            validcount += 1
    print(validcount)

def part1():
    validcount = 0
    for line in sys.stdin:
        blah = line.split()
        rng = blah[0]
        ch = blah[1][0]
        pwd = blah[2]
        lower, upper = rng.split('-')
        lower = int(lower)
        upper = int(upper)
        if lower <= pwd.count(ch) <= upper:
            validcount += 1
    print(validcount)

if __name__ == '__main__':
    main()
