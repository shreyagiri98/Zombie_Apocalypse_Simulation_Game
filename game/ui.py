
# import pygame
# import math
# import random

# class UI:
#     def __init__(self, screen):
#         self.screen = screen
#         pygame.font.init()
#         self.font = pygame.font.Font(pygame.font.match_font('verdana', bold=True), 24)
#         self.large_font = pygame.font.Font(pygame.font.match_font('verdana', bold=True), 48)
#         self.pulse_value = 0
#         self.pulse_direction = 1
#         self.show_run_alert = False
#         self.run_alert_timer = 0

#         # Colors
#         self.WHITE = (255, 255, 255)
#         self.BRIGHT_RED = (255, 80, 100)
#         self.BRIGHT_GREEN = (80, 255, 160)
#         self.BRIGHT_BLUE = (120, 200, 255)
#         self.SUNNY_YELLOW = (255, 235, 100)
#         self.SOFT_PURPLE = (200, 150, 255)
#         self.NEON_PINK = (255, 100, 200)
#         self.GAME_OVER_BG = (30, 30, 50, 220)

#         # Overlay
#         self.overlay = pygame.Surface((screen.get_width(), 80), pygame.SRCALPHA)
#         for i in range(80):
#             alpha = int(90 * (1 - i / 80))
#             pygame.draw.line(self.overlay, (255, 255, 255, alpha), (0, i), (screen.get_width(), i))

#         # Sparkles
#         self.sparkles = [(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())) for _ in range(30)]

#         # Point blinking
#         self.point_colors = [
#             (255, 235, 100),  # Yellow
#             (255, 150, 150),  # Pinkish
#             (150, 255, 200),  # Aqua
#             (200, 150, 255),  # Purple
#             (255, 255, 180),  # Pale Yellow
#         ]
#         self.color_index = 0
#         self.color_timer = 0

#     def draw_rounded_rect(self, surface, color, rect, radius=10):
#         pygame.draw.rect(surface, color, rect, border_radius=radius)

#     def trigger_run_alert(self):
#         self.show_run_alert = True
#         self.run_alert_timer = 30

#     def draw_points(self, point_positions, point_values):
#         self.color_timer += 1
#         if self.color_timer % 10 == 0:
#             self.color_index = (self.color_index + 1) % len(self.point_colors)

#         for (x, y), value in zip(point_positions, point_values):
#             pygame.draw.rect(self.screen, self.point_colors[self.color_index], (x, y, 20, 20), border_radius=6)
#             label = self.font.render(f"+{value}", True, self.BRIGHT_BLUE)
#             self.screen.blit(label, (x + 2, y - 22))

#     def draw(self, score, health, survival_time=0, in_safe_zone=False):
#         self.screen.blit(self.overlay, (0, 0))

#         # Sparkles
#         for x, y in self.sparkles:
#             sparkle_color = random.choice([self.BRIGHT_BLUE, self.SOFT_PURPLE, self.SUNNY_YELLOW])
#             pygame.draw.circle(self.screen, sparkle_color, (x, y), 2)

#         # Score
#         score_text = self.font.render(f"Score: {score}", True, self.SUNNY_YELLOW)
#         # self.draw_rounded_rect(self.screen, self.SOFT_PURPL, (10, 10, 170, 40), 10)
#         self.screen.blit(score_text, (20, 20))

       

#         # Time
#         time_text = self.font.render(f"Time: {survival_time}s", True, self.BRIGHT_GREEN)
#         self.screen.blit(time_text, (self.screen.get_width() - 200, 20))

#         # Safe Zone
#         if in_safe_zone:
#             self.pulse_value += self.pulse_direction * 6
#             if self.pulse_value >= 255 or self.pulse_value <= 0:
#                 self.pulse_direction *= -1
#             pulse_color = (self.BRIGHT_GREEN[0], self.BRIGHT_GREEN[1], self.BRIGHT_GREEN[2], self.pulse_value)
#             safe_text = self.large_font.render("SAFE ZONE!", True, pulse_color[:3])
#             text_rect = safe_text.get_rect(center=(self.screen.get_width() // 2, 50))
#             self.screen.blit(safe_text, text_rect)

#         # # Run Alert
#         # if self.show_run_alert:
#         #     if self.run_alert_timer > 0:
#         #         run_text = self.large_font.render("RUN FAST!", True, self.NEON_PINK)
#         #         text_rect = run_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
#         #         self.screen.blit(run_text, text_rect)
#         #         self.run_alert_timer -= 1
#         #     else:
#         #         self.show_run_alert = False

#     def draw_pause_menu(self):
#         pause_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
#         pause_overlay.fill((240, 240, 255, 180))
#         self.screen.blit(pause_overlay, (0, 0))

