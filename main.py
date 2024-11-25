import pygame
import logging  # Import logging module
from grid import Grid
from unit import Unit
from combat import combat_scene

# Set up logging
import os
logging.basicConfig(
    filename='game.log',
    filemode='w',  # Overwrite the log file each time
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Clear the log file at start
if os.path.exists('game.log'):
    open('game.log', 'w').close()

# Initialize Pygame and create the window
pygame.init()
screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fire Emblem Combat System")

# Create the grid and units
grid = Grid(rows=10, cols=10, cell_size=64)
unit1 = Unit(name='Unit1', position=(0, 0), health=100)
unit2 = Unit(name='Unit2', position=(9, 9), health=100)

player_turn = True
selected_unit = None

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            pos = pygame.mouse.get_pos()
            grid_x = pos[0] // grid.cell_size
            grid_y = pos[1] // grid.cell_size
            if selected_unit is None:
                # Select the player's unit
                if (grid_x, grid_y) == unit1.position:
                    selected_unit = unit1
                    possible_moves = unit1.get_possible_moves(grid)
                    grid.highlight_cells(possible_moves)
                    logging.debug(f'Unit {unit1.name} selected at position {unit1.position}')
            else:
                # Move the selected unit if the tile is valid
                if (grid_x, grid_y) in possible_moves:
                    logging.debug(f'Attempting to move {unit1.name} to position {(grid_x, grid_y)}')
                    unit1.position = (grid_x, grid_y)
                    selected_unit = None
                    grid.clear_highlights()
                    logging.info(f'{unit1.name} moved to {unit1.position}')
                    # Check for combat after moving
                    if unit1.position == unit2.position and unit2.alive:
                        logging.info(f'{unit1.name} encountered {unit2.name} at position {unit1.position}')
                        winner = combat_scene(screen, unit1, unit2)
                        logging.info(f'Combat result: {winner.name} won')
                        # Remove the defeated unit
                        if winner == unit1:
                            unit2.alive = False
                        else:
                            unit1.alive = False
                        running = False  # Exit game loop if a unit has died
                    else:
                        player_turn = False  # End player's turn

    if not player_turn:
        # Enemy unit's turn
        if unit2.alive:
            logging.debug(f"{unit2.name}'s turn")
            # Enemy AI movement towards the player's unit
            possible_moves = unit2.get_possible_moves(grid)
            # Determine the move that brings unit2 closest to unit1
            min_distance = float('inf')
            best_move = unit2.position
            for move in possible_moves:
                distance = abs(move[0] - unit1.position[0]) + abs(move[1] - unit1.position[1])
                if distance < min_distance:
                    min_distance = distance
                    best_move = move
            unit2.position = best_move
            logging.info(f'{unit2.name} moved to {unit2.position}')
            # Check for combat after moving
            if unit2.position == unit1.position and unit1.alive:
                logging.info(f'{unit2.name} encountered {unit1.name} at position {unit2.position}')
                winner = combat_scene(screen, unit1, unit2)
                logging.info(f'Combat result: {winner.name} won')
                # Remove the defeated unit
                if winner == unit1:
                    unit2.alive = False
                else:
                    unit1.alive = False
                running = False  # Exit game loop if a unit has died
            else:
                player_turn = True  # End enemy's turn

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid and units
    grid.draw(screen)
    if unit1.alive:
        unit1.draw(screen)
    if unit2.alive:
        unit2.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
