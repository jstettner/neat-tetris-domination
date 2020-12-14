import tetris as tet
import time
import neat # pip install neat-python
import numpy as np
import pickle       # pip install cloudpickle
import sys
import visualize
import multiprocessing
import os
import skimage.measure
import messagingReporter 

HEADLESS = True
POOL_X, POOL_Y = (4,1)

def one_hot(num, size):
    _arr = np.array(np.zeros(size))
    _arr[num] = 1
    return _arr

def eval_genome_board(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = tet.Game()

    while (game.tetris.state == 0):
        if not HEADLESS:
            game.tetris.print_board()

        # pooled = skimage.measure.block_reduce(game.tetris.get_projection(), \
        #      (POOL_X, POOL_Y), np.max)
        # print(pooled)
        # piece_vector = one_hot(game.tetris.tet.type, 7)
        # rotation_vector = one_hot(game.tetris.tet.rotation, 4)
        # print(piece_vector)
        # feature_vector =  np.concatenate((np.ndarray.flatten(pooled), piece_vector, rotation_vector))
        feature_vector = np.ndarray.flatten(game.tetris.get_projection())

        output = net.activate(feature_vector)
        mv = np.argmax(output)
        prev_board = np.copy(game.tetris.board)
        game.move(mv)

        if not HEADLESS:
            time.sleep(.5)

    return game.tetris.turns + game.tetris.score

def eval_genome_top_four(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # scores = []

    # for i in range(10):
    game = tet.Game()

    while (game.tetris.state == 0):
        if not HEADLESS:
            game.tetris.print_board()

        piece_vector = one_hot(game.tetris.tet.type, 7)
        rotation_vector = one_hot(game.tetris.tet.rotation, 4)
    
        board, row = game.tetris.get_top_four()
        # x_vector = np.array([game.tetris.tet.x])
        x_vector = one_hot(game.tetris.tet.x, 10)
        # y_vector = np.array([row - game.tetris.tet.y])
        y_vector = one_hot(row - game.tetris.tet.y, 40)
        board_vector = np.ndarray.flatten(board)
        feature_vector =  np.concatenate((piece_vector, rotation_vector, x_vector, y_vector, board_vector))
        # print(feature_vector)

        output = net.activate(feature_vector)
        mv = np.argmax(output)
        prev_board = np.copy(game.tetris.board)
        game.move(mv)

        if not HEADLESS:
            time.sleep(.05)

        
        # scores.append(game.tetris.turns + game.tetris.score)

    # return np.average(scores)
    return game.tetris.turns + 3*game.tetris.score

def train(generations = 100, checkpt = None):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-ff')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
    if checkpt == None:
        p = neat.Population(config)
    else:
        p = neat.Checkpointer.restore_checkpoint(checkpt)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))
    # p.add_reporter(messagingReporter.MessagingReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_top_four)
    # pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_board)
    # pe = neat.ParallelEvaluator(1, eval_genome_top_four)

    try:
        if (generations == -1):
            winner = p.run(pe.evaluate)
        else:
            winner = p.run(pe.evaluate, generations)

        print('\nBest genome:\n{!s}'.format(winner))
        with open('winner.pkl', 'wb') as output:
            pickle.dump(winner, output, 1)
    except KeyboardInterrupt:
        visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
        visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")


if __name__ == "__main__":
    print(sys.argv)
    assert(len(sys.argv) == 2 or len(sys.argv) == 3)

    epochs = int(sys.argv[1])
    if (len(sys.argv) == 3):
        _chkpt = sys.argv[2]
        train(epochs, _chkpt)
    else:
        train(epochs)
