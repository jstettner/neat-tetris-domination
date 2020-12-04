from tetromino import *
import colorama
import numpy as np

HEIGHT = 40
WIDTH = 10
ROW_VALUE = 100

class Tetris:
    board = []
    score = 0
    tet = None
    state = 0

    def __init__(self):
        self.board = np.array(np.zeros((HEIGHT, WIDTH)))
        self.new_tet()

    def is_out_of_bounds(self, x, y):
        return y >= len(self.board) or x >= len(self.board[0]) or x < 0

    def is_intersecting(self):
        # Is the piece colliding with another piece or out of bounds
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

    def end_game(self):
        self.state = 1

    def collide(self):
        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                if idx in self.tet.current():
                    self.board[self.tet.y + j][self.tet.x + i] = 1
        self.clear_rows()
        self.new_tet()
        if self.is_intersecting():
            self.end_game()

    def shift_down(self, from_row):
        for row in reversed(range(1, from_row + 1)):
            # from_row = 10
            # 10..1
            for col in range(len(self.board[0])):
                self.board[row][col] = self.board[row - 1][col]

        for col in range(len(self.board[0])):
            self.board[0][col] = 0

    def clear_rows(self):
        rows_cleared = 0
        for row in range(len(self.board)):
            gap = False
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    gap = True

            # If row complete
            if gap == False:
                for col in range(len(self.board[0])):
                    self.board[row][col] = 0
                self.shift_down(row)
                rows_cleared += 1

        self.score += ROW_VALUE * rows_cleared**2
    
    def move_down_fully(self):
        while not self.is_intersecting():
            self.tet.y += 1
        self.tet.y -= 1
        self.collide()
    
    def move_down(self):
        self.tet.y += 1
        if self.is_intersecting():
            self.tet.y -= 1
            self.collide()

    def move_lateral(self, d):
        self.tet.x += d
        if self.is_intersecting():
            self.tet.x -= d

    def rotate(self):
        old = self.tet.rotation
        self.tet.rotate()
        if self.is_intersecting():
            self.tet.rotation = old

    def print_board(self):
        def color_sign(x):
            c = colorama.Fore.GREEN if x > 0 else colorama.Fore.RED
            return f'{c}{x}'

        board_projection = np.copy(self.board)

        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                if idx in self.tet.current():
                    board_projection[self.tet.y + j][self.tet.x + i] = 2

        np.set_printoptions(formatter={'float': color_sign}, linewidth=1000)
        print(board_projection)
    

class Game:
    tetris = None

    def __init__(self):
        self.tetris = Tetris()
        print(self.tetris)

    def move(self, mv):
        mv = int(mv)
        # 0 = down, 1 = left, 2 = right, 3 = rotate 
        if (mv == 0):
            self.tetris.move_down()
        elif (mv == 1):
            self.tetris.move_lateral(-1)
        elif (mv == 2):
            self.tetris.move_lateral(1)
        elif (mv == 4):
            self.tetris.move_down_fully()
        else:
            self.tetris.rotate()

    def play(self):
        while (self.tetris.state == 0):
            self.tetris.print_board()
            mv = input()
            self.move(mv)
        print(self.tetris.score)






                


