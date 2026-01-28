import random
from organism import Organism

MAX_FOOD = 10 # Max food can be in a cell to stay within bounds of RGB color syntax
TARGET_FOOD = 5 # Aim to fluctuate around the midpoint
FOOD_PROBABILITY = 0.05 # Chance that a cell will start with food


class Environment:
    """Represents the 2d grid the organisms exist in"""
    def __init__(self, width, height):
        """
        Docstring for __init__

        :param width: integer representing number of horizontal tiles
        :param height: integer representing number of vertical tiles
        """
        self.width = width
        self.height = height

        # list of the organisms in the environment
        self.organisms = []

        # create an organism at a random spot within the bounds of the grid
        self.organisms.append(Organism(x_pos=random.randint(0, width-1), y_pos=random.randint(0, height-1)))

        # initialize a 2d grid to represent environment
        self.grid = []
        for x in range(width):
            column = []
            for y in range(height):
                # randomly seed some areas with higher starting concentration of food
                if random.random() < FOOD_PROBABILITY:
                    food = TARGET_FOOD
                else:
                    food = 0.0

                # each cell is a dictionary with amount of food, potentially add more data later
                column.append({"food": food})

            self.grid.append(column)

    def create_new_environment(self):
        pass

    def update_environment(self):
        """
        Docstring for update_environment

        Updates environment in each step, currently fluctuates food amount only
        """
        for x in range(self.width):
            for y in range(self.height):
                fluctuation = random.uniform(-0.02, 0.02)
                self.grid[x][y]["food"] = max(0, min(MAX_FOOD, self.grid[x][y]["food"] + fluctuation))

    def get_organisms(self):
        # returns lists of organisms in environment
        return self.organisms
