import sys

def main():
    with open(sys.argv[1], 'r') as fp:
        lines = fp.readlines()
        mytime = int(lines[0].strip())
        busnums = lines[1].strip().split(',')
    part1(busnums, mytime)
    part2again(lines[1])

def check_forward(buslist, index, num):
    '''given a buslist, an index and a current num to check,
    try to go to the next index by checking if that bus % num works out'''
    if index == len(buslist):
        return True
    elif num % buslist[index] != 0:
        return False
    else:
        return check_forward(buslist, index + 1, num + 1)


def part2again(line):
    line = line.strip()
    print(line)
    busints = []
    for ind,item in enumerate(line.split(',')):
        if 'x' not in item:
            busints.append((int(item), ind))
    print(busints)
    busints.sort()
    busints.reverse()
    print(busints)

    nums = relprimish(busints[0], busints[1])
    print(nums)

    diff = nums[1] - nums[0]
    newpair = (diff, diff - nums[0])
    print(newpair)
    nums = relprimish(newpair, busints[2])
    print(nums)
    pair1 = busints.pop(0)
    while len(busints) > 0:
        pair2 = busints.pop(0)

        nums = relprimish(pair1, pair2)

        pair1 = (nums[1] - nums[0], nums[1] - nums[0] - nums[0])
        print(nums)


    #largest = busints[-1]
    #second = busints[-2]
    #tposs = -largest[1]
    ##firstzero = 0
    #secondzero = 0
    #while secondzero == 0:
        #tposs += largest[0]
        #mod = (tposs + second[1]) % second[0]
#
        #if mod == 0:
            #print(f"{tposs} works for both {largest} and {second}")
            #if firstzero == 0:
                #firstzero = tposs
            #else:
                #secondzero = tposs
#
    #diff = secondzero - firstzero
    #for i in range(4):
        #print(tposs + diff)
        #tposs += diff

def relprimish(mbaseoffset, nbaseoffset):
    ''' finds the first two numbers t s.t.
        (t + moffset) % m == 0 and
        (t + noffset) % n == 0

        for peak efficiency, give m > n
    '''
    m, moffset = mbaseoffset
    n, noffset = nbaseoffset
    first0 = 0
    second0 = 0
    counter = -moffset 
    while second0 == 0:
        counter += m
        mod = (counter + noffset) % n

        if mod == 0:
            if first0 == 0:
                first0 = counter
            else:
                second0 = counter
    return first0, second0


def part2(line):
    line = line.strip()
    print(line)
    busints = []
    for ind,item in enumerate(line.split(',')):
        if 'x' not in item:
            busints.append((int(item), ind))
    print(busints)

    print(len(busints))

    i = busints[0][0]
    incamt = i ** len(busints)

    print(incamt)
    while True:
        found = True
        #thisround = []
        for ctr, off in busints:
            #thisround.append(i % ctr)
            if (i + off) % ctr != 0:
                found = False

        if found:
            return i
        i += incamt

def is_prime(n):
    # thx stackoverflow
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f+2) == 0: return False
        f += 6
    return True

def prime_factors(n):
    if is_prime(n):
        return [n]
    for i in range(2, int(n**2)):
        if n % i == 0:
            return [i] + prime_factors(n // i)
        

def part1(busnums, mytime):
    busints = []
    modints = []
    nextints = []
    minnext = 99999
    minnextbus = 99999
    for busnum in busnums:
        if busnum != 'x':
            busints.append(int(busnum))
            print(mytime % int(busnum))
            modints.append(mytime % int(busnum))
            nextints.append(busints[-1] - modints[-1])
            if nextints[-1] < minnext:
                minnext = nextints[-1]
                minnextbus = busints[-1]

    print(busints)
    print(modints)
    print(nextints)
    

    print(minnext * minnextbus)

if __name__ == '__main__':
    main()
