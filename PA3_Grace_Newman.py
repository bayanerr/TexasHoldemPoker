# PA3_Grace_Newman.py
# Student ID: 43355258
import argparse
import random
import pathlib
import os

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def greater_val(self, card):
        if self.value > card.value:
            return True
        elif self.value < card.value:
            return False
        else:
            return None

    def __repr__(self):
        return '%s%s' % (self.suit, self.value)

class Deck:
    def __init__(self):
        self.deck = []

        for suit in ['S', 'C', 'D', 'H']:
            for val in range(1,14):
                self.deck.append(Card(suit, val))

    def draw_card(self):
        rand = random.randint(1, len(self.deck) - 1)
        card = self.deck[rand]

        del self.deck[rand]

        return card

class Player:
    def __init__(self, id):
        self.id = id
        self.money = 10

        self.hole_cards = []
        self.hand = []
        self.rank = None
        self.points = 0
        self.highcard = None

    def print_hole_cards(self):
        print("Player {}: {}, {}".format(self.id, self.hole_cards[0], self.hole_cards[1]))

    def get_frequencies(self, full_hand):
        suit_freq = {}
        val_freq = {}

        for card in full_hand:
            if card.suit not in suit_freq.keys():
                suit_freq[card.suit] = 1
            else:
                suit_freq[card.suit] += 1

            if card.value not in val_freq.keys():
                val_freq[card.value] = 1
            else:
                val_freq[card.value] += 1

        return suit_freq, val_freq

    def determine_rank(self, table_cards):
        table1, table2, table3 = table_cards[0], table_cards[1], table_cards[2]
        full_hand = [self.hole_cards[0], self.hole_cards[1], table1, table2, table3]

        suit_freq, val_freq = self.get_frequencies(full_hand)

        val_list = list(val_freq.keys())

        for freq in suit_freq.values():
            if freq == 5:
                # royal flush
                if sorted(val_list) == [1, 10, 11, 12, 13]:
                    self.rank = 0
                    self.highcard = 13

                # straight flush
                elif val_list == list(range(val_list[0], val_list[0] + len(val_list))):
                    self.rank = 1
                    sval = sorted(val_list)
                    self.highcard = sval[-1]

                # flush
                else:
                    self.rank = 4
                    sval = sorted(val_list)
                    self.highcard = sval[-1]
            else:
                # four of a kind
                if 4 in val_freq.values():
                    self.rank = 2

                    vcopy = val_freq.copy()
                    for v in vcopy.keys():
                        if vcopy[v] == 4:
                            self.highcard = v
                            break

                # full house
                elif 3 in val_freq.values() and 2 in val_freq.values():
                    self.rank = 3

                    two_vals = []
                    vcopy = val_freq.copy()
                    for v in vcopy.keys():
                        if vcopy[v] == 3 and v not in two_vals:
                            two_vals.append(v)
                        elif vcopy[v] == 2 and v not in two_vals:
                            two_vals.append(v)
                    sval = sorted(two_vals)
                    self.highcard = sval[-1]

                # straight
                elif val_list == list(range(val_list[0], val_list[0] + len(val_list))):
                    self.rank = 5
                    sval = sorted(val_list)
                    self.highcard = sval[-1]

                # 3 of a kind
                elif 3 in val_freq.values():
                    self.rank = 6

                    vcopy = val_freq.copy()
                    for v in vcopy.keys():
                        if vcopy[v] == 3:
                            self.highcard = v
                            break

                # pairs and 2 pairs
                elif 2 in val_freq.values():
                    two_vals = []
                    vcopy = val_freq.copy()
                    for key, value in vcopy.items():
                        if 2 == value:
                            key2 = key
                            break
                    two_vals.append(key2)
                    del vcopy[key2]

                    # 2 pairs
                    if 2 in vcopy.values():
                        self.rank = 7

                        for k in vcopy.keys():
                            if vcopy[k] == 2:
                                two_vals.append(k)
                        sval = sorted(two_vals)
                        self.highcard = sval[-1]

                    # pairs
                    else:
                        self.rank = 8
                        self.highcard = two_vals[0]

                # highcard
                else:
                    self.rank = 9

                    sval = sorted(val_list)
                    self.highcard = sval[-1]

        return self.rank

    def determine_best_combo(self, table_cards):
        index_combos = [[0,1,2], [0,1,3], [0,1,4], [0,2,3], [0,2,4], [0,3,4], [1,2,3], [1,2,4], [1,3,4], [2,3,4]]

        best_rank = 10

        for combo in index_combos:
            sample_table = [table_cards[combo[0]], table_cards[combo[1]], table_cards[combo[2]]]

            sample_rank = self.determine_rank(sample_table)

            if sample_rank <= best_rank:
                best_rank = sample_rank

        self.rank = best_rank

    def get_decision(self):
        d = input("Would you like to Check, Bet, or Fold?   ")

        if d[0:5] == "Check":
            print('Player {}: Check'.format(self.id))
        elif d[0:4] == "Fold":
            print('Player {}: Fold'.format(self.id))
            return 'Fold'
        elif d[0:3] == "Bet":
            money = int(d[4:])
            self.money -= money
            print('Player {}: Bet ${}'.format(self.id, money))
            return money

        

