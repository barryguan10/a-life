UNOCCUPIED = 0
ENERGY = 1
CREATURE = 2
OMNI_ACTIONS = [
            (0, -1), (1, 0), (0, 1), (-1, 0),
            (1, -1), (1, 1), (-1, 1), (-1, -1)
        ]
NORTH = [(0, 1), (1, 1), (-1, 1)]
EAST = [(1, 0), (1, 1), (1, -1)]
SOUTH = [(0, -1), (1, -1), (-1, -1)]
WEST = [(-1, 0), (-1, 1), (-1, -1)]
NORTH_EAST = [(1, 1), (0, 1), (1, 0)]
SOUTH_EAST = [(1, -1), (0, -1), (1, 0)]
SOUTH_WEST = [(-1, -1), (0, -1), (-1, 0)]
NORTH_WEST = [(-1, 1), (0, 1), (-1, 0)]
DIRECTIONS = {
    'N': NORTH,
    'E': EAST,
    'S': SOUTH,
    'W': WEST,
    'NE': NORTH_EAST,
    'SE': SOUTH_EAST,
    'SW': SOUTH_WEST,
    'NW': NORTH_WEST
}
HEADINGS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
