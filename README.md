# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: Naked twins strategy is the idea that if two boxes within the same unit has same two possible choices, then those two choices must belong to those two boxes---thus other boxes in the unit cannot be one of those two choices.  This should be used together with other two constraint strategies, "eliminate" and "only choice", then it can be repeated until no more improvements are made.
In terms of implementing it, there are two distinct tasks involved here: finding the naked twins and removing the two possible digits from other boxes in the unit (or units, since the naked twins can technically belong to more than one unit).  Naked twins can be found by looping through each unit, look at all the boxes with two choices, and see if any of them have the same choices.  Once naked twins are found, we can loop through each pair, and take the two possible digits and remove them from all of the pair's shared peers (or the intersection of the sets of each naked twin's peers), which is equivalent to all the boxes that belong to all the units that both naked twins belong to (except the pair itself).

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: The implementation of diagonal sudoku constraint is very simple!  The constraints now have to apply to the diagonals as they do to other units.  Therefore, only change it needs from a normal sudoku solve is to include the diagonal units into the "unitlist".  Whenever a function calls loops through the units in unitlist, it'll loop through the diagonal units and apply the same constraints.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.