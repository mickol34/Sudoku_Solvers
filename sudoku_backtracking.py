import os
# import time
import sys

# we'll be using recursion at some deep level, so...
sys.setrecursionlimit(3000)


def prepare_presets(sudoku):
    # grid of True/False values, whether value is preset
    # (non-zero at the beginning)
    preset = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            preset[i][j] = True if sudoku[i][j] != 0 else False
    return preset


def show(sudoku):
    # sudoku printing
    for i in range(9):
        print(end="|")
        for j in range(9):
            value = sudoku[i][j] if sudoku[i][j] else " "
            print(value, end="|")
        print()


def is_valid(sudoku):
    # bool value for sudoku validation
    is_valid = True

    # rows validation
    for row in sudoku:
        row = [value for value in row if value != 0]
        if len(row) != len(set(row)):
            is_valid = False

    # columns validation
    for j in range(9):
        column = []
        for i in range(9):
            column.append(sudoku[i][j])
        column = [value for value in column if value != 0]
        if len(column) != len(set(column)):
            is_valid = False

    # boxes validation
    for x in range(3):
        for y in range(3):
            box = []
            for i in range(3*x, 3*x+3):
                for j in range(3*y, 3*y+3):
                    box.append(sudoku[i][j])
            box = [value for value in box if value != 0]
            if len(box) != len(set(box)):
                is_valid = False

    return is_valid


def coordinates_by_position(position):
    return int(position/9), position % 9


def backtrack(sudoku,
              preset,
              going_forward=True,
              current_position=0,
              counter=1):
    # Backtracking starts at position 0 (first possible input) and ends
    # at 80 (81 values). It tries to input values from 1 to 9 into
    # every position, until all positions are filled. If value is valid,
    # algorigthm proceeds to the next position. If it's not valid,
    # it adds 1 to the last changed position, to check for validation.
    # If all 9 numbers fail to meet validation, number is removed and
    # previously tried input is being changed by 1.
    # Somewhat close to bruteforcing.

    # loop of unknown length
    while True:

        # if is solved
        if not any(0 in row for row in sudoku):
            if is_valid(sudoku):
                break

        # get cords from current position
        curr_i, curr_j = coordinates_by_position(current_position)

        # show current state of sudoku
        show(sudoku)
        print("GOING FORWARD = ", going_forward)
        print("CURRENT POSITION = ", current_position)
        print("IS PRESET? = ", preset[curr_i][curr_j])
        print("IS VALID? = ", is_valid(sudoku))
        print("ITERATIONS =", counter)
        # time.sleep(0.001)
        os.system("cls")

        # if going forward
        if going_forward:
            # skip over preset values
            if preset[curr_i][curr_j]:
                current_position += 1
            else:
                # add 1 to current value and check, what's next
                sudoku[curr_i][curr_j] += 1
                # if valid, proceed to next position
                if is_valid(sudoku):
                    current_position += 1
                # if not valid...
                else:
                    # ... and already at 9, delete and go back
                    if sudoku[curr_i][curr_j] == 9:
                        sudoku[curr_i][curr_j] = 0
                        current_position -= 1
                        going_forward = False

        # if going backward
        else:
            # skip over preset values
            if preset[curr_i][curr_j]:
                current_position -= 1
            else:
                # if already at 9 -> delete and go backward
                if sudoku[curr_i][curr_j] == 9:
                    sudoku[curr_i][curr_j] = 0
                    current_position -= 1
                # if not at 9 -> proceed
                else:
                    going_forward = True

        counter += 1
        backtrack(sudoku, preset, going_forward, current_position, counter)

    return sudoku


sudoku = [[0, 9, 0, 0, 0, 0, 1, 7, 2],
          [0, 3, 0, 2, 0, 5, 0, 6, 9],
          [0, 0, 2, 0, 0, 4, 3, 0, 0],
          [2, 4, 7, 3, 0, 0, 6, 0, 0],
          [0, 0, 6, 0, 5, 0, 7, 0, 0],
          [0, 0, 5, 0, 0, 7, 8, 9, 4],
          [0, 0, 9, 1, 0, 0, 5, 0, 0],
          [4, 5, 0, 7, 0, 6, 0, 8, 0],
          [7, 2, 1, 0, 0, 0, 0, 4, 0]]

preset = prepare_presets(sudoku)
solved = backtrack(sudoku, preset)
show(solved)
