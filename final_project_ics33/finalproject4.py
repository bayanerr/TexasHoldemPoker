import random
from itertools import combinations
import argparse
import csv
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk
from os import getcwd

bots_money_left = {}
players_money_left = {}
cwd = getcwd()



#This function resizes the cards displayed on the gui
def resize_cards(card):
    our_card_img = Image.open(card)
    our_card_resize_image = our_card_img.resize((100,143))
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_image)
    return our_card_image

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
        values_list.append(int(i[1:]))
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

def highest_card(cards):
    x = []
    for i in cards:
        x.append(i[1])
    for i in x:
        if i == 1:
            return i
    return max(x)

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
        self.c1= random.choice(self.cards)
        self.c2=random.choice(self.cards)
        self.c3=random.choice(self.cards)
        self.c4=random.choice(self.cards)
        self.c5=random.choice(self.cards)
        self.user = [0, 10, self.rank, random.choice(self.cards), random.choice(self.cards), self.c1, self.c2, self.c3, self.c4, self.c5]
        for i in range(self.player_amount):
            self.players.append([i+1,10,self.rank, random.choice(self.cards), random.choice(self.cards), self.c1, self.c2, self.c3, self.c4, self.c5])
        #goes through the global dictionary and adjusts the bot players money from previous games if needed
        for i in self.players:
            for keys, values in bots_money_left.items():
                if keys == i[0]:
                    i[1] = values
        # goes through the global dictionary and adjusts the users money from previous games if needed
        for keys, values in players_money_left.items():
            if keys == 0:
                self.user[1] = values

    def starting_bids(self, user_bet):
        self.starting_bids_string = 'Computer Player Initial Bids:\n\n'
        for i in self.players:
            self.starting_bids_string = self.starting_bids_string + "Player " + str(i[0]) + ": "

            bot_bet = 1
            bot_max = int(i[1])
            
            small = int(bot_max / 3)
            med = int(bot_max / 2)
            large = bot_max - 2

            if user_bet >= 5:
                bot_bet += random.randint(0, small)
            elif user_bet <= 4 and user_bet >= 2:
                bot_bet += random.randint(small, med)
            else:
                bot_bet += random.randint(med, large)
            
            i[1] = i[1] - bot_bet

            self.starting_bids_string = self.starting_bids_string + f"amount bet: ${bot_bet}, money left: $" + str(i[1]) + "\n"
            self.betting_money = self.betting_money + 1
        return self.starting_bids_string

    #This determines the rank of the players after round 1
    def determine_rank_r1(self):
        for i in self.players:
            if Royal_Flush(i[3:8]) == True: i[2] = 0
            elif Straight_Flush(i[3:8]) == True: i[2] = 1
            elif four_of_a_kind(i[3:8]) == True: i[2] = 2
            elif full_house(i[3:8]) == True: i[2] = 3
            elif Flush(i[3:8]) == True: i[2] = 4
            elif Straight(i[3:8]) == True: i[2] = 5
            elif three_of_a_kind(i[3:8]) == True: i[2] = 6
            elif two_pairs(i[3:8]) == True: i[2] = 7
            elif pairs(i[3:8]) == True: i[2] = 8
            elif highcard(i[3:8]) == True: i[2] = 9

    #This decides if the players will bet and uses the bet function based on their rank
    #This also stores a string of whether the players bet or fold and how much they bet for the gui
    def betting(self):
        self.string = ''
        for i in self.players:

            bot_max = int(i[1])
            
            small = int(bot_max / 3) + 1
            med = int(bot_max / 2)
            large = bot_max - 1


            self.string = self.string + ("Player" + str(i[0]) + ": ")
            if i[2] >= 9:
                self.string = self.string + ("folds.\n")
                bots_money_left[i[0]] = i[1]

            elif i[2] <= 8 and i[2] >= 6:
                small_bet = random.randint(1, small)
                i[1] = i[1] - small_bet
                self.betting_money = self.betting_money + small_bet
                self.string = self.string + (f"amount bet: ${small_bet}, ")
                self.string = self.string + ("money left: $" + str(i[1]) + "\n")
                bots_money_left[i[0]] = i[1]

            elif i[2] <= 5 and i[2] >= 3:
                med_bet = random.randint(small, med)
                i[1] -= med_bet
                self.betting_money += med_bet
                self.string += (f"amount bet: {med_bet}, ")
                self.string += (f"money left: ${str(i[1])}\n")
                bots_money_left[i[0]] = i[1]

            else:
                large_bet = random.randint(med, large)
                i[1] -= large_bet
                self.betting_money += large_bet
                self.string += (f"amount bet: {large_bet}, ")
                self.string += (f"money left: ${str(i[1])}\n")
                bots_money_left[i[0]] = i[1]

        return self.string

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
def end_gui(root):
    root.destroy()

