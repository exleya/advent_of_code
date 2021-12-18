import sys
from collections import defaultdict
import binascii


def build_packet(binary):
    '''given a long binary string, build a packet
    (recursive)

    return Packet, index into string where next
    packet begins
    '''
    assert isinstance(binary, str), 'oops'
    #print(binary)
    if len(binary) < 8:
        return None, len(binary)
    else:
        version = int(binary[0:3],2)
        type = int(binary[3:6],2)
        if type == 4:
            i = 6
            num = ''
            while binary[i] == '1':
                num += binary[i+1:i+5]
                i += 5
            num += binary[i+1:i+5]
            val = int(num, 2)
            return Packet(version, type, value=val), i+5
        else:
            typeid = int(binary[6])
            p = Packet(version, type)
            #print(p)
            if typeid == 0:
                sp_length = int(binary[7:22],2)
                #print('sp length:' + str(sp_length))
                sp_start = 22
                sp_end = 22 + sp_length
                while sp_start < sp_end:
                    subp, offset = build_packet(binary[sp_start:sp_end])
                    if subp == None:
                        break
                    sp_start += offset
                    #print(subp, sp_start, sp_end)
                    p.sp_list.append(subp)
                return p, sp_end
            elif typeid == 1:
                sp_num = int(binary[7:18], 2)
                sp_start = 18
                for i in range(sp_num):
                    subp, offset = build_packet(binary[sp_start:])
                    sp_start += offset
                    p.sp_list.append(subp)
                return p, sp_start


class Packet:
    def __init__(self, version, type, value=None, typeid=None):
        self.sp_list = []
        self.version = version
        self.type = type
        self.value = value
        self.typeid = typeid

    def get_value(self):
        if self.type == 0:
            tot = 0
            for p in self.sp_list:
                tot += p.get_value()
            return tot
        elif self.type == 1:
            tot = 1
            for p in self.sp_list:
                tot *= p.get_value()
            return tot
        elif self.type == 2:
            m = float('inf')
            for p in self.sp_list:
                m = min(p.get_value(), m)
            return m
        elif self.type == 3:
            m = float('-inf')
            for p in self.sp_list:
                m = max(p.get_value(), m)
            return m
        elif self.type == 4:
            return self.value
        elif self.type == 5:
            if self.sp_list[0].get_value() > self.sp_list[1].get_value():
                return 1
            return 0
        elif self.type == 6:
            if self.sp_list[0].get_value() < self.sp_list[1].get_value():
                return 1
            return 0
        elif self.type == 7:
            if self.sp_list[0].get_value() == self.sp_list[1].get_value():
                return 1
            return 0

    def __repr__(self):
        if self.type == 4:
            return "v: {v}, t: {t}, value: {val}".format(v=self.version, t=self.type, val = self.value)
        else:
            s =  "v: {v}, t: {t} ".format(v=self.version, t=self.type)
            s += str(self.sp_list)
            return s

    def version_sum(self):
        if len(self.sp_list) == 0:
            return self.version
        else:
            tot = self.version
            for p in self.sp_list:
                tot += p.version_sum()
            return tot

    #
    # def build_as_subpacket(self):
    #     self.version = int(self.binary[0:3],2)
    #     #print(self.version)
    #     self.type = int(self.binary[3:6],2)
    #     #print(self.type)
    #     if self.type == 4:
    #         i = 6
    #         num = ''
    #         while self.binary[i] == '1':
    #             num += self.binary[i+1:i+5]
    #             i += 5
    #         num += self.binary[i+1:i+5]
    #         self.value = int(num, 2)
    #         return i
    #     else:
    #         self.typeid = int(self.binary[6])
    #         if self.typeid == 0:
    #             self.sp_length = int(self.binary[7:22],2)
    #             sp_start = 22
    #             sp_end = 22 + self.sp_length
    #             while sp_start < sp_end:
    #                 p = Packet(self.binary[sp_start:sp_end], False)
    #                 sp_start = p.build_as_subpacket()
    #                 self.sp_list.append(p)
    #             return sp_start
    #         elif self.typeid == 1:
    #             self.sp_num = int(self.binary[7:18], 2)
    #             sp_start = 18
    #             for i in range(self.sp_num):
    #                 p = Packet(self.binary[sp_start:sp_end], False)
    #                 sp_start = p.build_as_subpacket()
    #                 self.sp_list.append(p)
    #             return sp_start


def part1(fname):
    with open(fname) as fp:
        line = fp.readline()
        p, x = build_packet(bstring(line.strip()))
        return p.version_sum()

def part2(fname):
    with open(fname) as fp:
        line = fp.readline()
        p, x = build_packet(bstring(line.strip()))
        return p.get_value()

def bstring(hexstring):
    #print(hexstring)
    b = bin(int(hexstring, 16))[2:]
    b = b.zfill(((len(b) + 3) // 4) * 4)
    #print(b)
    i = 0
    while hexstring[i] == '0':
        b = '0000' + b
        i += 1
    return b

def main():

    # p = build_packet(bstring('D2FE28'))
    # print(p)
    # p = build_packet('11010001010')
    # print(p)

    # p = build_packet(bstring('38006F45291200'))
    # print(p)
    # p = build_packet(bstring('EE00D40C823060'))
    # print(p[0])
    p = build_packet(bstring('9C0141080250320F1802104A08'))
    print(p[0])
    print(p[0].get_value())
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
