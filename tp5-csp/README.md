# N-Queens Constraint Satisfaction Problem (CSP)

This project implements a solution to the N-Queens problem using a Constraint Satisfaction Problem (CSP) approach with backtracking. The N-Queens problem involves placing N queens on an N×N chessboard such that no two queens threaten each other. This means that no two queens can be in the same row, column, or diagonal.

## Project Structure

- `code/csp_nqueens.py`: Contains the main logic for the N-Queens CSP, including the `NQueensCSP` class that initializes the problem, checks constraints, and finds solutions using backtracking.
- `code/backtracking.py`: Implements the backtracking algorithm to solve the N-Queens problem. It exports a function `backtrack` that attempts to place queens on the board while checking for conflicts.
- `code/utils.py`: Includes utility functions such as `is_safe`, which checks if placing a queen in a specific position is valid, and `print_solution`, which formats and prints the solution.
- `requirements.txt`: Lists the dependencies required for the project.

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To solve the N-Queens problem, you can run the `csp_nqueens.py` script. You can specify the size of the board (N) as an argument. For example:

```
python code/csp_nqueens.py 8
```

This command will find and print all solutions for the 8-Queens problem.

## Examples

After running the script, you will see the solutions printed in a formatted manner. Each solution is represented as an array where the index represents the column and the value at that index represents the row position of the queen.

## License

This project is licensed under the MIT License.