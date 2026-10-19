"""raycaster.py
Funções de rotação e projeção (raycasting simplificado) para o cubo.
"""
import numpy as np
import math

def rotation_matrix(angle_x: float, angle_y: float) -> np.ndarray:
    """Retorna matriz de rotação 3x3 para ângulos em radianos.
    Rotação em X seguida de rotação em Y.
    """
    cx, sx = math.cos(angle_x), math.sin(angle_x)
    cy, sy = math.cos(angle_y), math.sin(angle_y)
    # Rotação X
    Rx = np.array([
        [1, 0, 0],
        [0, cx, -sx],
        [0, sx, cx]
    ])
    # Rotação Y
    Ry = np.array([
        [cy, 0, sy],
        [0, 1, 0],
        [-sy, 0, cy]
    ])
    return Ry @ Rx

def project(points: np.ndarray, fov: float, viewer_distance: float) -> np.ndarray:
    """Projeta pontos 3D (Nx3) em 2D (Nx2) usando perspectiva.
    fov: campo de visão em graus.
    viewer_distance: distância da câmera ao plano de projeção.
    """
    # Conversão de fov para fator de escala
    f = viewer_distance * math.tan(math.radians(fov) / 2)
    # Evita divisão por zero
    z = points[:, 2] + viewer_distance
    factor = f / z
    x = points[:, 0] * factor
    y = points[:, 1] * factor
    return np.column_stack((x, y))
