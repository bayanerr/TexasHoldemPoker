import random
from itertools import combinations
import argparse
import csv
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk

money_left = {}

#this function figures out if any players have a flush
def Flush(cards):
    suit_set = set()
    for i in cards:
        suit_set.add(i[0])
    if len(suit_set) == 1:
        return True
    return False

#this function figures out if any players have a royal flush
def Royal_Flush(cards):
    values_set = set()
    #reuse the Flush function to ensure it meets the Flush criteria first
    if Flush(cards) == False:
        return False
    for i in cards:
        values_set.add(i[1:])
    if values_set == {10,11,12,13,14}: return True
    if values_set == {'10','11', '12', '13', '14'}: return True
    return False


#this function figures out if any players have a straight flush
def Straight_Flush(cards):
    straight_flush_set = set()
    if Flush(cards) == False:
        return False
    for i in cards:
        straight_flush_set.add(int(i[1:]))
    print(straight_flush_set)
    sorted_set = sorted(straight_flush_set)
    if (sorted_set[0] + 1 == sorted_set[1]) and (sorted_set[1] + 1 == sorted_set[2]) \
            and (sorted_set[2] + 1 == sorted_set[3]) and (sorted_set[3] + 1 == sorted_set[4]):
        return True
    return False
#print(Straight_Flush(['C2', 'C3', 'C4', 'C6', 'C5']))

#this function figures out if any players have four of a kind
def four_of_a_kind(cards):
    values = []
    for i in cards:
        values.append(int(i[1:]))
    sorted_values = sorted(values)
    if sorted_values[0] == sorted_values[1] and sorted_values[1] == sorted_values[2] and sorted_values[2] == sorted_values[3]:
        return True
    elif sorted_values[1] == sorted_values[2] and sorted_values[2] == sorted_values[3] and sorted_values[3] == sorted_values[4]:
        return True
    return False
#print(four_of_a_kind(['C2', 'D2', 'H2', 'S2', 'C3']))

#this function figures out if any players have three of a kind
def three_of_a_kind(cards):
    card_values = []
    for i in cards:
        card_values.append(int(i[1:]))
    sorted_card_values = sorted(card_values)
    if sorted_card_values[0] == sorted_card_values[1] == sorted_card_values[2]:
        return True
    elif sorted_card_values[1] == sorted_card_values[2] == sorted_card_values[3]:
        return True
    elif sorted_card_values[2] == sorted_card_values[3] == sorted_card_values[4]:
        return True
    return False

#this function figures out if any players have a full house
def full_house(cards):
    values_set = set()
    if three_of_a_kind(cards) == True:
        for i in cards:
            values_set.add(int(i[1:]))
        if len(values_set) == 2: return True
    return False

#this function figures out if any players have a straight
def Straight(cards):
    values_list = []
    for i in cards:
        values_list.append(int(i[1]))
    values_list = sorted(values_list)
    if (values_list[0] + 1 == values_list[1]) and (values_list[1] + 1 == values_list[2]) and\
            (values_list[2] + 1 == values_list[3]) and (values_list[3] + 1 == values_list[4]): return True
    return False


#this function figures out if any players have two pairs
def two_pairs(cards):
    values_set = set()
    for i in cards:
        values_set.add(int(i[1:]))
    if len(values_set) == 3: return True
    return False


#this function figures out if any players have pairs
def pairs(cards):
    values_set = set()
    for i in cards:
        values_set.add(int(i[1:]))
    if len(values_set) == 4: return True
    return False

#this function determines if a player has a high card 10 or greater
def highcard(cards):
    highcard_numb = 10
    for i in cards:
        if int(i[1:]) >= highcard_numb: return True
        if int(i[1:]) == 0: return True
    return False

#this function generates the deck of cards
def generate_cards():
    card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ["C", "D", "H", "S"]
    cards = []
    for value in card_values:
        for suit in suits:
            cards.append(str(suit) + str(value))
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

    #This decides if the players will bet and uses the bet function based on their rank
    def betting(self):
        for i in self.players:
            if i[2] <= 8:
                i[1] = i[1]-1
                self.betting_money = self.betting_money + 1

    #this determines the rank for round 2
    def determine_rank_r2(self):
        for i in self.players:
            c = combinations(i[3:], 5)
            for j in list(c):
                if Royal_Flush(list(j)) == True:
                    if i[2] >= 0: i[2] = 0
                elif Straight_Flush(list(j)) == True:
                    if i[2] >= 1: i[2] = 1
                elif four_of_a_kind(list(j)) == True:
                    if i[2] >= 2: i[2] = 2
                elif full_house(list(j)) == True:
                    if i[2] >= 3: i[2] = 3
                elif Flush(list(j)) == True:
                    if i[2] >= 4: i[2] = 4
                elif Straight(list(j)) == True:
                    if i[2] >= 5: i[2] = 5
                elif three_of_a_kind(list(j)) == True:
                    if i[2] >= 6: i[2] = 6
                elif two_pairs(list(j)) == True:
                    if i[2] >= 7: i[2] = 7
                elif pairs(list(j)) == True:
                    if i[2] >= 8: i[2] = 8
                elif highcard(list(j)) == True:
                    if i[2] >= 9: i[2] = 9
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



#In progress
#Uses the dictionary at the top to store all the players money so that
    #in the event of a new game, the players still have their money
def adjusting_money(g):
    # goes through the stored dictionary and adjusts the bot players money from previous games if needed
    for i in g.players:
        for keys, values in money_left.items():
            if keys == i[0]:
                i[1] = values
    # goes through the stored dictionary and adjusts the users money from previous games if needed
    for keys, values in money_left.items():
        if keys == 0:
            g.user[1] = values

