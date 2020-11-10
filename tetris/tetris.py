from tetromino import *
import numpy as np

HEIGHT = 40
WIDTH = 10

class Tetris:
    board = []
    score = 0
    tet = None

    def __init__(self):
        self.board = np.array(np.zeros((HEIGHT, WIDTH)))

    def is_out_of_bounds(self, x, y):
        return y >= len(board) or x >= len(board[0]) or x < 0

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

    # def clear_rows(self):


