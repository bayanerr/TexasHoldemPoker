import random
from itertools import combinations
import argparse
import csv
from pathlib import Path
#this function figures out if any players have a flush
def Flush(cards):
    s = set()
    for i in cards:
        s.add(i[0])
    if len(s) == 1:
        return True
    return False
#this function figures out if any players have a royal flush
def Royal_Flush(cards):
    s = set()
    if Flush(cards) == False:
        return False
    for i in cards:
        s.add(i[1])
    if s == {10,11,12,13,1}: return True
    if s == {'10', '11', '12', '13', '1'}: return True
    return False
#this function figures out if any players have a straight flush
def Straight_Flush(cards):
    s = set()
    if Flush(cards) == False:
        return False
    for i in cards:
        s.add(i[1])
    x = sorted(list(s))
    if (int(x[0]) + 1 == int(x[1])) and (int(x[1]) + 1 == int(x[2])) and (int(x[2]) + 1 == int(x[3])) and (int(x[3]) + 1 == int(x[4])): return True
    return False
#this function figures out if any players have four of a kind
def four_of_a_kind(cards):
    x = []
    for i in cards:
        x.append(i[1])
    s = sorted(x)
    if s[0] == s[1] and s[1] == s[2] and s[2] == s[3]:
        return True
    elif s[1] == s[2] and s[2] == s[3] and s[3] == s[4]:
        return True
    return False
#this function figures out if any players have three of a kind
def three_of_a_kind(cards):
    x = []
    for i in cards:
        x.append(i[1])
    sort = sorted(x)
    if sort[0] == sort[1] == sort[2]:
        return True
    elif sort[1] == sort[2] == sort[3]:
        return True
    elif sort[2] == sort[3] == sort[4]:
        return True
    return False
#this function figures out if any players have a full house
def full_house(cards):
    s = set()
    if three_of_a_kind(cards) == True:
        for i in cards:
            s.add(i[1])
        if len(s) == 2: return True
    return False
#this function figures out if any players have a straight
def Straight(cards):
    x = []
    for i in cards:
        x.append(i[1])
    x = sorted(list(x))
    if (x[0] + 1 == x[1]) and (x[1] + 1 == x[2]) and (x[2] + 1 == x[3]) and (x[3] + 1 == x[4]): return True
    return False
#this function figures out if any players have two pairs
def two_pairs(cards):
    s = set()
    for i in cards:
        s.add(i[1])
    if len(s) == 3: return True
    return False
#this function figures out if any players have pairs
def pairs(cards):
    s = set()
    for i in cards:
        s.add(i[1])
    if len(s) == 4: return True
    return False
#this function determines who has the highest card
def highcard(cards):
    h = 10
    for i in cards:
        if int(i[1]) >= h: return True
        if int(i[1]) == 0: return True
    return False
def highest_card(cards):
    x = []
    for i in cards:
        x.append(i[1])
    for i in x:
        if i == 1:
            return i
    return max(x)

#This function generates and returns a deck of cards
def generate_cards():
    card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ["C", "D", "H", "S"]
    cards = []
    for value in card_values:
        for suit in suits:
            # c = Card(value, suit)
            cards.append((suit, value))
    return cards


