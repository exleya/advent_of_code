import sys
from collections import defaultdict

# witness my embarassing code!


def part1(fname):
    with open(fname) as fp:
        displist = []
        for line in fp:
            tup = line.split('|')
            displist.append((tup[0].strip().split(), tup[1].strip().split()))

        counter = 0
        for disp, output in displist:
            for outdig in output:
                if len(outdig) in [2,3,4,7]:
                    counter += 1
        return counter

class Mapping:
    unswitched = {
        0: 'abcefg',
        1: 'cf',
        2: 'acdeg',
        3: 'acdfg',
        4: 'bcdf',
        5: 'abdfg',
        6: 'abdefg',
        7: 'acf',
        8: 'abcdefg',
        9: 'abcdfg'
    }

    revus = {
        'abcefg':0,
        'cf'    :1,
        'acdeg' :2,
        'acdfg' :3,
        'bcdf'  :4,
        'abdfg' :5,
        'abdefg':6,
        'acf'   :7,
        'abcdefg':8,
        'abcdfg':9

    }

    segnums = {
        2: 'cf',
        3: 'acf',
        4: 'bcdf',
        5: 'abcdefg', # 2, 3, 5
        6: 'abcdefg', # 0, 6, 9
        7: 'abcdefg'  # 
        }


    def __init__(self):
        segs = 'abcdefg'
        self.orig_to_new = {}
        for orig in segs:
            self.orig_to_new[orig] = set(segs)
        self.mappings = None

    def generate_mappings(self):
        if self.mappings == None:
            self.mappings = []
            for repa in self.orig_to_new['a']:
                for repb in self.orig_to_new['b']:
                    for repc in self.orig_to_new['c']:
                        for repd in self.orig_to_new['d']-set(repb):
                            for repe in self.orig_to_new['e']:
                                for repf in self.orig_to_new['f']-set(repc):
                                    for repg in self.orig_to_new['g']-set(repe):
                                        self.mappings.append({'a': repa, 
                                        'b':repb,
                                        'c':repc,
                                        'd':repd,
                                        'e':repe,
                                        'f':repf,
                                        'g':repg})
        return self.mappings

    def apply(self, pattern, mapping):
        out = []
        for c in pattern:
            out.append(str(mapping[c]))
        out.sort()
        return ''.join(out)

    def revapply(self, pattern, mapping):
        out = []
        for c in pattern:
            for k,v in mapping.items():
                if v == c:
                    out.append(str(k))

        out.sort()
        return ''.join(out)

    def add_pattern(self, pattern):
        if len(pattern) == 2:
            for c in Mapping.segnums[2]:
                self.orig_to_new[c] = set(pattern)
            for c in 'eg':
                self.orig_to_new[c] -= self.orig_to_new['c']
        elif len(pattern) == 3:
            self.orig_to_new['a'] = set(pattern) - self.orig_to_new['c']
            for c in 'bcdefg':
                self.orig_to_new[c] -= set(self.orig_to_new['a'])
        elif len(pattern) == 4:
            self.orig_to_new['b'] = set(pattern) - self.orig_to_new['c']
            self.orig_to_new['d'] = set(pattern) - self.orig_to_new['c']
            for c in 'acefg':
                self.orig_to_new[c] -= set(self.orig_to_new['b'])
        else:
            toremove = []
            for mapping in self.generate_mappings():
                #print(mapping)
                #print('trying to match pattern:')
                #print(pattern)
                spattern = ''.join(sorted(list(pattern)))
                found = False
                for val in Mapping.unswitched.values():
                    if len(val) == len(pattern):
                        #print(val)
                        result = self.apply(val, mapping)
                        #print(result)
                        if result == spattern:
                            found = True
                            break
                if not found:
                    toremove.append(mapping)
            for tr in toremove:
                self.mappings.remove(tr)

def part2(fname):

    with open(fname) as fp:
        total = 0
        for line in fp:
            tup = line.split('|')
            patterns = tup[0].split()
            patterns.sort(key=lambda x: len(x))
            
            mp = Mapping()
            for pat in patterns:
                mp.add_pattern(pat)
            #print(mp.orig_to_new)
            #print(mp.generate_mappings())
            if len(mp.generate_mappings()) == 1:
                mapping = mp.generate_mappings()[0]
                digits = tup[1].split()
                #print(digits)
                num = ''
                for d in digits:
                    num += str(Mapping.revus[mp.revapply(d, mapping)])
                total += int(num)
            else:
                print('Damn!')
        return total


def main():
    'main function'    
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
