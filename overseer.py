import environment
import organism


class Overseer:
    def __init__(self):
        self.environment_instance = None

    def new_simulator(self):
        self.environment_instance = environment.Environment()

    def run_simulation(self, number_of_steps):
        for i in range(number_of_steps):
            self.simulate_step()

    def simulate_step(self):
        self.environment_instance.update_environment()
        for organism in self.environment_instance.get_organisms:
            organism.move()
        # call analysis function to update species
        # call display function to draw environment

    def save(self):
        pass

    def load(self):
        pass