#pragma once
#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <cstdlib>  // For std::rand and std::srand
#include <ctime>    // For seeding random number generator



/**
 * DiceRollAnimation Class
 * 
 * Description:
 *      This class represents a dice roll animation, handling the loading of animation frames, 
 *      updating the animation, and rendering the current frame.
 * 
 * Public Methods:
 *      - DiceRollAnimation(const std::string& folderPath, const std::string& framePrefix, sf::Time frameDuration)
 *      - bool loadFrames(int start, int end)
 *      - void startAnimation()
 *      - void update()
 *      - void setScale(float x, float y)
 *      - void setPosition(float x, float y)
 *      - void draw(sf::RenderWindow& window)
 *      - int getRandomFrame()
 *
 * 
 * Usage: 
 *      - DiceRollAnimation diceRoll(const std::string& folderPath, const std::string& framePrefix, sf::Time frameDuration);
 *      - diceRoll.loadFrames(int start, int end);
 *      - diceRoll.startAnimation();
 *      - diceRoll.update();
 *      - diceRoll.setScale(float x, float y);
 *      - diceRoll.setPosition(float x, float y);
 *      - diceRoll.draw(sf::RenderWindow& window);
 *      - diceRoll.getRandomFrame();
 */
class DiceRollAnimation {
private:
    std::vector<sf::Texture> textures; // Stores textures for animation frames
    sf::Sprite sprite;                 // Sprite to display the current frame
    sf::Clock clock;                   // Timer for frame updates
    sf::Time frameDuration;            // Duration of each frame
    size_t currentFrame;               // Index of the current frame
    bool isAnimating;                  // Is the animation playing?
    std::string framePrefix;           // Prefix for frame files
    std::string folderPath;            // Path to the folder containing frames
    size_t randomFrame;                // Random dice side (1-6)
    sf:: Texture ranText;


public:
    
    /**
     * Public: DiceRollAnimation
     * 
     * Description:
     *      Constructor for the DiceRollAnimation class.
     * 
     * Parameters:
     *      - const std::string& folderPath: Path to the folder containing the animation frames.
     *      - const std::string& framePrefix: Prefix for the animation frame file names.
     *      - sf::Time frameDuration: Duration of each animation frame (default is 1 millisecond).
     * 
     * Returns:
     *      - None
     */
    DiceRollAnimation(const std::string& folderPath, const std::string& framePrefix, sf::Time frameDuration = sf::milliseconds(1))
        : folderPath(folderPath), framePrefix(framePrefix), frameDuration(frameDuration), currentFrame(0), isAnimating(false), randomFrame(0) {}

    /**
     * Public: loadFrames
     * 
     * Description:
     *      Loads the animation frames from the specified folder.
     * 
     * Parameters:
     *      - int start: Starting frame number.
     *      - int end: Ending frame number.
     * 
     * Returns:
     *      - bool: True if the frames were loaded successfully, false otherwise.
     */
    bool loadFrames(int start, int end) {
        std::string frameNum[2] = {"00", "0"};
        int g = 0;

        for (int i = start; i <= end; ++i) {
            sf::Texture texture;
            if (i > 9) g = 1;
            std::string fileName = folderPath + framePrefix + frameNum[g] + std::to_string(i) + ".png";

            if (!texture.loadFromFile(fileName)) {
                std::cerr << "Error loading " << fileName << std::endl;
                return false;
            }
            textures.push_back(texture);
        }
        sprite.setTexture(textures[0]); // Start with the first frame
        return true;
    }


    /**
     * Public: getRandomFrame
     * 
     * Description:
     *      Returns the randomly selected dice side (1-6).
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - int: The randomly selected dice side.
     */
    int getRandomFrame()
    {
        return randomFrame;
    }


    /**
     * Public: startAnimation
     * 
     * Description:
     *      Starts the dice roll animation.
     * 
     * Parameters:
     *      - None
     * 
     * Returns:
     *      - None
     */
    void startAnimation() {
        if (!textures.empty()) {
            isAnimating = true;
            currentFrame = 0;
            clock.restart();
            randomFrame = std::rand() % 6 + 1; // Generate a random frame (1-6)
        }
    }


        /**
         * Public: update
         * 
         * Description:
         *      Updates the animation state.
         * 
         * Parameters:
         *      - None
         * 
         * Returns:
         *      - None
         */
        void update() {
        if (isAnimating) {
            if (clock.getElapsedTime() >= frameDuration) {
                clock.restart();
                currentFrame += 3;

                if (currentFrame >= textures.size()) {
                    isAnimating = false; // Stop the animation after the last frame

                    // Set to the random dice frame
                    ranText.loadFromFile("media/images/" + std::to_string(randomFrame) + ".png");
                    sprite.setTexture(ranText);
                } else {
                    sprite.setTexture(textures[currentFrame]);
                }
            }
        }
    }



    /**
     * Public: setScale
     * 
     * Description:
     *      Sets the scale of the sprite.
     * 
     * Parameters:
     *      - float x: Horizontal scale factor.
     *      - float y: Vertical scale factor.
     * 
     * Returns:
     *      - None
     */
    void setScale(float x, float y)
    {
        sprite.setScale(x,y);
    }


    /**
     * Public: setPosition
     * 
     * Description:
     *      Sets the position of the sprite.
     * 
     * Parameters:
     *      - float x: X-coordinate of the position.
     *      - float y: Y-coordinate of the position.
     * 
     * Returns:
     *      - None
     */
    void setPosition(float x, float y) {
        sprite.setPosition(x, y);
    }

    /**
     * Public: draw
     * 
     * Description:
     *      Draws the sprite on the specified window.
     * 
     * Parameters:
     *      - sf::RenderWindow& window: Window to draw the sprite on.
     * 
     * Returns:
     *      - None
     */
    void draw(sf::RenderWindow& window) {
        window.draw(sprite);
    }
};
