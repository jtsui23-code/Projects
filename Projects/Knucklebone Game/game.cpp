/*****************************************************************************
* 
*  Description:
*        This program displays a Knucklebone game window using SFMLL library.
*        Both players are prompted to enter their names. Once both names are entered,
*        the window transitions from the title screen to the game screen with two boards.
*        To roll, the player must press space on their respective turn. Then place their 
*        dice number on their grid which is labeled with their name. Once one of the two 
*        grids are filled, the winner is displayed. Players can destroy enmey columns if they
*        place a dice number on the same column as their opponent with the same dice number. 
*        Example) If player1 rolls a 5 and places it on column 2 and player2 has a 5 on any 
*        cell on their own column 2, then they lose that cell number with a 5 in it.
* 
*  Usage:
*       ./s.sh game.cpp -o game
*      ./game [filename]
* 
*  Files:            game.cpp
*                    game.exe 
*                    grid.hpp
*                    diceRoll.hpp
*                    diceRoll.exe (Do not need to run)
*                    s.sh (The bash file for compiling SFML faster)
*               
*****************************************************************************/

#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include "diceRoll.hpp"         // include animation for dice roll
#include "grid.hpp"             // include grid
#include<string>
#include <map> 
#include<vector>
#include <SFML/Audio.hpp>       


/**
 * Player Class
 * 
 * Description:
 *      This class represents a player in the Knucklebone game, 
 *      storing the player's name and score.
 * 
 * Public Methods:
 *      - void setName(std::string playerName)
 *      - std::string getName()
 *      - void setScore(int playerScore)
 *      - int getScore() const
 *      - void increaseScore(int points)
 *
 * 
 * Usage: 
 *      - Player player();
 *      - player.setName("Player Name");
 *      - player.getName();
 *      - player.setScore(100);
 *      - player.getScore();
 *      - player.increaseScore(50);
 */
class Player {
private:
    std::string name;
    int score;

public:

    Player() : score(0) {}

    /**
     * Public: setName
     * 
     * Description:
     *      Sets the player's name.
     * 
     * Parameters:
     *      - std::string playerName: The player's name.
     * 
     * Returns:
     *      - None
     */
    void setName(std:: string playerName) 
    {
        name = playerName;
    }

    /**
     * Public: getName
     * 
     * Description:
     *      Gets the player's name.
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - std::string: The player's name.
     */

    std::string getName()
    {
        return name;
    }

    /**
     * Public: setScore
     * 
     * Description:
     *      Sets the player's score.
     * 
     * Parameters:
     *      - int playerScore: The player's score.
     * 
     * Returns:
     *      - None
     */
    void setScore(int playerScore) {
        score = playerScore;
    }


    /**
     * Public: getScore
     * 
     * Description:
     *      Gets the player's score.
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - int: The player's score.
     */
    int getScore() const {
        return score;
    }

    /**
     * Public: increaseScore
     * 
     * Description:
     *      Increases the player's score by a specified amount.
     * 
     * Parameters:
     *      - int points: The amount to increase the score by.
     * 
     * Returns:
     *      - None
     */
    void increaseScore(int points) 
    {
        score += points;
    }

    
};

/**
 *  Game Class
 * 
 * Description:
 *      This class represents the Knucklebone game, handling game logic, 
 *      user input, and graphics rendering.
 * 
 * Public Methods:
 *      - void checkMouse(sf::Event event)
 *      - void close()
 *      - bool isOpen()
 *      - void inputNames(sf::Event event)
 *      - void loadAssets()
 *      - void rollDice()
 *      - void updateDice()
 *      - void updateGame()
 *      - int calculateScore()
 *
 * 
 * Usage: 
 *      - Game game(sf::RenderWindow &w);
 *      - game.checkMouse(sf::Event event);
 *      - game.close();
 *      - game.isOpen();
 *      - game.inputNames(sf::Event event);
 *      - game.rollDice();
 *      - game.loadAssets();
 *      - game.updateDice();
 *      - callculateScore(std::vector<sf::Text>& grid1);
 */


