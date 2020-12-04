import sys


def validate(passportstr):
    kvpairs = passportstr.split()
    pd = {}
    for pair in kvpairs:
        key, value = pair.split(':')
        pd[key] = value

    return ('byr' in pd and 
            'iyr' in pd and 
            'eyr' in pd and
            'hgt' in pd and
            'hcl' in pd and
            'ecl' in pd and
            'pid' in pd)


def bound(dct, key, lowval, hival):
    if key not in dct:
        return False
    return lowval <= int(dct[key]) <= hival

def valhair(hairstr):
    if len(hairstr) != 7:
        return False
    if hairstr[0] != '#':
        return False

    for c in hairstr[1:]:
        if c not in '1234567890abcdefg':
            return False
    return True

def validate2(passportstr):
    kvpairs = passportstr.split()
    pd = {}
    for pair in kvpairs:
        key, value = pair.split(':')
        pd[key] = value
    
    result = True
    result = result and bound(pd, 'byr', 1920, 2002)
    result = result and bound(pd, 'iyr', 2010, 2020)
    result = result and bound(pd, 'eyr', 2020, 2030)
    if 'hgt' not in pd:
        return False
    if 'cm' in pd['hgt']:
        pd['hgtcm'] = pd['hgt'][:-2]
        result = result and bound(pd, 'hgtcm', 150, 193)
    else:
        pd['hgtin'] = pd['hgt'][:-2]
        result = result and bound(pd, 'hgtin', 59, 76)

    if 'hcl' not in pd:
        return False
    hcl = pd['hcl']
    result = result and valhair(hcl) 

    if 'ecl' not in pd:
        return False
    result = result and (pd['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])

    if 'pid' not in pd:
        return False
    if len(pd['pid']) != 9:
        return False
    for c in pd['pid']:
        if c not in '1234567890':
            return False
    
    return result

def part1(lines):
    passport = ""
    validcount = 0
    for line in lines:
        if line.strip() != "":
            passport += line
        else:
            if validate2(passport):
                validcount += 1
            passport = ""

    if validate2(passport):
        validcount += 1
    return validcount

def main():
    filelines = sys.stdin.readlines()
    print(part1(filelines))

if __name__ == '__main__':
    main()
