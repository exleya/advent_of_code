import sys

def main():
    nums = []
    for line in sys.stdin:
        rnumber = line[0:7]
        cnumber = line[7:10]
        rnumber = rnumber.replace('F', '0')
        rnumber = rnumber.replace('B', '1')
        cnumber = cnumber.replace('L', '0')
        cnumber = cnumber.replace('R', '1')
        row = int(rnumber, base=2)
        col = int(cnumber, base=2)
        nums.append(row * 8 + col)

    print(max(nums))
    nsort = sorted(nums)
    prev = 0
    for val in nsort:
        if prev != val-1:
            print(prev)
        prev = val

if __name__ == '__main__':
    main()