#This class is used to design the game.
class Game:
    #It initializes through the player amount. In the initialization,
    #variables like the players and their individual 2 cards
    #and the deck of cards are also created
    def __init__(self, player_amount):
        self.player_amount = player_amount
        self.players = []
        self.cards = generate_cards()
        self.betting_money = 0
        self.rank = 10
        self.user = [0,10,self.rank, self.cards.pop(random.randrange(len(self.cards))),self.cards.pop(random.randrange(len(self.cards)))]
        for i in range(self.player_amount):
            self.players.append([i+1,10,self.rank, self.cards.pop(random.randrange(len(self.cards))),self.cards.pop(random.randrange(len(self.cards)))])
    #This takes 3 random cards from the deck of cards and adds them to the cards of all the players
    def set_community_r1(self):
        self.c1 = self.cards.pop(random.randrange(len(self.cards)))
        self.c2 = self.cards.pop(random.randrange(len(self.cards)))
        self.c3 = self.cards.pop(random.randrange(len(self.cards)))
        for i in self.players:
            i.append(self.c1)
            i.append(self.c2)
            i.append(self.c3)
        self.user.append(self.c1)
        self.user.append(self.c2)
        self.user.append(self.c3)
        return self.players
    def remove_fold(self):
        self.players_copy = self.players
        self.players = []
        for i in self.players_copy:
            if i[2] < 9:
                self.players.append(i)

    #This takes an additional 2 cards from the deck and adds them to the
    #cards of all players for round 2
    def set_community_r2(self):
        self.c4 = self.cards.pop(random.randrange(len(self.cards)))
        self.c5 = self.cards.pop(random.randrange(len(self.cards)))
        for i in self.players:
            i.append(self.c4)
            i.append(self.c5)
        if self.user[-1] != 'folded':
            self.user.append(self.c4)
            self.user.append(self.c5)
        return self.players

    def winner(self,player):
        for i in self.players:
            if i[0] == player:
                i[1] = i[1] - 1
                i[1] = i[1] + self.betting_money

    #This determines the rank of the players after round 1
    def determine_rank_r1(self):
        for i in self.players:
            if Royal_Flush(i[3:]) == True: i[2] = 0
            elif Straight_Flush(i[3:]) == True: i[2] = 1
            elif four_of_a_kind(i[3:]) == True: i[2] = 2
            elif full_house(i[3:]) == True: i[2] = 3
            elif Flush(i[3:]) == True: i[2] = 4
            elif Straight(i[3:]) == True: i[2] = 5
            elif three_of_a_kind(i[3:]) == True: i[2] = 6
            elif two_pairs(i[3:]) == True: i[2] = 7
            elif pairs(i[3:]) == True: i[2] = 8
            elif highcard(i[3:]) == True: i[2] = 9
        #for i in self.players:
            #if i[2] >= 9: self.players.remove(i)
    #This decides if the players will bet and uses the bet function based on their rank
    def betting(self):
        for i in self.players:
            if i[2] <= 8:
                i[1] = i[1]-1
                self.betting_money = self.betting_money + 1
    #this determines the rank for round 2
    def determine_rank_r2(self):
        #self.players.append(self.user)
        for i in self.players:
            c = combinations(i[3:], 5)
            for j in list(c):
                if Royal_Flush(list(j)) == True:
                    if i[2] >= 0:
                        i[2] = 0
                elif Straight_Flush(list(j)) == True:
                    if i[2] >= 1:
                        i[2] = 1
                elif four_of_a_kind(list(j)) == True:
                    if i[2] >= 2:
                        i[2] = 2
                elif full_house(list(j)) == True:
                    if i[2] >= 3:
                        i[2] = 3
                elif Flush(list(j)) == True:
                    if i[2] >= 4:
                        i[2] = 4
                elif Straight(list(j)) == True:
                    if i[2] >= 5:
                        i[2] = 5
                elif three_of_a_kind(list(j)) == True:
                    if i[2] >= 6:
                        i[2] =6
                elif two_pairs(list(j)) == True:
                    if i[2] >= 7:
                        i[2] = 7
                elif pairs(list(j)) == True:
                    if i[2] >= 8:
                        i[2] = 8
                elif highcard(list(j)) == True:
                    if i[2] >= 9:
                        i[2] = 9
    #this determines the winner and gives them the betting money
    def determine_winner(self):
        if self.user[-1] != 'folded':
            self.players.append(self.user)
        h = []
        for i in self.players:
            h.append(i[2])
        s = sorted(h)
        m = s[0]
        l = []
        for i in s:
            if i == m:
                l.append(i)
        x = 0
        if len(l) > 1:
            for i in self.players:
                if i[2] in l:
                    if highest_card(i[3:]) > x:
                        x = highest_card(i[3:])
            i[1] = i[1] + self.betting_money
            return i[0]
        else:
            for i in self.players:
                if i[2] == l[0]:
                    i[1] = i[1] + self.betting_money
                    return i[0]

#this is the user mode decision function
#the user has to make the same decision multiple times so its one function for simplicity and to avoid repetition
def user_decision(g):
    s = True
    while s:
        decision_1 = input("\nWould you like to bet or fold? Insert 'b' to bet and 'f' to fold: ")
        if decision_1 == 'b':
            bet = input("\nhow much money would you like to bet? enter a number only(ex '3'): ")
            if bet.isnumeric():
                if int(bet) < g.user[1]:
                    print("\nyou bet: " + bet + "$")
                    return int(bet)
                elif int(bet) == g.user[1]: return 'no money'
                else: print("\nyou don't have that much money to bet, try again")
            else:
                print("\ninvalid, please try again")
        elif decision_1 == 'f':
            print("\nyou have folded the game")
            return False
        else:
            print("\ninvalid input, please try again")

