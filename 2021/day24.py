import sys
import d24prog
from collections import defaultdict

INPUTCOUNTER = 0


def translate(line):
    global INPUTCOUNTER
    wds = line.split()
    if 'inp' in line:
        res = '    {} = input[{}]'.format(wds[1], INPUTCOUNTER)
        INPUTCOUNTER += 1
        return res
    elif 'add' in line:
        return "    {} = {} + {}".format(wds[1], wds[1], wds[2])
    elif 'mul' in line:
        return "    {} = {} * {}".format(wds[1], wds[1], wds[2])
    elif 'div' in line:
        return "    {} = {} // {}".format(wds[1], wds[1], wds[2])
    elif 'mod' in line:
        return "    {} = {} % {}".format(wds[1], wds[1], wds[2])
    elif 'eql' in line:
        return "    {} = 1 if {} == {} else 0".format(wds[1], wds[1], wds[2])


class Program:
    def __init__(self, val1list, val2list, input):
        self.val1list = val1list
        self.val2list = val2list
        self.reset(input)

    def reset(self, input):
        self.input = input
        self.count = 0
        self.w, self.x, self.y, self.z = 0,0,0,0

    def save(self):
        return (self.count, self.w, self.x, self.y, self.z)

    def load(self, saved, input):
        self.count, self.w, self.x, self.y, self.z = saved
        self.input = input

    def run(self, stopindex = -1):
        while self.count < len(self.input):
            self.w = int(self.input[self.count])
            self.x = (self.z % 26) + self.val1list[self.count]
            if self.val1list[self.count] < 0:
                self.z = self.z // 26
            if self.x == self.w:
                self.x = 0
            else:
                self.x = 1
            self.y = 25 * self.x + 1
            self.z *= self.y
            self.y = self.w + self.val2list[self.count]
            self.y *= self.x
            self.z += self.y
            #print(self.w,self.x,self.y,self.z)
            if self.count == stopindex:
                return self.x == 0
            self.count += 1

def MONAD(input):
    x,y,z,w = 0,0,0,0
    w = input[0]
    x = z
    x = x % 26
    x = x + 15
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0

    y = 25 * x + 1
    z = z * y
    y = w + 15
    y = y * x
    z = z + y
    # w = w
    # x = 1
    # y = 15+w
    # z = 15+w
    print('digit 0:')
    print(w,x,y,z)

    w = input[1]

    x = z
    x = x % 26
    x = x + 15
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0

    y = 25 * x + 1
    z = z * y
    y = w + 10
    y = y * x
    z = z + y
    print('digit 1:')
    print(w,x,y,z)
    w = input[2]

    x = z
    x = x % 26
    x = x + 12
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 2
    y = y * x
    z = z + y

    w = input[3]
    x = z
    x = x % 26
    x = x + 13
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 16
    y = y * x
    z = z + y

    w = input[4]
    x = z
    x = x % 26
    z = z // 26
    x = x + -12
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 12
    y = y * x
    z = z + y

    w = input[5]
    x = z
    x = x % 26
    x = x + 10
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 11
    y = y * x
    z = z + y

    w = input[6]
    x = z
    x = x % 26
    z = z // 26
    x = x + -9
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 5
    y = y * x
    z = z + y

    w = input[7]
    x = z
    x = x % 26
    x = x + 14
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 16
    y = y * x
    z = z + y

    w = input[8]
    x = z
    x = x % 26
    x = x + 13
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 6
    y = y * x
    z = z + y

    w = input[9]
    x = z
    x = x % 26
    z = z // 26
    x = x + -14
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 15
    y = y * x
    z = z + y

    w = input[10]
    x = z
    x = x % 26
    z = z // 26
    x = x + -11
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 3
    y = y * x
    z = z + y

    w = input[11]
    x = z
    x = x % 26
    z = z // 26
    x = x + -2
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 12
    y = y * x
    z = z + y

    w = input[12]
    x = z
    x = x % 26
    z = z // 26
    x = x + -16
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 10
    y = y * x
    z = z + y

    w = input[13]
    x = z
    x = x % 26
    z = z // 26
    x = x + -14
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z = z * y
    y = w + 13
    y = y * x
    z = z + y

