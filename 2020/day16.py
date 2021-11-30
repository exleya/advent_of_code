import sys

def part1(nearby_tickets, fields):
    err_val = 0
    legal_tickets = []
    for ticket in nearby_tickets.split('\n'):
        values = ticket.split(',')
        in_any_range = True
        for sval in values:
            val = int(sval)
            in_range = False
            for field, ranges in fields.items():
                if (ranges[0] <= val <= ranges[1]) or (ranges[2] <= val <= ranges[3]):
                    in_range = True
            if not in_range:
                in_any_range = False

        if not in_any_range:
            err_val += val
        else:
            legal_tickets.append(ticket.strip())

    return err_val, legal_tickets

def part2(legal_tix_list, my_ticket_str, field_dict):
    field_poss_map = {}
    for i in range(len(legal_tix_list[0].split(','))):
        field_poss_map[i] = set(field_dict.keys())

    arcs = []
    for i in field_poss_map:
        for j in field_poss_map:
            if i != j:
                arcs.append((i,j))

    for ticket in legal_tix_list:
        values = ticket.split(',')
        for i in range(len(values)):
            val = int(values[i])
            removeset = set()
            for field in field_poss_map[i]:
                rng = field_dict[field]
                if not((rng[0] <= val <= rng[1]) or (rng[2] <= val <= rng[3])):
                    removeset.add(field)

            field_poss_map[i] -= removeset

            # ensure arc-consistency between domains. thx AC3
            arcq = arcs[:]
            while len(arcq) > 0:
                i, j = arcq.pop(0)
                if len(field_poss_map[i]) == 1:
                    oldj = len(field_poss_map[j])
                    field_poss_map[j] -= field_poss_map[i]
                    if oldj != len(field_poss_map[j]):
                        for k in field_poss_map:
                            if k != j:
                                arcq.append((j,k))


    ctr = 0
    prod = 1
    mytik = my_ticket_str.strip().split(',')
    print(field_poss_map)
    for i in field_poss_map:
        if 'departure' in list(field_poss_map[i])[0]:
            ctr += 1
            prod *= int(mytik[i])
            print(mytik[i])

        if ctr > 5:
            return prod
        

def main():

    with open(sys.argv[1], 'r') as fp:
        text = fp.read()

    #commence the chopping into parts
    ntind = text.index('nearby tickets:')
    nttext = text[ntind+16:].strip()
    text = text[:ntind]
    
    ytind = text.index('your ticket:')
    yttext = text[ytind+13:].strip()
    text = text[:ytind]

    fields = {}
    for line in text.split('\n'):
        if ':' in line:
            name, rng = line.split(':')
            rng = rng.replace(' or ','-').split('-')
            for i in range(len(rng)):
                rng[i] = int(rng[i])
            fields[name] = rng

    errval, legal_tix = part1(nttext, fields)
    print(part2(legal_tix, yttext, fields))
        
if __name__ == '__main__':
    main()
