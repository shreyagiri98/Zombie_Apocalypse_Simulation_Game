

import pygame
import random
import math
import numpy as np
from enum import Enum
from game.resources import ResourceManager
from .pathfinding import find_path

class ZombieState(Enum):
    IDLE = "idle"
    WANDERING = "wandering"
    CHASING = "chasing"
    ALERTED = "alerted"

class Zombie:
    def __init__(self, world, grid_x, grid_y, sound_manager):
        self.world = world
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * world.cell_size
        self.y = grid_y * world.cell_size
        self.speed = 2
        self.size = world.cell_size - 4
        self.state = ZombieState.IDLE
        self.path = []
        self.update_timer = 0
        self.sound_manager = sound_manager
        self.sound_timer = 0

        self.vision_range = 6
        self.hearing_range = 6
        self.alert_radius = 5
        self.learning_rate = 0.1
        self.aggression = 0.5
        self.memory = []
        self.last_seen_player = None
        self.group_leader = None
        self.followers = []
        self.success_rate = 0.5

        self.is_leader = False
        self.preferred_distance = 2

        self.sprite = pygame.Surface((self.size, self.size))
        self.base_color = (255, 255, 255)
        self.update_sprite_color()

    def update_sprite_color(self):
        self.sprite.fill((0, 0, 0, 0))
        state_colors = {
            ZombieState.IDLE: (200, 0, 0),
            ZombieState.WANDERING: (255, 0, 0),
            ZombieState.CHASING: (255, 100, 0),
            ZombieState.ALERTED: (255, 0, 0),
        }
        base_color = state_colors[self.state]

        if self.is_leader:
            base_color = tuple(min(c + 50, 255) for c in base_color)

        center = (self.size // 2, self.size // 2)
        radius = self.size // 2 - 2

        pygame.draw.circle(self.sprite, base_color, center, radius)
        eye_radius = 2
        eye_offset_x = self.size // 5
        eye_offset_y = self.size // 5
        pygame.draw.circle(self.sprite, (0, 0, 0), (center[0] - eye_offset_x, center[1] - eye_offset_y), eye_radius)
        pygame.draw.circle(self.sprite, (0, 0, 0), (center[0] + eye_offset_x, center[1] - eye_offset_y), eye_radius)
        teeth_width = 2
        teeth_height = 3
        for i in range(3):
            pygame.draw.rect(self.sprite, (0, 0, 0), (center[0] - 4 + i * 3, center[1] + 4, teeth_width, teeth_height))

    def can_see_player(self, player):
        dist = math.sqrt((self.grid_x - player.grid_x)**2 + (self.grid_y - player.grid_y)**2)
        if dist > self.vision_range:
            return False
        effective_range = self.vision_range * (1.0 if not player.is_sneaking else 0.5)
        if dist > effective_range:
            return False
        if self.world.is_in_shadow(player.grid_x, player.grid_y):
            effective_range *= 0.5
        return dist <= effective_range

    def can_hear_player(self, player):
        dist = math.sqrt((self.grid_x - player.grid_x)**2 + (self.grid_y - player.grid_y)**2)
        noise_factor = player.noise_level / 100.0
        return dist <= self.hearing_range * noise_factor

    def update_ai(self, player, all_zombies):
        self.sound_timer -= 1
        if self.sound_timer <= 0:
            self.sound_manager.play_groan()
            self.sound_timer = random.randint(300, 600)

        if self.can_see_player(player):
            self.last_seen_player = (player.grid_x, player.grid_y)
            self.memory.append(self.last_seen_player)
            self.memory = self.memory[-5:]
            self.success_rate = min(1.0, self.success_rate + self.learning_rate)
        else:
            self.success_rate = max(0.0, self.success_rate - self.learning_rate * 0.5)

        self.vision_range = 6 + int(self.success_rate * 2)
        self.aggression = 0.5 + self.success_rate * 0.5

        nearby_zombies = [z for z in all_zombies if z != self and 
                          math.sqrt((self.grid_x - z.grid_x)**2 + (self.grid_y - z.grid_y)**2) < self.alert_radius]
        if nearby_zombies and not self.group_leader:
            leader = next((z for z in nearby_zombies if z.is_leader), None)
            if leader:
                self.group_leader = leader
                if self not in leader.followers:
                    leader.followers.append(self)
            elif random.random() < 0.2:
                self.is_leader = True
                self.followers = [z for z in nearby_zombies if not z.is_leader]
                for follower in self.followers:
                    follower.group_leader = self

class ZombieManager:
    def __init__(self, world, player, sound_manager):
        self.world = world
        self.player = player
        self.sound_manager = sound_manager
        self.zombies = []
        self.spawn_timer = 0
        self.spawn_interval = 600
        self.difficulty = 0.3
        self.level = 1
        self.elapsed_time = 0
        self.font = pygame.font.SysFont(None, 48)
        self.level_popup_timer = 0
        self.popup_alpha = 255
        self.spawn_zombie()

    def adjust_difficulty(self):
        self.difficulty = min(0.7, self.difficulty + 0.005)
        self.spawn_interval = max(300, 600 - self.difficulty * 100)
        for zombie in self.zombies:
            zombie.speed = 2 + self.difficulty + (self.level * 0.05)
            zombie.vision_range = 6 + int(self.difficulty * 4)
            zombie.hearing_range = 8 + int(self.difficulty * 3)

    def spawn_zombie(self):
        while True:
            x = random.randint(0, self.world.grid_width - 1)
            y = random.randint(0, self.world.grid_height - 1)
            if (not self.world.is_safe_zone(x, y) and 
                (abs(x - self.player.grid_x) > 5 or abs(y - self.player.grid_y) > 5)):
                new_zombie = Zombie(self.world, x, y, self.sound_manager)
                self.zombies.append(new_zombie)
                break

    def update(self):
        self.adjust_difficulty()
        self.elapsed_time += 1
        if self.elapsed_time >= self.level * 1800:
            self.level += 1
            self.level_popup_timer = 180
            self.popup_alpha = 255
            print(f"Level up! Now at Level {self.level}")

        while len(self.zombies) < self.level:
            self.spawn_zombie()

        for zombie in self.zombies:
            zombie.update_ai(self.player, self.zombies)

            if zombie.update_timer <= 0:
                target = None
                if zombie.can_see_player(self.player) or zombie.can_hear_player(self.player):
                    zombie.state = ZombieState.CHASING
                    target = (self.player.grid_x, self.player.grid_y)
                    for other in self.zombies:
                        if other != zombie and abs(other.grid_x - zombie.grid_x) + abs(other.grid_y - zombie.grid_y) <= zombie.alert_radius:
                            other.state = ZombieState.ALERTED
                            other.last_seen_player = target
                elif zombie.state == ZombieState.ALERTED and zombie.last_seen_player:
                    target = zombie.last_seen_player
                elif zombie.group_leader:
                    leader = zombie.group_leader
                    player_pos = (self.player.grid_x, self.player.grid_y)
                    idx = leader.followers.index(zombie) if zombie in leader.followers else 0
                    num_followers = max(1, len(leader.followers))
                    angle_offset = (2 * math.pi / num_followers) * idx
                    radius = zombie.preferred_distance
                    jitter_angle = random.uniform(-0.3, 0.3)
                    jitter_radius = random.uniform(-0.5, 0.5)
                    angle = angle_offset + jitter_angle
                    r = radius + jitter_radius
                    offset_x = int(round(math.cos(angle) * r))
                    offset_y = int(round(math.sin(angle) * r))
                    target = (player_pos[0] + offset_x, player_pos[1] + offset_y)
                if target:
                    tx, ty = target
                    if not self.world.is_safe_zone(tx, ty):
                        zombie.path = find_path((zombie.grid_x, zombie.grid_y), (tx, ty), self.world)
                zombie.update_timer = 30

            zombie.update_timer -= 1

            # --- FIXED: Smoother movement using unit vector ---
            if zombie.path:
                next_x, next_y = zombie.path[0]
                target_px = next_x * self.world.cell_size
                target_py = next_y * self.world.cell_size
                dx = target_px - zombie.x
                dy = target_py - zombie.y
                distance = math.hypot(dx, dy)
                if distance > 1:
                    dx /= distance
                    dy /= distance
                    move_step = min(zombie.speed, distance)
                    zombie.x += dx * move_step
                    zombie.y += dy * move_step
                if math.hypot(zombie.x - target_px, zombie.y - target_py) < zombie.speed:
                    zombie.x = target_px
                    zombie.y = target_py
                    zombie.grid_x = next_x
                    zombie.grid_y = next_y
                    zombie.path.pop(0)

            zombie.update_sprite_color()

        if self.level_popup_timer > 0:
            self.level_popup_timer -= 1
            self.popup_alpha = max(0, int(255 * (self.level_popup_timer / 180)))

    def draw(self, screen):
        for zombie in self.zombies:
            screen.blit(zombie.sprite, (round(zombie.x) + 2, round(zombie.y) + 2))
            if zombie.state in [ZombieState.CHASING, ZombieState.ALERTED]:
                pygame.draw.circle(screen, (255, 255, 0, 64),
                                   (int(zombie.x + zombie.size / 2), int(zombie.y + zombie.size / 2)),
                                   int(zombie.vision_range * self.world.cell_size), 1)

        if self.level_popup_timer > 0:
            popup_text = self.font.render(f"Level Up! ", True, (255, 255, 0))
            popup_surface = pygame.Surface(popup_text.get_size(), pygame.SRCALPHA)
            popup_surface.fill((0, 0, 0, 0))
            popup_surface.blit(popup_text, (0, 0))
            popup_surface.set_alpha(self.popup_alpha)
            screen.blit(popup_surface, (screen.get_width() // 2 - popup_text.get_width() // 2, 50))

    def check_player_collision(self, player):
        for zombie in self.zombies:
            if zombie.grid_x == player.grid_x and zombie.grid_y == player.grid_y:
                print(f"Collision! Player at ({player.grid_x}, {player.grid_y}), Zombie at ({zombie.grid_x}, {zombie.grid_y})")
                self.sound_manager.play_attack()
                return True
        return False
