import sys
from collections import defaultdict

def alldiff(s):
    stset = set(s)
    return len(stset) == len(s)

def part1(fname):
    with open(fname) as fp:
        text = fp.read()
        counter = 3
        while counter < len(text):
            if alldiff(text[counter-3:counter+1]):
                return counter+1
            counter += 1

def part2(fname):
    with open(fname) as fp:
        text = fp.read()
        counter = 13
        while counter < len(text):
            if alldiff(text[counter-13:counter+1]):
                return counter+1
            counter += 1

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
