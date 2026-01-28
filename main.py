'''
This code was generated with the help of chatgpt.This transcript shows the interaction on setting up the visual pygame display. 
https://chatgpt.com/share/69796b38-81fc-800d-93e0-1c6668b243cd
'''

import pygame
from overseer import Overseer


SCREEN_WIDTH = 800  # Screen Width (Pixels)
SCREEN_HEIGHT = 800  # Screen Height (Pixels)
TILE_SIZE = 20  # Tile Size (Pixels)
SIMULATION_SPEED = 10 # Update visual every number of these frames

# Determine number of tiles 
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE


    
def draw_environment(screen, env):
    """Draws the food grid and organisms on Pygame"""

    # Draw cell color based on food level
    for x in range(env.width):
        for y in range(env.height):
            food = env.grid[x][y]["food"]
            # black for cells without food
            if food == 0:
                color = (20,20,20)
            # green intensity for food abundance
            else:
                intensity = int((food/10.0)*255) # scale between 0 and 255 for RGB
                intensity = max(0, min(255, intensity)) # hard limit for valid RGB values in case of bad input
                color = (0,intensity,0)
            
            # draw rectangles for grid
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # draw organism
    for organism in env.get_organisms():
        x_center = organism.x_pos * TILE_SIZE + TILE_SIZE//2
        y_center = organism.y_pos * TILE_SIZE + TILE_SIZE//2
        radius = TILE_SIZE//2-2
        pygame.draw.circle(screen, organism.color, (x_center, y_center), radius)

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# create overseer to manage simulation
overseer = Overseer(GRID_WIDTH, GRID_HEIGHT)

# count how many frames for display updating
frame_count = 0
# boolean to check for pausing of simulation
paused = False

running = True
while running:
    clock.tick(60)
    frame_count += 1

    # handle user input for simulation
    for event in pygame.event.get():

        # close window when x clicked
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # if space is pressed, toggle pause
                paused = not paused
            elif event.key == pygame.K_RETURN and paused: # if enter pressed while paused, iterate one step
                overseer.simulate_step()
    # update simulation when not paused
    if frame_count % SIMULATION_SPEED == 0 and not paused:
        overseer.simulate_step()
    #draw the grid and organism
    draw_environment(screen, overseer.environment_instance)
    # pygame update display
    pygame.display.flip()

pygame.quit()