class Game
{
    private:

    // Array size 2 of Player objects
    // They represent the player1 and player2
    Player player[2];

    // This is the dimension of the 
    // window screen.
    int height;
    int width;

    // Creates music object for playing and storing music
    sf:: Music music;    
    

    // This creates two Grid objects
    // that are displayed on the screen
    // and that perform the gridNum logic
    Grid grid1;
    Grid grid2;

    // Variable for storing fonts used in the game
    sf::Font font;
    sf::Font titleFont;

    // This is a pointer to a sfml window
    sf::RenderWindow* window;

    // This texture is what gives the roll button its
    // red gradient 
    sf::Texture buttonTexture;

    // This stores the lamb image
    // to be the turn indicator
    sf:: Texture turnSkin;

    // This is the turn indicator
    // object itself that gets the lamb image
    // texture
    sf:: RectangleShape turnIndicator;   

    // This is the rectangle object that 
    // is the roll button 
    sf::RectangleShape button;

    // These are vectors that store all of the 
    // numbers on each respective grid
    std:: vector< sf::Text> grid1Num;
    std:: vector< sf::Text> grid2Num;

    // This is text that overlays the 
    // roll button to 
    // prompt the user to 
    // press space to roll the dice
    sf::Text roll;

    // This text prompts the user to input their name on
    // the title screen.
    sf::Text instructionText;

    // This text stores the text that is being 
    // typed dynamically
    sf::Text nameText;

    // This is text for displaying each player's name 
    // on their respective grid
    sf::Text displayName;
    sf::Text displayName2;


    
    // This stores the player names 
    std::string userInput[2];

    // This checks if each player has entered their names
    bool nameEntered[2] = {false, false};
    
    // Index for player names that are inputed 
    // Will increment when Player1 has their name inputed and 
    // INcrement again when player2 has their name inputed to 
    // Transition to game screen.
    int i;

    
    // This is text for display this "Score: " 
    // on the screen to indicate a scorer on 
    // each grid
    sf:: Text score1Display;
    sf:: Text score2Display;   

    // While this is the acutal number that is displayed 
    // after "Score:"
    sf:: Text score1;
    sf:: Text score2;

    // Create a DiceRollAnimation instance
    DiceRollAnimation diceRoll;  

    int diceNum;
    bool firstTurn;
    int diceRolls;

    // Text used to display text of the 
    // winner of the game.
    sf:: Text declareWinner;
    
    // Text used to display the game name
    // on the title screen.
    sf:: Text titleName;

    // label above the turn indicator
    // to explain what the turn indicator image
    // means
    sf:: Text turnText;



    public:

     /**
     * Public: Constructor
     * 
     * Description:
     *      Initializes the game with a reference to the SFML window.
     * 
     * Params:
     *      - sf::RenderWindow &w: Reference to the SFML window.
     * 
     * Return:
     *      Void
     */

    Game(sf::RenderWindow &w) : grid1(3, 3, 125.f, 120.f, 80.f), grid2(3, 3, 125.f, 800.f - 25.f, 80.f), window(&w),
    turnIndicator(sf:: Vector2f(150.f, 200.f)), button(sf:: Vector2f(200.f, 100.f)), roll("Space", font, 50)
    ,instructionText("Enter your Players' name:", font, 24), nameText("", font, 24), displayName("", font, 45)
    , displayName2("", font, 45), score1("Score: ", font, 45), score2("Score: ", font, 45), score1Display("Score: ", font, 45)
    ,score2Display("Score: ", font, 45), diceRoll("media/animations/dice_roll/", "frame_", sf::milliseconds(50))
    , declareWinner("", font, 60), titleName("Knucklebone", titleFont, 150), turnText("Turn", font, 45)

