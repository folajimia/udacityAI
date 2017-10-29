# Artificial Intelligence Nanodegree
Sudoku
Sudoku  is a logic-based, combinatorial, number-placement puzzle. The objective is to fill a 9×9 grid with digits so that each column, each row, and each of the nine 3×3 subgrids that compose the grid (also called "boxes", "blocks", or "regions") contains all of the digits from 1 to 9. The puzzle setter provides a partially completed grid, which for a well-posed puzzle has a single solution.[1]

Completed games are always a type of Latin square with an additional constraint on the contents of individual regions. For example, the same single integer may not appear twice in the same row, column, or any of the nine 3×3 subregions of the 9x9 playing board.

Basic Sudoku rules

The objective of the game is to fill the table with numbers from 1 to 9, while meeting the following conditions:

- There should be no column with two identical numbers
- There should be no row with two identical numbers
- Each 3 x 3 subgrid found in the grid should not have two identical numbers

There is a sudoku variation refered to as diagonal Sudoku, here in addition to the stated rules, the diagonals on the board should not have two diagonal numbers.


Sudoku A.I
The main aim of this project is to build an intelligent agent that will solve every possible sudoku using two well known A.I Techniques.

A.I techniques to solve Sudoku

Constraint Propagation
When trying to solve a constraint satisfaction problem, you'll find that there are three components, the variables,domains and the constraint[2]. To solve the problem within a domain space, constraints help you narrow the possibilities for the answer, which can be very helpful. constraints are applied iteratively to narrow a search space(domain). Constraint propagation can be used to solve a variety of problems such as calendar scheduling, and cryptographic puzzles.

Search
While solving a proble, solving, one can get to a stage where there are two or more options left. What do we do? What if we branch out and consider both of them? Maybe one of them will lead us to a position in which three or more possibilities are available. Then, we can branch out again. At the end, we can create a whole tree of possibilities and find ways to traverse the tree until we find our solution. This is an example of how search can be used.
These ideas may seem simple and they're actually intended to be! Through this lesson you'll see how AI is really composed of very simple ideas that can be put together to solve complex problems. Throughout this lesson, we challenge you to think of how you can apply these ideas to build AI agents to solve other puzzles and problems in your world!

Naming convention
Boxes:These are individual squares at the intersection of rows and columns. Boxes have the labels 'A1', 'A2', ..., 'I9'.
Units:These are complete rows, complete columns, and 3x3 squares. Each of the units have 9 boxes. Th board has 27 units in total.
Peers: These For a box 'A1', the other boxes that belong to the same common unit are its peer.



## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation employs two strategies, 
 - Eliminating a value x from a square's peers, if the square has the value x as its possible value.
 - If there is only one possible place for a value within a unit, the value should be placed there.
>In the case of naked twins, a pair of values xa are permitted to be in two boxes within a unit.
although it is not clear which of the two boxes each value belongs to, we apply the constrain propagation
 strategy to these two boxes hence excluding/limiting the values x and a from every other box within the unit 
 and restricting them only to the 2 boxes they appear in.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propagation is not applied directly to solve the diagonal sudoku. To solve the diagonal sudoku,
 a diagonal unit was created to contain all the diagonal boxes of the sudoku board and the existing code which 
 has the naked twin, eliminate and only choice functions was applied.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

[1] Wikipedi:https://en.wikipedia.org/wiki/Sudoku
[2]Artificial intelligence a modern approach.
[