#         text = self.large_font.render("PAUSED", True, self.SOFT_PURPLE)
#         text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
#         self.screen.blit(text, text_rect)

#         resume_text = self.font.render("Press 'P' to Resume", True, self.SUNNY_YELLOW)
#         quit_text = self.font.render("Press 'Q' to Quit", True, self.BRIGHT_RED)
#         self.screen.blit(resume_text, (self.screen.get_width() // 2 - 120, self.screen.get_height() // 2))
#         self.screen.blit(quit_text, (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 40))

#     def draw_game_over(self, final_score, survival_time):
#         game_over_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
#         game_over_overlay.fill(self.GAME_OVER_BG)
#         self.screen.blit(game_over_overlay, (0, 0))

#         # "GAME OVER" text
#         text = self.large_font.render("GAME OVER", True, self.NEON_PINK)
#         text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
#         self.screen.blit(text, text_rect)

#         # Final Score
#         score_text = self.font.render(f"Final Score: {final_score}", True, self.SUNNY_YELLOW)
#         score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
#         self.screen.blit(score_text, score_rect)

#         # Survived Time
#         time_text = self.font.render(f"Survived: {survival_time}s", True, self.BRIGHT_BLUE)
#         time_rect = time_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 10))
#         self.screen.blit(time_text, time_rect)

#         # "Press R to Restart"
#         restart_text = self.font.render("Press 'R' to Restart", True, self.BRIGHT_GREEN)
#         restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 70))
#         self.screen.blit(restart_text, restart_rect)

#         # "Press Q to Quit"
#         quit_text = self.font.render("Press 'Q' to Quit", True, self.BRIGHT_RED)
#         quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 110))
#         self.screen.blit(quit_text, quit_rect)


# # Helper function to check zombie proximity
# def check_zombie_proximity(player_pos, zombie_pos, ui):
#     dx = player_pos[0] - zombie_pos[0]
#     dy = player_pos[1] - zombie_pos[1]
#     distance = math.sqrt(dx * dx + dy * dy)
#     if distance <= 1:
#         ui.trigger_run_alert()
import pygame
import math
import random