class Game:
    def __init__(self, n_players, deck):
        self.n_players = n_players
        self.players = []
        self.deck = deck
        self.table = []
        self.pot = 0

    def generate_players(self):
        for i in range(1, self.n_players + 1):
            self.players.append(Player(i))

        return self.players

    def deal_hole_cards(self):
        for player in self.players:
            card1 = self.deck.draw_card()
            card2 = self.deck.draw_card()

            player.hole_cards = [card1, card2]

    def deal_table(self, num_cards):
        for i in range(num_cards):
            card = self.deck.draw_card()
            self.table.append(card)

    def print_table(self, num_cards):
        if num_cards == 3:
            print("Community Cards: {}, {}, {}".format(self.table[0], self.table[1], self.table[2]))
        else:
            print("Community Cards: {}, {}, {}, {}, {}".format(self.table[0], self.table[1], self.table[2], self.table[3], self.table[4]))

    def take_bet(self, id, amount):
        p = self.players[id - 1]
        print(p)
        p.money -= amount

        self.pot += amount

    def determine_winner(self):
        best_rank = 10
        winner = None
        for player in self.players:
            if player.rank < best_rank:
                best_rank = player.rank
                winner = [player]
            elif player.rank == best_rank:
                if player.highcard > winner[0].highcard:
                    winner = [player]
                elif player.highcard == winner[0].highcard:
                    winner = [player, winner[0]]

        return winner

    def print_balances(self):
        for player in self.players:
            print("Player {}: ${}".format(player.id, player.money))

    def check_and_boot(self):
        boot = []
        for i in range(len(self.players)):
            if self.players[i].money <=0:
                print('Player {} was booted for going BROKE!'.format(self.players[i].id))
                boot.append(0)
        
        if len(boot) > 0:
            del self.players[0]
            return True

    def get_bot_decisions(self, fold):
        decisions = []
        if fold == False:
            for bot in self.players[1:]:
                rank = bot.determine_rank(self.table)
                if rank <= 5:
                    decisions.append(random.randint(3, 7))
                else:
                    decisions.append('Player {}: Check'.format(bot.id))
        else:
            for bot in self.players:
                rank = bot.determine_rank(self.table)
                if rank <= 5:
                    decisions.append(random.randint(3, 7))
                else:
                    decisions.append('Player {}: Check'.format(bot.id))

        return decisions

    def final_bot_decisions(self, bot):
        if bot.rank <= 6:
            return random.randint(3, 7)
        else:
            return 'Check'

def take_input():
    parser = argparse.ArgumentParser()

    parser.add_argument('-usermode1', '-u', action='store_true',
                        help='Mode for the game, stores True if user mode.')
    parser.add_argument('-filemode2', '-f', action='store_true',
                        help='Mode for the game, stores True if file mode.')
    parser.add_argument('-info', '-p', '-i', type=str or int,
                        help='Denotes beginning of required info for game. Either num players or path to test cases.')

    args = parser.parse_args()
    umode, fmode, info = bool(args.usermode1), bool(args.filemode2), str(args.info)

    if umode == True:
        mode = 'usermode'
    else:
        mode = 'filemode'

    return mode, info


def get_test_results_file(dir_path):
    dir_path = pathlib.Path(dir_path)

    for f in dir_path.iterdir():
        if os.path.basename(f) == 'test_results.txt':
            return f


def store_test_results_file(path):
    d = {}

    with open(path) as f:
        for line in f.readlines():
            line = line.rstrip('\n').split(',')
            d[line[0]] = ','.join(line[1:])

    f.close()

    return d


def parse_directory(dir_path):
    dir_path = pathlib.Path(dir_path)

    test_files = []

    for f in dir_path.iterdir():
        if str(f)[-4:] == '.txt' and os.path.basename(f) != 'test_results.txt':
            test_files.append(f)

    return test_files


def _parse_file(path):
    path = pathlib.Path(path)

    with open(path) as f:
        players = []

        #ranks = []

        #for i in range(len(f.readlines())):
            #all_cards = f.readlines()[i].split(',')

            #p = Player(i)
            #players.append(p)

            #p.hole_cards = [all_cards[1], all_cards[2]]
            #tables = [all_cards[3], all_cards[4], all_cards[5]]
            #rank = p.determine_best_combo(tables)

            #ranks.append(rank)


        linecount = 0

        for line in f.readlines():
            cards = line.split(',')

            if len(cards) != 6:
                break

            else:

                all_cards = []

                for card in cards[1:]:
                    suit = card[0]
                    val = int(card[1:])

                    all_cards.append(Card(suit, val))


                p = Player(linecount)
                players.append(p)

                p.hole_cards = [all_cards[0], all_cards[1]]
                tables = [all_cards[2], all_cards[3], all_cards[4]]
                rank = p.determine_rank(tables)

                linecount += 1


        best_rank = 10
        winner = None
        for player in players:
            if player.rank < best_rank:
                best_rank = player.rank
                winner = [player]
            elif player.rank == best_rank:
                if player.highcard > winner[0].highcard:
                    winner = [player]
                elif player.highcard == winner[0].highcard:
                    winner = [player, winner[0]]

        winner_formatted = ''

        if len(winner) > 1:
            for winners in winner[:-1]:
                winner_formatted += str(winners.id)
                winner_formatted += ','
            winner_formatted += str(winner[-1].id)

        else:
            winner_formatted = str(winner[0].id)

        final = [os.path.basename(path), winner_formatted]

    f.close()

    return final
    

