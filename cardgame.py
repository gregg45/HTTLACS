class Cards:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.ranks = ['nuff','Ace',2,3,4,5,6,7,8,9,10,'Jack','Queen','King']
    def __str__(self):
        return "{0} of {1}".format(self.ranks[self.rank],self.suits[self.suit])
    def whatiswhat(self,other):
        if self.rank < other.rank:
            return -1
        if self.rank > other.rank:
            return 1
        if self.suit < other.suit:
            return -1
        if self.suit > other.suit:
            return 1
        return 0
    def __ge__(self,other):
        if Cards.whatiswhat(self,other) >= 0:
            return True
        return False
    def __eq__(self,other):
        if Cards.whatiswhat(self,other) == 0:
            return True
        return False
    def __gt__(self,other):
        if Cards.whatiswhat(self,other) == 1:
            return True
        return False
    def __lt__(self,other):
        if Cards.whatiswhat(self,other) == -1:
            return True
        return False
    def __le__(self,other):
        if Cards.whatiswhat(self,other) <= 0:
            return True
        return False
    def __ne__(self,other):
        if Cards.whatiswhat(self,other) != 0:
            return True
        return False

class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                self.cards.append(Cards(suit,rank))
    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s = s + " " * i + str(self.cards[i]) + "\n"
        return s
    def shuffle(self):
        import random
        rng = random.Random()
        rng.shuffle(self.cards)
    def remove(self,card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False
    def pop(self):
        return self.cards.pop()
    def is_empty(self):
        return self.cards == []
    def deal(self,hands,num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty():
                break
            card = self.pop()
            hand = hands[i % num_hands]
            hand.add(card)


class Hand(Deck):
    def __init__(self,name=""):
        self.cards = []
        self.name = name
    def add(self,card):
        self.cards.append(card)
    def __str__(self):
        s = "Hand " + self.name
        if self.is_empty():
            s += " is empty \n"
        else:
            s += " contains \n"
        return s + Deck.__str__(self)

class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

class OldMaidHand(Hand):
    def remove_matches(self):
        count = 0
        original_cards = self.cards[:]
        for card in original_cards:
            match = Cards(3 - card.suit, card.rank)
            if match in self.cards:
                self.cards.remove(card)
                self.cards.remove(match)
                print("Hand {0}: {1} matches {2}".format(self.name,card,match))
                count += 1
        return count

class OldMaidGame(CardGame):
    def play(self,names):
        # Remove Queen of Clubs
        self.deck.remove(Cards(0,12))

        # Make a hand for each player
        self.hands = []
        for name in names:
            self.hands.append(OldMaidHand(name))

        # Deal the cards
        self.deck.deal(self.hands)
        print("---------- Cards have been dealt")
        self.print_hands()

        # Remove initial matches
        matches = self.remove_all_matches()
        print("---------- Matches discarded, play begins")
        self.print_hands()

        # Play until all 50 cards are matched
        turn = 0
        num_hands = len(self.hands)
        while matches <25:
            matches += self.play_one_turn(turn)
            turn = (turn + 1) % num_hands

        print("--------- Game is over")
        self.print_hands()

    def play_one_turn(self,i):
        if self.hands[i].is_empty():
            return 0
        neighbor = self.find_neighbor(i)
        picked_card = self.hands[neighbor].pop()
        self.hands[i].add(picked_card)
        print("Hand",self.hands[i].name,"picked",picked_card)
        count = self.hands[i].remove_matches()
        self.hands[i].shuffle()
        return count

    def find_neighbor(self,i):
        num_hands = len(self.hands)
        for next in range(1,num_hands):
            neighbor = (i + next) % num_hands
            if not self.hands[neighbor].is_empty():
                return neighbor

    def remove_all_matches(self):
        count = 0
        for hand in self.hands:
            count += hand.remove_matches()
        return count

    def print_hands(self):
        for hand in self.hands:
            print(hand)
            
