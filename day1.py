
import sys

def main():
    numlist = []
    for line in sys.stdin:
        curr = int(line.strip())
        for vali in range(len(numlist)):
            if curr + numlist[vali] == 2020:
                print(curr * numlist[vali])
            for vali2 in range(len(numlist)):
                if vali != vali2 and curr + numlist[vali] + numlist[vali2] == 2020:
                    print(curr * numlist[vali] * numlist[vali2])
        numlist.append(curr)



if __name__ == '__main__':
    main()
