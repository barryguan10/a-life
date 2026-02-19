from genome import Genome
from colorsys import hsv_to_rgb
from random import choice
import globals as gl


class Organism:
    """Organism Class
    This class defines an organism. Each Organism has a Genome that defines
    its phenotype/traits. Traits derived from the organims Genotype are:
        - color
        - speed (movevement speed)
        - metabolism (how much, in energy, it costs to be alive for each step)
        - energy (how much energy it is born with)
    """

    def __init__(self, genome=None, x_pos=0, y_pos=0):
        self.age = 0  # track timesteps alive for reproduction, but can be repurposed more generally
        self.genome = genome if genome is not None else Genome(None, 6)
        phenotype = self.decode(self.genome)
        self.color = phenotype["color"]
        self.speed = phenotype["speed"]
        self.metabolism = phenotype["metabolism"]
        self.energy = phenotype["energy"]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heading = choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        self.actions = gl.OMNI_ACTIONS
        self.reproduction_age = phenotype["reproduction_age"]
        self.reproduction_energy_threshold = phenotype["reproduction_energy_threshold"]
        self.reproduction_energy_cost = phenotype["reproduction_energy_cost"]
        self.reproduction_cooldown = 0
        self.reproduction_cooldown_length = 30

    def decode(self, genome):
        genes = genome.get_genes()

        # using HSV for color so that minor changes in enes are color
        # consistent, visually.
        hue = float(genes[0])
        sat = 1.0
        val = 1.0
        rgb = hsv_to_rgb(hue, sat, val)
        # keep speed between 0 and 10
        speed = int((genes[1] * 2 + 1))
        # based on speed - Can update later to be genetic influenced
        metabolism = speed
        # total starting energy when born
        energy = int(genes[2] * 10) + 100
        # reproduction age for the organism
        reproduction_age = int(genes[3] * 50) + 5
        # reproduction energy threshold and cost
        reproduction_energy_threshold = int(genes[4] * 200) + 100
        reproduction_energy_cost = int(genes[4]*100) + 60
        return {
            "color": tuple([x * 255 for x in rgb]),
            "speed": speed,
            "metabolism": metabolism,
            "energy": energy,
            "reproduction_age": reproduction_age,
            "reproduction_energy_threshold": reproduction_energy_threshold,
            "reproduction_energy_cost": reproduction_energy_cost
        }

    def get_energy(self):
        """Method used to get the organisms current energy"""
        return self.energy

    def adjust_energy(self, energy_gain: int):
        """
        Method used to update the organisms current energy by
        energy_gain amount.

        Args:
            param1: energy_gain (int) represents how much to
            add to the organisms current energy.

        Returns:
            Organisms updated energy total
        """
        self.energy = self.energy + energy_gain
        return self.energy

    def get_pos(self):
        '''Returns tuple of the x and y position of the organism'''
        return self.x_pos, self.y_pos

    def set_pos(self, x_pos, y_pos):
        '''Sets the organisms postion'''
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_heading(self):
        """Returns the heading direction of the organism"""
        return self.heading

    def set_heading(self, heading):
        """Sets the organisms desired heading"""
        options = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        if heading in options:
            self.heading = heading

    def choose_action(self, local_view):
        """Takes a local view of an organisms surroundings and returns an
        action the organism desires to take.

        Args:
            param1: local_view is a list of tuples. Each tuple element has
            two elements itself; the first is a tuple representing the grid
            cell x, y coordinates and the second element is the occupancy
            status of the cell. Example Argument:
            local_view = [
                ((1, 1), 0),
                ((1, 2), 1}
                ]

        Returns:
            (x_pos, y_pos): tuple with two elements representing the grid cell
            coordinates for the cell the creature desires to move to.

            None: If there are no valid or prefered moves for the creature.

            #TODO: In the future may ammend this to return a prioritized list
            of actions, in order of preference for the creature.
        """
        energy_pos = []
        unoccupied_pos = []

        for element in local_view:
            pos, status, _ = element
            # Priority 1: Energy
            if status == gl.ENERGY:
                energy_pos.append(pos)

            # Final Priority: Random available direction
            if status == gl.UNOCCUPIED:
                unoccupied_pos.append(pos)

        if len(energy_pos) > 0:
            return choice(energy_pos)
        if len(unoccupied_pos) > 0:
            return choice(unoccupied_pos)
        return None

    def movement_cost(self):
        """
        Adds cost for moving
        Scales cost of movement with the speed and metabolism
        """
        return self.metabolism + self.speed

    def can_reproduce(self):
        """
        Returns True if organism meets conditions to reproduce
        """
        if self.age < self.reproduction_age:
            return False
        if self.energy < self.reproduction_energy_threshold:
            return False
        if self.reproduction_cooldown > 0:
            return False

        return True

    def genetic_comparison(self, other_organism):
        """
        Compares difference between all elements of the organism's genome.
        Potentially can revise in the future if we want to adjust how to assess similarities.
        """
        genome_1 = self.genome.get_genes()
        genome_2 = other_organism.genome.get_genes()

        # Take absolute value of the difference between each element in the genome
        difference = abs(genome_1-genome_2)

        # The average difference will be between 0 and 1, with a higher value indicating higher difference
        return 1 - difference.mean()

    def choose_interaction(self, local_view):
        """
        If organism detects neighboring organism, decide interactions with that organism
        """
        for pos, status, organism_object in local_view:
            if status == gl.CREATURE and organism_object is not None:
                # avoids any interactions with itself
                if organism_object is self:
                    continue

                if self.can_reproduce() and organism_object.can_reproduce():
                    genetic_compatibility = self.genetic_comparison(organism_object)

                    if genetic_compatibility > 0.25:
                        return ("reproduce", organism_object)

                # Draft for predation, simple rule is if energy is greater and not reproducing
                if self.energy > organism_object.energy * 10:
                    return ("attack", organism_object)
        return None

    def to_dictionary(self):
        """
        Generating a Dictionary of the Organism

        :param self: an Organism Object 
        """

        dictionary = {
            "genome": self.genome.to_dictionary(),
            "age": self.age,
            "x_pos": self.x_pos,
            "y_pos": self.y_pos,
            "energy": self.energy,
            "heading": self.heading,
            "reproduction_cooldown": self.reproduction_cooldown,
            "reproduction_cooldown_length": self.reproduction_cooldown_length
        }
        return dictionary

    @classmethod
    def from_dictionary(class_type, dictionary):
        """
        Creating an Organism Object from a dictionary

        :param class_type: Organism class
        :param dictionary: dictionary object of saved attributes
        """

        # Getting the parameters for Organism creation
        genome = Genome.from_dictionary(dictionary=dictionary["genome"])
        x_pos = dictionary["x_pos"]
        y_pos = dictionary["y_pos"]

        # Creating the object
        org = class_type(genome=genome, x_pos=x_pos, y_pos=y_pos)

        # Setting attributes
        org.energy = dictionary["energy"]
        org.age = dictionary["age"]
        org.heading = dictionary["heading"]
        org.reproduction_cooldown = dictionary["reproduction_cooldown"]
        org.reproduction_cooldown_length = dictionary["reproduction_cooldown_length"]

        return org
