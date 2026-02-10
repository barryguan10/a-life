import unittest
from environment import Environment


class TestMethods(unittest.TestCase):

    def test_grow_food(self):
        env = Environment(20, 20)
        for x in range(20):
            for y in range(20):
                env.grid[x][y]["occupancy"] = 0
        env.add_food(0, 0, 1)
        env.grow_plants()
        self.assertEqual(env.grid[0][0]["food"], 2)

    def test_grow_food_without_exceeding_max(self):
        env = Environment(20, 20)
        for x in range(20):
            for y in range(20):
                env.grid[x][y]["occupancy"] = 0
        env.add_food(0, 0, 1)
        for i in range(52):
            env.grow_plants()
        self.assertEqual(env.grid[0][0]["food"], 50)


if __name__ == "__main__":
    unittest.main()
