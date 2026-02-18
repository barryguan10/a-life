# config.py
class EditableParameters:
    """
    class that allows for editable parameters that user can change
    """
    def __init__(self):
        self._start_plants = 50
        self._start_organisms = 10

    # --- Plants ---
    def get_start_plants(self):
        return self._start_plants

    def set_start_plants(self, value):
        self._start_plants = max(0, value)

    # --- Organisms ---
    def get_start_organisms(self):
        return self._start_organisms

    def set_start_organisms(self, value):
        self._start_organisms = max(0, value)
