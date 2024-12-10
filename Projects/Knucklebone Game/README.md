## Knucklebone Game In SFML

### Description:
This program displays a Knucklebone game window using the SFML library. Both players are prompted to enter their names.
Once both names are entered, the window transitions from the title screen to the game screen with two boards. 
To roll, the player must press space on their respective turn. Then place their dice number on their grid which is labeled with their name. 
Once one of the two grids is filled, the winner is displayed. Players can destroy enemy columns if they place a dice number 
on the same column as their opponent with the same dice number. Example: If player1 rolls a 5 and places it on column 2 
and player2 has a 5 on any cell on their own column 2, then they lose that cell number with a 5 in it.

### Files:
|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | [game.cpp](https://github.com/jtsui23-code/2143-OOP/blob/main/Assignments/10-P03/game.cpp)        | This runs the program for Knucklkebone.      |
|   2   | [game.exe](https://github.com/jtsui23-code/2143-OOP/blob/main/Assignments/10-P03/game)          | This is the compiled Knucklebone game.                       |
|   3   | [grid.hpp](https://github.com/jtsui23-code/2143-OOP/blob/main/Assignments/10-P03/grid.hpp)        | Hpp file for Grid Class.      |
|   4  | [diceRoll.hpp](https://github.com/jtsui23-code/2143-OOP/blob/main/Assignments/10-P03/diceRoll.hpp)        | Hpp file for DiceRollAnimation Class.      |
|   5  | [diceRoll.exe](https://github.com/jtsui23-code/2143-OOP/blob/main/Assignments/10-P03/diceRoll)        | Compile DiceRollAnimation (do not run).      |
|   6  | [s.sh](https://github.com/jtsui23-code/2143-OOP/blob/main/Assignments/10-P03/s.sh)        | Bash script for making compiling SFML easier.      |


### Instructions:

- Compile the program
- Run the program using the terminal
- Enter the name of the input file as an argument
- Play game
  
### Example:
  - ./s.sh game.cpp -o [write the name of exe you want]
  - ./[name of exe] 
