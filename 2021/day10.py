import sys
from collections import defaultdict

def part1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        illegal = 0
        for line in linelist:

            stack = []
            for ch in line.strip():
                if ch in '[{<(':
                    stack.append(ch)
                elif ch in ']}>)':
                    m = stack.pop()
                    if ch == ']' and m != '[':
                        illegal += 57
                        break
                    elif ch == '}' and m != '{':
                        illegal += 1197
                        break
                    elif ch == '>' and m != '<':
                        illegal += 25137
                        break
                    elif ch == ')' and m != '(':
                        illegal += 3
                        break
        return illegal

def part2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        scorelist = []
        for line in linelist:

            stack = []
            illegal = False
            for ch in line.strip():
                if ch in '[{<(':
                    stack.append(ch)
                elif ch in ']}>)':
                    m = stack.pop()
                    if ch == ']' and m != '[':
                        illegal = True
                        break
                    elif ch == '}' and m != '{':
                        illegal = True
                        break
                    elif ch == '>' and m != '<':
                        illegal = True
                        break
                    elif ch == ')' and m != '(':
                        illegal = True
                        break
            if not illegal:
                score = 0
                while len(stack) > 0:
                    score *= 5
                    ch = stack.pop()
                    if ch == '(':
                        score += 1
                    elif ch == '[':
                        score += 2
                    elif ch == '{':
                        score += 3
                    elif ch == '<':
                        score += 4
                scorelist.append(score)
        scorelist.sort()
        return scorelist[len(scorelist)//2]

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
