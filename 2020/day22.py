import sys

def play_rec_combat(d1, d2):
    '''plays a GAME of recursive combat
    a GAME consists of a series of rounds
    '''
    history = set()
    while len(d1) > 0 and len(d2) > 0:
        #plays rounds of a single GAME
        #print(f"Player 1's deck: {d1}\nPlayer 2's deck:{d2}")

        # history is a set of tuples of hand pairs
        if (tuple(d1), tuple(d2)) in history:
            return 1
        else:
            history.add((tuple(d1), tuple(d2)))
    
            c1 = d1.pop(0)
            c2 = d2.pop(0)
            #print(f"Player 1 plays: {c1}\nPlayer 2 plays: {c2}")
            if len(d1) >= c1 and len(d2) >= c2:
                round_winner = play_rec_combat(d1[:c1], d2[:c2])
            else:
                if c1 > c2:
                    round_winner = 1
                else:
                    round_winner = -1
        if round_winner > 0:
            #print(f"Player 1 wins this round")
            d1.append(c1)
            d1.append(c2)
        else:
            #print(f"Player 2 wins this round")
            d2.append(c2)
            d2.append(c1)
        #input()

    score = 0
    for i in range(len(d1)):
        score += (len(d1) - i) * d1[i]
    for i in range(len(d2)):
        score -= (len(d2) - i) * d2[i]
    return score

def play_combat(d1, d2):
    
    while len(d1) > 0 and len(d2) > 0:
        c1 = d1.pop(0)
        c2 = d2.pop(0)
        if c1 > c2:
            d1.append(c1)
            d1.append(c2)
        else:
            d2.append(c2)
            d2.append(c1)

    score = 0
    for i in range(len(d1)):
        score += (len(d1) - i) * d1[i]
    for i in range(len(d2)):
        score += (len(d2) - i) * d2[i]

    return score

def main():
    p1deck = []
    p2deck = []
    player = None
    with open(sys.argv[1], 'r') as fp:
        for line in fp:
            if 'Player 1' in line:
                player = 1
            elif 'Player 2' in line:
                player = 2
            elif line.strip() != '':
                if player == 1:
                    p1deck.append(int(line.strip()))
                elif player == 2:
                    p2deck.append(int(line.strip()))

    print(p1deck)
    print(p2deck)
    print(play_rec_combat(p1deck, p2deck))

if __name__ == '__main__':
    main()
