import sys

def bag_explore(bd, color):
    if color not in bd:
        return set()
    else:
        ans = set(bd[color])
        for newcolor in bd[color]:
            ans = ans | bag_explore(bd, newcolor)
        return ans

def bag_fill(bt, color):
    counter = 0
    for sbcolor, count in bt[color]:
        counter += count
        if count > 0:
            counter += count * bag_fill(bt, sbcolor)
    return counter

def main():
    bagdesc = {}
    bagtree = {}
    for line in sys.stdin:
        bagval, bagkeys = line.split('bags contain')
        bagkeys = bagkeys.strip()
        bagkeys = bagkeys[:-1].split(',')
        bagval = bagval.strip()

        bagtree[bagval] = []

        for bk in bagkeys:
            bk = bk.split()
            if 'no' in bk[0]:
                count = 0
            else:
                count = int(bk[0])
            bk = bk[1] + ' ' + bk[2]
            bagtree[bagval].append((bk, count))
            bagdesc[bk] = bagdesc.get(bk, []) + [bagval]


    print(bag_fill(bagtree, 'shiny gold'))
    print(len(bag_explore(bagdesc, 'shiny gold')))

if __name__ == '__main__':
    main()
