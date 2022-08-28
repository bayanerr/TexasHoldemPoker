# finalproject.py
#Submitters:
# Grace Newman
# Bayan Tabbaa

import random
from itertools import combinations
import argparse
import csv
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk
from os import getcwd
import sys
import os

bots_money_left = {}
players_money_left = {}
cwd = getcwd()


############# CARD FUNCTIONS ############


# This function resizes the cards displayed on the gui
def resize_cards(card):
    our_card_img = Image.open(card)
    our_card_resize_image = our_card_img.resize((100, 143))
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_image)
    return our_card_image


# this function figures out if any players have a flush
def Flush(cards):
    suit_set = set()
    for i in cards:
        suit_set.add(i[0])
    if len(suit_set) == 1:
        return True
    return False


# this function figures out if any players have a royal flush
def Royal_Flush(cards):
    values_set = set()
    # reuse the Flush function to ensure it meets the Flush criteria first
    if Flush(cards) == False:
        return False
    for i in cards:
        values_set.add(i[1:])
    if values_set == {10, 11, 12, 13, 14}: return True
    if values_set == {'10', '11', '12', '13', '14'}: return True
    return False


# this function figures out if any players have a straight flush
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


# this function figures out if any players have four of a kind
def four_of_a_kind(cards):
    values = []
    for i in cards:
        values.append(int(i[1:]))
    sorted_values = sorted(values)
    if sorted_values[0] == sorted_values[1] and sorted_values[1] == sorted_values[2] and sorted_values[2] == \
            sorted_values[3]:
        return True
    elif sorted_values[1] == sorted_values[2] and sorted_values[2] == sorted_values[3] and sorted_values[3] == \
            sorted_values[4]:
        return True
    return False


# this function figures out if any players have three of a kind
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


# this function figures out if any players have a full house
def full_house(cards):
    values_set = set()
    if three_of_a_kind(cards) == True:
        for i in cards:
            values_set.add(int(i[1:]))
        if len(values_set) == 2: return True
    return False


# this function figures out if any players have a straight
def Straight(cards):
    values_list = []
    for i in cards:
        values_list.append(int(i[1:]))
    values_list = sorted(values_list)
    if (values_list[0] + 1 == values_list[1]) and (values_list[1] + 1 == values_list[2]) and \
            (values_list[2] + 1 == values_list[3]) and (values_list[3] + 1 == values_list[4]): return True
    return False


# this function figures out if any players have two pairs
def two_pairs(cards):
    values_set = set()
    for i in cards:
        values_set.add(int(i[1:]))
    if len(values_set) == 3: return True
    return False


# this function figures out if any players have pairs
def pairs(cards):
    values_set = set()
    for i in cards:
        values_set.add(int(i[1:]))
    if len(values_set) == 4: return True
    return False


# this function determines if a player has a high card 10 or greater
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


# this function generates the deck of cards
def generate_cards():
    card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ["C", "D", "H", "S"]
    cards = []
    for value in card_values:
        for suit in suits:
            cards.append(str(suit) + str(value))
    return cards


################### GAME CLASS ####################


