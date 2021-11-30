import sys
from collections import OrderedDict

class CupList:
    def __init__(self, initlist):
        self.d = {}
        self.max = max(initlist)
        for i in range(len(initlist)):
            self.d[initlist[i]] = initlist[(i+1)%len(initlist)]
        self.current = initlist[0]

    def print(self):
        cur = self.current
        for i in range(len(self.d)):
            if cur == self.current:
                print(f"({cur}) ", end = "")
            else:
                print(f"{cur} ", end = "")
            cur = self.d[cur]
        print()

    def move3(self):
        '''move 3 cups, starting from immediately after self.current

        index current+1, going to index that is the N-1, where N is the label of self.current,
        taking care to move them the least amount
        this is still O(n) seems like I need to do better than that.

        if cup relocation alters current, update it so that it is still
        referring to the same item
        '''
        #self.print()
        target = self.current - 1
        if target < 1:
            target = self.max

        cup1val = self.d[self.current]
        cup2val = self.d[cup1val]
        cup3val = self.d[cup2val]

        # remove the three cups
        self.d[self.current] = self.d[cup3val]

        #print(f"cups: {self.d}")
        #print(f"pickup: {cup1val}, {cup2val}, {cup3val}")
        #print(f"from: {self.current}")
        while (target == cup1val or 
               target == cup2val or
               target == cup3val):
            target -= 1
            if target < 1:
                target = self.max
        #print(f"to  : {target}")

        self.d[cup3val] = self.d[target]
        self.d[target] = cup1val


        self.current = self.d[self.current]
        #self.print()
            
    def cur_label(self):
        return self.d[self.current]

def play_game2(cups, moves):
    cl = CupList(cups)
    for i in range(moves):
        #if i % 100000 == 0:
        #    print(f"---- move {i} ----")
        cl.move3()
        #input()
        

    return cl.d[1] * cl.d[cl.d[1]]

def play_game1(cups, moves):

    maxcup = max(cups)
    current = 0
    for i in range(moves):
        if i % 100000 == 0:
            print(f"---- move {i} ----")
        currentlabel = cups[current]
        #print(f"cups: {cups} ({currentlabel})")
        pickup = []
        for j in range(3):
            if current+1 >= len(cups):
                pickup.append(cups.pop(0))
            else:
                pickup.append(cups.pop(current+1))

        destlabel = currentlabel - 1
        if destlabel < 1:
            destlabel = maxcup
        while destlabel in pickup:
            destlabel -= 1
            if destlabel < 1:
                destlabel = maxcup 

        dest = cups.index(destlabel)
        #print(f"pickup: {pickup}")
        #print(f"destlabel: {destlabel}")
        if dest+1 == len(cups):
            cups.insert(dest+1, pickup.pop(0))
            cups.insert(dest+2, pickup.pop(0))
            cups.insert(dest+3, pickup.pop(0))
        else:
            cups.insert((dest+1)%len(cups), pickup.pop(0))
            cups.insert((dest+2)%len(cups), pickup.pop(0))
            cups.insert((dest+3)%len(cups), pickup.pop(0))
        
        #print(cups)
        if currentlabel != cups[current]:
            #print(f"{cups.index(currentlabel)}, {current}")
            while cups.index(currentlabel) < current:
                cups.insert(0, cups.pop(len(cups)-1))  
            while cups.index(currentlabel) > current:
                cups.append(cups.pop(0))

        #print(cups, pickup, destlabel)
        #print()
        current = (current + 1) % len(cups)
    return cups

def main():
    cups = [int(c) for c in "389125467"]
    print(play_game2(cups, 10))

    cups = [int(c) for c in "872495136"]
    #print(play_game2(cups, 100))

    cups.extend(list(range(10,1000001))) 

    print(play_game2(cups, 10000000))

    #print(ans[ans.index(1):ans.index(1)+3])
    #print(ans[ans.index(1)+1] * ans[ans.index(1)+2])

if __name__ == '__main__':
    main()
