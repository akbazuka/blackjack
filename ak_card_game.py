"""
AK's Blackjack Implementation
"""
import random

class Card:
    '''Create a single card, by id number'''

    # Class variables, created once for the class
    suits = [ '\u2660', '\u2661', '\u2662', '\u2663' ]
    ranks = [ 'A','2','3','4','5','6','7','8','9','10','J','Q','K' ]
    #print(suits)

    def __init__(self, n=0):
        # instance variables for _num, _rank, _suit, _value
        if 0 <= n < 52:
            self._num = n
            self._rank = Card.ranks[n%13]       # note referencing class vars
            self._suit = Card.suits[n//13]

            self._value = n%13 + 1

            #Change values of cards to follow Black Jack game rules
            if self._rank == 'J' or self._rank == 'K' or self._rank == 'Q':
                self._value = 10
            if self._rank == 'A':
                self._value = 11

        else: # invalid card indicators
            self._rank = 'x'
            self._suit = 'x'
            self._value = -1
        
    def __repr__(self):
        return  self._rank + self._suit

    def __lt__(self,other):
        return self._value < other._value

    def __le__(self,other):
        return self._value <= other._value

    def __eq__(self,other):
        return self._value == other._value


class DeckOfCards:
    '''A Deck is a collection of cards'''

    def __init__(self):
        self._deck = [ Card(i) for i in range(52) ]

    ## implement __repr__(), shuffle(), deal_a_card(), cards_left()

    def __repr__(self):
        return str([card._rank + card._suit for card in self._deck])
    
    #Shuffle deck
    def shuffle(self):
        random.shuffle(self._deck)
    
    #Take a card from top of deck
    def deal_a_card(self):
        return self._deck.pop()

    #Check number of cards lef tin feck
    def cards_left(self):
        return len(self._deck)

class Player:
    def __init__(self):
        self._total = 0
        self._chips = 1000 #Set how much money player starts with
    '''
    def __repr__(self):
        return self._total
    '''
    def get_total(self):
        return self._total

    def get_chips(self):
        return self._chips

    def sum_points(self, value):
        self._total += value

    def add_chips(self, bet):
        self._chips += bet

    def sub_chips(self, bet):
        self._chips -= bet

def blackey_jackey():
    # make a deck
    deck = DeckOfCards()
    deck.shuffle() #shuffle the deck
    #print(deck)

    print("$$$ Welcome to the BLACKJACK table at AK's Casino $$$")
    print("\nRules of the game are general Blackjack rules (without the optiont to Split). \nIf you are unfamiliar with the rules of Blackjack, please leave AK's Casino.")

    answer = str(input("\nCare to risk it all? (yes/no): "))
    if answer.lower() == 'yes':

        print("\nGood lad. Let's play.")
        
        player = Player()
        dealer = Player()

        round = 1
        while True:
            print("\nYou have $",player.get_chips(),"worth of chips.")

            if round > 1:
                if(player.get_chips() > 25):
                    another_round = str(input("\nWould you like to play another round? (yes/no): "))
                    if another_round.lower() != 'yes':
                        print("\nThank you for playing Blackjack at AK's Casino. Please visit us again.")
                        break
                else:
                    print("You don't have enough chips to continue playing at this table. \nKindly leave without making a scene or we will be forced to call security.")
                    break

            print("\nRound",round)

            while True:
                original_bet = int(input("\nMinimum bet is $25.\n\nHow much would you like to bet? $"))
                if original_bet >= 25 and original_bet <= player.get_chips():
                    #print(bet)
                    #print(player.get_chips())
                    break
                else: print("You entered an invalid bet.")

            print("Your bet of $",original_bet," was accepted.")
            player.sub_chips(original_bet)

            #Dealer enters game
            dealers_cards = []
            #Player enters game:
            players_cards = []

            players_cards.append(deck.deal_a_card()) #Dealer deals player a card
            player.sum_points(players_cards[0]._value)
            dealers_cards.append(deck.deal_a_card()) #Dealer deals himself a card
            dealer.sum_points(dealers_cards[0]._value)
            dealer_point_first = dealer.get_total()

            players_cards.append(deck.deal_a_card()) #Dealer deals player second card
            player.sum_points(players_cards[1]._value)
            dealers_cards.append(deck.deal_a_card()) #Dealer deals himself second card (facedown)
            dealer.sum_points(dealers_cards[1]._value)

            print("\nDealer has dealt the opening cards.")

            print("Your cards are:", players_cards[0],players_cards[1])
            print("Your total now, is:", player.get_total())
            print("\nDealer's first card is:", dealers_cards[0])
            print("Dealer's total on the first card is:", dealer_point_first)

            #Offer player insurance bet if dealer has a 10 or an ACE as face up card AND if player has enough money to make one
            insurance_bet = 0
            if dealers_cards[0]._value >= 10 and player.get_chips() >= original_bet/2:
                answer = str(input("\nWould you like to make an insurance bet? (yes/no): "))
                if answer.lower() != 'yes':
                    print("Insurance bet was not made.")
                else: 
                    insurance_bet = original_bet/2.0
                    player.sub_chips(insurance_bet)
                    print("Insurance bet of half of your original bet was placed successfully.")

            if dealer.get_total() == 21:
                print("Dealer's second card is a", dealers_cards[1])
                print("Dealer has Blackjack!")
                if insurance_bet > 11: #If insurance bet was made
                    player.add_chips(insurance_bet*2 + original_bet*2)
                    print("You won your insurance bet. Your received $",insurance_bet*2 + original_bet*2,"back in chips.")
                
                if player.total() != 21:
                    print("You lost because your cards did not match the dealer's Blackjack.\n")
                    
                else: 
                    print("Your bet was returned and the play is pushed because you and the Dealer have Blackjack.")

            elif dealer.get_total() != 21 and player.get_total() == 21:
                print("Dealer's second card is a", dealers_cards[1])
                print("You have Blackjack and the dealer does not. You win!")
                print("You receive a total of $", original_bet*2.5,"back in chips.")
                player.add_chips(original_bet*2.5)

            else:
                if insurance_bet > 0:
                    print("\nYour insurance bet was lost because dealer did not have Blackjack.")
                    
                lose = 0 #To check if player lost
                dd = 0 #To check if player doubled down

                #Loop for input validation
                while True:
                    player_choice = str(input("\nIt is your turn. What will you choose to do? (stand= s / hit= h / double down= d): "))

                    #Player chooses to stand
                    if player_choice.lower() == 's':
                        break #To break input validation loop
                    
                    #Player chooses to hit
                    elif player_choice.lower() == 'h':
                        #Loop if player wants to hit again
                        while True:
                            players_cards.append(deck.deal_a_card())
                            print("You chose to hit. You were dealt a", players_cards[-1])
                            player.sum_points(players_cards[-1]._value)
                            print("Your total now, is:", player.get_total())
                            if player.get_total() > 21:
                                print("You lost because your hand was over 21.")
                                lose = 1
                                break
                            elif player.get_total() == 21:
                                print("Since your total is 21, you are choosing to stand by default.")
                                break
                            else:
                                answer = str(input("Would you like to hit again? (yes, no): "))
                                if answer.lower() != 'yes':
                                    print("You chose to stand.")
                                    break
                        break #To break input validation loop

                    #Player chooses to double down
                    elif player_choice.lower() == 'd': #Can only double down on first turn
                        print("You chose to double down. Your original bet has been doubled to a total of $", original_bet*2)
                        player.sub_chips(original_bet)
                        players_cards.append(deck.deal_a_card())
                        print("\nThe card you were dealt is a", players_cards[-1])
                        player.sum_points(players_cards[-1]._value)
                        print("Your total now, is:", player.get_total())
                        if player.get_total() > 21:
                            print("You lost because your hand was over 21.")
                            lose = 1
                        else:
                            print("You are now choosing to stand now by default.")
                        break #To break input validation loop

                    #Player entered invalid input
                    else:
                        print("You entered an invalid input.")

                #Dealer plays if player hasn't lost already
                if lose == 0:
                    print("\nIt is now the dealer's turn. \nThe dealer's down card was a",dealers_cards[1])
                    print("The dealer's total is:", dealer.get_total())
                    #Dealer continues to hit until a total of 17 or above is reached
                    while dealer.get_total() < 17:
                        dealers_cards.append(deck.deal_a_card())
                        print("\nThe dealer was dealt a", dealers_cards[-1])
                        dealer.sum_points(dealers_cards[-1]._value)
                        print("The dealer's total is now:", dealer.get_total())
                    
                    #If dealer busts
                    if dealer.get_total() > 21:
                        if dd == 1:
                            print("The dealer's hand was a bust, you win! $",original_bet*4)
                            player.add_chips(original_bet*4)
                        else:
                            print("The dealer's hand was a bust, you win! $",original_bet*2)
                            player.add_chips(original_bet*2)   

                    #If dealer and player have matching hands
                    elif dealer.get_total() == player.get_total():
                        if dd == 1:
                            print("You have the same total as the dealer. You get back your original bet of $",original_bet*2,"in chips.")
                            player.add_chips(original_bet*2)
                        else:
                            print("You the same total as the dealer. You get back your original bet of $",original_bet,"in chips.")
                            player.add_chips(original_bet)  
                    
                    #If player has bigger hand than dealer
                    elif player.get_total() > dealer.get_total():
                        if dd == 1:
                            print("Your hand was bigger than the dealer's, you win! $",original_bet*4)
                            player.add_chips(original_bet*4)
                        else:
                            print("Your hand was bigger than the dealer's, you win! $",original_bet*2)
                            player.add_chips(original_bet*2)

                    #If dealer has bigger hand then player
                    else:
                        print("Your hand was smaller than the dealer's, you lost.")

            round += 1

    else:
        print("\nYou chose to whimp out. Please leave AK's casino with whatever is left of your dignity.")

#Play Blackjack
blackey_jackey()
    


