import random
from organism import Organism

# Max food can be in a cell to stay within bounds of RGB color syntax
MAX_FOOD = 10
TARGET_FOOD = 5  # Aim to fluctuate around the midpoint
FOOD_PROBABILITY = 0.05  # Chance that a cell will start with food


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
        self.organisms.append(
            Organism(
                x_pos=random.randint(0, width - 1),
                y_pos=random.randint(0, height - 1)
            )
        )

        # initialize a 2d grid to represent environment
        self.grid = []
        for x in range(width):
            column = []
            for y in range(height):
                # randomly seed some areas with higher starting concentration
                # of food
                if random.random() < FOOD_PROBABILITY:
                    food = TARGET_FOOD
                else:
                    food = 0.0

                # each cell is a dictionary with amount of food, potentially
                # add more data later
                column.append({"food": food})
                if food > 0:
                    column[y]["occupancy"] = 1
                else:
                    column[y]["occupancy"] = 0

            self.grid.append(column)
        self.place_organisms_grid()

    def place_organisms_grid(self):
        """
        Docstring for place_organisms_grid

        Uses the list of organisms to update the location of each organism on
        the grid
        """
        for organism in self.organisms:
            pos_tuple = organism.get_pos()
            self.grid[pos_tuple[0]][pos_tuple[1]]["occupancy"] = 2
            print("organism added", self.grid[pos_tuple[0]][pos_tuple[1]])

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
                self.grid[x][y]["food"] = max(
                    0, min(MAX_FOOD, self.grid[x][y]["food"] + fluctuation)
                )
                if self.grid[x][y]["occupancy"] != 2:
                    self.grid[x][y]["occupancy"] = (
                        1 if self.grid[x][y]["food"] > 0 else 0
                    )
        self.place_organisms_grid()

    def get_organisms(self):
        # returns lists of organisms in environment
        return self.organisms

    def get_surroundings(self, organism: Organism):
        """
        A function to return the surroundings of an organism

        :param self: The environment instance
        :param organism: The organism for the surroundings to be returned
        """
        # Get the current position of the organism
        org_x, org_y = organism.get_pos()

        # Positions to check, can be replaced in the future with
        # the organism's sight
        surr_positions = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        surr_items = list()

        for pos in surr_positions:
            x_offset, y_offset = pos

            # Check each spot in the grid to see there is an object there and
            # if so add its location and what
            # it is to the positions
            if self.grid[org_x + x_offset][org_y + y_offset] != 0:
                surr_items.append(
                    (
                        (org_x + x_offset, org_y + y_offset),
                        self.grid[org_x + x_offset][org_y + y_offset],
                    )
                )

        return surr_items
