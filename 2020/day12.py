import sys

def navigate2(lines):
    x = 0
    y = 0
    d = 0
    wpx = 10
    wpy = 1
    for line in lines:
        if line[0] == 'N':
            wpy += int(line[1:])
        elif line[0] == 'S':
            wpy -= int(line[1:])
        elif line[0] == 'E':
            wpx += int(line[1:])
        elif line[0] == 'W':
            wpx -= int(line[1:])
        elif line[0] == 'L':
            for i in range(int(line[1:]) // 90):
                wpx, wpy = -wpy, wpx
        elif line[0] == 'R':
            for i in range(int(line[1:]) // 90):
                wpx, wpy = wpy, -wpx
        elif line[0] == 'F':
            for i in range(int(line[1:])):
                x += wpx
                y += wpy

    return abs(x) + abs(y)


def navigate(lines):
    x = 0
    y = 0
    d = 0
    for line in lines:
        if line[0] == 'N':
            y += int(line[1:])
        elif line[0] == 'S':
            y -= int(line[1:])
        elif line[0] == 'E':
            x += int(line[1:])
        elif line[0] == 'W':
            x -= int(line[1:])
        elif line[0] == 'L':
            d += (int(line[1:]) // 90)
        elif line[0] == 'R':
            d -= (int(line[1:]) // 90)
            if d < 0:
                d += 4
        elif line[0] == 'F':
            d = d % 4
            if d == 0:
                x += int(line[1:])
            elif d == 1:
                y += int(line[1:])
            elif d == 2:
                x -= int(line[1:])
            elif d == 3:
                y -= int(line[1:])

    return abs(x) + abs(y)

def main():
    lines = []
    with open(sys.argv[1], 'r') as fp:
        for line in fp:
            lines.append(line.strip())


    print(navigate2(lines))


if __name__ == '__main__':
    main()
