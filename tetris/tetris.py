from tetromino import *
import numpy as np

HEIGHT = 40
WIDTH = 10
ROW_VALUE = 100

class Tetris:
    board = []
    score = 0
    tet = None

    def __init__(self):
        self.board = np.array(np.zeros((HEIGHT, WIDTH)))

    def is_out_of_bounds(self, x, y):
        return y >= len(self.board) or x >= len(self.board[0]) or x < 0

    def is_intersecting(self):
        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                if idx in self.tet.current():
                    if self.is_out_of_bounds(self.tet.x + i, self.tet.y + j) or \
                            self.board[self.tet.y + j][self.tet.x + i] > 0:
                                return True

        return False

    def new_tet(self):
        self.tet = Tetromino(4, 0) 

    def collide(self):
        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                if idx in self.tet.current():
                    self.board[self.tet.y + j][self.tet.x + i] = 1

    def shift_down(from_row):
        for row in reversed(range(1, from_row)):
            for col in range(len(board[0])):
                self.board[row][col] = self.board[row - 1][col]

        for col in range(len(board[0])):
            self.board[0][col] = 0

    def clear_rows(self):
        rows_cleared = 0
        for row in range(len(board)):
            gap = False
            for col in range(len(board[0])):
                if self.board[row][col] == 0:
                    gap = True

            # If row complete
            if gap == False:
                for col in range(len(board[0])):
                    self.board[row][col] = 0
                self.shift_down(row)
                rows_cleared += 1

        self.score += ROW_VALUE * rows_cleared**2


                


