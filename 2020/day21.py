import sys

def main():
    allergens_to_ingreds = {}
    ingreds_to_allergens = {}
    ingred_count = {}

    with open(sys.argv[1], 'r') as fp:
        for line in fp:
            ingredients = line[:line.index('(')].split()
            allergens = [w.strip() for w in line[line.index('contains ')+8:line.index(')')].split(',')]

            for ing in ingredients:
                if ing not in ingreds_to_allergens:
                    ingreds_to_allergens[ing] = set()
                ingreds_to_allergens[ing].update(allergens)

                if ing not in ingred_count:
                    ingred_count[ing] = 0
                ingred_count[ing] += 1

            for allerg in allergens:
                if allerg not in allergens_to_ingreds:
                    allergens_to_ingreds[allerg] = set(ingredients)
                else:
                    allergens_to_ingreds[allerg].intersection_update(ingredients)

    atoi = {}
    changed = True
    while changed:
        changed = False
        for k, v in list(allergens_to_ingreds.items()):
            if len(v) == 1:
                for k2 in allergens_to_ingreds:
                    if k != k2:
                        allergens_to_ingreds[k2] -= v
                atoi[k] = list(v)[0]
                del allergens_to_ingreds[k]
                changed = True

    count = 0
    for i,c in ingred_count.items():
        if i not in atoi.values():
            count += c
        
    print(count)
    for k, v in sorted(list(atoi.items())):
        print(v + ",", end ='')
    print()
    print(atoi)

if __name__ == '__main__':
    main()
