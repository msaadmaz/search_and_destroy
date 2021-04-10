import agent
import environment
import get_averages
from environment import Maze

if __name__ == '__main__':
    agent_1_averages, agent_2_averages = get_averages.get_average(10)
    print(f'These are the averages for agent 1: {agent_1_averages}')
    print(f'This is the averages for agent 2: {agent_2_averages}')
