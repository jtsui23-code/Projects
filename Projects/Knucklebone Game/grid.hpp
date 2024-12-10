#pragma once

#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>
#include <utility>




/**
 * Grid Class
 * 
 * Description:
 *      This class represents a grid in the Knucklebone game, 
 *      handling grid logic, cell rendering, and user input.
 * 
 * Public Methods:
 *      - Grid()
 *      - Grid(int rows, int cols, float cellSize, float gridStartX, float gridStartY, std::string fontPath, float cellSpacing)
 *      - void loadAssets()
 *      - std::vector<sf::Text> getGridNum()
 *      - bool putNumOnClickedCell(const sf::Vector2f& pos, int diceNum)
 *      - int getLastClickedCellIndex()
 *      - void checkCanDestroyColumn(int enemyLastClickedIndex, int cellNum)
 *      - int countFillGrid()
 *      - void shiftCellsDown()
 *      - void draw(sf::RenderWindow& window)
 *
 * 
 * Usage: 
 *      - Grid grid();
 *      - Grid grid(int rows, int cols, float cellSize, float gridStartX, float gridStartY, std::string fontPath, float cellSpacing);
 *      - grid.loadAssets();
 *      - grid.getGridNum();
 *      - grid.putNumOnClickedCell(const sf::Vector2f& pos, int diceNum);
 *      - grid.getLastClickedCellIndex();
 *      - grid.checkCanDestroyColumn(int enemyLastClickedIndex, int cellNum);
 *      - grid.countFillGrid();
 *      - grid.shiftCellsDown();
 *      - grid.draw(sf::RenderWindow& window);
 */
class Grid {
private:
    int rows, cols;                        // Grid dimensions
    float cellSize;                        // Size of each cell
    float gridStartX, gridStartY;          // Starting position of the grid
    float cellSpacing;                     // Spacing between cells
    std::vector<sf::RectangleShape> grid;  // Vector to hold the grid cells
    std::vector<sf::Text> gridNum;         // Vector to hold the text (numbers) for the grid
    std::string fontPath;                  // Path to the font file
    sf::Font font;                         // Font object for rendering text
    int lastClickedCellIndex;              // Keeps track of the last cell that was clicked on the grid
                                           // needed for destroy enemy column mechanic

public:
    /**
     * Public: Grid()
     * 
     * Description:
     *      Default constructor for the Grid class.
     */
    Grid() {}

