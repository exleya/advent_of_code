import sys

def get_masks(maskline):
    ''' take a mask line and split it into an or mask
    and an and mask'''
    mask = maskline.split('=')[1].strip()
    ormask = int(mask.replace('X', '0'), 2)
    andmask = int(mask.replace('X', '1'), 2)
    return ormask, andmask


def memcommand(memline, mem, andmask, ormask):
    '''mem is a dictionary
    '''
    loc, val = memline.split('=')
    loc = loc.strip()
    loc = int(loc[4:-1])
    val = int(val.strip())

    mem[loc] = (val & andmask) | ormask

def part1():
    with open(sys.argv[1], 'r') as fp:
        lines = fp.readlines()

    mem = {}
    for line in lines:
        if 'mask' in line:
            ormask, andmask = get_masks(line)
        else:
            memcommand(line, mem, andmask, ormask)

    print(sum(mem.values()))

def get_maskset(maskline):
    mask = maskline.split('=')[1].strip()
    maskbase = int(mask.replace('X','0'), 2)
    exes = []
    for i in range(36):
        if mask[i] == 'X':
            exes.append(2**(36 - i - 1)) 
    return maskbase, exes

def get_all_mems(baseaddr, maskset):
    ''' generate all mem locs from 'floating' mask set bits
    '''
    addrs = [baseaddr]
    for m in maskset:
        newaddrs = []
        for old in addrs:
            newaddrs.append(old | m)
            newaddrs.append(old & (~m))
        addrs = newaddrs

    return addrs

def memcommand2(memline, mem, maskbase, maskset):
    loc, val = memline.split('=')
    loc = loc.strip()
    loc = int(loc[4:-1])
    val = int(val.strip())
    
    baseloc = loc | maskbase

    for loc in get_all_mems(baseloc, maskset):
        mem[loc] = val


def part2():
    with open(sys.argv[1], 'r') as fp:
        lines = fp.readlines()

    mem = {}
    for line in lines:
        if 'mask' in line:
            maskbase, maskset = get_maskset(line)
        else:
            memcommand2(line, mem, maskbase, maskset)

    print(sum(mem.values()))
    
if __name__ == '__main__':
    part2()
    

