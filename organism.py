from genome import Genome
from colorsys import hsv_to_rgb
from random import choice


OMNI_ACTIONS = [
            (0, -1), (1, 0), (0, 1), (-1, 0),
            (1, -1), (1, 1), (-1, 1), (-1, -1)
        ]


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
        self.genome = genome if genome is not None else Genome(None, 4)
        phenotype = self.decode(self.genome)
        self.color = phenotype["color"]
        self.speed = phenotype["speed"]
        self.metabolism = phenotype["metabolism"]
        self.energy = phenotype["energy"]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heading = choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        self.actions = OMNI_ACTIONS

    def decode(self, genome):
        genes = genome.get_genes()

        # using HSV for color so that minor changes in enes are color
        # consistent, visually.
        hue = float(genes[0])
        sat = 1.0
        val = 1.0
        rgb = hsv_to_rgb(hue, sat, val)
        # keep speed between 0 and 10
        speed = int((genes[1] * 10))
        # based on speed, value between 1 and 5
        metabolism = int(genes[1] * 5) + 1
        # total starting energy when born
        energy = int(genes[2] * 100)

        return {
            "color": tuple([x * 255 for x in rgb]),
            "speed": speed,
            "metabolism": metabolism,
            "energy": energy
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
            pos, status = element
            # Priority 1: Energy
            if status == 1:
                energy_pos.append(pos)

            # Final Priority: Random available direction
            if status == 0:
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
        return max(1, int(self.metabolism*(1 + self.speed*0.2)))
