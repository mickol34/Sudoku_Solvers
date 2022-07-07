from math import ceil
print("sudoku moment")


class Square:

    def __init__(self, value=None):
        self.value = value
        if not value:
            self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            self.possible_values = []

    def set_value(self, value):
        if value == 0:
            value = None
        if ((not self.value) and (value in self.possible_values)):
            self.value = value

    def get_value(self):
        return self.value

    def get_possible_values(self):
        return self.possible_values

    def remove_digit(self, digit):
        if not self.value:
            if digit in self.possible_values:
                self.possible_values.remove(digit)
            if len(self.possible_values) == 1:
                self.set_value(self.possible_values[0])
                self.possible_values = []


class Sudoku:

    def __init__(self, digits=None):
        self.riddle = [[], [], [], [], [], [], [], [], []]
        for i in range(9):
            for j in range(9):
                if digits:
                    self.riddle[i].append(Square(digits[i][j]))
                else:
                    self.riddle[i].append(Square())

    def show(self):
        for i in range(9):
            print(end="|")
            for j in range(9):
                value = self.riddle[i][j].get_value()
                if not value:
                    value = " "
                print(value, end="|")
            print()  # print(" ‾ ‾ ‾ ‾ ‾ ‾ ‾ ‾ ‾")

    def remove_from_row(self, row, column):
        digit_to_remove = self.riddle[row][column].get_value()
        for i in range(9):
            self.riddle[row][i].remove_digit(digit_to_remove)

    def remove_from_column(self, row, column):
        digit_to_remove = self.riddle[row][column].get_value()
        for i in range(9):
            self.riddle[i][column].remove_digit(digit_to_remove)

    def remove_from_box(self, row, column):
        digit_to_remove = self.riddle[row][column].get_value()
        box_row = 3*ceil((row+1)/3)-2
        box_column = 3*ceil((column+1)/3)-2
        for i in range(box_row-1, box_row+2):
            for j in range(box_column-1, box_column+2):
                self.riddle[i][j].remove_digit(digit_to_remove)

    def only_possible_in_row(self, row):
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        possible_appearances = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(9):
            possible_vals = self.riddle[row][i].get_possible_values()
            for possible_value in possible_vals:
                possible_appearances[possible_value-1] += 1
        for index in range(9):
            if possible_appearances[index] == 1:
                for i in range(9):
                    if not self.riddle[row][i].get_value():
                        self.riddle[row][i].set_value(digits[index])
        return possible_appearances

    def only_possible_in_column(self, column):
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        possible_appearances = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(9):
            possible_vals = self.riddle[i][column].get_possible_values()
            for possible_value in possible_vals:
                possible_appearances[possible_value-1] += 1
        for index in range(9):
            if possible_appearances[index] == 1:
                for i in range(9):
                    if not self.riddle[i][column].get_value():
                        self.riddle[i][column].set_value(digits[index])
        return possible_appearances

    def only_possible_in_box(self, box_row, box_column):
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        possible_appearances = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        box_row = 3*box_row-2
        box_column = 3*box_column-2
        for i in range(box_row-1, box_row-2):
            for j in range(box_column-1, box_column-2):
                possible_vals = self.riddle[i][j].get_possible_values()
                for possible_value in possible_vals:
                    possible_appearances[possible_value-1] += 1
        for index in range(9):
            if possible_appearances[index] == 1:
                for i in range(box_row-1, box_row-2):
                    for j in range(box_column-1, box_column-2):
                        if not self.riddle[i][j].get_value():
                            self.riddle[i][j].set_value(digits[index])
        return possible_appearances

    def iterate(self):
        for i in range(9):
            for j in range(9):
                self.remove_from_row(i, j)
                self.remove_from_column(i, j)
                self.remove_from_box(i, j)
        for i in range(9):
            self.only_possible_in_row(i)
            self.only_possible_in_column(i)
        for i in range(1, 4):
            for j in range(1, 4):
                self.only_possible_in_box(i, j)

    def count_squares_filled(self):
        squares_filled = 0
        for i in range(9):
            for j in range(9):
                if self.riddle[i][j].get_value():
                    squares_filled += 1
        return squares_filled

    def solve(self):
        prev_squares_filled = self.count_squares_filled()
        self.iterate()
        curr_squares_filled = self.count_squares_filled()
        iterations = 1
        while(curr_squares_filled > prev_squares_filled):
            self.iterate()
            prev_squares_filled = curr_squares_filled
            curr_squares_filled = self.count_squares_filled()
            iterations += 1
        self.show()
        return iterations


