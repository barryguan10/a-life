import unittest
import globals as gl
from environment import Environment
from editableParameters import EditableParameters
from overseer import Overseer


class TestMethods(unittest.TestCase):

    def test_grow_food(self):
        self.params = EditableParameters()
        env = Environment(20, 20, self.params.get_start_plants(),
                          self.params.get_start_organisms())
        env.organisms = []  # remove creatures
        for x in range(20):
            for y in range(20):
                env.grid[x][y]["occupancy"] = gl.UNOCCUPIED
                env.grid[x][y]["food"] = 0
        env.add_food(0, 0, 1)
        env.grow_plants()
        self.assertEqual(env.grid[0][0]["food"], 2)

    def test_grow_food_without_exceeding_max(self):
        self.params = EditableParameters()
        env = Environment(20, 20, self.params.get_start_plants(),
                          self.params.get_start_organisms())
        env.organisms = []  # remove creatures
        for x in range(20):
            for y in range(20):
                env.grid[x][y]["occupancy"] = gl.UNOCCUPIED
                env.grid[x][y]["food"] = 0
        env.add_food(0, 0, 1)
        for i in range(52):
            env.grow_plants()
        self.assertEqual(env.grid[0][0]["food"], 50)


class TestEditableParameters(unittest.TestCase):

    def setUp(self):
        self.params = EditableParameters()

    def test_default_values(self):
        self.assertEqual(self.params.get_start_plants(), 50)
        self.assertEqual(self.params.get_start_organisms(), 10)

    def test_set_start_plants(self):
        self.params.set_start_plants(100)
        self.assertEqual(self.params.get_start_plants(), 100)

    def test_set_start_organisms(self):
        self.params.set_start_organisms(25)
        self.assertEqual(self.params.get_start_organisms(), 25)

    def test_negative_values_clamped(self):
        self.params.set_start_plants(-10)
        self.assertEqual(self.params.get_start_plants(), 0)

        self.params.set_start_organisms(-5)
        self.assertEqual(self.params.get_start_organisms(), 0)


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.env = Environment(10, 10, 20, 5)

    def test_grid_size(self):
        self.assertEqual(len(self.env.grid), 10)
        self.assertEqual(len(self.env.grid[0]), 10)

    def test_organism_spawn_count(self):
        self.assertEqual(len(self.env.organisms), 5)

    def test_food_population_not_exceed_start(self):
        food_count = 0
        for x in range(10):
            for y in range(10):
                if self.env.grid[x][y]["food"] > 0:
                    food_count += 1

        self.assertLessEqual(food_count, 20)


class TestOverseer(unittest.TestCase):

    def setUp(self):
        self.params = EditableParameters()
        self.params.set_start_plants(30)
        self.params.set_start_organisms(7)

        self.overseer = Overseer(10, 10, self.params)

    def test_environment_initialized_correctly(self):
        env = self.overseer.environment_instance
        self.assertEqual(len(env.organisms), 7)

    def test_reset_simulation_uses_updated_parameters(self):
        self.params.set_start_plants(15)
        self.params.set_start_organisms(3)

        self.overseer.reset_simulation()

        env = self.overseer.environment_instance
        self.assertEqual(len(env.organisms), 3)

    def test_simulate_step_runs(self):
        self.overseer.simulate_step()  # should not crash


if __name__ == "__main__":
    unittest.main()
