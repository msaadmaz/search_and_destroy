import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from numpy import random


class Cell:
    """Information of for a given element in the map"""

    def __init__(self):
        """
        Initializes with basic values for information
        :param terrain: the type of terrain that cell is
        :param is_target: whether or not the cell is a target
        :param false_negative: the false negative probability if the cell
                                is a target
        """
        self.terrain = ""
        self.is_target = False
        self.is_found = False
        self.false_negative = 0


class Map:
    """Representation of the environment """

    def __init__(self, dim):
        self.dim = dim
        self.board = np.empty((dim, dim), dtype=object)
        for x in range(dim):
            for y in range(dim):
                self.board[x, y] = Cell()
                random_number = random.uniform(0, 1)
                if random_number < 0.25:
                    self.board[x, y].terrain = "flat"
                    self.board[x, y].false_negative = 0.1
                elif random_number < 0.5:
                    self.board[x, y].terrain = "hilly"
                    self.board[x, y].false_negative = 0.3
                elif random_number < 0.75:
                    self.board[x, y].terrain = "forested"
                    self.board[x, y].false_negative = 0.7
                else:
                    self.board[x, y].terrain = "caves"
                    self.board[x, y].false_negative = 0.9
        x = random.randint(0, dim)
        y = random.randint(0, dim)
        self.board[x, y].is_target = True


def show_board(board):
    """
    Show the board

    :param board: board that is desired to be shown
    """

    cmap = colors.ListedColormap(['white', 'grey', 'green', 'black', 'red', 'cyan'])
    bounds = [0, 1, 2, 3, 4, 5, 6]

    arr = np.zeros((len(board.board), len(board.board)))

    for x in range(len(board.board)):
        for y in range(len(board.board[x])):
            if board.board[x, y].is_target:
                if board.board[x, y].is_found:
                    arr[x, y] = 5
                else:
                    arr[x, y] = 4
            elif board.board[x, y].terrain == "flat":
                arr[x, y] = 0
            elif board.board[x, y].terrain == "hilly":
                arr[x, y] = 1
            elif board.board[x, y].terrain == "forested":
                arr[x, y] = 2
            else:
                arr[x, y] = 3

    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.imshow(arr, interpolation='none', cmap=cmap, norm=norm)

    plt.grid()

    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, board.dim, 1))
    ax.set_yticks(np.arange(-.5, board.dim, 1))
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    plt.show()
