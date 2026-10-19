import pygame
import math

class Weapon:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        self.is_firing = False
        self.fire_timer = 0
        self.weapon_char = "||[=]"

    def update(self):
        if self.is_firing:
            self.fire_timer -= 1
            if self.fire_timer <= 0:
                self.is_firing = False

    def render(self, screen):
        color = (0, 150, 0) if not self.is_firing else (255, 255, 255)
        font_size = 50 if not self.is_firing else 60
        font = pygame.font.SysFont("monospace", font_size, bold=True)
        offset_y = 0 if not self.is_firing else 20
        text_surf = font.render(self.weapon_char, True, color)
        text_rect = text_surf.get_rect(center=(self.sw // 2, self.sh - 50 + offset_y))
        screen.blit(text_surf, text_rect)
