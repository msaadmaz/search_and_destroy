import agent
from environment import Maze


def get_average(times):
    agent_1_score_counter = 0
    agent_2_score_counter = 0
    for time in range(times):
        maze = Maze(50)
        agent_1_score_counter += agent.agent(maze, 1)
        maze.reset()
        agent_2_score_counter += agent.agent(maze, 2)
        if time == 4:
            print("quarter of the way there")
        elif time == 9:
            print("half way there")
        elif time == 14:
            print("3/4 of the way there")
        elif time == 19:
            print("done !!!")

    return agent_1_score_counter / times, agent_2_score_counter / times