    {
    height = 1200;
    width = 800;
    window->setFramerateLimit(60); // Cap the frame rate to 60

    loadAssets();

    // Set sthe position and color of the game tile
    titleName.setPosition(sf::Vector2f(200.f, 10.f));
    titleName.setFillColor(sf::Color::White);

    // Set sthe position and color of the turn indicator label
    turnText.setPosition(sf::Vector2f(590.f, 350.f));
    turnText.setFillColor(sf::Color::White);

    // Set sthe position and texture of the turn indicator 
    turnIndicator.setPosition(sf::Vector2f(550.f, 450.f));
    turnIndicator.setTexture(&turnSkin);

    // Set sthe position and texture of the roll button 
    button.setPosition(535.f,630.f);
    button.setTexture(&buttonTexture);

    //Fills in 9 indexs with empty text 
    grid1Num.resize(9, sf::Text("0", font, 45));
    grid2Num.resize(9, sf::Text("0", font, 45));

    // Set sthe position and texture of the roll button text
    roll.setPosition(565.f, 640.f);
    roll.setFillColor(sf::Color::White);

    // Prompts for player name input
    instructionText.setPosition(50, 200);
    instructionText.setFillColor(sf::Color::White);

    // Set sthe position and color of the typed text in the 
    // player input screen 
    nameText.setPosition(350, 200);
    nameText.setFillColor(sf::Color::Green);


    // Set sthe position and color of the  player names 
    // that will be displayed above their respective 
    // grid during the game
    displayName.setPosition(300, 25);
    displayName.setFillColor(sf::Color::Yellow);

    displayName2.setPosition(950, 25);
    displayName2.setFillColor(sf::Color::Yellow);


    // Setting up the win declaration text.
    declareWinner.setPosition(380.f,630.f);
    declareWinner.setFillColor(sf::Color::White);

    // Sets up the position and color of the score that 
    // will be displayed under each grid. 
    // the score is displaying each player's total score
    score1.setFillColor(sf::Color:: White);
    score2.setFillColor(sf::Color::White);
    score1.setPosition(400.f, 455.f);
    score2.setPosition(width + 250.f, 455.f);

    score1Display.setFillColor(sf::Color:: White);
    score2Display.setFillColor(sf::Color::White);
    score1Display.setPosition(250.f, 450.f);
    score2Display.setPosition(width + 100.f, 450.f);

    // Set initial position for the dice animation
    diceRoll.setPosition(900.f, 560.f);
    diceRoll.setScale(1.2f,1.2f);


    // Sets names of players to nothing and
    // their checker to false to indicate
    // no names have been entered
    userInput[0] = {""};
    userInput[1] = {""};
    nameEntered[0] = {false};
    nameEntered[1] = {false};

    // Index for which player has entered their name
    // 0 representing player1
    // 1 repsenting player2
    i = 0;
   
    // Set the dice number to 0 so
    // player cannot one use 
    // previous dice roll on their own grid
    // and forcing player to have to roll once to 
    // start the game
     diceNum = 0;

     // checker for if its player1's turn
     firstTurn = true;

     // count for how many dice rolls are left per
     // player so player cannot do infinite dice rolls
     diceRolls = 1;


    }

    /**
     * Public: loadAssets()
     * 
     * Description:
     *      Loads the font file specified in fontPath.
     * 
     * Returns:
     *      - void: No return value.
     */

    void loadAssets()
    {
        // Loads music 
        
        if (!music.openFromFile("media/music/Intro.wav"))
        {
            std::cerr << "Failed to load music file!" << std::endl;
        }
    
        
        if (!titleFont.loadFromFile("media/extra/titleFont.ttf")) 
        {
        std::cerr << "Error: Could not load texture 'titleFont.ttf'\n";

        }

        if (!buttonTexture.loadFromFile("media/extra/Red.png")) 
        {
        std::cerr << "Error: Could not load texture 'Red.png'\n";

        }

        if (!turnSkin.loadFromFile("media/extra/Player1.png" )) 
        {
        std::cerr << "Error: Could not load texture 'Player1.png'\n";
        }

        if (!font.loadFromFile("media/fonts/arial.ttf")) 
        {
        // Handle error
        std::cout << "Can't load font";
        }

        if (!diceRoll.loadFrames(1, 24)) 

        {  
        std::cerr << "Failed to load dice roll frames!" << std::endl;
        }

    }

