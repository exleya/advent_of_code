import sys

def countchains(adapterlist, index):
    '''count all possible chains, starting from looking at removing index
    '''
    if index == len(adapterlist) - 1:
        return 1
    else:
        total = 0
        prev = adapterlist[index - 1]
        post = adapterlist[index + 1]
        if post - prev <= 3:
            shorterlist = adapterlist[:]
            shorterlist.pop(index)
            total = countchains(shorterlist, index)
        total += countchains(adapterlist, index + 1)
    return total
    

def main():
    numlist = []
    for line in sys.stdin:
        numlist.append(int(line.strip()))


    slist = sorted(numlist)
    prev = 0
    diffs = []
    slist.insert(0,0)
    slist.append(slist[-1] + 3)
    for j in slist[1:]:
        diffs.append(j - prev)
        prev = j
    print(f"ones: {diffs.count(1)}, threes: {diffs.count(3)+1}")
    inarow = [0,0,0,0,0,0,0,0,0,0,0]
    n = 0
    for j in diffs:
        if j == 1:
            n += 1
        elif j == 3:
            inarow[n] += 1
            n = 0

        
    print(diffs.count(1) * (diffs.count(3)))
    print(diffs)
    print(inarow)
    prod = 2 ** inarow[2] * 4 ** inarow[3] * 7 ** inarow[4]
    print(prod)
    #print(countchains(slist, 1))

if __name__ == '__main__':
    main()