'''
THIS IS THE MAIN FUNCTION FOR THE USERMODE
Only needs the input of bot player numbers
'''

def usermode_game(player_num):

    #sets up the game and stores the variables needed to be saved
    print("------------ Welcome to Texas Hold EM Poker ------------\n")
    #player_num = int(input("How many computer players would you like to play with: "))
    if player_num <= 1: raise Exception("invalid input")
    money_left = {}
    loop = True

    while loop:
        #creates a new game
        g = Game(player_num)

        #goes through the stored dictionary and adjusts the bot players money from previous games if needed
        for i in g.players:
            for keys, values in money_left.items():
                if keys == i[0]:
                    i[1] = values

        #goes through the stored dictionary and adjusts the users money from previous games if needed
        for keys, values in money_left.items():
            if keys == 0:
                g.user[1] = values



        #first round where everyone bets based solely on their cards
        print("\n---------------- Initialization ----------------")
        g.set_community_r1()
        print("\nWelcome to the Game, you are Player 0\n")
        print("Your Cards: " + str(g.user[3]) + ", " + str(g.user[4]))

        #gives the user the option to check
        decision = input("\nwould you like to check? input 'c' to check, press enter if you want to bet or fold instead: ")
        if decision != 'c':
            #if they choose not to directs them to the function that allows them to bet or fold
            decision = user_decision(g)
            print(decision)
            if decision == False:
                g.user.append('folded')
            if decision == 'no money':
                print("out of money, game over\n")
                loop = False
            else:
                g.betting_money = g.betting_money + decision
                g.user[1] = g.user[1] - decision
                print("your money left: " + str(g.user[1]) + "$")

        #The bot players now all bet 1$ based solely on their cards
        print("\n-------- Round 0 --------")
        for i in g.players:
            print("player" + str(i[0]))
            i[1] = i[1] - 1
            print("amount bet: 1$")
            print("money left: " + str(i[1]) + "$\n")
            g.betting_money = g.betting_money + 1

        #The function now displays the community cards
        #the bots will bet or fold depending on their rank
        #the user will bet or fold depending on their choice
        print("\n------------------ Round 1 ------------------\n")
        print("The Community Cards: " + str(g.c1) + ", " + str(g.c2) + ", " + str(g.c3))
        if decision != False:
            if decision != 'no money':
                decision = user_decision(g)
                print(decision)
                if decision == False:
                    g.user.append('folded')
                elif decision == 'no money':
                    print("out of money, game over")
                    loop = False
                else:
                    g.betting_money = g.betting_money + decision
                    g.user[1] = g.user[1] - decision
                    print("your money left: " + str(g.user[1]) + "$")
        g.determine_rank_r1()
        g.betting()

        for i in g.players:
            print("player" + str(i[0]))
            if i[2] >= 9:
                print("folds\n")
                money_left[i[0]] = i[1]
            elif i[2] <= 8:
                print("amount bet: 1$")
                print("money left: " + str(i[1]) + "$\n")
                money_left[i[0]] = i[1]
        g.remove_fold()

        # The function now displays the community cards along with the additional 2 community cards for round 2
        # the bots will all bet since all of the remaining are all rank 8 or above at this point
        # the user will bet or fold depending on their choice
        print("\n-------------Round 2-------------")
        g.set_community_r2()
        g.determine_rank_r2()
        g.betting()

        print("community cards: " + str(g.c1) + ", " + str(g.c2) + ", " + str(g.c3) + ", " + str(g.c4) + ", " + str(g.c5) + "\n")
        if decision != False:
            if decision != 'no money':
                decision = user_decision(g)
                print(decision)
                if decision == False:
                    g.user.append('folded')
                elif decision == 'no money':
                    print("out of money, game over")
                    print("your money left: " + str(g.user[1]))
                    loop = False
                else:
                    g.betting_money = g.betting_money + decision
                    g.user[1] = g.user[1] - decision
                    print("your money left: " + str(g.user[1]) + "$\n")
        for i in g.players:
            print("player " + str(i[0]) + ":")
            if i[2] <= 8:
                print("amount bet: 1$")
                print("money left: " + str(i[1]) + "$\n")
                money_left[i[0]] = i[1]
            if i[2] >= 9:
                print("folds\n")
                money_left[i[0]] = i[1]



        #This displays the results
        print ("\n-------------results-------------")
        winner = g.determine_winner()
        print("Winner: player " + str(winner))
        for keys, values in money_left.items():
            if keys == winner:
                money_left[keys] = int(values) + g.betting_money
        money_left[0] = g.user[1]
        #for i in g.players:
            #print("player" + str(i[0]) + ": $" + str(i[1]))
        print("\nCurrent Currency of all Players (you are player 0)")
        for keys, values in money_left.items():
            print('player ' + str(keys) + ': $' + str(values))

        #This choice determines if the loop will continue
        #However if the user is out of money the loop will end regardless of the user's choice
        continue_playing = input("\nwould you like to continue playing? input 'n' for no, or press enter/any key to continue: ")
        if continue_playing == 'n': loop = False

    print("\nGame(s) over, if you did not select 'n', you have run out of money and do not want to go into debt")


