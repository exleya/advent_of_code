class SeatGrid:
    def __init__(self, gridlines):
        self.gridlines = gridlines


    def step(self):
        neighbors = [(-1,-1), (-1,0), (-1,1), (0, -1), (0, 1), (1,-1), (1,0), (1,1)]
        nextgrid = []
        change = False
        for row in range(len(self.gridlines)):
            nextrow = ""
            for col in range(len(self.gridlines[row])):
                occ_neighbors = 0
                for i,j in neighbors:
                    if 0 <= row+i < len(self.gridlines) and 0 <= col+j < len(self.gridlines[i]) and \
                            self.gridlines[row + i][col + j] == '#':
                        occ_neighbors += 1

                if self.gridlines[row][col] == '#' and occ_neighbors >= 4:
                    change = True
                    nextch = 'L'
                elif self.gridlines[row][col] == 'L' and occ_neighbors == 0:
                    change = True
                    nextch = '#'
                else:
                    nextch = self.gridlines[row][col]
                nextrow += nextch
            nextgrid.append(nextrow)
        self.gridlines = nextgrid
        return change
            
    def step2(self):
        directions = [(-1,-1), (-1,0), (-1,1), (0, -1), (0, 1), (1,-1), (1,0), (1,1)]
        nextgrid = []
        change = False
        ROWS = len(self.gridlines)
        COLS = len(self.gridlines[0])
        for row in range(ROWS):
            nextrow = ""
            for col in range(COLS):
                if self.gridlines[row][col] != '.':
                    occ_vis = 0
                    for i,j in directions:
                        rr = row + i
                        cc = col + j
                        while 0 <= rr < ROWS and 0 <= cc < COLS:
                            if self.gridlines[rr][cc] == '#':
                                occ_vis += 1
                                rr = -1000
                            elif self.gridlines[rr][cc] == 'L':
                                rr = -1000
                            rr += i
                            cc += j
                    
                    if self.gridlines[row][col] == '#' and occ_vis >= 5:
                        change = True
                        nextch = 'L'
                    elif self.gridlines[row][col] == 'L' and occ_vis == 0:
                        change = True
                        nextch = '#'
                    else:
                        nextch = self.gridlines[row][col]
                else:
                    nextch = '.'
                nextrow += nextch
            nextgrid.append(nextrow)
        self.gridlines = nextgrid
        return change

    def get_occupied(self):
        occ = 0
        for row in self.gridlines:
            occ += row.count('#')
        return occ

    def print(self):
        for r in self.gridlines:
            print(r)

import sys

def main():
    initlines = []
    with open(sys.argv[1],'r') as fp:
        for line in fp:
            initlines.append(line.strip())
    s = SeatGrid(initlines)
    
    change = s.step2()
    s.print()
    while change:
        print('-' * 20)
        change = s.step2()
        s.print()
    print(s.get_occupied())


if __name__ == '__main__':
    main()
