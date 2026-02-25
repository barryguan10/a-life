# config.py
class EditableParameters:
    """
    class that allows for editable parameters that user can change
    """
    def __init__(self):
        self._start_plants = 50
        self._start_organisms = 10
        self._simulation_speed = 10

    # --- Plants ---
    def get_start_plants(self):
        """
        method to return the starting plants
        """
        return self._start_plants

    def set_start_plants(self, value):
        """
        method to set the starting plants
        """
        self._start_plants = max(0, value)

    # --- Organisms ---
    def get_start_organisms(self):
        """
        method to return the starting organisms
        """
        return self._start_organisms

    def set_start_organisms(self, value):
        """
        method to set the starting organisms
        """
        self._start_organisms = max(0, value)

    def get_simulation_speed(self):
        """
        method to return the simulation speed
        """
        return self._simulation_speed

    def set_simulation_speed(self, value):
        """
        method to set the simulation speed
        """
        self._simulation_speed = max(1, value)
