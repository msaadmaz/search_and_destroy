import numpy as np
from numpy import random

import environment


def get_manhattan_distance(cell1, cell2):
    (x1, y1) = cell1
    (x2, y2) = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def get_shortest_max_list(maze, max_values, previous_cell):
    distance_array = []
    for cell2 in max_values:
        distance_array.append((get_manhattan_distance(cell2, previous_cell), cell2))

    minimum_distance = distance_array[0][0]
    # get the minimum distance
    for x in range(len(distance_array)):
        if x == 0:
            continue
        manhattan_distance = distance_array[x][0]
        if manhattan_distance < minimum_distance:
            minimum_distance = manhattan_distance

    removal_distance = []
    # remove all the cells that aren't the minimum manhattan distance
    for manhattan_distance, cell2 in distance_array:
        if manhattan_distance != minimum_distance:
            # removal array is now an array of all non-minimum Manhattan distances
            removal_distance.append(cell2)

    # if the removal array is empty, then all the manhattan distances were the same and no cell needs to be removed
    # from the original max values list
    # if it is not empty, then all the distances that are not the minimum need to be removed
    if removal_distance:
        for (x, y) in removal_distance:
            max_values.remove((x, y))

    maze.traveled_distances.append(minimum_distance)
    return max_values


def get_current_max_cell(maze, option, prev, previous_cell):
    # if option is 1 then agent 1 is being used, if the option is 2 then agent 2 is being used
    if option == 1:
        temp_matrix = maze.belief_matrix
    else:
        temp_matrix = maze.confidence_matrix

    result = np.where(temp_matrix == np.amax(temp_matrix))
    list_of_maxes = list(zip(result[0], result[1]))
    if prev:
        list_of_maxes = get_shortest_max_list(maze, list_of_maxes, previous_cell)
    random_index = random.randint(0, len(list_of_maxes))
    return list_of_maxes[random_index]


def false_negative_of_cell(maze, cell):
    return maze.board[cell[0], cell[1]].false_negative


def get_total_distance_traveled(maze):
    return sum(maze.traveled_distances)


def search_cell(maze, cell):
    random_number = random.uniform(0, 1)
    if maze.board[cell[0], cell[1]].is_target:
        if random_number > maze.board[cell[0], cell[1]].false_negative:
            return True
        else:
            return False
    else:
        return False


def agent(maze, option):
    number_of_searches = 0
    (x, y) = get_current_max_cell(maze, option, False, (0, 0))
    maze.traveled_distances.append(0)
    while True:

        # the current cell is the cell that we want to search
        number_of_searches += 1

        # if the cell being searched is the target, and it is found then return the score
        if search_cell(maze, (x, y)):
            total_distance_traveled = get_total_distance_traveled(maze)
            # set the target as found
            # maze.board[x, y].is_found = True
            # environment.show_board(maze)
            return number_of_searches + total_distance_traveled
        else:
            # Calculate P(Target in Cell i | Observations ^ Failure in Cell j)
            # Use Baye's Theorem and update the Network

            # P(Target in current Cell) * P(Failure in  current Cell | Target in current Cell ) --> also the False
            # negative
            maze.belief_matrix[x, y] *= false_negative_of_cell(maze, (x, y))

            # Calculate P(failure in current Cell)
            sum_of_probabilities = np.sum(maze.belief_matrix)

            # Update the Baysien Network with new Probabilities
            maze.belief_matrix = maze.belief_matrix / sum_of_probabilities

            # update the confidence matrix for agent 2
            # the probabilities in the Confidence matrix represents cells which the algorithm believes to have the
            # highest probability of finding the target
            if option == 2:
                for i in range(maze.dim):
                    for j in range(maze.dim):
                        maze.confidence_matrix[x, y] = maze.belief_matrix[x, y] * (
                                    1 - false_negative_of_cell(maze, (x, y)))

        previous_cell = (x, y)
        (x, y) = get_current_max_cell(maze, option, True, previous_cell)
