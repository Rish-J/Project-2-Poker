import random
import math
import time

ROYAL_FLUSH = 1000
STRAIGHT_FLUSH = 900
FOUR_KIND = 800
FULL_HOUSE = 700
FLUSH = 600
STRAIGHT = 500
THREE_KIND = 400
TWO_PAIR = 300
ONE_PAIR = 200
PRE_FLOP = math.perm(50, 5)
PRE_TURN = math.perm(47, 3)
PRE_RIVER = math.perm(46, 3)
PRE_FLOP_CHILD = 45
PRE_TURN_CHILD = 44

# Each node represents a world in the game
class Node:
    def __init__(self, parent, deck, world, stage):
        self.t = 0
        self.n = 0
        self.children = []
        self.combinations = set()
        self.deck = deck
        self.world = world
        self.parent = parent
        self.stage = stage

# Each world gets its own deck, so there is a class for that
class Deck:
    def __init__(self, deck=None):
        self.deck = ["02club", "02heart", "02spade", "02diamond",
                      "03club", "03heart", "03spade", "03diamond",
                      "04club", "04heart", "04spade", "04diamond",
                      "05club", "05heart", "05spade", "05diamond",
                      "06club", "06heart", "06spade", "06diamond",
                      "07club", "07heart", "07spade", "07diamond",
                      "08club", "08heart", "08spade", "08diamond",
                      "09club", "09heart", "09spade", "09diamond",
                      "10club", "10heart", "10spade", "10diamond",
                      "11club", "11heart", "11spade", "11diamond",
                      "12club", "12heart", "12spade", "12diamond",
                      "13club", "13heart", "13spade", "13diamond",
                      "14club", "14heart", "14spade", "14diamond"] if not deck else deck
        self.id = random.randint(1, 100)
    # Randomly draw a cards
    def draw_cards(self, n):
        drawn = []
        for _ in range(n):
            card = random.choice(self.deck)
            self.deck.remove(card)
            drawn.append(card)
        return drawn
    # Get two opponent cards
    def select_opponent(self):
        opponent = []
        card = random.choice(self.deck)
        self.deck.remove(card)
        opponent.append(card)
        card = random.choice(self.deck)
        self.deck.remove(card)
        opponent.append(card)
        self.deck.extend(opponent)
        return opponent
    def copy_deck(self):
        return Deck(list(self.deck))

# All of the check functions below check if a given hand is the specified ranking

def check_royal_flush(cards):
    types = {}
    for card in cards:
        rank = card[0:2]
        suit = card[2:]
        if rank == "a" or rank == "k" or rank == "q" or rank == "j" or rank == "1":
            if suit not in types:
                types[suit] = [rank]
            else:
                if rank not in types[suit]:
                    types[suit].append(rank)
    for suit in types:
        if len(types[suit]) == 5:
            return True
    return False

def check_straight_flush(cards):
    types = {}
    for card in cards:
        rank = card[0:2]
        suit = card[2:]
        if suit not in types:
            types[suit] = [rank]
        else:
            if rank not in types[suit]:
                types[suit].append(rank)
    for suit in types:
        ranks = types[suit]
        if len(ranks) >= 5:
            ranks.sort()
            in_order = 1
            for i in range(1, len(ranks)):
                if int(ranks[i]) == int(ranks[i-1]) + 1:
                    in_order += 1
            return in_order >= 5
    return False

def check_four_kind(cards):
    types = {}
    for card in cards:
        rank = card[0:2]
        if rank not in types:
            types[rank] = 1
        else:
            types[rank] += 1
    for rank in types:
        if types[rank] == 4:
            return True
    return False

def check_full_house(cards):
    types = {}
    for card in cards:
        rank = card[0:2]
        if rank not in types:
            types[rank] = 1
        else:
            types[rank] += 1
    three = False
    two = False
    for rank in types:
        if types[rank] == 3:
            if two: return True
            three = True
        elif types[rank] == 2:
            if three: return True
            two = True
    return False

def check_flush(cards):
    types = {}
    for card in cards:
        suit = card[2:]
        if suit not in types:
            types[suit] = 1
        else:
            types[suit] += 1
    for suit in types:
        if types[suit] == 5:
            return True
    return False

def check_straight(cards):
    cards.sort(key=lambda a: int(a[0:2]))
    in_order = 0
    for i in range(1, len(cards)):
        if int(cards[i][0:2]) == int(cards[i-1][0:2]) + 1:
            in_order += 1
    return in_order >= 5

def check_three_kind(cards):
    types = {}
    for card in cards:
        rank = card[0:2]
        if rank not in types:
            types[rank] = 1
        else:
            types[rank] += 1
    for rank in types:
        if types[rank] == 3:
            return True
    return False

