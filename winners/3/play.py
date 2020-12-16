import sys
import pickle
import neat
import os
import numpy as np
import time
sys.path.append("src/")
import tetris as tet
import dominator

def play(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    game = tet.Game()

    while (game.tetris.state == 0):
        game.tetris.print_board()

        piece_vector = dominator.one_hot(game.tetris.tet.type, 7)
        rotation_vector = dominator.one_hot(game.tetris.tet.rotation, 4)
    
        board, row = game.tetris.get_top_four()
        x_vector = dominator.one_hot(game.tetris.tet.x, 10)
        y_vector = dominator.one_hot(row - game.tetris.tet.y, 40)
        board_vector = np.ndarray.flatten(board)
        feature_vector =  np.concatenate((piece_vector, rotation_vector, x_vector, y_vector, board_vector))

        output = net.activate(feature_vector)
        mv = np.argmax(output)
        prev_board = np.copy(game.tetris.board)
        game.move(mv)

        time.sleep(.05)


if __name__ == "__main__":
    file_name = sys.argv[1]
    config_file = sys.argv[2]

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_file)

    with open(file_name, 'rb') as input_file:
        winner = pickle.load(input_file)

    play(winner, config)
