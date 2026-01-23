class Organism:
    """Organism Class
    This class defines an organism. Each Organism has an Energy Value and a Genome. 
    """
    def __init__(self, energy, genome):
        self.energy = energy
        self.genome = genome

        def get_energy(self):
            '''Method used to get the organisms current energy'''
            return self.energy
        
        def set_energy(self, energy_gain: int):
            '''Method used to update the organisms current energy by energy_gain amount. 
            
            Args: 
                param1: energy_gain (int) represents how much to add to the organisms current energy.

            Returns:
                Organisms updated energy total 
            '''
            self.energy = self.energy + energy_gain
            return self.energy
    
