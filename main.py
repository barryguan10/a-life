'''
This code was generated with the help of chatgpt.This transcript shows the
interaction on setting up the visual pygame display.
https://chatgpt.com/share/69796b38-81fc-800d-93e0-1c6668b243cd
'''

import pygame
from overseer import Overseer
from buttons import Button
from editableParameters import EditableParameters

GRID_WIDTH = 25
GRID_HEIGHT = 25
CELL_SIZE = 25
WINDOW_SIZE = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
MAIN_WINDOW_SIZE = (GRID_WIDTH * CELL_SIZE + 400,
                    GRID_HEIGHT * CELL_SIZE + 100)
CAPTION_PLAY = "A-Life Simulation: PLAYING"
CAPTION_PAUSED = "A-Life Simulation: PAUSED"
FPS = 60
SIMULATION_SPEED = 10  # Update visual every number of these frames


def draw_environment(screen, env):
    """Draws the food grid and organisms on Pygame"""

    # Create Cell Grid Lines
    for x in range(env.width):
        for y in range(env.width):
            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    # Draw cell color based on food level
    for x in range(env.width):
        for y in range(env.height):
            food = env.grid[x][y]["food"]
            # black for cells without food
            if food == 0:
                color = (20, 20, 20)
            # green intensity for food abundance
            else:
                # scale between 0 and 255 for RGB
                intensity = int((food/10.0)*255)
                # hard limit for valid RGB values in case of bad input
                intensity = max(0, min(255, intensity))
                color = (0, intensity, 0)

            # draw rectangles for grid
            pygame.draw.rect(screen, color,
                             (x * CELL_SIZE + 2,
                              y * CELL_SIZE + 2,
                              CELL_SIZE - 4,
                              CELL_SIZE - 4))

    # draw organism
    for organism in env.get_organisms():
        x_center = organism.x_pos * CELL_SIZE + CELL_SIZE // 2
        y_center = organism.y_pos * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 4
        # draw Grey outline on for circle
        pygame.draw.circle(screen,
                           (128, 128, 128),
                           (x_center, y_center),
                           radius + 2)
        pygame.draw.circle(screen,
                           organism.color,
                           (x_center, y_center),
                           radius)

        font = pygame.font.SysFont(None, 14)
        energy_text = font.render(str(int(organism.energy)),
                                  True, (20, 20, 20))
        screen.blit(energy_text, (x_center - 8, y_center - 5))
        # TODO: Adjust numbers postion based on length of number


# initialize pygame
pygame.init()
main_screen = pygame.display.set_mode(MAIN_WINDOW_SIZE)
sim_surface = pygame.Surface(WINDOW_SIZE)
clock = pygame.time.Clock()

# create overseer to manage simulation
editable_parameters = EditableParameters()
overseer = Overseer(GRID_WIDTH, GRID_HEIGHT, editable_parameters)

# count how many frames for display updating
frame_count = 0
# boolean to check for pausing of simulation
paused = True

running = True

# create buttons
button_list = []
pause_button = Button((25, 630, 100, 25), "Play" if paused else "Pause")
button_list.append(pause_button)

# create buttons for inc, dec plant and organism
# Base positioning
base_y = 630
spacing = 10

# --- Plants Controls ---
plant_minus = Button((140, 630, 40, 25), "-")
plant_plus = Button((190, 630, 40, 25), "+")
plant_display = Button((240, 630, 120, 25),
                       f"Plants: {editable_parameters.get_start_plants()}")

# --- Organisms Controls ---
org_minus = Button((140, 665, 40, 25), "-")
org_plus = Button((190, 665, 40, 25), "+")
org_display = Button((240, 665, 120, 25),
                     f"Orgs: {editable_parameters.get_start_organisms()}")

# --- Reset Button ---
reset_button = Button((370, 630, 120, 25), "Reset")

button_list.extend([
    plant_minus, plant_plus, plant_display,
    org_minus, org_plus, org_display,
    reset_button
])


def handle_numeric_buttons(event, plus_button, minus_button,
                           display_button, get_func, set_func, label):
    """Handle + and - buttons for a numeric parameter."""
    changed = False

    if plus_button.is_button_clicked(event):
        set_func(get_func() + 1)
        changed = True
    elif minus_button.is_button_clicked(event):
        set_func(get_func() - 1)
        changed = True

    if changed:
        display_button.update_text(f"{label}: {get_func()}")


def handle_pause_button(event, pause_button, paused):
    """Toggle simulation pause/play."""
    if pause_button.is_button_clicked(event):
        paused = not paused
        if paused:
            pause_button.update_text("Play")
        else:
            pause_button.update_text("Pause")
    return paused


def handle_reset_button(event, reset_button, overseer):
    if reset_button.is_button_clicked(event):
        overseer.reset_simulation()


while running:
    clock.tick(60)
    frame_count += 1
    pygame.display.set_caption(CAPTION_PAUSED if paused else CAPTION_PLAY)

    # handle user input for simulation
    for event in pygame.event.get():

        # close window when x clicked
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # if space is pressed, toggle pause
            if event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    pause_button.update_text("Play")
                else:
                    pause_button.update_text("Pause")
            # if enter pressed while paused, iterate one step
            if event.key == pygame.K_RETURN and paused:
                overseer.simulate_step()
            # Button handling
        paused = handle_pause_button(event, pause_button, paused)
        handle_numeric_buttons(event, plant_plus, plant_minus, plant_display,
                               editable_parameters.get_start_plants,
                               editable_parameters.set_start_plants,
                               "Plants")
        handle_numeric_buttons(event, org_plus, org_minus, org_display,
                               editable_parameters.get_start_organisms,
                               editable_parameters.set_start_organisms,
                               "Orgs")
        handle_reset_button(event, reset_button, overseer)

    # update simulation when not paused
    if frame_count % SIMULATION_SPEED == 0 and not paused:
        overseer.simulate_step()

    # draw the grid and organism
    draw_environment(sim_surface, overseer.environment_instance)
    main_screen.blit(sim_surface, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    # Update button status and draw buttons
    for button in button_list:
        button.update_hover(mouse_pos)
        button.draw(main_screen)

    # pygame update display
    pygame.display.flip()

pygame.quit()
