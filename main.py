import sys
import numpy as np

from puzzle import Puzzle
from bfs import Bfs
from dfs import Dfs
from astr import Astr

# default values for height and width
puzzle_width = puzzle_height = 4


def print_initial_info(args, loaded_puzzle):
    print("""
Initial arguments list:
Strategy: {}
Search order or heuristic: {}
Input filename: {}
Output filename: {}
Additional filename: {}
Loaded state of puzzle: \n\n{}\n""".format(*args, loaded_puzzle))


def load_initial_puzzle(filename):
    global puzzle_height, puzzle_width

    with open(filename, 'r') as f:
        puzzle_height, puzzle_width = [int(value) for value in f.readline().strip("\r\n").split(" ")]

    return np.loadtxt(filename, dtype=int, skiprows=1)


def save_final_data(result, solution_filename, additional_filename):
    if "No solution found!" not in result:

        with open(solution_filename + ".txt", 'w') as f:
            f.write(str(len(result[0])) + "\n" + result[0])

        with open(additional_filename + ".txt", 'w') as f:
            f.write(str(len(result[0])) + "\n")
            f.write(str(result[2]) + "\n")
            f.write(str(result[3]) + "\n")
            f.write(str(result[1]) + "\n")
            f.write(str(result[4]))
            
    else:
        with open(solution_filename + ".txt", 'w') as f:
            f.write("-1")
        with open(additional_filename + ".txt", 'w') as f:
            f.write("-1")


def print_result(result):
    if "No solution found!" not in result:
        print("Solution string: {}\nMax depth: {}\nNumber of visited: {}\nNumber of processed: {}\nExecution time: {} ms".format(*result))
    else:
        print("No solution found!")


def use_bfs(initial_state, order, solution_filename, additional_filename):
    bfs = Bfs(initial_state, order)
    result = bfs.run_search()
    
    print_result(result)

    save_final_data(result, solution_filename, additional_filename)


def use_dfs(initial_state, order, solution_filename, additional_filename):
    dfs = Dfs(initial_state, order)
    result = dfs.run_search()

    print_result(result)

    save_final_data(result, solution_filename, additional_filename)


def use_a_star(initial_state, heuristic, solution_filename, additional_filename):
    a_star = Astr(initial_state, heuristic)
    result = a_star.run_search()

    print_result(result)

    save_final_data(result, solution_filename, additional_filename)



def choose_method(method, order, initial_state, solution_filename, additional_filename):
    switch_by_method = {
    'bfs': use_bfs,
    'dfs': use_dfs,
    'astr': use_a_star
    }
    method_to_use = switch_by_method.get(method.lower(), "Wrong method!")
    return method_to_use(initial_state, order.lower(), solution_filename, additional_filename) if type(method_to_use) is not str else print(method_to_use)


def main():
    """
    args[0] - method, bfs / dfs / astr
    args[1] - search order or heuristic e.g. ldur / rldu / manh / hamm
    args[2] - filename of puzzle file
    args[3] - filename of solution file
    args[4] - filename of additional data file

    """

    args = sys.argv[1:]

    if len(args) == 5:
        initial_puzzle = load_initial_puzzle(args[2])
        print_initial_info(args, initial_puzzle)
        
        Puzzle.puzzle_height, Puzzle.puzzle_width = puzzle_height, puzzle_width

        first_state = Puzzle(initial_puzzle)
        choose_method(args[0], args[1], first_state, args[3], args[4])

    else:
        print("Wrong number of arguments!")


if __name__ == "__main__":
    main()