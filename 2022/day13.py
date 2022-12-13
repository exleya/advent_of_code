import sys
from collections import defaultdict

class Packet:
    def __init__(self, p):
        self.packet = p

    def __lt__(self, rhs):
        return correct_order(self.packet, rhs.packet)

    def __gt__(self, rhs):
        return not correct_order(self.packet, rhs.packet)

    def __eq__(self, rhs):
        return self.packet == rhs.packet

def correct_order_helper(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        if p1 < p2:
            return 1
        elif p1 > p2:
            return -1
        else:
            return 0
    elif isinstance(p1, list) and isinstance(p2, list):
        i = 0
        while i < len(p1) and i < len(p2):
            if correct_order_helper(p1[i], p2[i]) != 0:
                return correct_order_helper(p1[i], p2[i])
            i += 1
        if len(p1) < len(p2):
            return 1
        elif len(p1) > len(p2):
            return -1
        else:
            return 0
    elif isinstance(p1, int) and isinstance(p2, list):
        return correct_order_helper([p1], p2)
    else:
        return correct_order_helper(p1, [p2])

def correct_order(p1, p2):
    result = correct_order_helper(p1, p2)
    if  result == 1:
        return True
    elif result == -1:
        return False
    else:
        print('o noes:' + str(result))
        return None

def part1(fname):
    with open(fname) as fp:
        lines = fp.readlines()
        ctr = 0
        indsum = 0
        while ctr < len(lines):
            val1 = eval("list(" + lines[ctr] + ")")
            val2 = eval("list(" + lines[ctr+1] + ")")
            if correct_order(val1, val2):
                #print((ctr//3)+1)
                indsum += (ctr//3+1)
            ctr += 3
    return indsum

def part2(fname):
    with open(fname) as fp:
        lines = fp.readlines()
        ctr = 0
        packetlist = []
        while ctr < len(lines):
            p = Packet(eval("list(" + lines[ctr] + ")"))
            p2 = Packet(eval("list(" + lines[ctr+1] + ")"))
            packetlist.append(p)
            packetlist.append(p2)
            ctr += 3
        packetlist.append(Packet([[2]]))
        packetlist.append(Packet([[6]]))
        packetlist.sort()
        #for p in packetlist: print(p.packet)
        return (packetlist.index(Packet([[2]]))+1) * (packetlist.index(Packet([[6]]))+1)

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
