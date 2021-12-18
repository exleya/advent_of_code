import sys
import copy
from collections import defaultdict

class SFNode:
    def __init__(self, data, parent):
        self.parent = parent
        if isinstance(data, list):
            self.left = SFNode(data[0], self)
            self.right = SFNode(data[1], self)
            self.leaf = False
        else:
            self.num = data
            self.leaf = True

    def magnitude(self):
        if self.leaf:
            return self.num
        else:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def explode(self):
        '''fully execute the explode op by adding
            this item's left and right data to next
            left and next right, then set this to 0'''
        trailer = self
        p = self.parent
        while p != None and p.left == trailer:
            p = p.parent
            trailer = trailer.parent
        if p != None:
            if p.left.leaf:
                p.left.num += self.left.num
            else:
                p = p.left
                while not p.right.leaf:
                    p = p.right
                p.right.num += self.left.num

        trailer = self
        p = self.parent
        while p != None and p.right == trailer:
            p = p.parent
            trailer = trailer.parent
        if p != None:
            if p.right.leaf:
                p.right.num += self.right.num
            else:
                p = p.right
                while not p.left.leaf:
                    p = p.left
                p.left.num += self.right.num
        self.left = None
        self.right = None
        self.leaf = True
        self.num = 0

    def __repr__(self):
        if self.leaf:
            return str(self.num)
        else:
            return "[" + str(self.left) + "," + str(self.right) + "]"

class SFNumber:
    def __init__(self, line):
        self.root = SFNode(eval(line), None)

    def magnitude(self):
        return self.root.magnitude()

    def add(self, addend):
        left = self.root
        right = addend.root
        self.root = SFNode([0,0], None)
        self.root.left = left
        left.parent = self.root
        self.root.right = right
        right.parent = self.root

    def reduce(self):
        change = True
        while change:
            change = False
            while self.explode():
                change = True
                #print("explode: " + str(self))

            if self.split():
                change = True
                #print("split:   " + str(self))

    def split(self):
        return self.rec_split(self.root)

    def rec_split(self, node):
        if node.leaf:
            if node.num >= 10:
                node.leaf = False
                node.left = SFNode(node.num // 2, node)
                node.right = SFNode(node.num // 2 + node.num % 2, node)
                return True
            return False
        else:
            sp = self.rec_split(node.left)
            if sp:
                return True
            sp = self.rec_split(node.right)
            if sp:
                return True
            return False

    def explode(self):
        return self.rec_explode(self.root, 4)

    def rec_explode(self, node, depth):
        if depth == 0:
            if not node.leaf:
                node.explode()
                return True
        else:
            if not node.left.leaf:
                exp = self.rec_explode(node.left, depth - 1)
                if exp:
                    return True
            if not node.right.leaf:
                exp = self.rec_explode(node.right, depth - 1)
                if exp:
                    return True
            return False

    def __repr__(self):
        return str(self.root)


def part1(fname):
    with open(fname) as fp:
        lines = fp.readlines()
        nums = []
        for line in lines:
            nums.append(SFNumber(line.strip()))

        while len(nums) >= 2:
            n = nums.pop(1)
            nums[0].add(n)
            nums[0].reduce()
            print(nums[0])

        return nums[0].magnitude()


def part2(fname):
    with open(fname) as fp:
        lines = fp.readlines()
        nums = []
        for line in lines:
            nums.append(SFNumber(line.strip()))

        mmax = 0
        for i in range(len(nums)):
            for j in range(len(nums)):
                if i != j:
                    ni = copy.deepcopy(nums[i])
                    nj = copy.deepcopy(nums[j])
                    ni.add(nj)
                    ni.reduce()
                    mmax = max(ni.magnitude(), mmax)
        return mmax

def main():

    'main function'
    print(part1(sys.argv[1]))
    print(part2(sys.argv[1]))

if __name__ == '__main__':
    main()
