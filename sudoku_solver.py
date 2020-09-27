class Sudoku:
    def __init__(self, board):
        self.board = board

    def is_safe(self, row, col, number):

        if number == '' or number == 0:
            return False

        # Check Horizontally
        for i in range(9):
            if not i == col:
                if self.board[row][i] == number:
                    return False

        # Check Vertically
        for i in range(9):
            if not i == row:
                if self.board[i][col] == number:
                    return False

        # Check Box
        box_x = row // 3
        box_y = col // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if not j == row and not i == col:
                    if self.board[j][i] == number:
                        return False

        return True

    def solve_sudoku(self):
        position = self.next_number()
        if not position:
            return True

        for number in range(1, 10):
            if self.is_safe(position[0], position[1], number):
                self.board[position[0]][position[1]] = number

                if self.solve_sudoku():
                    return True

                self.board[position[0]][position[1]] = 0

        return False

    def transform_zeros_to_strings(self):
        for i in range(9):
            for j, y in enumerate(self.board[i]):
                if y == 0:
                    self.board[i][j] = ''

    def next_number(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    return i, j

        return False

    def return_the_solution(self):
        self.transform_strings_to_zeros()
        if self.solve_sudoku():
            self.transform_zeros_to_strings()
            return self.board
        else:
            return False

    def transform_strings_to_zeros(self):
        for i in range(9):
            for j, y in enumerate(self.board[i]):
                if y == '':
                    self.board[i][j] = 0

    def check_if_solved(self):
        self.transform_strings_to_zeros()

        for i in range(9):
            for m, n in enumerate(self.board[i]):
                if not self.is_safe(i, m, n) and self.board[i][m] == 0:
                    return False

        return True

    def print_board(self):
        print('1')
        for i in self.board:
            print(i)


if __name__ == '__main__':
    game_table = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                  [6, 7, 2, 1, 9, 5, 3, 4, 8],
                  [1, 9, 8, 3, 4, 2, 5, 6, 7],
                  [8, 5, 9, 7, 6, 1, 4, 2, 3],
                  [4, 2, 6, 8, 5, 3, 7, 9, 1],
                  [7, 1, 3, 9, 2, 4, 8, 5, 6],
                  [9, 6, 1, 5, 3, 7, 2, 8, 4],
                  [2, 8, 7, 4, 1, 9, 6, 3, 5],
                  [3, 4, 5, 2, 8, 6, 1, 7, 9]]

    game = Sudoku(game_table)
    print(game.check_if_solved())