#this function is used for file mode to determine the winner.
def whose_the_winner(file):
    w = []
    x = []
    l = []
    for line in file:
        h = line.rstrip().split(",")
        l.append(h[0])
        for i in h[1:]:
            l.append((i[0], int(i[1:])))
        x.append(l)
        l = []
    for i in x:
        if Royal_Flush(i[1:]) == True:
            w.append((0, i[0], i[1:]))
        elif Straight_Flush(i[1:]) == True:
            w.append((1, i[0], i[1:]))
        elif four_of_a_kind(i[1:]) == True:
            w.append((2, i[0], i[1:]))
        elif full_house(i[1:]) == True:
            w.append((3, i[0], i[1:]))
        elif Flush(i[1:]) == True:
            w.append((4, i[0], i[1:]))
        elif Straight(i[1:]) == True:
            w.append((5, i[0], i[1:]))
        elif three_of_a_kind(i[1:]) == True:
            w.append((6, i[0], i[1:]))
        elif two_pairs(i[1:]) == True:
            w.append((7, i[0], i[1:]))
        elif pairs(i[1:]) == True:
            w.append((8, i[0], i[1:]))
        elif highcard(i[1:]) == True:
            w.append((9, i[0], i[1:]))
    s = sorted(w)
    if len(w) == 1:
        return s[0][1]
    if len(w) > 1:
        if s[0][0] != s[1][0]:
            #return ('the winner is ' + str(s[0][1]))
            return s[0][1]
        else:
            if highest_card(s[0][2]) == 1:
                return s[0][1]
            if highest_card(s[1][2]) == 1:
                return s[1][1]
            if highest_card(s[0][2]) > highest_card(s[1][2]):
                return s[0][1]
            else: return s[1][1]


#This function sees how many test cases the file mode function was able to read correctly
def compare_function(test_cases_results):
    failed_test_cases = 0
    compare_set = set()
    file = input("Please input the path of the file you would like to compare these results to: ")
    for line in open(file):
        line_elements = line.rstrip().split(',')
        compare_set.add((line_elements[0], line_elements[1]))
    compare_set = sorted(compare_set)
    test_cases_results = sorted(test_cases_results)
    if compare_set == test_cases_results:
        print('all tests passed')
    else:
        for i, j in zip(compare_set, test_cases_results):
            if i[1] != j[1]:
                print(str(i[0]) + " does not pass")
                failed_test_cases = failed_test_cases + 1
    print("failed test case amount: " + str(failed_test_cases))
    print("passed test case amount: " + str(50 - failed_test_cases))
    pass


usermode_game(6)
'''
MAIN FUNCTION FOR FILE MODE: SIMPLY INPUT DESIRED DIRECTORY OF TEST CASES
'''

def file_mode(directory):
    files = Path(directory).glob('*')
    test_cases_results = set()
    for file in sorted(files):
        f = open(file, 'r')
        winner = whose_the_winner(f)
        test_cases_results.add((file.name, winner))
    print('The winners of each file are displayed')
    for i in sorted(test_cases_results):
        print(i)
    compare = input("If you would like to compare these results to an existing text file, input 'c': ")
    if compare == 'c': compare_function(test_cases_results)

'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-usermode1', "-u", action='store_true', help='game mode, stores True if user chooses user mode')
    parser.add_argument('-filemode2', '-f', action='store_true', help='mode for the game, stores true if file mode')
    parser.add_argument('-info', '-p', '-i', type=str or int, help="tells required information for game")
    args = parser.parse_args()
    umode, fmode, info = bool(args.usermode1), bool(args.filemode2), str(args.info)
    if umode == True: mode = 'usermode'
    else: mode = 'filemode'
    return mode, info

if __name__ == "__main__":
    m = main()
    if m[0] == 'usermode': usermode_game(int(m[1]))
    if m[0] == 'filemode': file_mode(str(m[1]))
'''
