
import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds_enabled = True
        
        try:
            # Load sounds if they exist
            self.zombie_groan = self.load_sound('assets/zombie_groan.wav')
            self.zombie_alert = self.load_sound('assets/zombie_alert.wav')
            self.zombie_attack = self.load_sound('assets/zombie_attack.wav')
        except:
            print("Warning: Sound files not found. Game will run without sound.")
            self.sounds_enabled = False
    
    def load_sound(self, path):
        if os.path.exists(path):
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0.4)
            return sound
        return None
        
    def play_groan(self):
        if self.sounds_enabled and hasattr(self, 'zombie_groan') and self.zombie_groan:
            self.zombie_groan.play()
        
    def play_alert(self):
        if self.sounds_enabled and hasattr(self, 'zombie_alert') and self.zombie_alert:
            self.zombie_alert.play()
        
    def play_attack(self):
        if self.sounds_enabled and hasattr(self, 'zombie_attack') and self.zombie_attack:
            self.zombie_attack.play()
