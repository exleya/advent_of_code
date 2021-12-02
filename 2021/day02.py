import sys

def p1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        hor, depth = 0, 0
        for line in linelist:
            if 'forward' in line:
                amt = int(line.split()[1])
                hor += amt
            elif 'down' in line:
                amt = int(line.split()[1])
                depth += amt
            elif 'up' in line:
                amt = int(line.split()[1])
                depth -= amt
    return depth* hor

def p2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        hor, depth, aim = 0, 0, 0
        for line in linelist:
            if 'forward' in line:
                amt = int(line.split()[1])
                hor += amt
                depth += aim*amt
            elif 'down' in line:
                amt = int(line.split()[1])
                aim += amt
            elif 'up' in line:
                amt = int(line.split()[1])
                aim -= amt
    return depth* hor


def main():
    'main function'    
    print(p1(sys.argv[1]))
    print(p2(sys.argv[1]))

if __name__ == '__main__':
    main()
