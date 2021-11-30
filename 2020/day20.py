import sys

def revstr(s):
    r = ""
    for c in s:
        r = c + r
    return r

class Tile:
    def __init__(self, num, rows):
        self.num = num
        self.rows = rows
        # the number of things this can connect to...
        self.valence = 0
        
        leftedge = ''
        rightedge = ''
        for row in rows:
            leftedge += row[0]
            rightedge += row[-1]

        # index 0 = top, then clockwise, also read them clockwise
        self.edges =      [rows[0], rightedge, revstr(rows[-1]), revstr(leftedge)]
        self.flipedges = [revstr(rows[0]), leftedge, rows[-1], revstr(rightedge)]
        self.edgeposs = set()
        self.edgeposs.update(set(self.edges))
        self.edgeposs.update(set(self.flipedges))

        self.otheredges = set()
        

    def __repr__(self):
        return f"Tile {self.num}, {self.edges}"

    def __hash__(self):
        return self.num

    def to_print(self):
        s = f"Tile: {self.num}\n"
        for row in self.rows:
            s += row + "\n"
        return s

    def orient(self, edge, side):
        '''change the orientation of this tile so that the given
        edge is on the given side 0 = top, 1 = right, etc.
        '''
        if edge in self.flipedges:
            self.edges, self.flipedges = self.flipedges, self.edges
            self._lrfliprows()

        diff = self.edges.index(edge) - side
        #print(f"{diff}, {side}, {self.edges.index(edge)}")
        if diff < 0:
            diff += 4
        for i in range(diff):
            self.edges.append(self.edges.pop(0))
            self._leftrotrows()

    def _lrfliprows(self):
        for i in range(len(self.rows)):
            self.rows[i] = revstr(self.rows[i])

    def _leftrotrows(self):
        '''left-rotate the self.rows stuff
        '''
        N = len(self.rows)
        newrows = ["" for i in range(N)]
        for i in range(N):
            newrows[0] += self.rows[i][-1]
            newrows[1] += self.rows[i][-2]
            newrows[2] += self.rows[i][-3]
            newrows[3] += self.rows[i][-4]
            newrows[4] += self.rows[i][-5]
            newrows[5] += self.rows[i][-6]
            newrows[6] += self.rows[i][-7]
            newrows[7] += self.rows[i][-8]
            newrows[8] += self.rows[i][-9]
            newrows[9] += self.rows[i][-10]
        self.rows = newrows
    
    def __lt__(self, other):
        return self.num < other.num


def generate_search_order():
    inds = []
    for i in range(12):
        for j in range(0,i+1):
            inds.append(i + 11 * j)

    downctr = 11
    for i in range(23, 144, 12):
        for j in range(0, downctr):
            inds.append(i + 11 * j)
        downctr -= 1
    return inds

search_order = [4, 3, 1, 0, 5, 2, 7, 6, 8]

def rec_search(grid, tilelist):
    if None not in grid:
        return grid

    compare_to = []
    for i in generate_search_order():
        if grid[i] == None:
            index = i
            break

    tomatch = []
    matchorient = []
    if index >= 12:
        tomatch.append(revstr(grid[index-12].edges[2]))
        matchorient.append(0)
    elif index % 12 != 0:
        tomatch.append(revstr(grid[index-1].edges[1]))
        matchorient.append(3)
        
    for tile in tilelist:
        if len(tomatch) == 1 and tomatch[0] in tile.edgeposs:
            tile.orient(tomatch[0], matchorient[0])
            grid[index] = tile
            tiles = tilelist[:]
            tiles.remove(tile)
            ans = rec_search(grid, tiles)
            if ans != None:
                return ans
            grid[index] = None
        elif tomatch[0] in tile.edgeposs and tomatch[1] in tile.edgeposs:
            tile.orient(matchorient[0])
            if tile.edges(matchorient[1]) == tomatch[1]:
                grid[index] = tile
                tiles = tilelist[:]
                tiles.remove(tile)
                ans = rec_search(grid, tiles)
                if ans != None:
                    return ans
                grid[index] = None
        #print(f"Could not match {tomatch}")
        # we looked at all the tiles, found no solution :(
    return None

def search(tilelist, first):
    # top level is special, we should always choose orientation 0 unflipped
    # in middle spot, all other tiles can be oriented relative to this one

    grid = [None] * len(tilelist)

    answers = []

    tiles = tilelist[:]
    tiles.remove(first)

    grid[0] = first

    #ok fortunately, the initial tile is in a good orientation
    ans = rec_search(grid, tiles)

    return ans

