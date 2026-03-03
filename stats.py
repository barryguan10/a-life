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
        self.color_dict = {}
        self.color_over_time = []

    def tally_alive_organism(self, org: Organism):
        """Takes in an organism and adds it to all the stats
            Needs to be called every time an organism is made"""
        self.organism_count += 1
        self.total_speed += org.speed
        self.curr_organism_alive_count += 1
        color = org.color
        if color in self.color_dict:
            self.color_dict[color] += 1
        else:
            self.color_dict[color] = 1

    def tally_dead_organism(self, org: Organism):
        """Adjusts the current organim stats for when an organism dies"""
        self.curr_organism_alive_count -= 1
        self.curr_speed_sum -= org.speed
        color = org.color
        if color in self.color_dict:
            self.color_dict[color] -= 1

    def tally_alive_plant(self):
        """tallies an alive plant"""
        self.total_plants += 1
        self.curr_plant_alive_count += 1

    def tally_dead_plant(self):
        """Adjusts the current stats for when a plant gets eaten"""
        self.curr_plant_alive_count -= 1

    def snapshot(self, time):
        """Method for gathering current data and logging the time"""

        # Capture current amount of organisms alive
        self.alive_over_time.append((time, self.curr_organism_alive_count))

        # capture current color population
        self.color_over_time.append((time, self.color_dict.copy()))

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

    def get_color_over_time(self):
        """Returns list of tuples of time and color dictionary at that time"""
        return self.color_over_time

    def get_plant_over_time(self):
        """Returns list of tuples of time and alive plants at that time"""
        return self.plants_over_time

    def to_dictionary(self):
        """Converts the object into a dictionary"""
        dictionary = {
            "organism_count": self.organism_count,
            "total_plants": self.total_plants,
            "total_speed": self.total_speed,
            "curr_speed_sum": self.curr_speed_sum,
            "curr_organism_alive_count": self.curr_organism_alive_count,
            "curr_plant_alive_count": self.curr_plant_alive_count,
            "alive_over_time": self.alive_over_time,
            "plants_over_time": self.plants_over_time,
            "average_speed_over_time": self.average_speed_over_time,
            "color_dict": [[list(k), v] for k, v in self.color_dict.items()],
            "color_over_time": [[t, [[list(k), v] for k, v in cdict.items()]] for t, cdict in self.color_over_time]
        }
        return dictionary

    @classmethod
    def from_dictionary(class_type, dictionary):
        """Converts a dictionary to an object"""
        stat = class_type()
        stat.organism_count = dictionary["organism_count"]
        stat.total_plants = dictionary["total_plants"]
        stat.curr_speed_sum = dictionary["curr_speed_sum"]
        stat.curr_organism_alive_count = dictionary["curr_organism_alive_count"]
        stat.curr_plant_alive_count = dictionary["curr_plant_alive_count"]
        stat.alive_over_time = list(tuple(i) for i in dictionary["alive_over_time"])
        stat.plants_over_time = list(tuple(i) for i in dictionary["plants_over_time"])
        stat.average_speed_over_time = list(tuple(i) for i in dictionary["average_speed_over_time"])
        stat.color_dict = {tuple(k): v for k, v in dictionary["color_dict"]}
        stat.color_over_time = [(t, {tuple(k): v for k, v in color_items}) for t, color_items
                                in dictionary["color_over_time"]]
        return stat
