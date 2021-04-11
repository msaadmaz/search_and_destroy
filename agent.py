import numpy as np
from numpy import random


def get_manhattan_distance(cell1, cell2):
    """
    Obtains the manhattan distance from cell1 to cell2
    :param cell1: initial cell
    :param cell2: destination cell
    :return: manhattan distance from cell 1 to cell 2
    """
    (x1, y1) = cell1
    (x2, y2) = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def get_shortest_max_list(maze, max_values, previous_cell):
    """
    Gets the maxes that are the shortest distance away from the previous searched cell
    :param maze: Maze where target is
    :param max_values: array of tupples containing all the cells with the maximum values
    :param previous_cell: previous searched cell
    :return: list of tuples of maxes that are shortest distance away from previous searched cell
    """
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
    """
    Gets next cell to be searched based of metrics based in project instructions, manhattan distance, then ties broken
    by randomness
    :param maze: Maze where the cells are located
    :param option: Which agent is being used
    :param prev: boolean to see if there is a previous cell
    :param previous_cell: previous searched cell
    :return: the cell to be searched
    """
    # if option is 1 then agent 1 is being used, if the option is 2 then agent 2 is being used
    if option == 1:
        temp_matrix = maze.belief_matrix
    elif option == 2:
        temp_matrix = maze.confidence_matrix
    else:
        temp_matrix = maze.distance_belief_matrix

    result = np.where(temp_matrix == np.amax(temp_matrix))
    list_of_maxes = list(zip(result[0], result[1]))
    if prev:
        list_of_maxes = get_shortest_max_list(maze, list_of_maxes, previous_cell)
    random_index = random.randint(0, len(list_of_maxes))
    return list_of_maxes[random_index]


def false_negative_of_cell(maze, cell):
    """
    Gets the false negative rate for a given cell
    :param maze: Maze where terrain type is stored
    :param cell: cell where the false negative is needed
    :return: the false negative rate
    """
    return maze.board[cell[0], cell[1]].false_negative


def get_total_distance_traveled(maze):
    """
    Gets the total distance traveled throughout the searching
    :param maze: Maze with the distances array
    :return: sum of traveled distances
    """
    return sum(maze.traveled_distances)


def search_cell(maze, cell):
    """
    Search a given cell for target
    :param maze: Maze where search is being conducted
    :param cell: cell being searched
    :return: True if the target was found, false if it wasn't
    """
    random_number = random.uniform(0, 1)
    if maze.board[cell[0], cell[1]].is_target:
        if random_number > maze.board[cell[0], cell[1]].false_negative:
            return True
        else:
            return False
    else:
        return False


def fill_distance_matrix(maze, cell):
    """
    Makes distance matrix from celli to all other cells filled by manhattan distances
    :param maze: Maze to get distances from
    :param cell: starting cell
    :return:
    """
    distance_matrix = np.zeros((maze.dim, maze.dim))
    (x1, y1) = cell
    for x2 in range(maze.dim):
        for y2 in range(maze.dim):
            distance_matrix[x2, y2] = get_manhattan_distance(cell, (x2, y2))

    return distance_matrix


def agent(maze, option, starting_cell):
    """

    :param maze: The maze where target is
    :param option: Use agent 1, 2, or 3 (the improved agent)
    :param starting_cell: The cell to start searching from
    :return:
    """
    number_of_searches = 0
    (x, y) = starting_cell
    # (x, y) = get_current_max_cell(maze, option, False, (0, 0))
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

                # Normalize the confidence matrix as well
                sum_of_probabilities_confidence = np.sum(maze.confidence_matrix)
                maze.confidence_matrix = maze.confidence_matrix / sum_of_probabilities_confidence

            # Agent 3 utilizes another metric of distance on top of belief
            # Agent 3 assumes failure on the next cell, so it searches the closest maxes with the highest
            # probabilities around it
            if option == 3:
                # generate a matrix of manhattan distances from the current cell
                manhattan_distance_matrix = fill_distance_matrix(maze, (x, y))
                # normalize matrix using logarithm
                log_distances = 1 + np.log(1 + manhattan_distance_matrix)
                # make the distance belief matrix based upon the distance metric
                maze.distance_belief_matrix = maze.belief_matrix / log_distances

        # get the next cell to search for the iterations
        previous_cell = (x, y)
        (x, y) = get_current_max_cell(maze, option, True, previous_cell)