def printgrid(grid):
    for i in range(0,7, 3):
        print(f"{grid[i].edges[0]} {grid[i+1].edges[0]} {grid[i+2].edges[0]}")
        for j in range(1,9):
            tilenum = "    "
            if j == 3:
                tilenum = str(grid[i].num)
            print(f"{revstr(grid[i].edges[3])[j]}  {tilenum}  {grid[i].edges[1][j]} ", end='')

            if j == 3:
                tilenum = str(grid[i+1].num)
            print(f"{revstr(grid[i+1].edges[3])[j]}  {tilenum}  {grid[i+1].edges[1][j]} ", end='')

            if j == 3:
                tilenum = str(grid[i+2].num)
            print(f"{revstr(grid[i+2].edges[3])[j]}  {tilenum}  {grid[i+2].edges[1][j]}")

        print(f"{revstr(grid[i].edges[2])} {revstr(grid[i+1].edges[2])} {revstr(grid[i+2].edges[2])}")
        print()


def printgrid2(grid, gridlen):
    for i in range(0, gridlen):
        for r in range(0, 10):
            for j in range(0, gridlen):
                print(f"{grid[i*gridlen + j].rows[r]} ", end = '')
            print()
        print()

def create_pic(grid, gridlen):
    picstr = ''
    for i in range(0, gridlen):
        for r in range(1, 9):
            for j in range(0, gridlen):
                picstr += f"{grid[i*gridlen+j].rows[r][1:-1]}"
            picstr+='\n'
    return picstr

def overwrite(line, subline, index):
    newline = line[:index]
    for i in range(len(subline)):
        if subline[i] == '#' and line[index + i] in '#O':
            newline += 'O'
        else:
            newline += line[index + i]
    newline += line[index+len(subline):]
    assert len(newline) == len(line), 'error in overwrite, lengths differ'
    return newline
    
def overlay(big, sm):
    '''look for matches of sm in big, where matches are, 
    translate # to O. (O also matches)
    
    both big, sm are a list of strs

    '''
    for i in range(len(big) - len(sm) + 1):
        for j in range(len(big[0]) - len(sm[0]) + 1):
            match = True
            for ii in range(len(sm)):
                for jj in range(len(sm[ii])):
                    if sm[ii][jj] == '#' and big[i+ii][j+jj] not in '#O':
                        match = False
            
            if match:
                for ii in range(len(sm)):
                    big[i+ii] = overwrite(big[i+ii], sm[ii], j)

def main():
    with open(sys.argv[1], 'r') as fp:
        lines = fp.readlines()

    tiles = []
    tilerows = []
    for line in lines:
        if 'Tile' in line:
            tilenum = line.strip()[:-1]
            tilenum = int(tilenum.split()[1])
        elif line == '\n':
            tiles.append(Tile(tilenum, tilerows))
            tilerows = []
        else:
            tilerows.append(line.strip())
    tiles.append(Tile(tilenum, tilerows))

    matchcount = {}
    for i in range(len(tiles)):
        tile = tiles[i]
        foundcount = 0
        for edge in tile.edgeposs:
            found = False
            j = 0
            while j < len(tiles) and not found:
                if i != j and edge in tiles[j].edgeposs:
                    tile.otheredges.add(edge)
                    foundcount += 1
                    found = True
                j += 1
        matchcount[tile] = foundcount

    counts = []
    for k,v  in matchcount.items():
        counts.append((v,k))

    counts.sort()

    print(counts[0][1].num * counts[1][1].num * counts[2][1].num * counts[3][1].num)
    grid = search(tiles, counts[0][1])

    #printgrid2(grid, 12)
    pic = create_pic(grid, 12)
    #print(pic)

    img = pic.split('\n')
    if img[-1] == '':
        img = img[:-1]

    subimg = ["                  # ",
              "#    ##    ##    ###", 
              " #  #  #  #  #  #   "]
    overlay(img, subimg)
    subimgf = [revstr(line) for line in subimg]
    overlay(img, subimgf)

    subimg.reverse()
    overlay(img, subimg)

    subimgf.reverse()
    overlay(img, subimgf)

    subimg2 = [" # ",
               "#  ",
               "   ",
               "   ",
               "#  ",
               " # ",
               " # ",
               "#  ",
               "   ",
               "   ",
               "#  ",
               " # ",
               " # ",
               "#  ",
               "   ",
               "   ",
               "#  ",
               " # ",
               " ##",
               " # "]

    overlay(img, subimg2)
    subimg2f = [revstr(line) for line in subimg2]
    overlay(img, subimg2f)
    subimg2.reverse()
    overlay(img, subimg2)
    subimg2f.reverse()
    overlay(img, subimg2f)
    
    total = 0 
    for line in img:
        #print(line)
        total += line.count('#')

    print(total)

if __name__ == '__main__':
    main()
