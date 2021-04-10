import agent
from environment import Maze


def get_average(times):
    agent_1_score_counter = 0
    agent_2_score_counter = 0
    agent_1_averages = []
    agent_2_averages = []
    counter = 0
    for time in range(times):
        maze = Maze(50)
        for time2 in range(times):
            agent_1_score_counter += agent.agent(maze, 1)
            maze.reset()
            agent_2_score_counter += agent.agent(maze, 2)
            maze.reset()
        agent_1_averages.append(agent_1_score_counter / times)
        agent_2_averages.append(agent_2_score_counter / times)
        counter += 1
        agent_1_score_counter = 0
        agent_2_score_counter = 0
        print(f'Maze {counter} is done')

    return agent_1_averages, agent_2_averages