     /**
     * Public: checkMouse
     * 
     * Description:
     *      Checks for mouse input and places dice number on grid and 
     *      handles destroy column mechanic.
     * 
     * Params:
     *      - sf::Event event: SFML event object.
     * 
     * Returns:
     *      Void
     */

    void checkMouse(sf::Event event)
    {
        

        // Checks for mouse input
        if(event.type == sf:: Event:: MouseButtonPressed && event.mouseButton.button == sf:: Mouse::Left)
            {

                // Stores the mouse posiiton of the mouse click
                sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);

                // This ensures that the player
                // has rolled a new dice because once a player has rolled
                // and placed the number down diceNum becomes 0 
                // making it to where a player cannot use their opponets last 
                // dice roll on their own grid
                if(diceNum > 0)
                {
                    // This checks if it is the first player's turn
                    if(firstTurn)
                    {
                        
                        // Places the dice number the player roll onto an cell
                        // if it is emepty 
                        if(grid1.putNumOnClickedCell(mousePos, diceNum))
                        {
                            
                            //This gives the player a dice roll allow them to roll
                            // otherwise the roll animation/function would not run
                            // this is in place to prevent rerolling dices
                            diceRolls++;

                            // This onlys players to place numbers on cells while
                            // no grid are fully filled
                            if ( grid1.countFillGrid() < 9  && grid2.countFillGrid() < 9)
                            {
                                // This logic check if the lastly dice number placement 
                                // can destroy the opponents column
                                int lastClickedCellIndexP1 = grid1.getLastClickedCellIndex();
                                grid2.checkCanDestroyColumn(lastClickedCellIndexP1, diceNum);

                                // Have to check if cells in column can be shifted down or there will
                                // be floating cells after a destroyed column
                                grid2.shiftCellsDown();
                            }

                            //Updates vector storing all grid1's numbers
                            grid1Num = grid1.getGridNum();
                            // Sets diceNum to 0 so other player can't use the same dice roll of their
                            // grid
                            diceNum = 0;

                            //Switches turn
                            firstTurn = !firstTurn;
                        }
                        
                    }

                    //This runs whenever its the second player's turn
                    else if(!firstTurn)
                    {
  
                        // Places the dice number the player roll onto an cell
                        // if it is emepty 
                        if(grid2.putNumOnClickedCell(mousePos, diceNum))
                        {

                            //This gives the player a dice roll allow them to roll
                            // otherwise the roll animation/function would not run
                            // this is in place to prevent rerolling dices
                            diceRolls++;

                            // This onlys players to place numbers on cells while
                            // no grid are fully filled
                            if(grid2.countFillGrid() < 9 && grid1.countFillGrid() < 9)
                            {
                                // This logic check if the lastly dice number placement 
                                // can destroy the opponents column
                                int lastClickedCellIndexP2 = grid2.getLastClickedCellIndex();
                                grid1.checkCanDestroyColumn(lastClickedCellIndexP2, diceNum);

                                // Have to check if cells in column can be shifted down or there will
                                // be floating cells after a destroyed column
                                grid1.shiftCellsDown();

                            }

                            //Updates vector storing all grid2's numbers
                            grid2Num = grid2.getGridNum();

                            // Sets diceNum to 0 so other player can't use the same dice roll of their
                            // grid
                            diceNum = 0;

                            //Switches turn
                            firstTurn = !firstTurn;
                        }
                    }
                }
           }    


    }

     /**
     * Public: close
     * 
     * Description:
     *      Closes the game window.
     * 
     * Para:
     *      None
     * 
     * Returns:
     *      Void
     */

    void close()
    {
        window->close();
    }

    /**
     * Public: isOpen
     * 
     * Description:
     *      Checks if the game window is open.
     * 
     * Para: 
     *      - None
     * 
     * Returns:
     *      - bool: True if the window is open, false otherwise.
     */

    bool isOpen()
    {
        return window->isOpen();
    }

    /**
     * Public: inputNames
     * 
     * Description:
     *      Handles user input for player names.
     * 
     * Params:
     *      - sf::Event event: SFML event object.
     * 
     * Returns:
     *      - None
     */

    void inputNames(sf::Event event)
    {
        // Checks if both players have entered their name
        if (!nameEntered[i] && i < 2) 
        {
            // Checks if key input is a letter, backspace or enter key
            if (event.type == sf::Event::TextEntered) 
            {
                if (event.text.unicode == '\b') 
                {
                    // Handle backspace
                    if (!userInput[i].empty()) 
                    {
                        userInput[i].pop_back();
                    }
                }   
                else if (event.text.unicode == '\r') 
                {
                    // Handle enter
                    nameEntered[i] = true;

                    if (i == 0) {
                        displayName.setString(userInput[0]);
                    }

                    if (i == 1) {
                        displayName2.setString(userInput[1]);
                    }

                    if (i < 1) 
                    {
                        i++;
                    }
                }    

                else if (event.text.unicode < 128) 
                {
                // Handle valid characters
                userInput[i] += static_cast<char>(event.text.unicode);

                }

                nameText.setString(userInput[i]);
            }
        }
    }


    
    /**
     * Public: rollDice
     * 
     * Description:
     *      Rolls the dice and updates the game state.
     * 
     * Parameters:
     *      - sf::Event event: SFML event object.
     * 
     * Returns:
     *      - None
     */
    void rollDice(sf::Event event)
    {
        // Start the animation on space key press
            if (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::Space) {
                if (diceRolls != 0)
                {
                    // Can only roll dice if no grid is fill
                    if(grid2.countFillGrid() < 9 && grid1.countFillGrid() < 9)
                    {

                        diceRoll.startAnimation(); // Start the animation when Space is pressed
                        diceNum = diceRoll.getRandomFrame();
                        diceRolls--;
                    }
                }
            }
    }

    /**
     * Public: updateDice
     * 
     * Description:
     *      Updates the dice animation.
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - None
     */
    void updateDice()
    {
        diceRoll.update();
    }


    /**
     * Public: clear
     * 
     * Description:
     *      Clears the game window.
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - None
     */
    void clear()
    {
    window->clear(sf::Color::Black);
    }

    /**
     * Public: playMusic
     * 
     * Description:
     *      Starts playing the music of the game.
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - None
     */

    void playMusic()
    {

        music.setVolume(25.f);
        // Plays the music on loop
        if (music.getStatus() != sf::Music::Playing) 
        {
            music.play();
        }

    }

    /**
     * Public: updateGame
     * 
     * Description:
     *      Updates the game state and renders the game window.
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - None
     */
    void updateGame()
    {
    
        //Starts playing the music right away to prevent
        // delay between loops
        playMusic(); 
            
        // This will make the game remain on the title screen or
        //  until both player has entered their 
        // names
         if (!nameEntered[i] && i < 2) 
        {
            window->draw(titleName);
            window->draw(instructionText);
            window->draw(nameText);
        } 
        
        // This is the game screen
        // that appears after both players have entered their names 
        // 
        else
        {
            // If none of the grids are filled, 
            // Continue the game loop
            if(grid2.countFillGrid() < 9 && grid1.countFillGrid() < 9)
            {
                if (firstTurn)
                {
                    turnIndicator.setScale(1.f,1.f);
                    turnIndicator.setPosition(sf::Vector2f(550.f, 450.f));
                }
                if (!firstTurn)
                {
                    turnIndicator.setScale(-1.f, 1.f);
                    // If you don't reoffset the position
                    // then the image will be positioned off to the left
                    turnIndicator.setPosition(sf::Vector2f(550.f + 150.f , 450.f));
                }

                // Displays the turn indicator label
                window->draw(turnText);

                // Displays the turn indicator 
                window->draw(turnIndicator);

                // Makes a copy of the vector of Text 
                // Containing all of the numbers on a single grid
                grid1Num = grid1.getGridNum();
                grid2Num = grid2.getGridNum();

                // Displays the grid and the numbers in each of the 
                // grid cells
                grid1.draw(*window);
                grid2.draw(*window);

                // renders the roll button on the screen
                window->draw(button);
                window->draw(roll);

                //Displays both players' names
                window->draw(displayName);
                window->draw(displayName2);

                // Displays both players' score on the bottom of their grid
                window->draw(score1Display);
                window->draw(score2Display);

                diceRoll.draw(*window);           // Draw the dice animation


                // Gets the calculated scores for each player with the 
                // multiplier for any of the same numbers in the common column
                int sc1 = calculateScore(grid1Num);
                int sc2 = calculateScore(grid2Num);


                // This converts the int scores into strings 
                // so they are in a data type that can by displayed on
                // the window
                score1.setString(std::to_string(sc1));
                score2.setString(std::to_string(sc2));

                // Displays the scores
                window->draw(score1);
                window->draw(score2);

                
                // Stores the name of the player and their score in player class
                player[0].setScore(std::stoi(score1.getString().toAnsiString()));
                player[0].setName(displayName.getString());

                player[1].setScore(std::stoi(score2.getString().toAnsiString()));
                player[1].setName(displayName2.getString());

                


            }

            // If one of the grids are filled, 
            // Show who the winner is of the game and stop
            // the game loop
            if(grid2.countFillGrid() >= 9 || grid1.countFillGrid() >= 9)
            {
                // Makes a copy of the vector of Text 
                // Containing all of the numbers on a single grid
                grid1Num = grid1.getGridNum();
                grid2Num = grid2.getGridNum();

                // Displays the grid and the numbers in each of the 
                // grid cells
                grid1.draw(*window);
                grid2.draw(*window);

                //Displays both players' names
                window->draw(displayName);
                window->draw(displayName2);

                // Displays both players' score on the bottom of their grid
                window->draw(score1Display);
                window->draw(score2Display);


                // Gets the calculated scores for each player with the 
                // multiplier for any of the same numbers in the common column
                int sc1 = calculateScore(grid1Num);
                int sc2 = calculateScore(grid2Num);


                // This converts the int scores into strings 
                // so they are in a data type that can by displayed on
                // the window
                score1.setString(std::to_string(sc1));
                score2.setString(std::to_string(sc2));

                // Displays the scores
                window->draw(score1);
                window->draw(score2);


                 // Stores the name of the player and their score in player class
                player[0].setScore(std::stoi(score1.getString().toAnsiString()));
                player[0].setName(displayName.getString());

                player[1].setScore(std::stoi(score2.getString().toAnsiString()));
                player[1].setName(displayName2.getString());

                // Checks which player has the higher score and 
                // declares them the winner through the text display.
                if(player[0].getScore() > player[1].getScore())
                {
                    declareWinner.setString(player[0].getName() + " has won the game.");
                }

                else if(player[0].getScore() < player[1].getScore())
                {
                    declareWinner.setString(player[1].getName() + " has won the game.");
                }

                window->draw(declareWinner);

            }
            

        }
        

        
        // Display everything
        window->display();

        // Render the window
        //window.clear(sf::Color::White);  // Clear the window with a white color
        
        
    }

    /**
     * Public: calculateScore
     * 
     * Description:
     *      Calculates the score for a given grid. Accounts for the score multiplier 
     *      if there are many of the same numbers in a common column. 
     *      If there are two fo the same number then double their sum.
     *      Ex) If there are two 3's in the same column their score would add up to 
     *      be 3 + 3 = 6 * 2 so 12. 
     *      If there are 3 of the same number in a common column then 
     *      their sum is triples. 
     *      Ex) If there are four 5's in the same column then the score for those cells would be
     *      5 + 5 + 5 = 15 * 3 = 45
     * 
     * Parameters:
     *      - const std::vector<sf::Text>& gridNumbers: Vector of Text objects representing the grid numbers.
     * 
     * Returns:
     *      - int: The calculated score.
     */
    

    int calculateScore(const std::vector<sf::Text>& gridNumbers) 
    {
        int score = 0;
        int gridCol = 3;  // Number of columns in the grid
        int gridRow = 3;  // Number of rows in the grid

        // Map to store frequencies of numbers per column
        // An array of maps 
        // the key of the map is the number that 
        // appears in the colmn and its pair is the frequency 
        // of that number appearing in a colmn
        // ex) a colmn of 2 2 5
        // the map would look like {2: 2, 5:1}
        std::map<int, int> frequencyCounter[gridCol];

        // Count frequencies per column
        for (int i = 0; i < gridNumbers.size(); i++) 
        {
            if (!gridNumbers[i].getString().isEmpty()) 
            {
                int number = std::stoi(gridNumbers[i].getString().toAnsiString());

                // Calculate the column index
                int colIndex = i % gridCol;

                // Increment the frequency of the number in this column


                // Exlanation: [colIndex] access a specific index in the array of maps
                // so in the first iteration of the for loop 
                // this will access the first map in the array of maps { 1.{_:_, _:_}, 2.{_:_, _:_}, 3.{_:_, _:_}}
                // then it will set the key of that map to the value of the cell in the grid
                // then it will increment how many times it has seen that value in the map by 1
                // which is indicated by the ++ in frequencyCounter[colIndex][number]++;

                // Ex) If the second column is filled with 3 4 3 
                // this would pick the second map in the array { 1.{_:_, _:_}, 2.{_:_, _:_}, 3.{_:_, _:_}}
                // then it would make a key {3:2, 4:1} 


                frequencyCounter[colIndex][number] = frequencyCounter[colIndex][number] + 1;
            }
        }

        // Calculate the score based on frequencies        

        // Iterates through the array of maps 
        // then goes through the whole map that its focuses on 
        // first iteration it will go through the first map 
        // { 1.{_:_, _:_}, 2.{_:_, _:_}, 3.{_:_, _:_}}
        for (int col = 0; col < gridCol; col++) 
        {
            for (const auto& pair : frequencyCounter[col]) 
            {
                int number = pair.first;   // The number in the column
                int frequency = pair.second; // How many times it appears

                if (frequency == 2) 
                {
                    // Double the sum if the number appears twice
                    score += (number * 2 * 2); // (sum) * 2
                } 
                else if (frequency == 3) 
                {

                    // Triple the sum if the number appears three or more times
                    score += (number * 3 * 3); // (sum) * 3
                } 
                else 
                {

                    // Add the number as is if it appears only once
                    score += number;
                }

                
            }
        }

        return score;
    }


   


    
  
};



int main() 
{
    // Creates game window
    sf::RenderWindow window(sf::VideoMode(1200, 800), "KnuckleBone");

    // Creates game object and passes in the window createdd above
    Game game(window);

    //Load the assets of the game
    game.loadAssets();


    // Seed the random number generator for the dice roll
    // This is so every new game has a different set of dice rolls
    std::srand(static_cast<unsigned>(std::time(nullptr)));




    // Main game loop
    while (window.isOpen()) 
    {


        // Game event object used for tracking mouse input/ keyboard input
        sf::Event event;
        while (window.pollEvent(event)) 
        {
            // Checks if the user clicks x button on the game
            // If so exit the game
            if (event.type == sf::Event::Closed) 
            {
                game.close();
            }
            
            // Checks for mouse input 
            game.checkMouse(event);

            // Checks for keyboard input
            game.inputNames(event);

            // Start the animation on space key press
            game.rollDice(event);
        }

        // Rolls the dice
        game.updateDice();

        // Clears screen to remove old displayed objects
        game.clear();       
        
        // Updates the game logic and window
        game.updateGame();


    }
    return 0;
}

