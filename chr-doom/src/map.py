import numpy as np
import random

class GameMap:
    def __init__(self, width=31, height=31):
        # Dimensões devem ser ímpares para o algoritmo funcionar bem (paredes nas bordas)
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.grid = self.generate_maze()
        
    def generate_maze(self):
        # Inicializa tudo como parede (1)
        maze = np.ones((self.height, self.width), dtype=int)
        
        # Algoritmo Recursive Backtracker (DFS)
        # Começa em uma célula ímpar, ímpar (dentro das bordas)
        start_x, start_y = 1, 1
        maze[start_y, start_x] = 0
        
        stack = [(start_x, start_y)]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # 2 passos para pular a parede
        
        while stack:
            x, y = stack[-1]
            # Embaralha direções
            random.shuffle(directions)
            found = False
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Verifica se está dentro dos limites (deixando 1 de borda)
                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                    if maze[ny, nx] == 1:  # Se não visitado
                        # Derruba a parede entre a atual e a próxima
                        maze[y + dy//2, x + dx//2] = 0
                        maze[ny, nx] = 0
                        stack.append((nx, ny))
                        found = True
                        break
            
            if not found:
                stack.pop()
        
        # Opcional: Adiciona alguns loops aleatórios para não ser "perfeito" demais
        self.add_loops(maze, num_loops=10)
        
        return maze
    
    def add_loops(self, maze, num_loops=10):
        """Quebra algumas paredes aleatórias para criar loops/ciclos"""
        for _ in range(num_loops):
            # Pega uma parede aleatória (coordenadas pares = paredes internas)
            wx = random.randrange(1, self.width - 1)
            wy = random.randrange(1, self.height - 1)
            if maze[wy, wx] == 1:
                # Verifica se é uma parede entre dois corredores (não borda do mapa)
                neighbors = 0
                if wy > 0 and maze[wy-1, wx] == 0: neighbors += 1
                if wy < self.height-1 and maze[wy+1, wx] == 0: neighbors += 1
                if wx > 0 and maze[wy, wx-1] == 0: neighbors += 1
                if wx < self.width-1 and maze[wy, wx+1] == 0: neighbors += 1
                if neighbors >= 2:
                    maze[wy, wx] = 0

    def get_spawn_point(self):
        """Retorna uma posição válida (chão) para o jogador nascer"""
        # Procura a partir do centro para fora
        cx, cy = self.width // 2, self.height // 2
        for radius in range(1, max(self.width, self.height)):
            for dx in range(-radius, radius+1):
                for dy in range(-radius, radius+1):
                    if abs(dx) == radius or abs(dy) == radius:
                        x, y = cx + dx, cy + dy
                        if 0 <= x < self.width and 0 <= y < self.height:
                            if self.grid[y, x] == 0:
                                return [float(x) + 0.5, float(y) + 0.5]
        # Fallback
        return [1.5, 1.5]

    def is_wall(self, x, y):
        if 0 <= int(x) < self.width and 0 <= int(y) < self.height:
            return self.grid[int(y), int(x)] == 1
        return True