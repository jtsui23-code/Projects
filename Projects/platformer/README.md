# Platformer Game using Pygame

### Overview
A 2D platformer game built with Pygame, based on Pygame tutorial. I've extended the original tutorial by implementing additional features including:
- New particle effects for enemy projectiles
- Multiple jumps system
- Overuse of multiple jump penalty system


### Technical Implementation
- Built using Python and Pygame
- Implements sprite-based animation system
- Features collision detection and physics
- Uses JSON for level data storage
- Includes particle system for visual effects
  
### Description:
This program displays a Pygame platformer game. To move the character, use WASD or arrow keys. If the user presses space then the character dashes and can defeat enemies through dashing into them. When all enemies are defeated then the player transitions to the next level. Once the player has passed the third level, then the player has won the game.

### Files:
|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | [main.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/main.py)        | This runs the program for platformer.      |
|   2   | [levelEditor.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/levelEditor.py )         | This is runs the program for the level editor.                       |
|   3   | [data](https://github.com/jtsui23-code/Projects/tree/main/Projects/platformer/data)        | This folder contains all of the assets for the game.      |
|   4  | [level](https://github.com/jtsui23-code/Projects/tree/main/Projects/platformer/levels)        | This folder contains all of the levels of the game in json format.      |
|   5  | [script](https://github.com/jtsui23-code/Projects/tree/main/Projects/platformer/scripts)        | This folder contains all of the other scripts for the platformer.      |
|   6  | [beings.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/scripts/beings.py)        | Script for player and enemy physics and animations.      |
|   7  | [clouds.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/scripts/clouds.py)        | Script for generating clouds in the background.      |
|   8  | [particles.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/scripts/particle.py)        | Script for generating particle effects.      |
|   9  | [spark.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/scripts/spark.py)        | Script for generating spark particle effects for projectiles.      |
|   10  | [tilemap.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/scripts/tilemap.py)        | Script for tilemapping in the game.      |
|   11  | [utils.py](https://github.com/jtsui23-code/Projects/blob/main/Projects/platformer/scripts/util.py)        | Script for loading images and animations.      |

### Controls
- WASD/Arrow Keys: Movement
- Spacebar: Dash Attack


### Learning Outcomes
- Gained experience with game development principles
- Implemented physics and collision detection
- Created modular code structure with separate script files
- Designed custom game mechanics

### Instructions:

- Run main.py
- Play game
  

### Future Goals
- Plan to make other games using Pygame library with new knowledge acquired



