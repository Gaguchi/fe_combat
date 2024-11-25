import pygame

class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size
        self.highlighted_cells = []

    def draw(self, screen):
        for x in range(self.cols + 1):
            pygame.draw.line(
                screen, (255, 255, 255),
                (x * self.cell_size, 0),
                (x * self.cell_size, self.height)
            )
        for y in range(self.rows + 1):
            pygame.draw.line(
                screen, (255, 255, 255),
                (0, y * self.cell_size),
                (self.width, y * self.cell_size)
            )
        # Draw highlighted cells
        for cell in self.highlighted_cells:
            rect = pygame.Rect(
                cell[0] * self.cell_size,
                cell[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)  # Yellow border with thickness 3

    def highlight_cells(self, cells):
        self.highlighted_cells = cells

    def clear_highlights(self):
        self.highlighted_cells = []
