import sys

def foo(fname):
    with open(fname) as fp:
        prevnum = 99999
        counter = 0
        for line in fp.readlines():
            num = int(line.strip())
            if num > prevnum:
                counter += 1
            prevnum = num
    return counter


def bar(fname):
    with open(fname) as fp:
        lines = fp.readlines()
        for i in range(len(lines)):
            lines[i] = int(lines[i].strip())

        prevsum = 9999999
        counter = 0
        for i in range(len(lines)-2):
            winsum = sum(lines[i:i+3])
            if winsum > prevsum:
                counter += 1
            prevsum = winsum
    return counter

def main():
    'main function'
    print(foo(sys.argv[1]))
    print(bar(sys.argv[1]))

if __name__ == '__main__':
    main()
