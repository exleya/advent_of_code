import sys
from collections import defaultdict

class DirNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.subdirs = {}
        self.files = {}
        self.parent = parent
        self.total_size = 0

    def add_file(self, name, size):
        if name not in self.files:
            self.files[name] = size
            self.total_size += size
            ptr = self.parent
            while ptr != None:
               ptr.total_size += size
               ptr = ptr.parent

    def print(self):
        print(self.name + "(" + str(self.total_size) + ")")
        for f in self.files:
            print(f + " " + str(self.files[f]))
        for d in self.subdirs.values():
            d.print()

def buildtree(fname):
    rootdir = DirNode("/")
    currentdir = rootdir
    with open(fname) as fp:
        lines = fp.readlines()
        ctr = 0
        while ctr < len(lines):
            line = lines[ctr]
            #print(currentdir)
            #print(line)
            if line[0:4] == '$ cd':
                dname = line[5:].strip()
                if dname == '/':
                    currentdir = rootdir
                elif dname == '..':
                    currentdir = currentdir.parent
                else:
                    currentdir = currentdir.subdirs[dname]
            elif line[0:4] == '$ ls':
                ctr += 1
                while ctr < len(lines) and lines[ctr][0] != '$':
                    nextline = lines[ctr]
                    if nextline[0:3] == 'dir':
                        dname = nextline[4:].strip()
                        dnode = DirNode(dname, currentdir)
                        currentdir.subdirs[dname] = dnode
                    else:
                        size, name = nextline.strip().split()
                        currentdir.add_file(name, int(size))
                    ctr += 1
                if ctr < len(lines): ctr -= 1
            else:
                print("error processing commands...")
            ctr += 1
    return rootdir

def sumsmall(tree):
    ts = tree.total_size
    if ts <= 100000:
        result = ts
    else:
        result = 0

    sum = 0
    for subdir in tree.subdirs.values():
        sum += sumsmall(subdir)

    return sum + result


def part1(fname):
    tree = buildtree(fname)
    #tree.print()
    return sumsmall(tree)

def findmindir(tree, amount):
    min = None
    if tree.total_size > amount:
        min = tree
        print(tree.name, tree.total_size)

    for subdir in tree.subdirs.values():
        sdmin = findmindir(subdir, amount)
        if min == None:
            min = sdmin
        elif sdmin != None and sdmin.total_size < min.total_size:
            min = sdmin
    return min

def part2(fname):
    tree = buildtree(fname)
    #tree.print()
    total = 70000000
    unused = total - tree.total_size
    print("unused:", unused)
    needed = 30000000 - unused
    print("needed:", needed)
    d = findmindir(tree, needed)
    print(d.name, d.total_size)
    return d.total_size

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
