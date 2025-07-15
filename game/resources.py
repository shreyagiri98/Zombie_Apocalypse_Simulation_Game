import pygame
import random

class Resource:
    def __init__(self, world, grid_x, grid_y, lifetime=600):
        self.world = world
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = world.cell_size - 8
        self.lifetime = lifetime  # Lifetime in frames

        # Create glowing coin sprite
        self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        center = self.size // 2
        for radius in range(center, 0, -1):
            alpha = int(255 * (radius / center) ** 2)
            color = (255, 255, 100, alpha)
            pygame.draw.circle(self.sprite, color, (center, center), radius)

        pygame.draw.circle(self.sprite, (255, 255, 0), (center, center), center // 2)

    def update(self):
        self.lifetime -= 1
        return self.lifetime > 0

class ResourceManager:
    def __init__(self, world):
        self.world = world
        self.resources = []
        self.spawn_timer = 0
        self.base_spawn_interval = 150  # Reduced from 300 for faster spawns
        self.level = 1
        self.level_up_interval = 1800  # Every 30 seconds at 60 FPS

        # Initial resources
        for _ in range(5):
            self.spawn_resource()

    def spawn_resource(self):
        x = random.randint(0, self.world.grid_width - 1)
        y = random.randint(0, self.world.grid_height - 1)
        lifetime = max(300, 600 - self.level * 20)
        self.resources.append(Resource(self.world, x, y, lifetime=lifetime))

    def update(self):
        self.spawn_timer += 1
        spawn_interval = max(30, self.base_spawn_interval - self.level * 15)

        if self.spawn_timer >= spawn_interval:
            # Spawn multiple coins at once (increase this number as needed)
            for _ in range(2):
                if len(self.resources) < 100:  # Optional cap
                    self.spawn_resource()
            self.spawn_timer = 0

        # Remove expired resources
        self.resources = [r for r in self.resources if r.update()]

    def level_up(self):
        self.level += 1

    def check_collection(self, player):
        collected_amount = 0
        new_resources = []

        for resource in self.resources:
            if resource.grid_x == player.grid_x and resource.grid_y == player.grid_y:
                # --- Give triangular growth points ---
                points = self.level * (self.level + 1) // 2  # e.g., 1, 3, 6, 10...
                collected_amount += points
            else:
                new_resources.append(resource)

        self.resources = new_resources
        return collected_amount


    def draw(self, screen):
        for resource in self.resources:
            x = resource.grid_x * self.world.cell_size + 4
            y = resource.grid_y * self.world.cell_size + 4
            screen.blit(resource.sprite, (x, y))