#in progress
#function directed when folding button is clicked
def folding_button(g, root, button_frame, numb, frame):
    button_frame.destroy()
    frame.destroy()

    g.user.append("folded")

    frame = Frame(root, bg="white")
    frame.pack(pady=10)

    game_summary = Label(frame, text = "Game Summary:")
    game_summary.grid(row=0, column=1)
    starting_bids = Label(frame, bg="ghost white", text=g.starting_bids(0))
    starting_bids.grid(row=1, column=0, padx=10)
    g.determine_rank_r1()
    round1_betting = Label(frame, bg= "ghost white", text="Round 1 Bids: \n\n" + g.betting())
    round1_betting.grid(row=1, column=1, padx=10)
    g.determine_rank_r2()
    round2_betting = Label(frame, bg="ghost white", text="Round 2 Bids: \n\n" + g.betting())
    round2_betting.grid(row=1, column=2, padx=10)


    # creating a frame for the buttons
    button_frame = Frame(root, bg="white")
    button_frame.pack(pady=50)

    # creating a check, fold, and bet, button that directs the player to different functions if clicked
    continue_playing = Button(button_frame, text="continue\nplaying",
                          command=lambda: player_setup(root, numb, frame, button_frame))
    continue_playing.grid(row=1, column=0, ipady=12, ipadx=10)
    quit = Button(button_frame, text="quit", command=lambda: end_gui(root))
    quit.grid(row=1, column=2, ipady=20, ipadx=20)


def bot_player_r3_choices():
    pass

def bot_player_r2_choices():
    pass





def community_round_2(g, root, card_frame):
    community_card_4 = Label(card_frame, text='')
    community_card_5 = Label(card_frame, text='')
    community_card_4.grid(row=1, column=3)
    community_card_5.grid(row=1, column=4)
    global community_card_image4
    global community_card_image5
    community_card_image4 = resize_cards('{}/card_deck/{}.png'.format(cwd, g.c4))
    community_card_image5 = resize_cards('{}/card_deck/{}.png'.format(cwd, g.c5))
    community_card_4.config(image=community_card_image4)
    community_card_5.config(image=community_card_image5)
    pass

#In progress
#Function directed when checking button is pressed
def checking_button(g, button_frame, root, bet_amount_get=0, bet_amount=None, betting_label=None, bet_amount_button=None):
    button_frame.destroy()

    if bet_amount: bet_amount.destroy()
    if bet_amount_button: bet_amount_button.destroy()
    if betting_label: betting_label.destroy()

    #creating a frame for the community cards
    frame = Frame(root, bg="white")
    frame.pack(pady=10)


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

    community_card_image1 = resize_cards('{}/card_deck/{}.png'.format(cwd, g.c1))
    community_card_image2 = resize_cards('{}/card_deck/{}.png'.format(cwd, g.c2))
    community_card_image3 = resize_cards('{}/card_deck/{}.png'.format(cwd, g.c3))
    community_card_1.config(image=community_card_image1)
    community_card_2.config(image=community_card_image2)
    community_card_3.config(image=community_card_image3)

    button_frame = Frame(root, bg="white")
    button_frame.pack()

    fold_button = Button(button_frame, text="fold")
    fold_button.grid(row=2, column=0, ipady=20, ipadx=20)

    bet_button = Button(button_frame, text="bet", command=lambda: betting_button(g, root, card_frame))
    bet_button.grid(row=2, column=1, ipady=20, ipadx=20)












def betting_button(g, button_frame, root):
    button_frame.destroy()

    betting_label = Label(root,text="You currently have ${} max to bet!\nInsert the amount of money you would like to bet as a single integer, then press enter. ".format(g.user[2]),padx=85, pady=4, bg="honeydew", fg="black")
    betting_label.pack()

    bet_amount = Entry(root, width=75, bg="ghost white", fg="black", borderwidth=1)
    bet_amount.pack()


    bet_amount.insert(5, '')
    bet_amount_button = Button(root, text="Enter", fg="black", bg="black", pady=10, padx=10, command=lambda: bot_player_r1_choices('bet', g, button_frame, root, int(bet_amount.get()), bet_amount, betting_label, bet_amount_button))
    #bet_amount_button = Button(root, text="Enter", fg="black", bg="black", pady=10, padx=10, command= player_bet(bet_amount))
    bet_amount_button.pack(pady=20)
    pass



