import sys

def sum_two(win, val):
    for i in range(len(win) - 1):
        for j in range(i+1, len(win)):
            if win[i] + win[j] == val:
                return True
    return False

def window(numlist, winlen):
    win = []
    for i in range(winlen):
        win.append(numlist[i])

    for val in numlist[winlen:]:
        if not sum_two(win, val):
            return val
        else:
            win.append(val)
            win.pop(0)

    return -1


def consecutive_sum(numlist, target):
    for i in range(len(numlist)):
        for j in range(i+1, len(numlist)):
            consec_sum = sum(numlist[i:j])
            if consec_sum == target:
                return i,j
    return -1

def main():
    numlist = []
    for line in sys.stdin:
        numlist.append(int(line.strip()))

    #print(window(numlist, 5))

    i,j = consecutive_sum(numlist, 373803594)
    print(min(numlist[i:j]) + max(numlist[i:j]))
    #print(consecutive_sum(numlist, 127))

main()