def check_two_pair(cards):
    types = {}
    for card in cards:
        suit = card[2:]
        if suit not in types:
            types[suit] = 1
        else:
            types[suit] += 1
    pairs = 0
    for suit in types:
        if types[suit] == 2:
            if pairs == 1: return True
            pairs += 1
    return False

def check_one_pair(cards):
    types = {}
    for card in cards:
        suit = card[2:]
        if suit not in types:
            types[suit] = 1
        else:
            types[suit] += 1
    for suit in types:
        if types[suit] == 2:
            return True
    return False

def best_ranking(cards):
    cards.sort(key=lambda a: int(a[0:2]))
    high_card = int(max(cards, key=lambda a: int(a[0:2]))[0:2])
    if check_royal_flush(cards):
        return ROYAL_FLUSH + high_card
    elif check_straight_flush(cards):
        return STRAIGHT_FLUSH + high_card
    elif check_four_kind(cards):
        return FOUR_KIND + high_card
    elif check_full_house(cards):
        return FULL_HOUSE + high_card
    elif check_flush(cards):
        return FLUSH + high_card
    elif check_straight(cards):
        return STRAIGHT + high_card
    elif check_three_kind(cards):
        return THREE_KIND + high_card
    elif check_two_pair(cards):
        return TWO_PAIR + high_card
    elif check_one_pair(cards):
        return ONE_PAIR + high_card
    else:
        return high_card

def ucb1(node, N):
    return (node.t/node.n) + (2*math.log(N)/node.n) if node.n > 0 else math.inf

def rollout(world, deck, hole):
    opponent = world[0:2]
    community = world[2:]
    community += deck.draw_cards(5-len(community))
    return best_ranking(hole+community) > best_ranking(opponent+community)

def print_stats(wins, games, stage):
    stage_name = ""
    if stage == PRE_FLOP:
        stage_name = "Pre-flop"
    elif stage == PRE_TURN:
        stage_name = "Pre-turn"
    elif stage == PRE_RIVER:
        stage_name = "Pre-river"
    print(f"{stage_name} win percentage {round((wins/games)*100, 2)}%")

def next_stage(stage):
    if stage == PRE_FLOP:
        return PRE_TURN
    elif stage == PRE_TURN:
       return PRE_RIVER
    else:
        return None

def draw_count(stage):
    if stage == PRE_FLOP:
        return 5
    elif stage == PRE_TURN or stage == PRE_RIVER:
       return 3
    elif stage == PRE_FLOP_CHILD or stage == PRE_TURN_CHILD:
        return 1
    
def get_child_stage(node):
    if node.stage == PRE_FLOP:
        return PRE_FLOP_CHILD
    elif node.stage == PRE_FLOP_CHILD or node.stage == PRE_TURN:
        return PRE_TURN_CHILD
    else:
        return 0
    
# Perform the Monte Carlo Tree Search on the given hand and stage
def mcts(root, hole):
    start_time = time.time()
    wins = 0
    games = 0
    current = root
    while time.time() - start_time < 10:
        while len(current.combinations) == current.stage:
            current = max(current.children, key=lambda a: ucb1(a, current.n))
        deck = current.deck
        child_deck = deck.copy_deck()
        possibility = child_deck.draw_cards(draw_count(current.stage))
        possibility.extend(current.world)
        possibility = tuple(possibility)
        try:
            if possibility in current.combinations:
                continue
        except:
            print(possibility, current.world)
            exit()
        child = Node(root, child_deck, list(possibility), get_child_stage(current))
        current.children.append(child)
        current.combinations.add(possibility)
        outcome = rollout(list(possibility), child_deck, hole)
        wins += outcome
        games += 1
        while current.parent:
            current.t = outcome
            current.n += 1
            current = current.parent
    print_stats(wins, games, current.stage)
    
def game():
    deck = Deck()
    hole = deck.draw_cards(2)
    opponent = deck.select_opponent()
    print(f"Hole: {hole}")
    root = Node(None, deck, [], PRE_FLOP)
    mcts(root, hole)
    root.world.extend(root.deck.draw_cards(3))
    root.stage = PRE_TURN
    print(f"Flop community cards: {root.world}")
    mcts(root, hole)
    root.world.extend(root.deck.draw_cards(1))
    root.stage = PRE_RIVER
    print(f"Turn community cards: {root.world}")
    mcts(root, hole)
    root.world.extend(root.deck.draw_cards(1))
    print(f"River community cards: {root.world}")
    print(f"Opponent cards: {opponent}")

game()