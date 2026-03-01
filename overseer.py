import environment
import json
import os


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

    def save(self, slot_number):
        """
        Method to save objects of the simulation to a JSON File
        """
        if slot_number in (1, 2, 3):
            file_name = f"saves/{slot_number}.json"
            data = self.environment_instance.to_dictionary()
            with open(file_name, "w") as f:
                json.dump(data, f)
        else:
            return

    def load(self, slot_number):
        """
        Method to load the simulation from a JSON file
        """
        if slot_number in (1, 2, 3):
            file_name = f"saves/{slot_number}.json"
            if not os.path.exists(file_name):
                return

            with open(file_name, "r") as f:
                data = json.load(f)
            self.environment_instance = (
                environment.Environment.from_dictionary(data))

    def get_saves(self):

        slots = (1, 2, 3)
        existing = set()

        for i in slots:
            file_name = f"saves/{i}.json"
            if os.path.exists(file_name):
                existing.add(i)

        return existing
