import agent
import environment
from environment import Maze

if __name__ == '__main__':
    maze = Maze(50)
    print(agent.agent(maze, 2))
