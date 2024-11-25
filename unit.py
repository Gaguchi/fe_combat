import pygame
import logging  # Import logging module

class Unit:
    def __init__(self, name, position, health):
        self.name = name
        self.position = position  # (x, y) grid coordinates
        self.health = health
        self.alive = True
        self.color = (0, 255, 0) if name == 'Unit1' else (0, 0, 255)
        self.cell_size = 64  # Assuming cell size is consistent
        self.move_range = 3  # Movement range
        self.selected = False  # For tracking selection state

    def move(self, direction):
        x, y = self.position
        if direction == 'up' and y > 0:
            y -= 1
        elif direction == 'down' and y < 9:
            y += 1
        elif direction == 'left' and x > 0:
            x -= 1
        elif direction == 'right' and x < 9:
            x += 1
        self.position = (x, y)
        logging.info(f'{self.name} moved {direction} to {self.position}')

    def get_possible_moves(self, grid):
        x, y = self.position
        moves = []
        for dx in range(-self.move_range, self.move_range + 1):
            for dy in range(-self.move_range, self.move_range + 1):
                if abs(dx) + abs(dy) <= self.move_range:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < grid.cols and 0 <= new_y < grid.rows:
                        moves.append((new_x, new_y))
        return moves

    def draw(self, screen):
        x, y = self.position
        rect = pygame.Rect(
            x * self.cell_size,
            y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(screen, self.color, rect)
