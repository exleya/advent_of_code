import sys

def p1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        gamma = ''
        epsilon = ''

        for pos in range(len(linelist[0]) - 1):
            fstr = ''
            for line in linelist:
                fstr += line[pos]
            if fstr.count('0') > fstr.count('1'):
                gamma += '0'
                epsilon += '1'
            else:
                gamma += '1'
                epsilon += '0'
        print(gamma)
        print(epsilon)
        gamma = int(gamma, 2)
        epsilon = int(epsilon,2)
        return gamma * epsilon

def p2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        gamma = ''
        epsilon = ''

        gammalist = linelist[:]
        epsilonlist = linelist[:]

        index = 0
        while len(gammalist) > 1:
            tot = ''
            for line in gammalist:
                tot += line[index]
            newlist = []
            if tot.count('0') > tot.count('1'):
                for line in gammalist:
                    if line[index] == '0':
                        newlist.append(line)
            else:
                for line in gammalist:
                    if line[index] == '1':
                        newlist.append(line)
            gammalist = newlist
            index += 1
        print(gammalist[0])
        index = 0
        while len(epsilonlist) > 1:
            tot = ''
            for line in epsilonlist:
                tot += line[index]
            newlist = []
            if tot.count('0') <= tot.count('1'):
                for line in epsilonlist:
                    if line[index] == '0':
                        newlist.append(line)
            else:
                for line in epsilonlist:
                    if line[index] == '1':
                        newlist.append(line)
            epsilonlist = newlist
            index += 1
        print(epsilonlist[0])
        return int(gammalist[0], 2) * int(epsilonlist[0], 2)


def main():
    'main function'    
    print(p1(sys.argv[1]))
    print(p2(sys.argv[1]))

if __name__ == '__main__':
    main()
