import tetris as tet
import time
import neat
import numpy as np
import pickle       # pip install cloudpickle

HEADLESS = True

def one_hot(num, size):
    _arr = np.array(np.zeros(size))
    _arr[num] = 1
    return _arr

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = tet.Game()

    while (game.tetris.state == 0):
        if not HEADLESS:
            game.tetris.print_board()

        feature_vector = np.ndarray.flatten(game.tetris.get_projection())

        output = net.activate(feature_vector)
        mv = np.argmax(output)
        prev_board = np.copy(game.tetris.board)
        game.move(mv)

        if not HEADLESS:
            time.sleep(.1)

    return game.tetris.turns

def train(generations = 100, checkpt = None):
    if checkpt == None:
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             'config-ff')

        p = neat.Population(config)
    else:
        p = neat.Checkpointer.restore_checkpoint(checkpt)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    pe = neat.ParallelEvaluator(10, eval_genome)

    winner = p.run(pe.evaluate)

    print('\nBest genome:\n{!s}'.format(winner))
    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)

    

if __name__ == "__main__":
    train(500)