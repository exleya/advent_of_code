import sys

class BingoBoard:
    def __init__(self, fivelines):
        '''fivelines is a list of strings?'''
        self.board = []
        for line in fivelines:
            nums = line.split()
            for i in range(len(nums)):
                nums[i] = [int(nums[i]), False]
            self.board.append(nums)

    def mark(self, num):
        for row in self.board:
            for item in row:
                if item[0] == num:
                    item[1] = True

    def __repr__(self):
        s = ''
        for col in range(len(self.board)):
            for row in range(len(self.board)):
                if self.board[col][row][1]:
                    s += '*'
                else:
                    s += ' '
                s += '{x:02d} '.format(x=self.board[col][row][0])
            s += '\n'
        return s

    def winner(self):
        colcount = [0]*5
        rowcount = [0]*5
        for col in range(len(self.board)):
            for row in range(len(self.board)):
                if self.board[col][row][1] == True:
                    colcount[col] += 1
                    rowcount[row] += 1
        for i in range(len(colcount)):
            if colcount[i] == 5 or rowcount[i] == 5:
                return True
        return False

    def winsum(self):
        colcount = [0]*5
        rowcount = [0]*5
        for col in range(len(self.board)):
            for row in range(len(self.board)):
                if self.board[col][row][1] == True:
                    colcount[col] += 1
                    rowcount[row] += 1
        total = 0
        for col in range(len(self.board)):
            for row in range(len(self.board)):
                if self.board[col][row][1] == False:
                    total += self.board[col][row][0]
        return total
            


def p1(fname):
    with open(fname) as fp:
        nums = fp.readline()
        rest = fp.readlines()
        boardlist = []
        for i in range(0, len(rest), 6):
            boardlist.append(BingoBoard(rest[i+1:i+6]))

        nums = nums.split(',')
        for i in range(len(nums)):
            nums[i] = int(nums[i])

        for var in nums:
            print(var)
            for board in boardlist:
                board.mark(var)
                if board.winner():
                    print('winner!')
                    print(board)
                    return board.winsum() * var

def p2(fname):
    with open(fname) as fp:
        nums = fp.readline()
        rest = fp.readlines()
        boardlist = []
        for i in range(0, len(rest), 6):
            boardlist.append(BingoBoard(rest[i+1:i+6]))

        nums = nums.split(',')
        for i in range(len(nums)):
            nums[i] = int(nums[i])

        for var in nums:
            print(var)
            toremove = []
            for board in boardlist:
                board.mark(var)
                if board.winner():
                    if len(boardlist) == 1:
                        print(boardlist[0])
                        return boardlist[0].winsum() * var
                    print('removing board:')
                    print(board)
                    toremove.append(board)
            for board in toremove:
                boardlist.remove(board)


def main():
    'main function'    
    print(p1(sys.argv[1]))
    print(p2(sys.argv[1]))

if __name__ == '__main__':
    main()
