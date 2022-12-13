import sys
from collections import defaultdict

class Monkey:
    Group = []
    Divisors = set()
    Mod = 1

    def __init__(self, num, items, op, tests):
        self.inspect = 0
        Monkey.Group.append(self)
        self.id = int(num.split()[1].split(':')[0])
        self._parse_items(items)
        self._parse_op(op)
        self._parse_tests(tests)

    def setmod(self):
        Monkey.Mod = 1
        for d in Monkey.Divisors:
            Monkey.Mod *= d

    def _parse_op(self, op):
        op = op[op.find(":")+2:].strip()
        self.optype = op.split()[3]
        self.operand = op.split()[4]

    def _parse_items(self, items):
        items = items[items.find(":")+2:]
        items = items.split(',')
        self.items = []
        for i in items: self.items.append(int(i))

    def _parse_tests(self, tests):
        self.testdiv = int(tests[0][tests[0].find("by")+3:])
        Monkey.Divisors.add(self.testdiv)
        self.true = int(tests[1][tests[1].find("monkey")+7:])
        self.false = int(tests[2][tests[2].find("monkey")+7:])

    def __repr__(self):
        out = "Monkey " + str(self.id) + '\n'
        out += "Op: new = old " + self.optype + self.operand + '\n'
        out += str(self.items) + '\n'
        out += str(self.testdiv) + " true to " + str(self.true)
        out += " false to " + str(self.false)
        return out

    def add_item(self, item):
        self.items.append(item)

    def execute_op(self, item):
        #print(" Worry level is ", end = '')
        if self.operand == 'old':
            oper = item
        else:
            oper = int(self.operand)
        if self.optype == '+':
            #print(" increased by",oper,"to",(item+oper))
            return item + oper
        elif self.optype == '*':
            #print(" multiplied by",oper,"to",(item*oper))
            return item * oper

    def take_turn2(self):
        while len(self.items) > 0:
            item = self.items.pop(0)
            self.inspect += 1
            #print("Monkey inspects item with worry level",item)
            item = self.execute_op(item)
            item = item % Monkey.Mod
            #item = item // 3
            #print(" Monkey gets bored, divided by 3 to",item)
            if item % self.testdiv == 0:
                #print(" Divisible by",self.testdiv,"so thrown to",self.true)
                Monkey.Group[self.true].add_item(item)
            else:
                #print(" Not divisible by",self.testdiv,"so thrown to",self.false)
                Monkey.Group[self.false].add_item(item)

    def take_turn(self):
        while len(self.items) > 0:
            item = self.items.pop(0)
            self.inspect += 1
            #print("Monkey inspects item with worry level",item)
            item = self.execute_op(item)
            item = item // 3
            #print(" Monkey gets bored, divided by 3 to",item)
            if item % self.testdiv == 0:
                #print(" Divisible by",self.testdiv,"so thrown to",self.true)
                Monkey.Group[self.true].add_item(item)
            else:
                #print(" Not divisible by",self.testdiv,"so thrown to",self.false)
                Monkey.Group[self.false].add_item(item)

def part1(fname):
    with open(fname) as fp:
        lines = fp.readlines()
        ctr = 0
        while ctr < len(lines):
            if "Monkey" in lines[ctr]:
                m1 = Monkey(lines[ctr], lines[ctr+1],
                            lines[ctr+2], lines[ctr+3:ctr+6])
                #print(m1)
                ctr+=5
            ctr+=1

        for i in range(20):
            for m in Monkey.Group:
                m.take_turn()

        cts = [m.inspect for m in Monkey.Group]
        #print(cts)
        m = max(cts)
        cts.remove(m)
        m2 = max(cts)
        return m * m2

def part2(fname):
    Monkey.Group = []
    Monkey.Divisors = set()
    with open(fname) as fp:
        lines = fp.readlines()
        ctr = 0
        while ctr < len(lines):
            if "Monkey" in lines[ctr]:
                m1 = Monkey(lines[ctr], lines[ctr+1],
                            lines[ctr+2], lines[ctr+3:ctr+6])
                #print(m1)
                ctr+=5
            ctr+=1

        Monkey.Group[0].setmod()
        for i in range(10000):
            #print(i)
            for m in Monkey.Group:
                m.take_turn2()

        cts = [m.inspect for m in Monkey.Group]
        print(cts)
        m = max(cts)
        cts.remove(m)
        m2 = max(cts)
        return m * m2

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
