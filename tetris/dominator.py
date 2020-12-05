import tetris as tet
import neat
import numpy as np

MAX_STAGNANT = 500

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = tet.Game()

        turns_without_change = 0
        timedout = False
        while (game.tetris.state == 0):
            if turns_without_change > MAX_STAGNANT:
                timedout = True
                break

            # game.tetris.print_board()

            # piece_vector = np.zeros(7)
            # piece_vector[game.tetris.tet.type] = 1
            # [0, 1, 0, 0, 0, 0, 0]

            # rotation_vector = np.array([game.tetris.tet.rotation])

            # position_vector = np.array([game.tetris.tet.x, game.tetris.tet.y])

            # board_vector = np.ndarray.flatten(game.tetris.board)
            feature_vector = np.ndarray.flatten(game.tetris.get_projection())
            # print(feature_vector)
            # print(turns_without_change)

            output = net.activate(feature_vector)
            mv = np.argmax(output)
            prev_board = np.copy(game.tetris.board)
            game.move(mv)

            if np.array_equal(game.tetris.board, prev_board):
                turns_without_change += 1
            else:
                turns_without_change = 0

        # print(game.tetris.score)j
        genome.fitness = game.tetris.score if not timedout else -500
        # print(genome.fitness)

def train(generations = 100):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-ff')

    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 300)

    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True) #, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 10)

if __name__ == "__main__":
    train(5)