def bot_player_r1_choices(button_clicked, g, button_frame, root, bet_amount_numb=0, bet_amount=None, betting_label=None, bet_amount_button=None):
    #getting rid of previous screen
    if button_frame: button_frame.destroy()
    if betting_label != None: betting_label.destroy()
    if bet_amount != None: bet_amount.destroy()
    if bet_amount_button != None: bet_amount_button.destroy()

    g.user[1] = g.user[1] - bet_amount_numb

    user_bid = Label(root, bg='ghost white', text= f"You bet ${bet_amount_numb}. You have ${g.user[1]} left.")
    user_bid.pack()

    #Displays the starting bids of all the bot players
    starting_bids = Label(root, bg = "ghost white", text = g.starting_bids(bet_amount_numb))
    starting_bids.pack()

    if button_clicked == 'check': pass
    if button_clicked == 'bet': pass
    if button_clicked == 'fold': pass
    pass


def player_setup(root, numb, frame, button_frame, title1=None, player_amount=None, player_amount_button=None):
    if frame: frame.destroy()
    if button_frame: button_frame.destroy()
    #removing previous screen
    if title1: title1.destroy()
    if player_amount: player_amount.destroy()
    if player_amount_button: player_amount_button.destroy()

    #starting new game using the Game class created
    g = Game(numb)
    if g.user[1] <= 0:
        print("not enough money to continue playing")
        end_gui(root)



    #creating a frame for the cards
    frame = Frame(root, bg="ghost white")
    frame.pack(pady=10)


    #creating a label for the frame
    playerframe = LabelFrame(frame, text="Your Cards Are: ", bd=0)
    playerframe.grid(row=0, column=0, padx=10, ipadx=2)

    #creating a spot for each of the player's card
    card_1 = Label(playerframe, text='')
    card_1.grid(row = 1, column = 0)
    card_2 = Label(playerframe, text='')
    card_2.grid(row = 1, column = 1)

    #adding an image into the spot
    global player_image
    global player_image2
    player_image = resize_cards(f'{cwd}/card_deck/{g.user[3]}.png')
    player_image2 = resize_cards(f'{cwd}/card_deck/{g.user[4]}.png')
    card_1.config(image=player_image)
    card_2.config(image=player_image2)

    #creating a frame for the buttons
    button_frame = Frame(root, bg="white")
    button_frame.pack(pady=50)

    #creating a check, fold, and bet, button that directs the player to different functions if clicked
    check_button = Button(button_frame, text="check", command = lambda: bot_player_r1_choices('check', g, button_frame, root))
    check_button.grid(row=3, column=0, ipady=20, ipadx=20)
    fold_button = Button(button_frame, text="fold", command = lambda: folding_button(g, root, button_frame, numb, frame))
    fold_button.grid(row=3, column=3, ipady=20, ipadx=20)
    bet_button = Button(button_frame, text="bet", command =lambda: betting_button(g, button_frame, root))
    bet_button.grid(row=3, column=5, ipady=20, ipadx=20)




#This checks the users player amount input
#If it is valid it allows them to proceed to the next step
#They must enter a valid computer player number for them to move on
def check_player_numb(root, title1, player_amount, player_amount_button, player_numb=None):
    frame=None
    button_frame=None
    if player_numb.isnumeric():
        if int(player_numb) > 1:
            if int(player_numb) <= 10:
                player_setup(root, int(player_numb), frame, button_frame, title1, player_amount, player_amount_button)


#This starts off the user interface
#It gives a title and geometry and makes the color
#This also has an entry space and an enter button so that the user can enter the amount of computer players
def start_gui(root=None):
    if root: root.destroy()
    root = Tk()
    root.title("Welcome to Texas Holdem Poker")
    root.geometry("1000x700")
    root.configure(background="honeydew")



    #giving info about what to do with following entry space
    prompt1 = Label(root, text = "Insert the number of computer players you would like to play with and press enter (min=1, max=10) ", padx=85,pady=4, bg= "honeydew", fg="black")
    prompt1.pack()

    #creating the entry space
    player_amount = Entry(root,width=75,bg="ghost white",fg="black",borderwidth=1)
    player_amount.pack()
    player_amount.insert(5, '')

    #creating the enter button and directing to the check_player_numb if clicked to make sure its valid
    player_amount_button = Button(root, text="enter", command=lambda: check_player_numb(root, prompt1, player_amount, player_amount_button, player_amount.get()), padx=10, pady=10, fg="black", bg="black")
    player_amount_button.pack(pady=20)

    #needed to loop everything and keep it on the screen
    root.mainloop()


start_gui()

