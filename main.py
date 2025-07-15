import pygame
import sys
from game.world import World
from game.player import Player
from game.zombie import ZombieManager
from game.resources import ResourceManager
from game.ui import UI
from game.sound import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.WINDOW_SIZE = (800, 600)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Zombie Apocalypse")

        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game components
        self.world = World(20, 15)  # 20x15 grid
        self.sound_manager = SoundManager()
        self.player = Player(self.world)
        self.zombie_manager = ZombieManager(self.world, self.player, self.sound_manager)
        self.resource_manager = ResourceManager(self.world)
        self.ui = UI(self.screen)

        # Game state
        self.score = 0
        self.survival_time = 0  # Time survived in seconds
        self.game_over = False

        # Initialize real-world clock
        self.start_time = pygame.time.get_ticks()  # Get the current time when the game starts

        self.current_level = 1
        self.last_level_up_time = 0  # Time in seconds when last level-up happened

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.__init__()  # Restart the game

        if not self.game_over:
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)

    def update(self):
        if not self.game_over:
            # Get the elapsed time in seconds
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert milliseconds to seconds
            self.survival_time = int(elapsed_time)  # Set survival time to the number of seconds passed

            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.zombie_manager.update()
            self.resource_manager.update()

            # # Update score but prevent gain in safe zones
            # if self.survival_time % 60 == 0 and not self.world.is_safe_zone(self.player.grid_x, self.player.grid_y):
            #     self.score += 1  # Increase score if NOT in a safe zone

       
        
            # Check if player collides with a zombie
            if self.zombie_manager.check_player_collision(self.player):
                self.game_over = True

            # Check if player collects a resource
            collected_points = self.resource_manager.check_collection(self.player)
            if collected_points > 0:
    # Increase score based on collected points
               self.score += collected_points  # Increase score by the collected points per resource

    # Show floating text based on collected points
               self.player.floating_text = f"+{collected_points}"  # Show floating text with collected points
               self.player.text_timer = 30  # Display for 30 frames
               
            # # Give bonus points for being in dangerous areas
            # if not self.world.is_safe_zone(self.player.grid_x, self.player.grid_y):
            #     if self.survival_time % 30 == 0:  # Every 30 seconds
            #         self.score += 2  # Bonus points for staying in danger

        # In your main game update loop, after certain conditions:
                    # Level up every 30 seconds
        if self.survival_time - self.last_level_up_time >= 30:
            self.current_level += 1
            self.last_level_up_time = self.survival_time
            self.resource_manager.level_up()
    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw game world
        self.world.draw(self.screen)
        self.resource_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.zombie_manager.draw(self.screen)

        # Draw UI with additional information
        self.ui.draw(
    score=self.score,
    health=self.player.health,
    survival_time=self.survival_time,
    in_safe_zone=self.world.is_safe_zone(self.player.grid_x, self.player.grid_y),
    stamina=self.player.stamina,
    max_stamina=self.player.max_stamina
)


        if self.game_over:
            self.ui.draw_game_over(self.score, self.survival_time)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Keep frame rate at 60 FPS

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
