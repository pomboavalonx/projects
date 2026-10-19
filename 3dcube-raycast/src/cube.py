"""cube.py
Definição da geometria do cubo e suas arestas.
"""
import numpy as np

# Vertices do cubo centrado na origem, tamanho 2 (de -1 a 1)
VERTICES = np.array([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1],
], dtype=float)

# Cada aresta é um par de índices de VERTICES
EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # base inferior
    (4, 5), (5, 6), (6, 7), (7, 4),  # base superior
    (0, 4), (1, 5), (2, 6), (3, 7)   # laterais
]
