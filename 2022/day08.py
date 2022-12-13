import sys
from collections import defaultdict


def part1(fname):
    grid = []
    visgrid = []
    with open(fname) as fp:
        for line in fp:
            grid.append(line.strip())

        visgrid = [[False for i in range(len(grid[0]))]
                        for j in range(len(grid))]

        #from top and bottom
        for col in range(len(grid[0])):
            topch = grid[0][col]
            botch = grid[-1][col]
            visgrid[0][col] = True
            visgrid[-1][col] = True
            for row in range(1, len(grid)):
                if grid[row][col] > topch:
                    visgrid[row][col] = True
                topch = max(grid[row][col],topch)

                if grid[-(row+1)][col] > botch:
                    visgrid[-(row+1)][col] = True
                botch = max(grid[-(row+1)][col],botch)


        # from left and right
        for row in range(len(grid)):
            leftch = grid[row][0]
            rightch = grid[row][-1]
            visgrid[row][0] = True
            visgrid[row][-1] = True
            for col in range(1,len(grid[0])):
                if grid[row][col] > leftch:
                    visgrid[row][col] = True
                leftch = max(grid[row][col],leftch)

                if grid[row][-(col+1)] > rightch:
                    visgrid[row][-(col+1)] = True
                rightch = max(grid[row][-(col+1)],rightch)
        #print(visgrid)
        count = 0
        for i in range(len(visgrid)):
            for j in visgrid[i]:
                if j: count += 1
        return count

def scenicscore(grid, row, col):
    scoreup = 0
    scoredown = 0
    scoreleft = 0
    scoreright = 0
    i = col - 1
    height = grid[row][col]
    while i >= 0:
        if grid[row][i] >= height:
            scoreleft = (col - i)
            i = -1
        i -= 1
    if scoreleft == 0: scoreleft = col

    i = col + 1
    while i < len(grid[row]):
        if grid[row][i] >= height:
            scoreright = (i - col)
            i = len(grid[row])
        i += 1
    if scoreright == 0: scoreright = len(grid[row]) - col - 1

    i = row - 1
    while i >= 0:
        if grid[i][col] >= height:
            scoreup = (row - i)
            i = -1
        i -= 1
    if scoreup == 0: scoreup = row

    i = row + 1
    while i < len(grid):
        if grid[i][col] >= height:
            scoredown = (i - row)
            i = len(grid)
        i += 1
    if scoredown == 0: scoredown = len(grid) - row - 1

    score = scoreup * scoredown * scoreleft * scoreright
    #print(row,col,scoreup, scoredown, scoreleft, scoreright)
    return score

def part2(fname):
    grid = []
    with open(fname) as fp:
        for line in fp:
            grid.append(line.strip())

    score = 0
    for row in range(1, len(grid)-1):
        for col in range(1, len(grid[0])-1):
            score = max(score, scenicscore(grid, row, col))
    return score

def main():
    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
