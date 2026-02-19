from organism import Organism


class Stats:
    """Represents a class to store different statistics about the simulation"""
    def __init__(self):
        """Stats variable to keep track of"""
        self.organism_count = 0
        self.total_plants = 0
        self.total_speed = 0
        self.curr_speed_sum = 0
        self.curr_organism_alive_count = 0
        self.curr_plant_alive_count = 0
        self.alive_over_time = []
        self.plants_over_time = []
        self.average_speed_over_time = []

    def tally_alive_organism(self, org: Organism):
        """Takes in an organism and adds it to all the stats
            Needs to be called every time an organism is made"""
        self.organism_count += 1
        self.total_speed += org.speed
        self.curr_organism_alive_count += 1

    def tally_dead_organism(self, org: Organism):
        """Adjusts the current organim stats for when an organism dies"""
        self.curr_organism_alive_count -= 1
        self.curr_speed_sum -= org.speed

    def tally_alive_plant(self):
        """tallies an alive plant"""
        self.total_plants += 1
        self.curr_plant_alive_count += 1

    def tally_dead_plant(self):
        """Adjusts the current stats for when a plant gets eaten"""
        self.curr_organism_alive_count -= 1

    def snapshot(self, time):
        """Method for gathering current data and logging the time"""

        # Capture current amount of organisms alive
        self.alive_over_time.append((time, self.curr_organism_alive_count))

        if self.curr_organism_alive_count > 0:
            alive = self.curr_organism_alive_count
            average_speed = self.curr_speed_sum / alive

            self.average_speed_over_time.append((time, average_speed))
        else:
            self.average_speed_over_time.append((time, 0))

        self.plants_over_time.append((time, self.curr_plant_alive_count))

    def get_organism_count(self):
        """Returns total count of organisms"""
        return self.organism_count

    def get_plant_count(self):
        """Returns total count of plants"""
        return self.total_plants

    def get_alive_over_time(self):
        """Returns list of tuples of time and alive organisms at that time"""
        return self.alive_over_time
