import sys


def newnewmath(line):
    line = line.replace('(', ' ( ').replace(')', ' ) ')
    tokens = line.split()

    numstack = [0]
    opstack = ['+']
    for tok in tokens:
        if tok == '+' or tok == '*':
            opstack.insert(0, tok)
        elif tok == '(':
            numstack.insert(0,0)
            opstack.insert(0,'(')
            opstack.insert(0,'+')
        elif tok == ')':
            while opstack[0] != '(':
                num = numstack.pop(0)
                if opstack[0] == '*':
                    numstack[0] *= num
                    opstack.pop(0)
            opstack.pop(0)
            if opstack[0] == '+':
                num = numstack.pop(0)
                numstack[0] += num
                opstack.pop(0)
        else:
            num = int(tok)
            if opstack[0] == '+':
                numstack[0] += num
                opstack.pop(0)
            elif opstack[0] == '*':
                numstack.insert(0, num)

    while len(opstack) > 0:
        op = opstack.pop(0)
        if op == '*':
            v1 = numstack.pop(0)
            numstack[0] *= v1
    return numstack[0]

def newmath(line):
    line = line.replace('(', ' ( ').replace(')', ' ) ')
    tokens = line.split()

    numstack = [0]
    opstack = ['+']
    for tok in tokens:
        if tok == '+' or tok == '*':
            opstack.insert(0, tok)
        elif tok == '(':
            numstack.insert(0,0)
            opstack.insert(0,'+')
        elif tok == ')':
            num = numstack.pop(0)
            op = opstack.pop(0)
            if op == '+':
                numstack[0] += num
            elif op == '*':
                numstack[0] *= num
        else:
            num = int(tok)
            op = opstack.pop(0)
            if op == '+':
                numstack[0] += num
            elif op == '*':
                numstack[0] *= num
    return numstack[0]

def main():
    with open(sys.argv[1], 'r') as fp:
        lines = fp.read().split('\n')

    tot = 0
    for line in lines:
        tot += newnewmath(line)

    print(tot)

    

if __name__ == '__main__':
    main()
