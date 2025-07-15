import pygame
import math

class Player:
    def __init__(self, world):
        self.world = world
        self.grid_x = world.grid_width // 2
        self.grid_y = world.grid_height // 2
        self.x = self.grid_x * world.cell_size
        self.y = self.grid_y * world.cell_size

        # --- Movement speeds (cells per tick) ---
        self.walk_speed = world.cell_size / 1000
        self.sneak_speed = self.walk_speed * 0.5

        # --- Stamina & Noise ---
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_regen = 0.3       # per move tick
        self.stamina_drain = 1.0       # per sneak move
        self.noise_level = 0           # 0–100
        self.is_sneaking = False

        # --- Other stats/UI ---
        self.health = 100
        self.size = world.cell_size - 4
        self.floating_text = None  
        self.text_timer = 0  
        self.score = 0  

        # --- Input cooldown ---
        self.move_cooldown = 200  # milliseconds
        self.last_move_time = pygame.time.get_ticks()

        # --- Sprite setup ---
        self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.update_sprite_color()

    def handle_input(self, keys):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_cooldown:
            return

        # --- Sneak toggle (hold LSHIFT) ---
        self.is_sneaking = keys[pygame.K_LSHIFT] and self.stamina > 0

        # Choose speed
        speed = self.sneak_speed if self.is_sneaking else self.walk_speed

        moved = False
        if keys[pygame.K_w]:
            self.grid_y -= 1; moved = True
        elif keys[pygame.K_s]:
            self.grid_y += 1; moved = True
        elif keys[pygame.K_a]:
            self.grid_x -= 1; moved = True
        elif keys[pygame.K_d]:
            self.grid_x += 1; moved = True

        if moved:
            # clamp to world
            self.grid_x = max(0, min(self.grid_x, self.world.grid_width - 1))
            self.grid_y = max(0, min(self.grid_y, self.world.grid_height - 1))
            self.x = self.grid_x * self.world.cell_size
            self.y = self.grid_y * self.world.cell_size
            self.last_move_time = current_time

            # --- Update noise & stamina ---
            if self.is_sneaking:
                self.noise_level = 20
                self.stamina = max(0, self.stamina - self.stamina_drain)
            else:
                self.noise_level = 100
                self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen)
        else:
            # idle: very quiet, regen stamina
            self.noise_level = 5
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen)

    def update(self, keys=None):
        # clear floating text timer
        if self.text_timer > 0:
            self.text_timer -= 1
            if self.text_timer == 0:
                self.floating_text = ""

    def draw(self, screen):
        screen.blit(self.sprite, (self.x + 2, self.y + 2))
        if self.floating_text:
            font = pygame.font.Font(None, 30)
            text_surf = font.render(self.floating_text, True, (255, 255, 0))
            screen.blit(text_surf, (self.x + 10, self.y - 20))

    def update_sprite_color(self):
        self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        color = (0, 255, 0)
        center = (self.size//2, self.size//2)
        outer = self.size//2
        inner = self.size//4
        points = []
        for i in range(10):
            r = outer if i%2==0 else inner
            theta = i*(math.pi/5) - math.pi/2
            points.append((center[0]+math.cos(theta)*r, center[1]+math.sin(theta)*r))
        pygame.draw.polygon(self.sprite, color, points)


