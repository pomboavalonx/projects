import pygame
import numpy as np
import math
from .map import GameMap

class Raycaster:
    def __init__(self, screen_width, screen_height, game_map):
        self.sw = screen_width
        self.sh = screen_height
        self.fov = math.pi / 3
        self.map = game_map

    def render(self, screen, player_pos, player_angle):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (20, 20, 20), (0, self.sh // 2, self.sw, self.sh // 2))
        start_angle = player_angle - self.fov / 2
        for x in range(0, self.sw, 2):
            ray_angle = start_angle + (x / self.sw) * self.fov
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            dist = 0
            while dist < 20:
                dist += 0.1
                test_x = player_pos[0] + cos_a * dist
                test_y = player_pos[1] + sin_a * dist
                if self.map.is_wall(test_x, test_y):
                    break
            dist = dist * math.cos(ray_angle - player_angle)
            wall_height = min(self.sh, (self.sh / (dist + 0.0001)))
            color_val = max(0, min(255, int(200 - (dist * 20))))
            color = (0, color_val, 0)
            # Parede preta com grade verde (Wireframe/Grid style)
            wall_top = (self.sh - wall_height) // 2
            wall_bottom = (self.sh + wall_height) // 2
            slice_width = 2  # Largura da fatia = passo do loop (2px)
            
            # 1. Corpo da parede (Preto Sólido)
            pygame.draw.rect(screen, (0, 0, 0), (x, wall_top, slice_width, wall_height))
            
            # 2. Grade Verde: Linhas horizontais no topo e base da fatia
            # Verde neon brilhante (estilo Tron/Terminal)
            grid_color = (0, 255, 0)  # Verde puro, máximo brilho
            pygame.draw.line(screen, grid_color, (x, wall_top), (x + slice_width, wall_top), 1)
            pygame.draw.line(screen, grid_color, (x, wall_bottom), (x + slice_width, wall_bottom), 1)
