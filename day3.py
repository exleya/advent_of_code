import sys

def main():
    lines = sys.stdin.readlines()
    v1 = slope(lines, 1,1)
    print(v1)
    v2 = slope(lines, 3,1)
    print(v2)
    v3 = slope(lines, 5,1)
    print(v3)
    v4 = slope(lines, 7,1)
    print(v4)
    v5 = slope(lines, 1,2)
    print(v5)
    print(v1*v2*v3*v4*v5)

def slope(lines, dx, dy):
    y = 0
    x = 0
    treecount = 0
    while y < len(lines):
        line = lines[y].strip()
        if line[x % len(line)] == '#':
            treecount += 1
        y += dy
        x += dx

    return treecount

if __name__ == '__main__':
    main()
