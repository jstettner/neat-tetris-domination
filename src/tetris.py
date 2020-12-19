from tetromino import *
import colorama
import numpy as np
import random 

HEIGHT = 40
WIDTH = 10
ROW_VALUE = 100

class Tetris:
    board = []
    score = 0
    tet = None
    state = 0
    turns = 0

    def __init__(self):
        # random.seed(4701)
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
                            self.board[self.tet.y + j][self.tet.x + i] == 1:
                                return True

        return False

    def new_tet(self):
        self.tet = Tetromino(4, 0, random.randint(0, 6)) 

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
        self.turns += 1
        while not self.is_intersecting():
            self.tet.y += 1
        self.tet.y -= 1
        self.collide()
    
    def move_down(self):
        self.tet.y += 1
        self.turns += 1
        if self.is_intersecting():
            self.tet.y -= 1
            self.collide()

    def move_lateral(self, d):
        self.tet.x += d
        if self.is_intersecting():
            self.tet.x -= d

        self.move_down()

    def rotate(self):
        old = self.tet.rotation
        self.tet.rotate()
        if self.is_intersecting():
            self.tet.rotation = old

        self.move_down()

    def get_projection(self):
        board_projection = np.copy(self.board)

        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                if idx in self.tet.current():
                    board_projection[self.tet.y + j][self.tet.x + i] = 1

        return board_projection

    def get_top_four(self):
        def row_with_first_item():
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if self.board[i][j] == 1:
                        return i

            return HEIGHT - 1

        r = row_with_first_item()
        if  HEIGHT - r > 4: 
            return np.copy(self.board)[r:r+4][:], r
        else:
            return np.copy(self.board)[HEIGHT - 4:][:], r

    def print_board(self):
        def color_sign(x):
            c = colorama.Fore.GREEN if x == 1 else colorama.Fore.RED if x == 0 else colorama.Fore.BLUE
            return f'{c}{x}'

        board_projection = np.copy(self.board)

        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                if idx in self.tet.current():
                    board_projection[self.tet.y + j][self.tet.x + i] = 1

        np.set_printoptions(formatter={'float': color_sign}, linewidth=1000)
        print(board_projection)
    

class Game:
    tetris = None

    def __init__(self):
        self.tetris = Tetris()

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






                


