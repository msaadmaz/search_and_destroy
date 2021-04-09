import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from numpy import random
from collections import namedtuple

Cell = namedtuple('Cell', ['row', 'col'])


class cellInfo:
    """Information of for a given element in the maze"""

    def __init__(self, row, col):
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
        self.row = row
        self.col = col

    def __repr__(self):
        return f'{(self.row, self.col)}'


class Maze:
    """Representation of the environment """

    def __init__(self, dim):
        self.dim = dim
        self.board = np.empty((dim, dim), dtype=object)
        for x in range(dim):
            for y in range(dim):
                self.board[x, y] = cellInfo(x, y)
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
        self.belief_matrix = np.full((dim, dim), 1/(dim**2))
        self.confidence_matrix = np.full((dim, dim), 1/(dim**2))
        self.traveled_distances = []


def show_board(maze):
    """
    Show the Maze

    :param maze: maze that is desired to be shown
    """

    cmap = colors.ListedColormap(['white', 'grey', 'green', 'black'])
    bounds = [0, 1, 2, 3, 4]

    arr = np.zeros((maze.dim, maze.dim))

    for x in range(maze.dim):
        for y in range(maze.dim):
            if maze.board[x, y].terrain == "flat":
                arr[x, y] = 0
            elif maze.board[x, y].terrain == "hilly":
                arr[x, y] = 1
            elif maze.board[x, y].terrain == "forested":
                arr[x, y] = 2
            else:
                arr[x, y] = 3

    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.imshow(arr, interpolation='none', cmap=cmap, norm=norm)

    plt.grid()

    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, maze.dim, 1))
    ax.set_yticks(np.arange(-.5, maze.dim, 1))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    for (j, i), label in np.ndenumerate(arr):
        if maze.board[i, j].is_target:
            if maze.board[i, j].is_found:
                ax.text(i, j, 'X', color='blue', fontstyle='oblique', fontsize='xx-large', fontweight='bold',
                        ha='center')
            else:
                ax.text(i, j, 'X', color='red', fontstyle='oblique', fontsize='xx-large', fontweight='bold',
                        ha='center')

    plt.show()
