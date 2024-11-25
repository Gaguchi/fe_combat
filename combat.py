import pygame
import logging  # Import logging module

def combat_scene(screen, unit1, unit2):
    # Set up the combat environment
    combat_running = True
    clock = pygame.time.Clock()

    # Positions for the units in combat scene
    unit1_pos = [160, 320]
    unit2_pos = [480, 320]
    unit1_color = (0, 255, 0)
    unit2_color = (0, 0, 255)

    logging.info(f'Starting combat between {unit1.name} (Health: {unit1.health}) and {unit2.name} (Health: {unit2.health})')

    # Simple combat logic
    while combat_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                combat_running = False
                pygame.quit()
                exit()

        # Unit1 attacks Unit2
        unit2.health -= 10
        logging.debug(f'{unit1.name} attacks {unit2.name}, {unit2.name} health: {unit2.health}')
        pygame.time.delay(500)
        if unit2.health <= 0:
            logging.info(f'{unit2.name} has been defeated by {unit1.name}')
            combat_running = False
            return unit1

        # Unit2 attacks Unit1
        unit1.health -= 10
        logging.debug(f'{unit2.name} attacks {unit1.name}, {unit1.name} health: {unit1.health}')
        pygame.time.delay(500)
        if unit1.health <= 0:
            logging.info(f'{unit1.name} has been defeated by {unit2.name}')
            combat_running = False
            return unit2

        # Draw combat scene
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, unit1_color, (unit1_pos[0], unit1_pos[1], 64, 64))
        pygame.draw.rect(screen, unit2_color, (unit2_pos[0], unit2_pos[1], 64, 64))

        # Update the display
        pygame.display.flip()
        clock.tick(60)
