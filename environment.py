import random
from organism import Organism
import globals as gl

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
                    column[y]["occupancy"] = gl.ENERGY
                else:
                    column[y]["occupancy"] = gl.UNOCCUPIED

            self.grid.append(column)
        self.place_organisms_grid()

    def create_grid(self):
        """Initializes a grid structure"""
        grid = [[{
            "occupancy": gl.UNOCCUPIED,
            "food": 0
            }
            for _ in range(self.width)]
                for _ in range(self.height)]
        return grid

    def add_food(self, x, y, energy_val):
        """Add food with an specified energy value at postion x, y in grid"""
        self.grid[x][y]["occupancy"] = gl.ENERGY
        self.grid[x][y]["food"] = energy_val

    def place_organisms_grid(self):
        """
        Docstring for place_organisms_grid

        Uses the list of organisms to update the location of each organism on
        the grid
        """
        for organism in self.organisms:
            x, y = organism.get_pos()
            self.grid[x][y]["occupancy"] = gl.CREATURE
            print("organism added", self.grid[x][y])

    def create_new_environment(self):
        pass

    def update_environment(self):
        """Updates environment in each step"""
        self.resolve_moves()
        # TODO: Call Update and update_food method, once created.

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
        surr_positions = organism.actions

        surr_items = list()

        for pos in surr_positions:
            x_offset, y_offset = pos

            new_x = org_x + x_offset
            new_y = org_y + y_offset

            # Check each spot in the grid to see there is an object there and
            # if so add its location and what
            # it is to the positions

            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                surr_items.append(
                    ((new_x, new_y), self.grid[new_x][new_y]["occupancy"])
                )

        return surr_items

    def take_energy(self, organism: Organism):
        """
        Docstring for take_energy
        :param self: Environment
        :param organism: Organism

        returns energy level from the square the organism is on
        """
        # To discuss, may want to make this more open ended for
        # combat and eating, each square may want to have a type
        # and energy instead of food
        # Get the energy in the square
        pos_x = organism.x_pos
        pos_y = organism.y_pos
        energy_amount = self.grid[pos_x][pos_y]["food"]

        self.grid[pos_x][pos_y]["food"] = 0

        return energy_amount

    def resolve_moves(self):
        """Handles Moves for all Creatures for each simulation step"""
        move_dict = {}

        for org in self.organisms:
            surroundings = self.get_surroundings(org)
            move = org.choose_action(surroundings)

            if move not in move_dict:
                move_dict[move] = org
            else:
                pass  # TODO: Handle collisions in future

        for move, org in move_dict.items():
            new_x, new_y = move
            old_x, old_y = org.get_pos()
            self.grid[old_x][old_y]["occupancy"] = gl.UNOCCUPIED
            org.set_pos(new_x, new_y)
            org.adjust_energy(self.take_energy(org))
            self.grid[new_x][new_y]["occupancy"] = gl.CREATURE
