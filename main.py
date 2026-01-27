import globals as gl
import pygame
import environment


pygame.init()
screen = pygame.display.set_mode(gl.WINDOW_SIZE)
clock = pygame.time.Clock()


def draw_grid(screen):
    for x in range(gl.GRID_WIDTH):
        for y in range(gl.GRID_HEIGHT):
            rect = pygame.Rect(
                x * gl.CELL_SIZE,
                y * gl.CELL_SIZE,
                gl.CELL_SIZE,
                gl.CELL_SIZE
            )
            pygame.draw.rect(screen, (128, 128, 128), rect, 1)


def draw_energy(screen, env):
    for x in range(gl.GRID_WIDTH):
        for y in range(gl.GRID_HEIGHT):
            if env.grid[x, y] == gl.ENERGY_CELL:
                rect = pygame.Rect(
                    x * gl.CELL_SIZE + 3,
                    y * gl.CELL_SIZE + 3,
                    gl.CELL_SIZE - 6,
                    gl.CELL_SIZE - 6
                )
                pygame.draw.rect(screen, (0, 255, 0), rect)


# Main Entry
def main():
    running = True
    paused = True

    env = environment.Environment(gl.GRID_WIDTH, gl.GRID_HEIGHT, 10)

    while running:
        clock.tick(gl.FPS)
        pygame.display.set_caption(
            gl.CAPTION_PAUSED if paused else gl.CAPTION_PLAY
            )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Spacebar for Pause
                if event.key == pygame.K_SPACE:
                    paused = not paused

                # "c" for clearing the screen, resetting
                if event.key == pygame.K_c:
                    paused = True
                    # TODO: Add Restart conditions here

        screen.fill((20, 20, 20))
        draw_grid(screen)
        draw_energy(screen, env)
        pygame.display.update()

    pygame.quit()  # Close Window


if __name__ == "__main__":
    main()
