




import pygame
import random

class World:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = 40

        self.width = grid_width * self.cell_size
        self.height = grid_height * self.cell_size

        # Define safe zones (corners)
        self.safe_zones = [
            (0, 0), (0, 1), (1, 0), (1, 1),
            (0, grid_height-2), (0, grid_height-1), (1, grid_height-2), (1, grid_height-1),
            (grid_width-2, 0), (grid_width-1, 0), (grid_width-2, 1), (grid_width-1, 1),
            (grid_width-2, grid_height-2), (grid_width-1, grid_height-2),
            (grid_width-2, grid_height-1), (grid_width-1, grid_height-1)
        ]

        self.shadow_map = [[False for _ in range(grid_height)] for _ in range(grid_width)]
        self._generate_fixed_shadows()

        self.grid_surface = pygame.Surface((self.width, self.height))
        self.shadow_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.create_grid()

    def _generate_fixed_shadows(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) not in self.safe_zones and (x + y) % 3 == 0:
                    self.shadow_map[x][y] = True

    def is_in_shadow(self, x, y):
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height and self.shadow_map[x][y]

    def is_safe_zone(self, x, y):
        return (x, y) in self.safe_zones

    def create_grid(self):
        # Bluish black background
        self.grid_surface.fill((10, 12, 28))  # Very dark blue
        self.shadow_overlay.fill((0, 0, 0, 0))  # Transparent overlay

        # Gentle blue glow under safe zones
        glow_color = (0, 170, 255, 60)  # Aqua blue glow
        for x, y in self.safe_zones:
            pygame.draw.rect(
                self.shadow_overlay,
                glow_color,
                (x * self.cell_size - 4, y * self.cell_size - 4, self.cell_size + 8, self.cell_size + 8)
            )

        # Safe zones with neon blue
        for x, y in self.safe_zones:
            pygame.draw.rect(
                self.grid_surface,
                (0, 190, 255),  # Neon cyan-blue
                (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            )

        # Shadow regions with deep transparent navy
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.shadow_map[x][y]:
                    pygame.draw.rect(
                        self.shadow_overlay,
                        (0, 0, 100, 100),  # Subtle blue shadow
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    )

        # Minimalist light blue grid lines
        line_color = (80, 160, 255)  # Soft sky blue
        for x in range(self.grid_width + 1):
            pygame.draw.line(
                self.grid_surface,
                line_color,
                (x * self.cell_size, 0),
                (x * self.cell_size, self.height),
                width=1
            )
        for y in range(self.grid_height + 1):
            pygame.draw.line(
                self.grid_surface,
                line_color,
                (0, y * self.cell_size),
                (self.width, y * self.cell_size),
                width=1
            )

    def draw(self, screen):
        screen.blit(self.grid_surface, (0, 0))
        screen.blit(self.shadow_overlay, (0, 0))