def part1(fname):
    p = Program([15,15,12,13,-12,10,-9,14,13,-14,-11,-2,-16,-14],
                [15,10, 2,16, 12,11, 5,16, 6, 15,  3,12, 10, 13],
                '99948911111112')
    p.run()
    print(p.w,p.x,p.y,p.z)
    print(d24prog.prog('99948911111132'))
    nums = '123456789'
    md = {}
    for i in nums:
        for j in nums:
            for k in nums:
                for l in nums:
                    for m in nums:
                        num = i+j+k+l+m+'111111111'
                        p.reset(num)
                        result = p.run(stopindex = 4)
                        if result:
                            p.count += 1
                            md[num[:5]] = p.save()

    print(1,len(md))
    md2 = {}
    for val in md:
        for i in nums:
            for j in nums:
                num = val+i+j+'1111111'
                p.load(md[val], num)
                result = p.run(stopindex = 6)
                if result:
                    md2[num[:7]] = p.save()

    print(2,len(md2))
    md3 = {}
    for val in md2:
        for i in nums:
            for j in nums:
                for k in nums:
                    num = val+i+j+'1111'
                    p.load(md2[val], num)
                    result = p.run(stopindex = 9)
                    if result:
                        md3[num[:10]] = p.save()
    print(3,len(md3))
    md4 = {}
    for val in md3:
        for i in nums:
            num = val+i+'111'
            p.load(md3[val], num)
            result = p.run(stopindex = 10)
            if result:
                md4[num[:11]] = p.save()
    print(4,len(md4))
    md5 = {}
    for val in md4:
        for i in nums:
            num = val+i+'11'
            p.load(md4[val], num)
            result = p.run(stopindex = 11)
            if result:
                md5[num[:12]] = p.save()
    print(5,len(md5))
    md6 = {}
    for val in md5:
        for i in nums:
            num = val+i+'1'
            p.load(md5[val], num)
            result = p.run(stopindex = 12)
            if result:
                md6[num[:13]] = p.save()
    print(6,len(md6))
    md7 = []
    for val in md6:
        for i in nums:
            num = val+i
            p.load(md6[val], num)
            p.run()
            if p.z == 0:
                md7.append(num)
    print(7,len(md7))
    md7.sort()
    print(md7[-1])

def lastdigit3():
    for w in '123456789':
        w = int(w)
        for z in range(1000):
            startz = z
            x,y = 0,0
            x = x * 0
            x = x + z
            x = x % 26
            z = z // 26
            x = x + -2
            x = 1 if x == w else 0
            x = 1 if x == 0 else 0
            y = y * 0
            y = y + 25
            y = y * x
            y = y + 1
            z = z * y
            y = y * 0
            y = y + w
            y = y + 12
            y = y * x
            z = z + y
            if z in range(0,26):
                print('3:',w, startz)


def lastdigit2():
    for w in '123456789':
        w = int(w)
        for z in range(100):
            startz = z
            x,y = 0,0
            x = x * 0
            x = x + z
            x = x % 26
            z = z // 26
            x = x + -16
            x = 1 if x == w else 0
            x = 1 if x == 0 else 0
            y = y * 0
            y = y + 25
            y = y * x
            y = y + 1
            z = z * y
            y = y * 0
            y = y + w
            y = y + 10
            y = y * x
            z = z + y
            if z in range(15,20):
                print('2:',w, startz)

def lastdigit():
    for w in '123456789':
        w = int(w)
        for z in range(100):
            startz = z
            x,y = 0,0
            x = x * 0
            x = x + z
            x = x % 26  # x = z % 26
            z = z // 26 # z = z // 26
            x = x + -14 # x = x - 14
            x = 1 if x == w else 0
            x = 1 if x == 0 else 0
            y = y * 0
            y = y + 25
            y = y * x
            y = y + 1  # y = 25 * x + 1
            z = z * y  # z = z * (25 * x + 1)
            y = y * 0
            y = y + w
            y = y + 13 # need z == -((w+13) * x)
            y = y * x  # need z == -(y*x)
            z = z + y  # need z == 0 need z == -y at this point.
            if z == 0:
                print('1:',w, startz)


def part2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        for line in linelist:
            print(translate(line.strip()))


def main():
    'main function'
    #print(part1(sys.argv[1]))
    #lastdigit() # must be 1..6
    #lastdigit2() # must be 5..9
    lastdigit3()
    #print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
