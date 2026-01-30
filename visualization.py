import pygame


class PyVisualization:

    def __init__(self, screen_height, screen_width, tile_size):
        pygame.init()
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.tile_size = tile_size
        self.width_cell_count = screen_width // tile_size
        self.height_cell_count = screen_height // tile_size
        self.tile_size

        # Color RGB
        self.BLACK = (0, 0, 0,)
        self.GREY = (128, 128, 128)
        self.GREEN = (0, 255, 0)
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def draw_grid(self, positions=None):
        '''
        Draws the positions of "Alive" cells
        Argument: positions is a set of alive cells only (no need to look at
        every cell)
        '''
        self.screen.fill(self.GREY)

        # draw alive cells
        if positions:
            for position in positions:
                col, row = position
                top_left = (col * self.tile_size, row * self.tile_size)
                pygame.draw.rect(self.screen, self.GREEN, (*top_left,
                                                           self.tile_size,
                                                           self.tile_size))

        # Draw Grid Lines
        for row in range(self.height_cell_count):
            pygame.draw.line(self.screen, self.BLACK,
                             (0, row * self.tile_size),
                             (self.screen_width, row * self.tile_size))

        for col in range(self.width_cell_count):
            pygame.draw.line(self.screen, self.BLACK,
                             (col * self.tile_size, 0),
                             (col * self.tile_size, self.screen_height))


def main():
    viz = PyVisualization(600, 800, 20)

    running = True
    while running:
        for event in pygame.event.get():  # REQUIRED
            if event.type == pygame.QUIT:
                running = False
        viz.draw_grid()
        pygame.display.update()


if __name__ == "__main__":
    main()
