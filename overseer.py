import environment
import json


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

    def run_simulation(self, number_of_steps):
        for i in range(number_of_steps):
            self.simulate_step()

    def simulate_step(self):
        self.environment_instance.update_environment()
        # call analysis function to update species
        # call display function to draw environment

    def save(self, filename="save.json"):
        data = self.environment_instance.to_dictionary()
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename="save.json"):
        with open(filename, "r") as f:
            data = json.load(f)
        self.environment_instance = environment.Environment.from_dict(data)