digits = [[0, 9, 0, 0, 0, 0, 1, 7, 2],
          [0, 3, 0, 2, 0, 5, 0, 6, 9],
          [0, 0, 2, 0, 0, 4, 3, 0, 0],
          [2, 4, 7, 3, 0, 0, 6, 0, 0],
          [0, 0, 6, 0, 5, 0, 7, 0, 0],
          [0, 0, 5, 0, 0, 7, 8, 9, 4],
          [0, 0, 9, 1, 0, 0, 5, 0, 0],
          [4, 5, 0, 7, 0, 6, 0, 8, 0],
          [7, 2, 1, 0, 0, 0, 0, 4, 0]]

digit2 = [[0, 0, 0, 0, 0, 0, 1, 7, 0],
          [0, 0, 0, 2, 0, 5, 0, 6, 0],
          [0, 0, 2, 0, 0, 4, 3, 0, 0],
          [2, 0, 7, 3, 0, 0, 6, 0, 0],
          [0, 0, 6, 0, 0, 0, 7, 0, 0],
          [0, 0, 5, 0, 0, 7, 8, 9, 4],
          [0, 0, 9, 1, 0, 0, 5, 0, 0],
          [4, 5, 0, 0, 0, 6, 0, 8, 0],
          [7, 2, 1, 0, 0, 0, 0, 4, 0]]

digit3 = [[0, 0, 1, 6, 0, 2, 0, 0, 0],
          [7, 9, 0, 0, 0, 0, 1, 4, 0],
          [0, 6, 0, 0, 0, 1, 0, 0, 0],
          [0, 0, 9, 1, 0, 4, 5, 0, 7],
          [0, 8, 0, 0, 2, 0, 0, 1, 0],
          [4, 0, 7, 5, 0, 9, 6, 0, 0],
          [0, 0, 0, 4, 0, 0, 0, 6, 0],
          [0, 7, 6, 0, 0, 0, 0, 5, 3],
          [0, 0, 0, 9, 0, 6, 7, 0, 0]]

emptys = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]

digit4 = [[3, 0, 0, 0, 0, 8, 1, 5, 0],
          [4, 5, 0, 0, 0, 0, 3, 0, 2],
          [0, 0, 7, 9, 3, 0, 0, 6, 0],
          [0, 0, 4, 5, 0, 1, 0, 0, 9],
          [0, 0, 0, 0, 8, 0, 0, 0, 0],
          [9, 0, 0, 2, 0, 4, 8, 0, 0],
          [0, 2, 0, 0, 5, 6, 9, 0, 0],
          [8, 0, 1, 0, 0, 0, 0, 2, 5],
          [0, 9, 6, 1, 0, 0, 0, 0, 3]]

sudoku = Sudoku(digit2)
sudoku.show()
print()
print(sudoku.solve())
print()
print()
print()
sudoku.iterate()
sudoku.show()
sudoku.iterate()
sudoku.show()
sudoku.iterate()
sudoku.show()

# row_blocking
# column_blocking
# czyli narzucenie przez pełność danej części kolumny tego, że brakująca
# liczba musi być w innej kolumnie w boxie, a nie w innej

# narzucanie rzędu przez wyłączną możliwość w innych rzędach w innych boxach