#In progress
#Function directed when checking button is pressed
def checking_button(g, button_frame, root, bet_amount=0):
    button_frame.destroy()
    g.set_community_r1()
    #creating a frame for the community cards
    frame = Frame(root, bg="white")
    frame.pack(pady=20)


    #creating a frame label
    card_frame = LabelFrame(frame, text=f"  {g.user[2]}The Round 1 Community Cards Are: ", bd=0)
    card_frame.grid(row=0, column=0, padx=10, ipadx=2)

    #creating a spot for each card
    community_card_1 = Label(card_frame, text='')
    community_card_1.grid(row = 1, column = 0)

    community_card_2 = Label(card_frame, text='')
    community_card_2.grid(row = 1, column = 1)

    community_card_3 = Label(card_frame, text='')
    community_card_3.grid(row =1, column = 2)

    #putting a photo of the community card spots in each slot
    global community_card_image1
    global community_card_image2
    global community_card_image3

    community_card_image1 = resize_cards(f'card_deck/{g.c1}.png')
    community_card_image2 = resize_cards(f'card_deck/{g.c2}.png')
    community_card_image3 = resize_cards(f'card_deck/{g.c3}.png')
    community_card_1.config(image=community_card_image1)
    community_card_2.config(image=community_card_image2)
    community_card_3.config(image=community_card_image3)

#in progress
#function directed when folding button is clicked
def folding_button(g, button_frame, root):
    button_frame.destroy()

def betting_button(g, button_frame, root):
    button_frame.destroy()

    betting_label = Label(root,text=f"You currently have {g.user[2]}$ max to bet\ninsert the amount of money you would like to bet as a single integer, then press enter ",padx=85, pady=4, bg="white", fg="black")
    betting_label.pack()

    bet_amount = Entry(root, width=75, bg="azure", fg="black", borderwidth=1)
    bet_amount.pack()


    bet_amount.insert(5, '')
    bet_amount_button = Button(root, text="enter", fg="pink", bg="black", command=lambda: checking_button(g, button_frame, root, bet_amount.get()))
    bet_amount_button.pack(pady=20)
    pass


def resize_cards(card):
    our_card_img = Image.open(card)
    our_card_resize_image = our_card_img.resize((100,143))
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_image)
    return our_card_image



def player_setup(numb, root, title1, player_amount, player_amount_button):
    #setup new screen and start game
    title1.destroy()
    player_amount.destroy()
    player_amount_button.destroy()
    g = Game(numb)


    #creating a frame
    frame = Frame(root, bg="white")
    frame.pack(pady=20)


    #creating a frame for the cards
    playerframe = LabelFrame(frame, text="Your Cards Are: ", bd=0)
    playerframe.grid(row=0, column=0, padx=10, ipadx=2)

    #labeling the frame
    card_1 = Label(playerframe, text='')
    card_1.grid(row = 1, column = 0)

    card_2 = Label(playerframe, text='')
    card_2.grid(row = 1, column = 1)

    global player_image
    global player_image2
    player_image = resize_cards(f'card_deck/{g.user[3]}.png')
    player_image2 = resize_cards(f'card_deck/{g.user[4]}.png')
    card_1.config(image=player_image)
    card_2.config(image=player_image2)

    button_frame = Frame(root, bg="white")
    button_frame.pack(pady=50)

    check_button = Button(button_frame, text="check", command = lambda: checking_button(g, button_frame, root))
    check_button.grid(row=3, column=0, ipady=20, ipadx=20)

    fold_button = Button(button_frame, text="fold", command = lambda: folding_button(g, button_frame, root))
    fold_button.grid(row=3, column=3, ipady=20, ipadx=20)

    bet_button = Button(button_frame, text="bet", command =lambda: betting_button(g, button_frame, root))
    bet_button.grid(row=3, column=5, ipady=20, ipadx=20)

    root.mainloop()


    pass



#This checks the users player amount input
#If it is valid it allows them to proceed to the next step
#They must enter a valid computer player number for them to move on
def check_player_numb(root, title1, player_amount, player_amount_button, player_numb=0):
    if player_numb.isnumeric():
        if int(player_numb) > 1:
            if int(player_numb) <= 10:
                player_setup(int(player_numb), root, title1, player_amount, player_amount_button)


#This starts off the user interface
#It gives a title and geometry and makes the color
#This also has an entry space and an enter button so that the user can enter the amount of computer players
def start_gui():
    #gui setup
    root = Tk()
    root.title("Welcome to Texas Holdem Poker")
    root.geometry("800x600")
    root.configure(background="azure")

    #giving info about what to do with following entry space
    prompt1 = Label(root, text = "insert the number of computer players you would like to play with and press enter (min=1, max=10): ", padx=85,pady=4, bg= "white", fg="black")
    prompt1.pack()

    #creating the entry space
    player_amount = Entry(root,width=75,bg="azure",fg="black",borderwidth=1)
    player_amount.pack()
    player_amount.insert(5, '')

    #creating the enter button and directing to the check_player_numb if clicked to make sure its valid
    player_amount_button = Button(root, text="enter", command=lambda: check_player_numb(root, prompt1, player_amount, player_amount_button, player_amount.get()), fg="pink", bg="black")
    player_amount_button.pack(pady=20)


    root.mainloop()



start_gui()


#Notes prior arg parse function
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

#Notes prior UI function
'''

def usermode_game(player_num):

    #sets up the game and stores the variables needed to be saved
    #print("------------ Welcome to Texas Hold EM Poker ------------\n")

    #if player_num <= 1: raise Exception("invalid input")
    #money_left = {}
    #loop = True

    while loop:
        #creates a new game
        #g = Game(player_num)

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
'''