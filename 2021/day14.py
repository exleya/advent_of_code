import sys
from collections import defaultdict

class Polymer:

    lu = defaultdict(int)

    def __init__(self, base):
        self.base = {}
        for i, ch in enumerate(base):
            self.base[i] = ch
        self.rules = {}

    def addrule(self, lhs, rhs):
        self.rules[lhs] = rhs

    def gen(self):
        #print(self.base)
        self.newbase = {}
        for k in range(len(self.base)):
            self.newbase[k*2] = self.base[k]

        for k in range(1,len(self.base)*2-1, 2):
            self.newbase[k] = self.rules[self.newbase[k-1] + self.newbase[k+1]]

        self.base = self.newbase

    def count(self, depth):
        counter = defaultdict(int)
        counter[self.base[0]] += 1
        for i in range(len(self.base)-1):
            #print(i)
            self.reccount(self.base[i], self.base[i+1], counter, depth)
        return counter


    def reccount(self, ch1, ch2, counter, depth):
        if (ch1,ch2,depth) in Polymer.lu:
            #print(ch1+ch2+str(depth) + " in table...")
            #print(Polymer.lu[(ch1,ch2,depth)])
            combine(counter,Polymer.lu[(ch1,ch2,depth)])
            return
        elif depth == 0:
            counter[ch2] += 1
            return
        else:
            middle = self.rules[ch1+ch2]
            temp = defaultdict(int)
            self.reccount(ch1, middle, temp, depth-1)
            self.reccount(middle, ch2, temp, depth-1)
            Polymer.lu[(ch1,ch2,depth)] = temp
            combine(counter,temp)
            return


    def __repr__(self):
        s = ''
        for k in sorted(list(self.base.keys())):
            s += self.base[k]
        return s

def combine(a, b):
    for k in set(list(a.keys()) + list(b.keys())):
        a[k] += b[k]

def part1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        polymer = Polymer(linelist[0].strip())
        for line in linelist[2:]:
            l, r = line.strip().split(' -> ')
            polymer.addrule(l,r)

        for i in range(10):
            polymer.gen()

        valcounts = {}
        for val in set(polymer.base.values()):
            valcounts[val] = list(polymer.base.values()).count(val)
        print(valcounts)
        return max(valcounts.values()) - min(valcounts.values())

def part2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        polymer = Polymer(linelist[0].strip())
        for line in linelist[2:]:
            l, r = line.strip().split(' -> ')
            polymer.addrule(l,r)


        valcounts = polymer.count(40)
        #print(valcounts)

        return max(valcounts.values()) - min(valcounts.values())



def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
