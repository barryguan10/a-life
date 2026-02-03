import random
from organism import Organism
import globals as gl
import genome

# Max food is the maximum energy value a piece of food can have
MAX_FOOD = 10
FOOD_PROBABILITY = 0.05  # Chance that a cell will start with food
UNIQUE_STARTING_CREATURES = 2
STARTING_POPULATION = 5


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
        self.grid = self.create_grid()
        self.create_new_environment()

    def create_grid(self):
        """Initializes a grid structure"""
        # uses list comprehension and formatted so additional dict keys
        # can be added easily.
        grid = [[{
            "occupancy": gl.UNOCCUPIED,
            "food": 0
            }
            for _ in range(self.width)]
                for _ in range(self.height)]
        return grid

    def add_food(self, x, y, energy_val):
        """Add food with a specified energy value at postion x, y in grid"""
        self.grid[x][y]["occupancy"] = gl.ENERGY
        self.grid[x][y]["food"] = energy_val

    def populate_food(self):
        """Populates the starting grid with food."""
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < FOOD_PROBABILITY:
                    self.add_food(x, y, MAX_FOOD)

    def is_occupied(self, x, y):
        """Returns true if grid location x, y is occupied"""
        return self.grid[x][y]["occupancy"] != 0

    def new_organism_list(self, population, unique_count=1):
        """Creates a new list of organisms
                Args:
            param1: population (int)
                    represents how many organisms to create
            param2: unique_count (int)
                    represents how many unique creatures

        Returns: List of Organisms
        """
        # Make sure args are valid
        if unique_count <= 0:
            unique_count = 1
        if population <= 0:
            population = 1

        # get genomes for starting creature types
        unique_genomes = []
        for _ in range(unique_count):
            unique_genomes.append(genome.Genome())

        organisms = []
        i = 0  # used to iterate over unique_genomes, keeps species counts even
        for _ in range(population):
            occupied = True
            while occupied:  # Could have infinite loop if grid full!!!!
                x = random.randint(0, self.width-1)
                y = random.randint(0, self.height-1)
                occupied = self.is_occupied(x, y)
            organisms.append(Organism(unique_genomes[i], x, y))
            # Because organism location is not added to grid until
            # place_organisms_grid is called - two organisms could occupy
            # the same starting cell. Need to modify place_organisms_grid
            # to place the currenly created organism in the grid, then call 
            # here.
            i += 1
            if i >= unique_count:
                i = 0
        return organisms

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
        """Populates Grid with Food and Organisms"""
        self.populate_food()
        self.organisms = self.new_organism_list(STARTING_POPULATION,
                                                UNIQUE_STARTING_CREATURES)
        self.place_organisms_grid()

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