class UI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(
            pygame.font.match_font('verdana', bold=True), 24
        )
        self.large_font = pygame.font.Font(
            pygame.font.match_font('verdana', bold=True), 48
        )
        self.pulse_value = 0
        self.pulse_direction = 1
        self.show_run_alert = False
        self.run_alert_timer = 0

        # Colors
        self.WHITE = (255, 255, 255)
        self.BRIGHT_RED = (255, 80, 100)
        self.BRIGHT_GREEN = (80, 255, 160)
        self.BRIGHT_BLUE = (120, 200, 255)
        self.SUNNY_YELLOW = (255, 235, 100)
        self.SOFT_PURPLE = (200, 150, 255)
        self.NEON_PINK = (255, 100, 200)
        self.GAME_OVER_BG = (30, 30, 50, 220)

        # Overlay
        self.overlay = pygame.Surface((screen.get_width(), 80), pygame.SRCALPHA)
        for i in range(80):
            alpha = int(90 * (1 - i / 80))
            pygame.draw.line(
                self.overlay,
                (255, 255, 255, alpha),
                (0, i),
                (screen.get_width(), i)
            )

        # Sparkles
        self.sparkles = [
            (random.randint(0, screen.get_width()),
             random.randint(0, screen.get_height()))
            for _ in range(30)
        ]

        # Point blinking colors
        self.point_colors = [
            (255, 235, 100),  # Yellow
            (255, 150, 150),  # Pinkish
            (150, 255, 200),  # Aqua
            (200, 150, 255),  # Purple
            (255, 255, 180),  # Pale Yellow
        ]
        self.color_index = 0
        self.color_timer = 0

    def draw_rounded_rect(self, surface, color, rect, radius=10):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def trigger_run_alert(self):
        self.show_run_alert = True
        self.run_alert_timer = 30

    def draw_points(self, point_positions, point_values):
        self.color_timer += 1
        if self.color_timer % 10 == 0:
            self.color_index = (self.color_index + 1) % len(self.point_colors)

        for (x, y), value in zip(point_positions, point_values):
            pygame.draw.rect(
                self.screen,
                self.point_colors[self.color_index],
                (x, y, 20, 20),
                border_radius=6
            )
            label = self.font.render(f"+{value}", True, self.BRIGHT_BLUE)
            self.screen.blit(label, (x + 2, y - 22))

    def draw(self,
             score,
             health,
             survival_time=0,
             in_safe_zone=False,
             stamina=0,
             max_stamina=100):
        # 1) Base overlay & sparkles
        self.screen.blit(self.overlay, (0, 0))
        for x, y in self.sparkles:
            sparkle_color = random.choice(
                [self.BRIGHT_BLUE, self.SOFT_PURPLE, self.SUNNY_YELLOW]
            )
            pygame.draw.circle(self.screen, sparkle_color, (x, y), 2)

        # 2) Score
        score_text = self.font.render(f"Score: {score}", True, self.SUNNY_YELLOW)
        self.screen.blit(score_text, (20, 20))

        # 3) Stamina Bar
        bar_x, bar_y = 20, 60
        bar_w, bar_h = 200, 15
        pct = max(0, min(1, stamina / max_stamina))

        # background
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            (bar_x, bar_y, bar_w, bar_h),
            border_radius=4
        )
        # fill
        fill_w = int(bar_w * pct)
        pygame.draw.rect(
            self.screen,
            self.BRIGHT_GREEN,
            (bar_x, bar_y, fill_w, bar_h),
            border_radius=4
        )
        # border
        pygame.draw.rect(
            self.screen,
            self.WHITE,
            (bar_x, bar_y, bar_w, bar_h),
            2,
            border_radius=4
        )
        # # numeric
        # stam_txt = self.font.render(
        #     f"Stamina: {int(stamina)}/{max_stamina}", True, self.WHITE
        # )
        # self.screen.blit(stam_txt, (bar_x, bar_y - stam_txt.get_height() - 2))

        # 4) Survival Time
        time_text = self.font.render(f"Time: {survival_time}s", True, self.BRIGHT_GREEN)
        self.screen.blit(time_text, (self.screen.get_width() - 200, 20))

        # 5) Safe Zone Pulse
        if in_safe_zone:
            self.pulse_value += self.pulse_direction * 6
            if self.pulse_value >= 255 or self.pulse_value <= 0:
                self.pulse_direction *= -1
            pulse_col = (
                self.BRIGHT_GREEN[0],
                self.BRIGHT_GREEN[1],
                self.BRIGHT_GREEN[2],
                self.pulse_value
            )
            safe_text = self.large_font.render("SAFE ZONE!", True, pulse_col[:3])
            text_rect = safe_text.get_rect(
                center=(self.screen.get_width() // 2, 50)
            )
            self.screen.blit(safe_text, text_rect)

        # 6) Run Alert
        if self.show_run_alert:
            if self.run_alert_timer > 0:
                run_text = self.large_font.render("RUN FAST!", True, self.NEON_PINK)
                text_rect = run_text.get_rect(
                    center=(
                        self.screen.get_width() // 2,
                        self.screen.get_height() // 2 - 100
                    )
                )
                self.screen.blit(run_text, text_rect)
                self.run_alert_timer -= 1
            else:
                self.show_run_alert = False

    def draw_pause_menu(self):
        pause_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pause_overlay.fill((240, 240, 255, 180))
        self.screen.blit(pause_overlay, (0, 0))

        text = self.large_font.render("PAUSED", True, self.SOFT_PURPLE)
        text_rect = text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)
        )
        self.screen.blit(text, text_rect)

        resume_text = self.font.render("Press 'P' to Resume", True, self.SUNNY_YELLOW)
        quit_text = self.font.render("Press 'Q' to Quit", True, self.BRIGHT_RED)
        self.screen.blit(
            resume_text,
            (self.screen.get_width() // 2 - 120, self.screen.get_height() // 2)
        )
        self.screen.blit(
            quit_text,
            (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 40)
        )

    def draw_game_over(self, final_score, survival_time):
        game_over_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        game_over_overlay.fill(self.GAME_OVER_BG)
        self.screen.blit(game_over_overlay, (0, 0))

        # GAME OVER
        text = self.large_font.render("GAME OVER", True, self.NEON_PINK)
        text_rect = text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100)
        )
        self.screen.blit(text, text_rect)

        # Final Score
        score_text = self.font.render(
            f"Final Score: {final_score}", True, self.SUNNY_YELLOW
        )
        score_rect = score_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30)
        )
        self.screen.blit(score_text, score_rect)

        # Survived Time
        time_text = self.font.render(
            f"Survived: {survival_time}s", True, self.BRIGHT_BLUE
        )
        time_rect = time_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 10)
        )
        self.screen.blit(time_text, time_rect)

        # Restart/Quit prompts
        restart_text = self.font.render("Press 'R' to Restart", True, self.BRIGHT_GREEN)
        restart_rect = restart_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 70)
        )
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font.render("Press 'Q' to Quit", True, self.BRIGHT_RED)
        quit_rect = quit_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 110)
        )
        self.screen.blit(quit_text, quit_rect)
