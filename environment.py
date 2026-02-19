import random
from organism import Organism
import globals as gl
import genome
import numpy as np
import stats

# Max food is the maximum energy value a piece of food can have
MAX_FOOD = 50
TARGET_FOOD = 5  # Aim to fluctuate around the midpoint
FOOD_PROBABILITY = 0.15  # Chance that a cell will start with food
SPAWN_PLANT_TIME = 5  # How long until a new plant gets placed on the board
UNIQUE_STARTING_CREATURES = 2


class Environment:
    """Represents the 2d grid the organisms exist in"""

    def __init__(self, width, height, start_plants, start_organisms):
        """
        Docstring for __init__

        :param width: integer representing number of horizontal tiles
        :param height: integer representing number of vertical tiles
        :param start_plants: integer representing number of starting plants
        :param start_organisms: integer representing number of starting
        organisms
        """
        self.organisms = None
        self.width = width
        self.height = height
        self.count_down_spawn_plant = SPAWN_PLANT_TIME
        self.empty_places = set()
        self.grid = self.create_grid()
        self.stats = stats.Stats()
        self.start_plants = start_plants
        self.start_organisms = start_organisms
        self.create_new_environment()
        self.iteration_count = 0
        self.stats.snapshot(self.iteration_count)

    def create_grid(self):
        """Initializes a grid structure"""
        # uses list comprehension and formatted so additional dict keys
        # can be added easily.
        grid = [
            [
                (
                    self.empty_places.add((x, y)),
                    {"occupancy": gl.UNOCCUPIED, "food": 0}
                )[1]
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]
        return grid

    def toggle_empty_places(self, coordinates: tuple):
        """Adjusts empty places list to account for changes in space status"""
        if coordinates in self.empty_places:
            self.empty_places.remove(coordinates)
        else:
            self.empty_places.add(coordinates)

    def add_food(self, x, y, energy_val):
        """Add food with a specified energy value at postion x, y in grid"""
        self.grid[x][y]["occupancy"] = gl.ENERGY
        self.grid[x][y]["food"] = energy_val
        self.toggle_empty_places((x, y))

    def populate_food_clustered(self, radius=3):
        """Populate food in clusters using total start_plants count"""
        plants_added = 0
        clusters = max(1, self.start_plants // 10)
        for _ in range(clusters):
            if plants_added >= self.start_plants:
                break
            cx = random.randint(0, self.width - 1)
            cy = random.randint(0, self.height - 1)
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):

                    if plants_added >= self.start_plants:
                        return
                    x = cx + dx
                    y = cy + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if random.random() < 0.6:
                            if self.grid[x][y]["food"] == 0:
                                self.add_food(x, y, MAX_FOOD)
                                plants_added += 1

    def grow_plants(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]["occupancy"] == gl.ENERGY:
                    if self.grid[x][y]["food"] < MAX_FOOD:
                        self.grid[x][y]["food"] += 1

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
            # TODO:The below loop could have infinite loop condition if grid is
            # full. This is because it's trying to randomly find an open cell
            # this also occurs in Nicole's spawn_plant method. We should
            # consider making a set data structure for available unoccupied
            # cells.
            while occupied:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
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
            self.toggle_empty_places((x, y))
            # print("organism added", self.grid[x][y])

    def spawn_plant(self):
        # Spawn plant
        while True:  # TODO: See Justin's "To Do" note in new_organism_list
            random_x = random.randint(0, self.width - 1)
            random_y = random.randint(0, self.height - 1)
            if self.grid[random_x][random_y]["occupancy"] == gl.UNOCCUPIED:
                self.grid[random_x][random_y]["occupancy"] = gl.ENERGY
                self.grid[random_x][random_y]["food"] = 1
                self.toggle_empty_places((random_x, random_y))
                break
        self.count_down_spawn_plant = None

    def set_spawn_plant_timer(self):
        if self.count_down_spawn_plant is None:
            new_timer = random.randint(
                int(SPAWN_PLANT_TIME * 0.7), int(SPAWN_PLANT_TIME * 1.3)
            )
            self.count_down_spawn_plant = new_timer

    def decrement_spawn_plant_timer(self):
        if self.count_down_spawn_plant == 0:
            self.spawn_plant()
        elif self.count_down_spawn_plant is not None:
            self.count_down_spawn_plant -= 1

    def create_new_environment(self):
        """Populates Grid with Food and Organisms"""
        self.populate_food_clustered()
        self.organisms = self.new_organism_list(self.start_organisms,
                                                UNIQUE_STARTING_CREATURES)
        for org in self.organisms:
            self.stats.tally_alive_organism(org)
        self.place_organisms_grid()

    def update_environment(self):
        """Updates environment in each step"""
        self.place_organisms_grid()
        self.set_spawn_plant_timer()
        self.decrement_spawn_plant_timer()
        self.grow_plants()
        for org in self.organisms:
            org.age += 1  # increment every step to track age of organisms
            org.adjust_energy(-org.metabolism)
            if org.reproduction_cooldown > 0:
                org.reproduction_cooldown -= 1
        self.resolve_organism_interactions()
        self.resolve_moves()
        self.resolve_asexual_reproduction()
        self.remove_dead_organisms()
        self.iteration_count += 1
        self.stats.snapshot(self.iteration_count)
        # TODO: Call Update and update_food method, once created.

    def get_organisms(self):
        # returns lists of organisms in environment
        return self.organisms

    def remove_dead_organisms(self):
        """
        Remove dead organisms if their energy goes below 0
        """
        alive_organisms = []

        for org in self.organisms:
            if org.get_energy() > 0:
                alive_organisms.append(org)
            else:
                x, y = org.get_pos()
                self.stats.tally_dead_organism(org)
                self.grid[x][y]["occupancy"] = 0
                self.toggle_empty_places((x, y))

        self.organisms = alive_organisms

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
                cell = self.grid[new_x][new_y]
                occupancy = cell["occupancy"]
                occupant_object = None

                # Search the list of organisms for this organism so we can
                # return instance of it
                if occupancy == gl.CREATURE:
                    for organism in self.organisms:
                        if organism.get_pos() == (new_x, new_y):
                            occupant_object = organism
                            break
                surr_items.append(
                    ((new_x, new_y),
                     self.grid[new_x][new_y]["occupancy"],
                     occupant_object)
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
            if org.get_energy() <= 0:
                continue
            surroundings = self.get_surroundings(org)
            move = org.choose_action(surroundings)
            if move is None:
                continue
            if move not in move_dict:
                move_dict[move] = org
            else:
                pass  # TODO: Handle collisions in future

        for move, org in move_dict.items():
            new_x, new_y = move
            old_x, old_y = org.get_pos()
            self.grid[old_x][old_y]["occupancy"] = gl.UNOCCUPIED
            self.toggle_empty_places((old_x, old_y))
            org.adjust_energy(-org.movement_cost())
            org.set_pos(new_x, new_y)
            org.adjust_energy(self.take_energy(org))
            # Checks if the cell was not empty before
            if self.grid[new_x][new_y]["occupancy"] == gl.ENERGY:
                self.toggle_empty_places((old_x, old_y))
            self.grid[new_x][new_y]["occupancy"] = gl.CREATURE
            self.toggle_empty_places((old_x, old_y))

    def get_empty_adjacent_spaces(self, x, y):
        empty_spaces = []

        for dx, dy in gl.OMNI_ACTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[nx][ny]["occupancy"] == gl.UNOCCUPIED:
                    empty_spaces.append((nx, ny))

        return empty_spaces

    def resolve_asexual_reproduction(self):
        new_organisms = []

        for org in self.organisms:
            # Check if internal conditions to reproduce are met by organism
            if not org.can_reproduce():
                continue

            x, y = org.get_pos()
            empty_spaces = self.get_empty_adjacent_spaces(x, y)
            # Check if there is any adjacent space to place new organism
            if not empty_spaces:
                continue

            # Choose a random space from the empty adjacent spaces to spawn
            child_x, child_y = random.choice(empty_spaces)
            child_genome = org.genome.copy_genes()
            child_genome.mutate(rate=0.05, std_dev=0.1)
            org.adjust_energy(-org.reproduction_energy_cost)

            child = Organism(genome=child_genome, x_pos=child_x, y_pos=child_y)
            self.grid[child_x][child_y]["occupancy"] = gl.CREATURE
            self.toggle_empty_places((child_x, child_y))
            new_organisms.append(child)
            self.stats.tally_alive_organism(child)
            org.reproduction_cooldown = org.reproduction_cooldown_length

        self.organisms.extend(new_organisms)

    def resolve_organism_interactions(self):
        """
        resolves interactions between organisms
        """
        # a set to keep track of pairs that have already interacted,
        # preventing repeats
        resolved_pairs = set()
        new_organisms = []

        for org in self.organisms:
            surroundings = self.get_surroundings(org)
            interaction = org.choose_interaction(surroundings)
            # return none if no organisms nearby to interact with
            if interaction is None:
                continue

            # separate the action returned and the organism to interact with
            action, target_organism = interaction

            # id gets address of object, then it's sorted to prevent repeats
            # then converted to a tuple so it can be stored in a set
            pair = tuple(sorted([id(org), id(target_organism)]))
            if pair in resolved_pairs:
                continue

            resolved_pairs.add(pair)

            if action == "reproduce":
                child = self.resolve_sexual_reproduction(org, target_organism)
                new_organisms.append(child)
                self.stats.tally_alive_organism(child)

            elif action == "attack":
                self.resolve_predation(org, target_organism)

        self.organisms.extend(new_organisms)

    def resolve_sexual_reproduction(self, parent_1, parent_2):
        """
        Combines genomes from two parents to create a child
        """

        x, y = parent_1.get_pos()
        empty_spaces = self.get_empty_adjacent_spaces(x, y)
        # Check if there is any adjacent space to place new organism
        if not empty_spaces:
            return None

        # Choose a random space from the empty adjacent spaces to spawn
        child_x, child_y = random.choice(empty_spaces)

        genome_1 = parent_1.genome.copy_genes()
        genome_2 = parent_2.genome.copy_genes()

        # splits genome into two parts and combines them into child genome
        split = random.randint(1, len(genome_1.get_genes())-1)
        child_genes = np.concatenate((genome_1.get_genes()[:split],
                                      genome_2.get_genes()[split:]))
        child_genome = genome.Genome(child_genes)
        child_genome.mutate(rate=0.05, std_dev=0.1)

        parent_1.adjust_energy(-parent_1.reproduction_energy_cost)
        parent_2.adjust_energy(-parent_2.reproduction_energy_cost)

        child = Organism(genome=child_genome, x_pos=child_x, y_pos=child_y)
        self.grid[child_x][child_y]["occupancy"] = gl.CREATURE
        self.toggle_empty_places((child_x, child_y))
        parent_1.reproduction_cooldown = parent_1.reproduction_cooldown_length
        parent_2.reproduction_cooldown = parent_2.reproduction_cooldown_length

        return child

    def resolve_predation(self, predator, prey):
        """
        Resolve interactions where one organism consumes another
        """
        prey.adjust_energy(-prey.energy)
        predator.adjust_energy(prey.energy)
