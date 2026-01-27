import globals as gl
import numpy as np
from random import randrange


class Environment:
    def __init__(self, grid_width, grid_height, energy_density=25):
        self.grid = np.zeros((grid_width, grid_height))

        # Create Energy Sources
        for _ in range(grid_width*grid_height*energy_density//100):
            x = randrange(grid_width)
            y = randrange(grid_height)
            self.grid[x, y] = gl.ENERGY_CELL

        def get_energy(self, x, y):
            if self.grid[x, y] == gl.ENERGY_CELL:
                self.grid[x, y] = gl.EMPTY_CELL
                return 1
            return 0

    def create_new_environment(self):
        pass

    def update_environment(self):
        pass

    def get_organisms(self):
        # lists of organisms
        return []
