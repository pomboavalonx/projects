"""main.py
Pygame loop que renderiza um cubo wireframe 3D giratório usando raycasting simplificado.
"""
import sys
import math
import pygame
import numpy as np

from cube import VERTICES, EDGES
from raycaster import rotation_matrix, project

# Configurações da janela
WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Parâmetros de projeção
FOV = 60  # graus
BASE_DISTANCE = 5.0
AMPLITUDE = 2.0
zoom_phase = 0.0

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Wireframe Cube - Raycasting")
clock = pygame.time.Clock()

# Angulos de rotação iniciais
angle_x = 0.0
angle_y = 0.0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Atualiza ângulos (rad/s)
    dt = clock.get_time() / 1000.0  # delta time em segundos
    angle_x += math.radians(30) * dt  # 30°/s em X
    angle_y += math.radians(20) * dt  # 20°/s em Y
    # Atualiza fase de zoom (oscila entre -π/2 e π/2)
    zoom_phase += math.radians(90) * dt  # 90°/s de fase
    # Mantém fase dentro de 0..2π
    zoom_phase %= 2 * math.pi
    # Rotaciona vértices
    rot = rotation_matrix(angle_x, angle_y)
    rotated_vertices = VERTICES @ rot.T  # (8,3)

    # Projeta para 2D
    viewer_distance = BASE_DISTANCE + AMPLITUDE * math.sin(zoom_phase)
    projected = project(rotated_vertices, FOV, viewer_distance)
    # Converte para coordenadas da tela
    points_2d = []
    for x, y in projected:
        sx = int(x * WIDTH / 2) + CENTER_X
        sy = int(-y * HEIGHT / 2) + CENTER_Y  # y invertido (pygame y cresce para baixo)
        points_2d.append((sx, sy))

    # Desenha
    screen.fill((0, 0, 0))  # fundo preto
    # Desenha arestas
    for start, end in EDGES:
        pygame.draw.line(screen, (255, 255, 255), points_2d[start], points_2d[end], 2)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit()
