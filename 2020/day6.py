import sys

def count(grpstr):
    cd = {}
    for c in grpstr:
        if 'a' <= c <= 'z':
            cd[c] = cd.get(c, 0) + 1
    items = list(cd.items())[:]
    for k,v in items:
        if v != len(grpstr.split()):
            del cd[k]
    return cd

def main():
    group = ""
    grouplist = []
    for line in sys.stdin:
        group += line

        if line.strip() == "":
            grouplist.append(group)
            group = ""

    grouplist.append(group)

    total = 0
    for grp in grouplist:
        total += len(count(grp))

    print(total)
    

if __name__ == '__main__':
    main()
