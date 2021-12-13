import sys
from collections import defaultdict

class Cave:
    def __init__(self, name):
        self.name = name
        #self.visit = 0

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

class CaveSystem:
    def __init__(self):
        self.adjlist = defaultdict(set)
        self.ucases = []
        self.bigcavemap = {}

    def add_connection(self, cave1, cave2):
        #if cave1[0].islower() and cave2[0].islower():
        self.adjlist[Cave(cave1)].add(Cave(cave2))
        self.adjlist[Cave(cave2)].add(Cave(cave1))
        #else:
            #self.ucases.append((cave1, cave2))

    def getpaths2(self, start, end, path):
        if start == end:
            return [path]
        else:
            paths = []
            for cave in self.adjlist[start]:
                if cave.name[0].isupper() or cave not in path:
                    paths.extend(self.getpaths2(cave, end, path + [cave]))
            return paths

    def getpaths3(self, start, end, path):
        if start == end:
            return [path]
        else:
            paths = []
            for cave in self.adjlist[start]:
                if cave.name != 'start':
                    if cave.name[0].isupper():
                        paths.extend(self.getpaths3(cave, end, path + [cave]))
                    elif cave not in path:
                        paths.extend(self.getpaths3(cave, end, path + [cave]))
                    elif cave in path:
                        paths.extend(self.getpaths2(cave, end, path + [cave]))
            return paths

    def expand_ucase(self):
        print(self.ucases)
        while len(self.ucases) > 0:
            pair = self.ucases.pop()
            print("h: " + str(pair))
            if pair[0][0].isupper():
                bigcave = pair[0]
                cons = [pair[1]]
            elif pair[1][0].isupper():
                bigcave = pair[1]
                cons = [pair[0]]

            toremove = []
            for pair2 in self.ucases:
                if bigcave == pair2[0]:
                    cons.append(pair2[1])
                elif bigcave == pair2[1]:
                    cons.append(pair2[0])
                toremove.append(pair2)

            for p in toremove:
                self.ucases.remove(p)

            for i in range(len(cons)):
                for j in range(len(cons)):
                    self.add_connection(bigcave.lower() + str(i), cons[j])
                    self.bigcavemap[bigcave.lower() + str(i)] = bigcave

    def getpaths(self, start, end, path):
        if start == end:
            return [path]
        else:
            paths = []
            for cave in self.adjlist[start]:
                if cave not in path:
                    paths.extend(self.getpaths(cave, end, path + [cave]))
            return paths

def part1(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        cs = CaveSystem()
        for line in linelist:
            cave1, cave2 = line.strip().split('-')
            cs.add_connection(cave1, cave2)
        cs.expand_ucase()
        paths = cs.getpaths2(Cave('start'), Cave('end'), [Cave('start')])
        pathset = set()
        for path in paths:
            for i in range(len(path)):
                if path[i].name in cs.bigcavemap:
                    path[i] = cs.bigcavemap[path[i].name]
                else:
                    path[i] = path[i].name
            pathset.add('-'.join(path))
        return len(pathset)


def part2(fname):
    with open(fname) as fp:
        linelist = fp.readlines()
        cs = CaveSystem()
        for line in linelist:
            cave1, cave2 = line.strip().split('-')
            cs.add_connection(cave1, cave2)
        cs.expand_ucase()
        paths = cs.getpaths3(Cave('start'), Cave('end'), [Cave('start')])
        pathset = set()
        for path in paths:
            for i in range(len(path)):
                if path[i].name in cs.bigcavemap:
                    path[i] = cs.bigcavemap[path[i].name]
                else:
                    path[i] = path[i].name
            pathset.add(','.join(path))
        #for p in sorted(list(pathset)):
        #    print(p)
        return len(pathset)

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
