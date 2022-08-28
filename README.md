# Final_Project.py
## Grace Newman
### Student ID: 43355258
## Bayan Tabbaa
### Student ID: 86148723
## Texas Hold'em

PA3 is a construction of an interactive Python game of Texas Hold'em, one of the most popular poker games worldwide. A user who understands its interface should be able to play the game with up to 10 "bot" players. You are able to interact with the program by running it in a Python environment. This should display a Tkintr window that will provide instructions.
 

## Build Status

The program fits the specifications provided for the assignment, featuring both with "smart" bots and an interactive graphical user interface (GUI).

## Code Style

Texas Hold'em uses mostly object-oriented programming (OOP), however, some free-floating functions are used in the program's file mode. A game of Texas Hold'em and the program's GUI are abstracted into two large classes. The GUI class initializes an instance of the Game class upon its creation.

## Framework

We used Visual Studio Code and my Macbook's Terminal to edit and test this code, although the modules used are compatible with Windows and Linux operating systems. Python 3.9.x is required to run this program.

## Installation

Install our .zip file from [UCI Canvas](https://canvas.eee.uci.edu/)! Texas Hold'em uses Python modules *random*, *itertools*, *argparse*, *csv*, *pathlib*, *tkinter*, *PIL*, *os*, and *sys* in its operations. A subdirectory of card image files should be in the *same directory* as the Texas Hold'em program file itself.

### *Important*
In order to run Texas Hold'em, you must install the third-party library PIL, or Pillow. We recommend using [pip](https://pip.pypa.io/en/stable/installation/) to access PIL via command line. If you are working in a virtual environment, pip should be installed by default. In order to install PIL from command line, simply type:
```bash
pip install pillow
```
in the command line editor of your choice.

## Tests
Texas Hold'em should be tested by having all its features and combinations of actions (Check, Fold, or Bet) be explored. The user has three "rounds" per game available to test, and up to 10 "bot" players are available to play with. Betting money is variable per round–- just don't go into debt!

## Usage

The Final Project runs in a Python3 environment with PIL installed to the environment's base.

There are two main features of this edition of Texas Hold'em.

### Smart Bots

There are two main considerations the bots make when deciding how much to bet: their current amount of money, and their calculated rank, based on their individual hand and the available community cards.

An algorithm determines, out of all possible combinations of cards, what the best ranking for each bot is, given their unique hand. This determines how much they should bet.

If bots have a "bad" ranking, they make a "small" bet. If bots have a "good" ranking, they make a "large" bet. If bots have a "medium" ranking, they make a "medium" bet. The size of the bets, however, are based on how much money each bot has, and thus vary from bot to bot.

### GUI

The GUI utilizes the Tkinter library. Buttons, Labels, and Entries allow the user to interact with the program at every stage, including:
* How many bot players they would like to play against
* What action they would like to take at every stage
* If they bet, how much
* Quit and Continue Playing functionality

The GUI is the user's key to interacting with the back-end of Texas Hold'em.

## Credit
Card images were downloaded from Wikimedia Commons.

Thank you to Professor He and TA Brooke for helping us build our first medium-size Python program!

### Individual Contributions
Bayan: main body of card and ranking functionality, root functions of GUI, debugging
Grace: OOP styling, button programming, "smart bot" algorithm, debugging

## License
This code is property of its developers and UCI Donald Bren School of Information and Computer Science.
