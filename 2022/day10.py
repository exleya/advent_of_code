import sys
from collections import defaultdict

class Circuit:
    def __init__(self):
        self.cycle_reg = [1]
        self.crt = ["", "", "", "", "", ""]
        #self._write_crt()

    def _write_crt(self):
        row = (len(self.cycle_reg) - 1) // 40
        col = (len(self.cycle_reg) - 1) % 40
        regval = self.cycle_reg[-1]
        if abs(regval - col) <= 1:
            ch = '#'
        else:
            ch = '.'
        self.crt[row] += ch

    def execute(self, instr):
        # print(self.crt)
        # input(self.cycle_reg)
        self._write_crt()
        self.cycle_reg.append(self.cycle_reg[-1])
        if "addx" in instr:
            val = int(instr.split()[1])
            self._write_crt()
            self.cycle_reg.append(self.cycle_reg[-1] + val)


    def get_st(self, ind):
        return ind * self.cycle_reg[ind-1]

def part1(fname):
    c = Circuit()
    with open(fname) as fp:
        for line in fp:
            c.execute(line)
    for k in c.crt: print(k)
    return (c.get_st(20) + c.get_st(60) + c.get_st(100) +
            c.get_st(140) + c.get_st(180) + c.get_st(220))

def part2(fname):
    with open(fname) as fp:
        pass

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
