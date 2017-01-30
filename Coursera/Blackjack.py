# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = {'Dealer':'Dealer','Player':'Player','Option':'Hit or Stand ?','Outcome':''}
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand=[]

    def __str__(self):
        # return a string representation of a hand
        hand_string=""
        for card in self.hand:
            hand_string += " " + str(card)
        return "Hand contains" + hand_string

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        ace_checker = False
        
        for card in self.hand:
            value += VALUES[card.get_rank()]
            if VALUES[card.get_rank()] == 1:
                ace_checker = True                
        if ace_checker and value <= 11:
            value += 10           
        return value
               
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(0,len(self.hand)):
            if i < 5:
                self.hand[i].draw(canvas,[pos[0] + 100 * i, pos[1]])
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck=[]
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        deck_string=""
        for card in self.deck:
            deck_string += " " + str(card)
        return "Deck contains" + deck_string


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    if not in_play:
        player_hand = Hand()
        dealer_hand = Hand()
        deck = Deck()
        deck.shuffle()
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    
        outcome['Option'] = "Hit or Stand ?"
        outcome['Outcome'] = ""
        in_play = True
        
    elif in_play :
        player_hand = Hand()
        dealer_hand = Hand()
        deck = Deck()
        deck.shuffle()
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        score -= 1
    
        outcome['Option'] = "Hit or Stand ?"
        outcome['Outcome'] = "You gave up last game."

def hit(): 
    global score, in_play
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value()<=21:
            player_hand.add_card(deck.deal_card())

    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value()>21:

            in_play = False
            outcome['Option'] = "New Deal?"
            outcome['Outcome'] = "You Lose."
            score -= 1
       
def stand():
    global score, in_play
    if player_hand.get_value()>21:
        pass
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    else:
        if in_play:
            while dealer_hand.get_value()<17:
                dealer_hand.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
            if dealer_hand.get_value()>21:
                outcome['Option'] = "New Deal?"
                outcome['Outcome'] = "You win!"
                score += 1
                in_play = False
            else:
                if dealer_hand.get_value()>=player_hand.get_value():
                    outcome['Option'] = "New Deal?"
                    outcome['Outcome'] = "You lose."
                    score -= 1
                    in_play = False
                else:
                    outcome['Option'] = "New Deal?"
                    outcome['Outcome'] = "You win!"
                    score += 1
                    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, score
    canvas.draw_text("Black Jack",[100,100],50,"Red")
    canvas.draw_text(outcome['Player'],[50,365],35,"Black")
    canvas.draw_text(outcome['Dealer'],[50,170],35,"Black")
    canvas.draw_text(outcome['Option'],[250,170],35,"Black")
    canvas.draw_text(outcome['Outcome'],[250,365],35,"Black")
    canvas.draw_text("Score: "+str(score),[450,100],30,"Black")
    dealer_hand.draw(canvas,[50,200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50+CARD_BACK_CENTER[0], 200+CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    player_hand.draw(canvas,[50,400])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()