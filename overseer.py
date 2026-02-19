import environment


class Overseer:
    def __init__(self, width, height, editable_parameters):
        self.width = width
        self.height = height
        self.editable_parameters = editable_parameters

        self.environment_instance = environment.Environment(
            width,
            height,
            self.editable_parameters.get_start_plants(),
            self.editable_parameters.get_start_organisms()
        )

    def reset_simulation(self):
        self.environment_instance = environment.Environment(
            self.width,
            self.height,
            self.editable_parameters.get_start_plants(),
            self.editable_parameters.get_start_organisms()
        )
        self.stats = stats.Stats()
        self.iteration_count = 0

    def run_simulation(self, number_of_steps):
        for i in range(number_of_steps):
            self.simulate_step()

    def simulate_step(self):
        self.environment_instance.update_environment()
        # call analysis function to update species
        # call display function to draw environment

    def save(self):
        pass

    def load(self):
        pass
