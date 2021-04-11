import numpy as np
import random

import agent
from environment import Maze
import matplotlib.pyplot as plt


def generate_strategy_bar_plot(dim):
    plots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    agent_1_averages = []
    agent_2_averages = []

    for plot in plots:
        maze = Maze(dim)
        trials = 10
        agent_1_score_counter = 0
        agent_2_score_counter = 0
        for i in range(0, trials):
            target_location = (random.randrange(maze.dim), random.randrange(maze.dim))
            start_value = random.randrange(maze.dim), random.randrange(maze.dim)
            maze.board[target_location].is_target = True
            print("plot = ", plot, "trial = ", i + 1)
            agent_1_score_counter += agent.agent(maze, 1, start_value)
            maze.reset()
            agent_2_score_counter += agent.agent(maze, 2, start_value)
            maze.reset()
            maze.board[target_location].is_target = False
        agent_1_averages.append(agent_1_score_counter / trials)
        agent_2_averages.append(agent_2_score_counter / trials)

    print("Strategy 1: ", agent_1_averages)
    print("Strategy 2: ", agent_2_averages)

    x = np.arange(len(plots))
    width = .35
    fig, ax = plt.subplots()
    ax.bar(x - width / 2, agent_1_averages, width, label='Strategy 1')
    ax.bar(x + width / 2, agent_2_averages, width, label='Strategy 2')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average Performance')
    ax.set_title('Agent 1 and 2 Performances')
    ax.set_xticks(x)
    ax.set_xticklabels(plots)
    ax.legend()
    plt.savefig("strategy1_and_2.png")


def bar_plot_agent_3(dim):
    plots_x_axis_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    agent_3_averages = []
    for plot in plots_x_axis_values:
        maze = Maze(dim)
        # target_location = target_locations[plot - 1]
        trials = 10
        sum_strat3 = 0

        for i in range(0, trials):
            target_location = (random.randrange(maze.dim), random.randrange(maze.dim))
            start_value = random.randrange(maze.dim), random.randrange(maze.dim)
            maze.board[target_location].is_target = True
            print("plot = ", plot, "trial = ", i + 1)

            sum_strat3 += agent.agent(maze, 3, start_value)
            maze.board[target_location].is_target = False
            maze.reset()

        agent_3_averages.append(sum_strat3 / trials)

    print("Strategy 3: ", agent_3_averages)

    x = np.arange(len(plots_x_axis_values))
    width = .35
    fig, ax = plt.subplots()
    ax.bar(x, agent_3_averages, width, label='Advanced Strategy')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average Performance')
    ax.set_title('Agent 3 Performance')
    ax.set_xticks(x)
    ax.set_xticklabels(plots_x_axis_values)
    ax.legend()
    plt.savefig("Advanced_graph.png")
