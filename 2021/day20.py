import sys
from collections import defaultdict

class Image:
    def __init__(self, linelist, alg, default = '.'):
        self.inf_default = default
        self.alg = alg
        self.pixels = defaultdict(lambda:default)
        for j in range(len(linelist)):
            for i in range(len(linelist[j])):
                self.pixels[(i,j)] = linelist[j][i]
        self.xmin, self.ymin = 0,0
        self.xmax, self.ymax = len(linelist[0]), len(linelist)

    def counthash(self):
        return list(self.pixels.values()).count('#')

    def __repr__(self):
        s = ''
        for j in range(self.ymax):
            for i in range(self.xmax):
                s += self.pixels[(i,j)]
            s += '\n'
        return s

    os = [(-1,-1), (0,-1), (1,-1),
          (-1,0),  (0,0),  (1, 0),
          (-1,1),  (0,1),  (1, 1)]

    def get_pixel(self, x, y):
        s = ''
        for off in Image.os:
            if self.pixels[(x+off[0], y+off[1])] == '.':
                s += '0'
            else:
                s += '1'
        return int(s, 2)

    def apply_enhancement(self):
        newimage = []
        for j in range(-2, self.ymax+2):
            newrow = ''
            for i in range(-2, self.xmax+2):
                newrow += self.alg[self.get_pixel(i,j)]
            newimage.append(newrow)

        return Image(newimage,self.alg,self.alg[self.get_pixel(-2,-2)])

def part1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        alg = linelist[0].strip()

        imagelist = []
        for line in linelist[2:]:
            imagelist.append(line.strip())
        img = Image(imagelist, alg)
        print(img)
        print(img.get_pixel(-1,-1))
        print(img.xmax, img.ymax)
        img2 = img.apply_enhancement()
        print(img2)
        print(img2.xmax, img2.ymax)
        img3 = img2.apply_enhancement()
        print(img3)
        print(img3.xmax, img3.ymax)
        return img3.counthash()

def part2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        alg = linelist[0].strip()

        imagelist = []
        for line in linelist[2:]:
            imagelist.append(line.strip())
        img = Image(imagelist, alg)
        for i in range(50):
            print(i)
            img = img.apply_enhancement()
        return img.counthash()


def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
