import sys
from collections import defaultdict

def part1(fname):
    with open(fname) as fp:
        completeoverlap = 0
        partialoverlap = 0
        for line in fp:
            line = line.split(',')
            ff, fs = line[0].split('-')
            sf, ss = line[1].split('-')
            ff = int(ff)
            fs = int(fs)
            sf = int(sf)
            ss = int(ss)
            if ff <= sf and ss <= fs:
                completeoverlap += 1
            elif sf <= ff and fs <= ss:
                completeoverlap += 1

            if sf <= ff <= ss:
                partialoverlap += 1
            elif sf <= fs <= ss:
                partialoverlap += 1
            elif ff <= sf <= fs:
                partialoverlap += 1
            elif ff <= ss <= fs:
                partialoverlap += 1
        return completeoverlap, partialoverlap

def findcommonletter(s1,s2,s3):
    for ch in s1:
        if ch in s2 and ch in s3:
            return ch



def main():
    'main function'
    print(part1(sys.argv[1]))
    #print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
