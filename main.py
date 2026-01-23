import pygame
from random import randrange


#### GLOBALS
SCREEN_WIDTH = 800          # Screen Width (Pixels)
SCREEN_HEIGHT = 800         # Screen Height (Pixels)
TILE_SIZE = 20               # Tile Size (Pixels)
# Number of "Cells" in Screen for both Width and Height 
WIDTH_CELL_COUNT = SCREEN_WIDTH // TILE_SIZE
HEIGHT_CELL_COUNT = SCREEN_HEIGHT // TILE_SIZE
# Captions for Python Screen
CAPTION_PLAY = "Conway's Game of Life: PLAYING"
CAPTION_PAUSED = "Conway's Game of Life: PAUSED"
UPDATE_FREQ = 20  # Responsible for how fast the simulation updates (20= slow, 5 = fast)

# Colors Used
BLACK = (0,0,0,)
GREY = (128,128,128)
GREEN = (0, 255, 0)

# Frames per second
FPS = 60 

### Classes

    # To be added later

### Pygame setup

# Required for pygame to work - Initializes
pygame.init()

# creates a screen display surface of width, height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# instantiates the clock for the game
clock = pygame.time.Clock()


### Function Definitions

def gen(num):
    ''' Generate a set of cell positions, represented as (x, y) integer positions'''
    # used set comprehension. Long line so broken up on multi-line
    return {(randrange(0, WIDTH_CELL_COUNT), randrange(0, HEIGHT_CELL_COUNT)) 
                for _ in range(num)}

def draw_grid(positions): 
    '''
    Draws the positions of "alive" cells
    Argument: positions is a set of alive cells only (no need to look at every cell)
    '''
    # draw alive cells
    for position in positions:
        col, row = position         # It's "Col, Row" due to X, Y (think 2D-Cartesian Coordinates)
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
                # Draw a Rectangle Object. RectValue is top left position and then 
                # rectangle width and height from that point. *top_left is just unpacking 
        pygame.draw.rect(screen, GREEN, (*top_left, TILE_SIZE, TILE_SIZE))

    # Draw Grid Lines
    for row in range(HEIGHT_CELL_COUNT): 
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (SCREEN_WIDTH, row * TILE_SIZE))

    for col in range(WIDTH_CELL_COUNT):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, SCREEN_HEIGHT))

# Adjust Grid Positions (ESSENTIALLY THIS FUNCTION IS SIMILAR TO OUR "OVERSEER")
def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions: 
        neighbors = get_neighbors(position)
        
        # add all neighbors (alive or dead) to a set of all neighbors 
        all_neighbors.update(neighbors)

        neighbor_list = []
        # loop over each neighbor
        for neighbor in neighbors:
            # check if neighbor is alive (i.e. in positions set)
            if neighbor in positions:
                # alive, add to neighbor_list
                neighbor_list.append(neighbor)
        
        if len(neighbor_list) in [2, 3]:
            # cell position has 2 or 3 neighbors, it survives
            new_positions.add(position)

    # check if any positions in all neighbors needs to come alive
    for position in all_neighbors:
        if position not in positions:
            neighbors = get_neighbors(position)
            neighbor_list = []
            # loop over each neighbor
            for neighbor in neighbors:
                # check if neighbor is alive (i.e. in positions set)
                if neighbor in positions:
                    # alive, add to neighbor_list
                    neighbor_list.append(neighbor)
            # if number of neighbors for unalive cell is 3, cell comes to life, 
            # i.e., add to new_positions
            if len(neighbor_list) == 3:
                new_positions.add(position)   
    
    # return all new game positions
    return new_positions         


def get_neighbors(pos):
    '''Get list of all neighbor cells around the cell at argument "pos" '''
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        # check if neighbor is off grid (i.e., left of 0 or right of screen width), skip if so 
        if x + dx < 0 or x + dx > WIDTH_CELL_COUNT:
            continue
        for dy in [-1, 0, 1]:
            # check if neighbor is off grid (i.e., above 0 or below screen height), skip if so
            if y + dy < 0 or y + dy > HEIGHT_CELL_COUNT:
                continue
            # check if "neighbor" is actually the position; you can't be your own neighbor!
            if dy == 0 and dx == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors        

# Main Entry
def main(): 
    running = True  # varible to see if game should stop running
    playing = False # varible for pause
    count = 0       # Used for game speed control, in conjunction with UPDATE_FREQ
    positions = set()       # Set of all alive postitions (initilized here)
    
    while running:
        
        # Limit frame rate so computer isn't burning from running as quickly 
        # as possilbe  (less resource intensive)
        clock.tick(FPS)

        if playing: 
            count += 1      # Note: increasing count also updates how fast game runs 
        
        if count >= UPDATE_FREQ:
            count = 0 
            positions = adjust_grid(positions)

        pygame.display.set_caption(CAPTION_PLAY if playing else CAPTION_PAUSED)

        # Cycle through event polls 
        for event in pygame.event.get(): 
            # Check for event type QUIT (all caps) to see if user exits window. 
            if event.type == pygame.QUIT:
                running = False
            
            # check for mouse button event type
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get pixel postion on pygame screen
                x, y = pygame.mouse.get_pos()
                # integer division to obtain top-left coordinate of box clicked in
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)    # save in tuple
                # Add/Remove from positions set
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                
                # if spacebar is pressed, pause
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                # if "c" pressed, clear screen positions
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    # should update count if clearing screen
                    count = 0 
                
                # if "g" key is pressed, generate random positions
                if event.key == pygame.K_g:
                    positions = gen(randrange(4 , 10) * WIDTH_CELL_COUNT)


        # Set background color of the screen (must draw in order (or you risk overwriting))
        screen.fill(GREY)
        draw_grid(positions)
        
        # must call this to actually update the display (REVIEW .update vs .flip for project code)
        pygame.display.update()
    
    pygame.quit()           # Close Window


if __name__ == "__main__":
    main()    


