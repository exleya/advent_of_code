import sys



def runprog(instlist):
    states = []
    pc = 0
    acc = 0
    while pc < len(instlist):
        state = pc
        if state in states:
            return -acc
        states.append(state)
        inst, amt = instlist[pc]
        if inst == 'acc':
            pc += 1
            acc += amt
        elif inst == 'jmp':
            pc += amt
        elif inst == 'nop':
            pc += 1
    return acc
        
def main():
    prog = sys.stdin.readlines()
    for ind in range(len(prog)):
        inst = prog[ind].strip().split()
        prog[ind] = (inst[0], int(inst[1]))
    for ind in range(len(prog)):
        copy = prog[:]
        if prog[ind][0] == 'nop':
            copy[ind] = ('jmp', prog[ind][1])
        elif prog[ind][0] == 'jmp':
            copy[ind] = ('nop', prog[ind][1])
        result = runprog(copy)

        if result > 0:
            print(result)

if __name__ == '__main__':
    main()
