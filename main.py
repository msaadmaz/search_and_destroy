import agent
import environment
import get_averages
from environment import Maze

if __name__ == '__main__':
    agent_1_average, agent_2_average = get_averages.get_average(20)
    print(f'This is the average for agent 1: {agent_1_average}')
    print(f'This is the average for agent 2: {agent_2_average}')
