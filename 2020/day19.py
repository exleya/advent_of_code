import sys

class TableRule:
    '''Represents a rule from our grammar when building our table.
    RHS are also references to rules, not strings, unless this is
    a terminal rule
    '''
    def __init__(self, lhs, rhs1, rhs2=None):
        self.lhs = lhs
        self.rhs1 = rhs1
        self.rhs2 = rhs2

    def terminal(self):
        return isinstance(self.rhs1, str)

    def __repr__(self):
        if self.rhs2:
            return '%s -> %s %s' % (self.lhs, self.rhs1.lhs, self.rhs2.lhs)
        elif isinstance(self.rhs1, str):
            return '%s -> %s' % (self.lhs, self.rhs1)
        else:
            return '%s -> %s' % (self.lhs, self.rhs1.lhs)

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs1 == other.rhs1 and self.rhs2 == other.rhs2

class TableEntry:
    '''Container object for our table entries

    '''
    def __init__(self):
        self._list = []

    def add_rule(self, lhs, rhs1, rhs2):
        '''adds the rules
            lhs -> rhs1 rhs2 and the indexes of where to find the subrules
            to this table entry
        '''
        assert (isinstance(lhs, str)  and isinstance(rhs1, TableRule) and
            isinstance(rhs2, TableRule)), 'Rules must be strs'

        self._list.append(TableRule(lhs, rhs1, rhs2))

    def add_unary_rule(self, lhs, rhs):
        self._list.append(TableRule(lhs, rhs))

    def get_productions(self):
        retlist = []
        for item in self._list:
            retlist.append(item.lhs)
        return retlist

    def get_rules(self):
        return self._list

    def __repr__(self):
        st = '(  '
        for tr in self._list:
           st += str(tr) + ', '
        return st[:-2] + ')'

def find_rules(te1, te2, grammar):
    ''' build a list of rules from grammar that
        can be used to span te1 and te2'''
    assert isinstance(te1, TableEntry) and isinstance(te2, TableEntry)
    rulelist = []
    #print(f"looking for a rule to handle {te1} and {te2}")
    for rule1 in te1.get_rules():
        for rule2 in te2.get_rules():
            for nt in grammar.rhs_ntlookup(rule1.lhs, rule2.lhs):
                rulelist.append(TableRule(nt, rule1, rule2))
    return rulelist

def recursive_unaries(te, gr):
    '''search through the nonterminal unary productions in gr and
    recursively add to te if appropriate'''
    updated = True
    ntu = gr.get_nt_unaries()
    while updated:
        updated = False
        for rule in te.get_rules():
            for lhs in ntu:
                for rhs in ntu[lhs]:
                    if rhs == rule.lhs and TableRule(lhs, rule) not in te._list:
                        te.add_unary_rule(lhs, rule)
                        updated = True

def ckyparse(sentence, grammar):
    '''
    return parse trees for the given sentence
    '''
    assert isinstance(sentence, list)

    N = len(sentence)

    #print(sentence)
    # initialize table
    table = []
    for i in range(N+1):
        table.append([])
        for j in range(N+1):
            table[i].append(TableEntry())

    # CKY algorithm
    for j in range(1, N+1):
        # add unaries
        nts = grammar.rhs_tlookup(sentence[j-1])
        for nt in nts:
            table[j-1][j].add_unary_rule(nt, sentence[j-1])

        recursive_unaries(table[j-1][j], grammar)
        #print(table[j-1])
        #print(f"{j-1},{j}:{table[j-1][j]}")

        # i loop
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                rules = find_rules(table[i][k], table[k][j], grammar)
                for rule in rules:
                    table[i][j].add_rule(rule.lhs, rule.rhs1, rule.rhs2)

            recursive_unaries(table[i][j], grammar)
            #print(table[i])
    #print_parse(table)
    #print(table[0][N].get_productions())
    for rule in table[0][-1].get_rules():
        if rule.lhs == '0':
            return True
    return False

def print_parse(ckytable):
    N = len(ckytable) - 1
    for rule in ckytable[0][N].get_rules():
        if rule.lhs == '0':
            rec_print_tree(rule)

def rec_print_tree(rule, depth=0):
    if isinstance(rule, str):
        print(rule, end='')
        return
    print(('\t'*depth) + '(' + str(rule.lhs) + '\t', end='')
    rec_print_tree(rule.rhs1)
    if rule.rhs2:
        rec_print_tree(rule.rhs2, depth+1)
    print(('\t' * (depth+1)) + ')')

class Grammar:
    def __init__(self):
        self._ntrules = {}
        self._trules = {}
        self._ntunary = {}

    def add_rule(self, line):
        line = line.strip()
        sp = line.split(':')
        lhs = sp[0].strip()
        rhs = sp[1]
        if '"' in rhs:
            self._add_terminal(lhs, rhs.replace('"','').strip())
        elif '|' in rhs:
            self.add_rule(lhs +': '+ rhs.split('|')[0])
            self.add_rule(lhs +': '+ rhs.split('|')[1])
        elif len(rhs.strip().split()) == 1:
            self._add_unary(lhs, rhs.strip())
        else:
            self._add_nt(lhs, rhs)

    def _add_terminal(self, lhs, rhs):
        if lhs not in self._trules:
            self._trules[lhs] = []
        self._trules[lhs].append(rhs)


    def _add_nt(self, lhs, rhs):
        if lhs not in self._ntrules:
            self._ntrules[lhs] = []
        r1, r2 = rhs.strip().split()
        self._ntrules[lhs].append((r1, r2))

    def _add_unary(self, lhs, rhs):
        if lhs not in self._ntunary:
            self._ntunary[lhs] = []
        self._ntunary[lhs].append(rhs.strip())

    def get_nt_unaries(self):
        return self._ntunary

    def get_nt_rules(self, lhs):
        r1 = []
        if lhs in self._ntrules:
            r1 = self._ntrules[lhs]

        r2 = []
        if lhs in self._ntunary[lhs]:
            r2 = self._ntunary[lhs]

        return r1 + r2

    def rhs_ntlookup(self, rhs1, rhs2):
        retlist = []
        for nt in self._ntrules:
            for rhstup in self._ntrules[nt]:
                if rhstup[0] == rhs1 and rhstup[1] == rhs2:
                    retlist.append(nt)
        return retlist
        

    def rhs_tlookup(self, rhs):
        '''lookup based on rhs terminal rule

            Return value: list of possible lhs
        '''
        retlist = []
        for nt in self._trules:
            if rhs in self._trules[nt]:
                retlist.append(nt)

        return retlist
    
    def __str__(self):
        outstr = ''
        for lhs in self._ntrules:
            for rhstup in self._ntrules[lhs]:
                outstr += "%s -> %2s %2s\n" % (lhs, rhstup[0], rhstup[1])

        for lhs in self._ntunary:
            for rhs in self._ntunary[lhs]:
                outstr += "%s -> %s\n" % (lhs, rhs)

        for lhs in self._trules:
            for rhs in self._trules[lhs]:
                outstr += "%s -> %s\n" % (lhs, rhs)

        return outstr

def main():
    with open(sys.argv[1], 'r') as fp:
        lines = fp.readlines()

    gr = Grammar()
    msgs = []
    ctr = 0
    for line in lines:
        line = line.strip()
        if ':' in line:
            gr.add_rule(line)
        elif 'a' in line or 'b' in line:
            print(line.strip() + " ... ", end = '')
            if ckyparse(list(line.strip()), gr):
                print(" True")
                ctr += 1

            else:
                print(" False")
    print(ctr) 


if __name__ == '__main__':
    main()