    /**
     * Public: Grid(int rows, int cols, float cellSize, float gridStartX, float gridStartY, std::string fontPath = "media/fonts/Arial.ttf", float cellSpacing = 0.f)
     * 
     * Description:
     *      Parameterized constructor to initialize grid attributes and create grid cells.
     * 
     * Params:
     *      - int rows: The number of rows in the grid.
     *      - int cols: The number of columns in the grid.
     *      - float cellSize: The size of each grid cell.
     *      - float gridStartX: The starting X coordinate for the grid.
     *      - float gridStartY: The starting Y coordinate for the grid.
     *      - std::string fontPath: The path to the font file.
     *      - float cellSpacing: The spacing between each cell.
     * 
     * Return:
     *      - void
     */
    Grid(int rows, int cols, float cellSize, float gridStartX, float gridStartY, std::string fontPath = "media/fonts/Arial.ttf", float cellSpacing = 0.f)
        : rows(rows), cols(cols), cellSize(cellSize), gridStartX(gridStartX), gridStartY(gridStartY), cellSpacing(cellSpacing), fontPath(fontPath) 
    {
        loadAssets();

        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                sf::RectangleShape cell(sf::Vector2f(cellSize, cellSize));
                cell.setFillColor(sf::Color::Black);  // Default cell color
                cell.setOutlineColor(sf::Color::White);
                cell.setOutlineThickness(2.f);

                // Calculate the position of each cell
                float x = gridStartX + col * (cellSize + cellSpacing);
                float y = gridStartY + row * (cellSize + cellSpacing);
                cell.setPosition(x, y);

                // Initialize the text for each cell with "0"
                gridNum.push_back(sf::Text("0", font, 45));
                gridNum.back().setPosition(x + 50.f, y + 35.f);
                gridNum.back().setFillColor(sf::Color::White);

                // Add the cell to the grid vector
                grid.push_back(cell);
            }
        }
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
        if (!font.loadFromFile(fontPath)) 
        {
            std::cout << "Can't load font";  // Print error if font fails to load
        }
    }

    /**
     * Public: getGridNum()
     * 
     * Description:
     *      Returns the vector of grid numbers (sf::Text objects).
     * 
     * Returns:
     *      - std::vector<sf::Text>: The vector of text objects representing numbers in the grid.
     */
    std::vector<sf::Text> getGridNum() 
    {
        return gridNum;
    }


    /**
     * Public: putNumOnClickedCell(const sf::Vector2f& pos, int diceNum)
     * 
     * Description:
     *      - Checks if the mouse click is on any cell and places the dice number in the first available empty cell in the clicked column.
     * 
     * Params:
     *      - const sf::Vector2f& pos: The mouse click position.
     *      - int diceNum: The number to place in the clicked cell.
     * 
     * Returns:
     *      - bool: True if the number was placed, false if the cell was full.
     */
    bool putNumOnClickedCell(const sf::Vector2f& pos, int diceNum) 
    {
        for (int row = 0; row < rows; ++row)
         {
            for (int col = 0; col < cols; ++col)
             {
                int index = row * cols + col;

                // Calculate cell boundaries
                float x = gridStartX + col * (cellSize + cellSpacing);
                float y = gridStartY + row * (cellSize + cellSpacing);

                // Check if the mouse click is within the current cell
                if (pos.x >= x && pos.x <= x + cellSize && pos.y >= y && pos.y <= y + cellSize)
                 {
                    // Place the number in the bottom-most empty cell of the column
                    // and checks if the cell is empty
                    if (gridNum[index + cols + cols].getString() == "0") 
                    {
                        gridNum[index + cols + cols].setString(std::to_string(diceNum));
                        lastClickedCellIndex = index + cols + cols;
                        return true;
                    }
                    else if (gridNum[index + cols].getString() == "0") 
                    {
                        gridNum[index + cols].setString(std::to_string(diceNum));
                        lastClickedCellIndex = index + cols;

                        return true;
                    }

                    else if (gridNum[index].getString() == "0")
                    {
                        gridNum[index].setString(std::to_string(diceNum));
                        lastClickedCellIndex = index;

                        return true;
                    }

                    else
                    {
                        return false;
                    }
                }
            }

        }

        return false;
    }

    /**
     * Public: getLastClickedCellIndex()
     * 
     * Description:
     *      - Retrieves the index of the lasted clicked cell on the grid.
     * 
     * Params:
     *      - None
     * 
     * Returns:
     *      - Int: Index of the lasted clicked cell on the grid.
     */

    int getLastClickedCellIndex()
    {
        return lastClickedCellIndex;
    }

     /**
     * Public: checkCanDestroyColumn()
     * 
     * Description:
     *      - Checks if the enemy places the same dice number on the same cell 
     *        if so the player loses their cell number.
     * 
     * Params:
     *      - Two integer variables
     * 
     * Returns:
     *      - Void: Return Nothing.
     */
    void checkCanDestroyColumn(int enemyLastClickedIndex, int cellNum)
    {

        int gridWidth = 3;

        //Checks if the enemy places the same dice number on the same cell 
        // if so the player loses their cell number
        if(gridNum[enemyLastClickedIndex].getString() == std::to_string(cellNum))
        {
            gridNum[enemyLastClickedIndex].setString("0");

        }

        //Checks if the enemy places the same dice number on the same column 
        // if so the player loses any cell on that column with the same dice number
        if(gridNum[enemyLastClickedIndex + gridWidth].getString() == std::to_string(cellNum))
        {
            gridNum[enemyLastClickedIndex + gridWidth].setString("0");

        }

        //Checks if the enemy places the same dice number on the same column 
        // if so the player loses any cell on that column with the same dice number
        if(gridNum[enemyLastClickedIndex + gridWidth + gridWidth].getString() == std::to_string(cellNum))
        {
            gridNum[enemyLastClickedIndex + gridWidth + gridWidth].setString("0");
  
        }

        //Checks if the enemy places the same dice number on the same column 
        // if so the player loses any cell on that column with the same dice number
        if(gridNum[enemyLastClickedIndex - gridWidth].getString() == std::to_string(cellNum))
        {
            gridNum[enemyLastClickedIndex - gridWidth].setString("0");

        }

        //Checks if the enemy places the same dice number on the same column 
        // if so the player loses any cell on that column with the same dice number
        if(gridNum[enemyLastClickedIndex - gridWidth - gridWidth].getString() == std::to_string(cellNum))
        {
            gridNum[enemyLastClickedIndex - gridWidth - gridWidth].setString("0");

        }
        shiftCellsDown();


    }

    /**
     * Public: countFillGrid()
     * 
     * Description:
     *      - Checks how many cells in the grid have values.
     * 
     * Params:
     *      - None
     * 
     * Returns:
     *      - Int: Return count of number of filled cells in grid.
     */
    int countFillGrid()
    {
        int count = 0;

        // Only counts the gridNUm if the 
        // values are valid 1-6
        for (const auto& value:gridNum)
        {
            if(value.getString() != "0") 
            {
                count++;
            }
        }
        return count;
    }

    /**
     * Public: shiftCellsDown()
     * 
     * Description:
     *      - Checks there is an empty cell under each cell after doing destroyColumn.
     * 
     * Params:
     *      - None
     * 
     * Returns:
     *      - Void: Return Nothing.
     */

    void shiftCellsDown()
    {
        
        // Shifts each cell down if there is 
        // a empty cell on the same column
        for(int i = 0; i < gridNum.size(); i++)
        {
            if(gridNum[i + cols].getString() == "0")
            {
                gridNum[i + cols].setString(gridNum[i].getString());
                gridNum[i].setString("0");
            }
            
        }
    }


    /**
     * Public: draw(sf::RenderWindow& window)
     * 
     * Description:
     *      Draws the grid and numbers onto the specified window.
     * 
     * Params:
     *      - sf::RenderWindow& window: The window where the grid will be drawn.
     * 
     * Returns:
     *      - void: No return value.
     */
    void draw(sf::RenderWindow& window) 
    {
        // Draw each grid cell
        for (const auto& cell : grid) 
        {
            window.draw(cell);
        }

        // Draw the grid numbers if they are not "0"
        for (const auto& value : gridNum) 
        {
            if (value.getString() != "0") 
            {
                window.draw(value);
            }
        }
    }
};