# This class is used to design the game.
class Game:
    # It initializes through the player amount. In the initialization,
    # variables like the players and their individual 2 cards
    # and the deck of cards are also created
    def __init__(self, player_amount):
        self.player_amount = player_amount
        self.players = []
        self.cards = generate_cards()
        self.betting_money = 0
        self.rank = 11
        self.c1 = random.choice(self.cards)
        self.c2 = random.choice(self.cards)
        self.c3 = random.choice(self.cards)
        self.c4 = random.choice(self.cards)
        self.c5 = random.choice(self.cards)
        self.user = [0, 10, self.rank, random.choice(self.cards), random.choice(self.cards), self.c1, self.c2, self.c3,
                     self.c4, self.c5]

        for i in range(self.player_amount):
            self.players.append(
                [i + 1, 10, self.rank, random.choice(self.cards), random.choice(self.cards), self.c1, self.c2, self.c3,
                 self.c4, self.c5])
        # goes through the global dictionary and adjusts the bot players money from previous games if needed
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
        self.players_copy2 = self.players
        self.players = []
        for i in self.players_copy2:
            self.starting_bids_string = self.starting_bids_string + "Player " + str(i[0]) + ": "

            bot_bet = 1
            bot_max = int(i[1])
            small = int(bot_max / 3)
            med = int(bot_max / 2)
            large = bot_max - 2

            if i[1] > 1:
                if user_bet >= 5:
                    bot_bet += random.randint(0, small)
                elif user_bet <= 4 and user_bet >= 2:
                    bot_bet += random.randint(small, med)
                else:
                    bot_bet += random.randint(med, large)
                i[1] = i[1] - bot_bet
                self.betting_money += bot_bet
                self.players.append(i)
            elif i[1] == 0:
                pass
            else:
                bot_bet = 0
                i[1] = i[1] - bot_bet
                self.players.append(i)
            self.starting_bids_string = self.starting_bids_string + f"amount bet: ${bot_bet}, money left: $" + str(
                i[1]) + "\n"
            #self.betting_money = self.betting_money + 1
        return self.starting_bids_string

    # This determines the rank of the players after round 1
    def determine_rank_r1(self):
        for i in self.players:
            if Royal_Flush(i[3:8]) == True:
                i[2] = 0
            elif Straight_Flush(i[3:8]) == True:
                i[2] = 1
            elif four_of_a_kind(i[3:8]) == True:
                i[2] = 2
            elif full_house(i[3:8]) == True:
                i[2] = 3
            elif Flush(i[3:8]) == True:
                i[2] = 4
            elif Straight(i[3:8]) == True:
                i[2] = 5
            elif three_of_a_kind(i[3:8]) == True:
                i[2] = 6
            elif two_pairs(i[3:8]) == True:
                i[2] = 7
            elif pairs(i[3:8]) == True:
                i[2] = 8
            elif highcard(i[3:8]) == True:
                i[2] = 9

    # This decides if the players will bet and uses the bet function based on their rank
    # This also stores a string of whether the players bet or fold and how much they bet for the gui
    def betting(self):
        self.string = ''
        self.players_copy = self.players
        self.players = []
        for i in self.players_copy:
            bot_max = int(i[1])
            small = int(bot_max / 3)
            med = int(bot_max / 2)
            large = bot_max - 1
            self.string = self.string + ("Player" + str(i[0]) + ": ")
            if i[2] == 10:
                self.string += "folds.\n"
            if i[1] == 0:
                self.string += "out of money, out of game.\n"
            elif i[2] <= 7 and i[2] >= 3:
                med_bet = random.randint(small, med)
                i[1] -= med_bet
                self.betting_money += med_bet
                self.string += (f"amount bet: ${med_bet}, ")
                self.string += (f"money left: ${str(i[1])}\n")
                bots_money_left[i[0]] = i[1]
                self.players.append(i)

            elif i[2] <= 2:
                large_bet = random.randint(med, large)
                i[1] -= large_bet
                self.betting_money += large_bet
                self.string += (f"amount bet: ${large_bet}, ")
                self.string += (f"money left: ${str(i[1])}\n")
                bots_money_left[i[0]] = i[1]
                self.players.append(i)
            else:
                try:
                    small_bet = random.randint(1, small)
                except:
                    small_bet = 1

                i[1] = i[1] - small_bet
                self.betting_money += small_bet
                self.string = self.string + (f"amount bet: ${small_bet}, ")
                self.string = self.string + ("money left: $" + str(i[1]) + "\n")
                bots_money_left[i[0]] = i[1]
                self.players.append(i)

        return self.string

    # this determines the rank for round 2
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

    # this determines the winner and gives them the betting money
    def determine_winner(self):
        if self.user[-1] != 'folded':
            self.players.append(self.user)
            #players_money_left[self.user[0]] += self.user[0]
        h = []
        for i in self.players:
            h.append(i[2])
        s = sorted(h)
        m = s[0]
        l = []
        for i in s:
            if i == m:
                l.append(i)
        #x = 0
        if len(l) > 1:
            for i in self.players:
                if i[2] in l:
                    if highest_card(i[3:]) > 0:
                        x = highest_card(i[3:])
            i[1] = i[1] + self.betting_money
            bots_money_left[i[0]] += i[1]
            return i[0]
        else:
            for i in self.players:
                if i[2] == l[0]:
                    i[1] = i[1] + self.betting_money
                    bots_money_left[i[0]] += i[1]
                    return i[0]
    def results(self):
        self.results_string = ''
        self.results_string += "The winner of this round is: player "
        self.results_string += str(self.determine_winner()) + "\n"
        self.results_string += "Final Player Standings\n"
        for i in self.players:
            if i[0] == 0: self.results_string += ("You, money left: " + str(i[1]) + "$\n")
            else: self.results_string += ("player " + str(i[0]) + ", money left: " + str(i[1]) + "$\n")
        return self.results_string


class gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Welcome to Texas Hold'em!")
        self.root.geometry("1000x700")
        self.root.configure(background="honeydew")
        self.bet_amount = Entry(self.root, width=75, bg="ghost white", fg="black", borderwidth=1)
        self.bet_amount_button = Button(self.root, text="Enter", fg="black", bg="black", pady=10, padx=10,
                                        command=lambda: self._bot_decisions())
        self.round = 0


    def start_gui(self, game, num=None):
        self.num = num
        if num == None:
            # giving info about what to do with following entry space
            self.player_amount_prompt = Label(self.root,
                                              text="Insert the number of computer players you would like to play with and press enter (min=1, max=10) ",
                                              padx=85, pady=4, bg="honeydew", fg="black")
            self.player_amount_prompt.pack()

            # creating the entry space
            self.player_amount_entry = Entry(self.root, width=75, bg="ghost white", fg="black", borderwidth=1)
            self.player_amount_entry.pack()
            self.player_amount_entry.insert(5, '')

            # creating the enter button and directing to the check_player_numb if clicked to make sure its valid
            self.player_amount_button = Button(self.root, text="enter",
                                               command=lambda: self.check_num_players(
                                                   int(self.player_amount_entry.get())),
                                               padx=10, pady=10, fg="black", bg="black")
            self.player_amount_button.pack(pady=20)
        else:
            #self.g.distribute_cards(self.num)
            self.g = Game(self.num)
            self.player_setup(self.num)


    def button_frame_function(self, checking=None):

        self.button_frame = Frame(self.root, bg="white")
        self.button_frame.pack(pady=20)
        self.moves = []
        if checking == None: self.checking_button = Button(self.button_frame, text="check",
                                                           command=self.checking_button_command)
        self.folding_button = Button(self.button_frame, text="fold", command=lambda: self.folding_button_command())
        self.betting_button = Button(self.button_frame, text="bet", command=lambda: self.betting_button_command())
        self.betting_label = Label(self.root, padx=85, pady=4, bg="honeydew", fg="black")


    def check_num_players(self, num, destroy=None):
        self.num = num
        if num >= 1 and num <= 10:
            if destroy != None:
                #self.g.distribute_cards(self.num)
                self.g = Game(self.num)
                self.player_setup(num)
            else:
                self.player_setup(num, 'destroy')

    def player_setup(self, num, destroy=None):
        self.num = num
        if destroy == 'destroy':
            self.player_amount_prompt.destroy()
            self.player_amount_entry.destroy()
            self.player_amount_button.destroy()
            #self.user_card_frame.destroy()
            #self.button_frame.forget()
            #self.summary_frame.destroy()
            #self.cp_button_frame.destroy()
            #self.user_card_frame.destroy()
        self.g = Game(num)
        if self.g.user[1] <= 0:
            print("You went BROKE!\nGAME OVER")
            self.end_gui()
        self.user_card_frame = Frame(self.root, bg="ghost white")
        self.user_card_frame.pack(pady=10)

        # creating a label for the frame
        self.user_card_label = LabelFrame(self.user_card_frame, text="Your Cards Are: ", bd=0)
        self.user_card_label.grid(row=0, column=0, padx=10, ipadx=2)

        # creating a spot for each of the player's card
        self.card_1 = Label(self.user_card_label, text='')
        self.card_1.grid(row=1, column=0)
        self.card_2 = Label(self.user_card_label, text='')
        self.card_2.grid(row=1, column=1)

        # implementing card images
        self.card_1_image = resize_cards(f'{cwd}/card_deck/{self.g.user[3]}.png')
        self.card_2_image = resize_cards(f'{cwd}/card_deck/{self.g.user[4]}.png')
        self.card_1.config(image=self.card_1_image)
        self.card_2.config(image=self.card_2_image)

        # packing button frame
        # button_frame = self.button_frame
        # button_frame.pack(pady=50)
        # self.button_frame = Frame(self.root, bg="white").pack(pady=50)
        self.button_frame_function()

        # packing move buttons
        cb = self.checking_button
        fb = self.folding_button
        bb = self.betting_button
        cb.grid(row=3, column=0, ipady=20, ipadx=20)
        fb.grid(row=3, column=3, ipady=20, ipadx=20)
        bb.grid(row=3, column=5, ipady=20, ipadx=20)

    def round_two(self):
        if self.round <= 3:
            self.round += 1
            #self.bet_amount.forget()
            #self.bet_amount_button.forget()
            self.button_frame_function('no')
            self.betting_button.pack()
            self.folding_button.pack()
        else:
            self.folding_button_command()

    def checking_button_command(self):
        self._destroy_move_buttons()
        self._bot_decisions()
        self.round_two()
        pass

    def folding_button_command(self):
        self._destroy_move_buttons()
        self.user_card_frame.forget()
        self.summary_frame = Frame(self.root, bg="white")
        self.summary_frame.pack(pady=10)

        self.game_summary = Label(self.summary_frame, text="Game Summary:")
        self.game_summary.grid(row=0, column=1)
        # if init_bot_bets:
        # starting_bids = Label(frame, bg="ghost white", text=init_bot_bets)
        # starting_bids.grid(row=1, column=0, padx=10)
        # else:
        # starting_bids = Label(frame, bg="ghost white", text=g.starting_bids(0))
        # starting_bids.grid(row=1, column=0, padx=10)
        self.g.determine_rank_r1()
        self.round1_betting = Label(self.summary_frame, bg="ghost white", text="Round 1 Bids: \n\n" + self.g.betting())
        self.round1_betting.grid(row=1, column=1, padx=10)
        self.g.determine_rank_r2()
        self.round2_betting = Label(self.summary_frame, bg="ghost white", text="Round 2 Bids: \n\n" + self.g.betting())
        self.round2_betting.grid(row=1, column=2, padx=10)
        results = self.g.results()
        self.round2_betting = Label(self.summary_frame, bg="ghost white", text=results)
        self.round2_betting.grid(row=1, column=3, padx=10)

        # creating a frame for the buttons
        self.cp_button_frame = Frame(self.root, bg="white")
        self.cp_button_frame.pack(pady=50)
        num = self.num
        self.g.__init__(self.num)
        # creating a check, fold, and bet, button that directs the player to different functions if clicked
        self.continue_playing = Button(self.cp_button_frame, text="continue\nplaying",
                                       command=lambda: start_gui(num, self.root))
        self.continue_playing.grid(row=1, column=0, ipady=12, ipadx=10)
        self.quit = Button(self.cp_button_frame, text="quit", command=lambda: self.end_gui())
        self.quit.grid(row=1, column=2, ipady=20, ipadx=20)

    def betting_button_command(self):
        self._destroy_move_buttons()
        self.round += 1
        if int(self.g.user[2]) > 0:
            self.betting_label[
                "text"] = "You currently have ${} max to bet!\nInsert the amount of money you would like to bet as a single integer, then press enter. ".format(
                self.g.user[2])
            self.betting_label.pack()
            if self.round < 2:
                self.bet_amount.pack()
            else:
                self.bet_amount = Entry(self.root, width=75, bg="ghost white", fg="black", borderwidth=1)
                self.bet_amount.pack()

            self.bet_amount.insert(5, '')
            self.bet_amount_button.pack(pady=20)
            if self.round > 1:
                self.betting_label[
                    "text"] = "You currently have ${} max to bet!\nInsert the amount of money you would like to bet as a single integer, then press enter. ".format(
                    self.g.user[2])
                #self.betting_label.forget()
                #self._show_ccs()
                self.round_two()
        else:
            self.end_gui()
            print('You went BROKE!\nGAME OVER')
    def _destroy_buttons_after_betting(self):
        self.betting_label.forget()
        self.bet_amount.forget()
        self.bet_amount_button.forget()
        pass

    def _bot_decisions(self):
        if self.bet_amount.get().isnumeric():
            self.user_bet_amount = int(self.bet_amount.get())
        else:
            self.user_bet_amount = 0
        #self._destroy_buttons_after_betting()
        # can use self.user_bet_amount now
        self.info_frame = Frame()
        self.info_frame.pack()
        self.g.user[1] = self.g.user[1] - self.user_bet_amount
        self.g.betting_money += self.user_bet_amount

        self.user_bid_label = Label(self.info_frame,
                                    text=f"You bet ${self.user_bet_amount}. You have ${self.g.user[1]} left.").pack()
        self.bots_bid_label = Label(self.info_frame, text=f"{self.g.betting()}").pack()
        # Displays the starting bids of all the bot players
        # self.bot_bids_label["text"] = f"{self.g.betting()}"
        # self.bot_bids_label.pack()

        # self.betting_label.forget
        # self.bet_amount.forget

        # if self.round in (1, 2):
        if self.round == 1:
            self.betting_label.forget()
            self.bet_amount.forget()
            self.bet_amount_button.forget()
            self._show_ccs()
            self.round_two()

    def _append_move(self, move):
        self.moves.append(move)

    def _destroy_move_buttons(self):
        button_frame = self.button_frame
        c = self.checking_button
        f = self.folding_button
        b = self.betting_button

        buttons = [c, f, b, button_frame]

        for button in buttons:
            button.forget()

    def _show_ccs(self):

        if self.round == 1:
            self.cc_card_frame = Frame(self.root, bg="ghost white")
            self.cc_card_frame.pack(pady=10)
            # creating a label for the frame
            self.cc_card_label = LabelFrame(self.cc_card_frame, text="The Community Cards Are: ", bd=0)
            self.cc_card_label.grid(row=0, column=0, padx=10, ipadx=2)
            # creating a spot for each of the player's card
            self.cc_1 = Label(self.cc_card_label, text='')
            self.cc_1.grid(row=1, column=0)
            self.cc_2 = Label(self.cc_card_label, text='')
            self.cc_2.grid(row=1, column=1)
            self.cc_3 = Label(self.cc_card_label, text='')
            self.cc_3.grid(row=1, column=2)

            # implementing card images
            self.cc_1_image = resize_cards(f'{cwd}/card_deck/{self.g.c1}.png')
            self.cc_2_image = resize_cards(f'{cwd}/card_deck/{self.g.c2}.png')
            self.cc_3_image = resize_cards(f'{cwd}/card_deck/{self.g.c3}.png')
            self.cc_1.config(image=self.cc_1_image)
            self.cc_2.config(image=self.cc_2_image)
            self.cc_3.config(image=self.cc_3_image)

        if self.round > 1:
            self.cc_card_frame.forget()
            self.cc_card_frame.pack(pady=10)
            #self.cc_card_frame = Frame(self.root, bg="ghost white")
            #self.cc_card_frame.pack(pady=10)

            # creating a label for the frame
            #self.cc_card_label = LabelFrame(self.cc_card_frame, text="The Community Cards Are: ", bd=0)
            #self.cc_card_label.grid(row=0, column=0, padx=10, ipadx=2)

            #self._destroy_buttons_after_betting()
            self.cc_1 = Label(self.cc_card_label, text='')
            self.cc_1.grid(row=1, column=0)
            self.cc_2 = Label(self.cc_card_label, text='')
            self.cc_2.grid(row=1, column=1)
            self.cc_3 = Label(self.cc_card_label, text='')
            self.cc_3.grid(row=1, column=2)

            # implementing card images
            self.cc_1_image = resize_cards(f'{cwd}/card_deck/{self.g.c1}.png')
            self.cc_2_image = resize_cards(f'{cwd}/card_deck/{self.g.c2}.png')
            self.cc_3_image = resize_cards(f'{cwd}/card_deck/{self.g.c3}.png')
            self.cc_1.config(image=self.cc_1_image)
            self.cc_2.config(image=self.cc_2_image)
            self.cc_3.config(image=self.cc_3_image)

            self.cc_4 = Label(self.cc_card_label, text='')
            self.cc_4.grid(row=1, column=3)
            self.cc_5 = Label(self.cc_card_label, text='')
            self.cc_5.grid(row=1, column=4)

            self.cc_4_image = resize_cards(f'{cwd}/card_deck/{self.g.c4}.png')
            self.cc_5_image = resize_cards(f'{cwd}/card_deck/{self.g.c5}.png')
            self.cc_4.config(image=self.cc_4_image)
            self.cc_5.config(image=self.cc_5_image)


    def end_gui(self):
        self.root.destroy()


#starts the gui and resets when the player wants to continue playing
def start_gui(num=None, roots=None):
    if roots:
        roots.destroy()
        game = Game(num)
    else: game = None
    g = gui()
    g.start_gui(game, num)
    g.root.mainloop()
    # gui.start_gui()


if __name__ == '__main__':
    # gui = gui()
    # gui.start_gui()
    # gui.root.mainloop()
    start_gui()
