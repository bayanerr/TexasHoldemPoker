# PA3_Grace_Newman.py
## Texas Hold'em

PA3 is a construction of an interactive Python game of Texas Hold'em, one of the most popular poker games worldwide. A user who understands its interface should be able to play the game with bots, or they can run test cases through a .txt file with the expected results as a comparison with the program's output.
 

## Build Status

My program fits the specifications provided for the assignment, however I would like to make my bots more intelligent and/or add a more dynamic UI in the future.

## Code Style

PA3 uses mostly object-oriented programming (OOP), however, some free-floating functions are used in the program's file mode. Cards, decks, players, and games are all abstracted into their own classes.

## Framework

I used Visual Studio Code and my Macbook's Terminal to edit and test this code, although the modules used are compatible with Windows and Linux operating systems. Python3 is required to run this program.

## Installation

Install my program from [UCI Canvas](https://canvas.eee.uci.edu/)! PA3 uses Python modules *argparse*, *random*, *pathlib*, and *os* in its operations.

## Tests

The "file mode" of this project is meant to test the card ranking algorithm using .txt files in a directory. One .txt file, titled "test_results.txt", should exist in the same directory as the other .txt files. The program will print the number of successful test cases processed by the algorithm.

## Usage

PA3 should be run from your machine's command line. Because I own a Macbook, I use Terminal. In the Terminal syntax, the beginning of the line should read:

```unix
python3 PA3_Grace_Newman.py
```

This will be followed by the selected mode and some other information pertinent to the program's functionality.


There are two "modes" with which you can use this Texas Hold'em program. 

### User Mode

The first, "user mode", should can be accessed with this command:

```unix
python3 PA3_Grace_Newman.py -u -p number_of_players
```

The number of players includes you, and any remaining players will be filled-in by bots. Every player starts the game with 10 virtual "dollars".

You will be dealt hole cards and shown community cards through printed messages in the command line. Once you examine your cards, you can Check, Bet, or Fold. To Check or Fold, simply type one of those words, then hit Enter or Return.
To Bet, type:
```unix
Bet money_to_bet
```
and hit enter. *money_to_bet* should be an integer value between 1 and 10, but be careful not to bet more than what you have!

This process repeats itself twice, with more community cards being displayed each time. Bots will work in the background, and the winner of the round will be revealed at the end.

At the end of the game, you can choose to replay or quit after being given this command:
```unix
Would you like to play again? (y/n)
```
Simply type 'y' for yes, or 'n' for no, and hit Enter or Return.

### File Mode

To access "file mode", type this command:
```unix
python3 PA3_Grace_Newman.py -f -i path_to_directory
```
The indicated directory should contain test cases in .txt files, with this format:
```unix
1,H1,H3,D12,C6,S7
2,D9,S12,S4,H4,C10
```
etc. It should also contain one file, "test_results.txt", which contains the file names and the expected winners from each provided file. It should look like this:
```unix
0.txt,1
1.txt,3
```
etc.

The program will parse through these files and compare the calculated results with the expected results gleaned from *test_results.txt*. It will print the number of matching/successful test cases into the command line in this format:
```unix
38 tests successfully run
```
This will end the program.


## Credit
Thank you to Professor He and TA Brooke for helping me build my coding skills to this point! Brooke specifically helped me learn how to use the *argparse* module effectively.

I frequently utilized the Python Standard Library to better understand some of the commands I was using. This helped me avoid rewriting code that is already free for use in the public domain.

## License
I think my code technically belongs to UCI...