def calculate_and_format_results(test_files):
    d = {}

    for file in test_files:
        l = _parse_file(file)
        d[l[0]] = l[1]

    return d



def compare_output(result1, result2):
    total_successes = 0

    for key in result1.keys():
        if result1[key] == result2[key]:
            total_successes += 1

    return total_successes



if __name__ == '__main__':
        mode, info = take_input()

        if mode == 'usermode':
            print('Welcome, Player 1!')
            print('When asked to Check, Bet, or Fold, simply type your decision.')
            print('If your decision is to Check or Fold, just type Check or Fold and hit enter!')
            print('If your decision is to Bet, type \'Bet\', followed by one Space and the amount you would like to Bet.')

            info = int(info)

            replay = True

            while replay == True:
                
                deck = Deck()

                game = Game(info, deck)
                game.generate_players()

                game.deal_hole_cards()

                print("------Initializing Game--------")

                user = game.players[0]

                user.print_hole_cards()

                game.deal_table(3)
                game.print_table(3)

                table_cards = game.table

                print("------Round 1--------")

                user.determine_rank(table_cards)
                print("Player 1: Rank {}".format(user.rank))
                pot_money = user.get_decision()
                if type(pot_money) == int:
                    game.pot += pot_money
                    user_folded = False
                elif pot_money == 'Fold':
                    del game.players[0]
                    user_folded = True
                else:
                    user_folded = False


                if user_folded == False:
                    bot_ds = game.get_bot_decisions(False)
                    for i in range(len(bot_ds)):
                        if type(bot_ds[i]) == int:
                            print('Player {}: Bet ${}'.format(i + 2, bot_ds[i]))
                        else:
                            print(bot_ds[i])
                            if bot_ds[i][-4:] == 'Fold':
                                del game.players[i + 1]
                else:
                    bot_ds = game.get_bot_decisions(True)
                    for i in range(len(bot_ds)):
                        if type(bot_ds[i]) == int:
                            print('Player {}: Bet ${}'.format(i, bot_ds[i]))
                        else:
                            print(bot_ds[i])
                            if bot_ds[i][-4:] == 'Fold':
                                del game.players[i]

                boot = game.check_and_boot()
                if boot == True:
                    user_folded = True

                print("------Round 2--------")

                game.deal_table(2)

                if user_folded == False:
                    user.print_hole_cards()

                game.print_table(5)

                if user_folded == False:
                    user.determine_rank(table_cards)
                    print("Player 1: Rank {}".format(user.rank))
                    pot_money = user.get_decision()
                    if type(pot_money) == int:
                        game.pot += pot_money
                        user_folded2 = False
                    elif pot_money == 'Fold':
                        del game.players[0]
                        user_folded2 = True
                    else:
                        user_folded2 = False

                        if user_folded2 == False:

                            bots = game.players[1:]
                            for i in range(len(bots)):
                                bots[i].determine_best_combo(game.table)
                                decision = game.final_bot_decisions(bots[i])
                                if type(decision) == int:
                                    game.pot += decision
                                    bots[i].money -= decision
                                    print('Player {}: Bet ${}'.format(i + 2, decision))
                                else:
                                    print('Player {}: {}'.format(i + 2, decision))

                else:
                    for player in game.players:
                        player.determine_best_combo(game.table)
                        player.determine_best_combo(game.table)
                        decision = game.final_bot_decisions(player)
                        if type(decision) == int:
                            game.pot += decision
                            player.money -= decision
                            print('Player {}: Bet ${}'.format(player.id, decision))
                        else:
                            print('Player {}: {}'.format(player.id, decision))

                

                game.check_and_boot()

                print("------Results--------")

                winner = game.determine_winner()
                if len(winner) == 1:
                    winner[0].money += game.pot
                    print("Winner: Player {}".format(winner[0].id))
                else:
                    print("Tie between:")
                    for w in winner:
                        w.money += game.pot / len(winner)
                        print("Player {}".format(w.id))

                game.print_balances()

                game.check_and_boot()

                print("------End of Game--------")
                print("\n")

                replay_q = input('Would you like to play again? (y/n)   ')

                if replay_q == 'y':
                    replay = True
                else:
                    replay = False

        elif mode == 'filemode':
            info = pathlib.Path(info)

            test_results = get_test_results_file(info)

            d1 = store_test_results_file(test_results)

            test_files = parse_directory(info)

            d2 = calculate_and_format_results(test_files)

            successes = compare_output(d1, d2)

            print("{} tests successfully run".format(successes))
