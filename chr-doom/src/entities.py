import pygame
import math
import random

class Enemy:
    SPRITE_LINES = [
        " ||  || ",
        " \\\\()// ",
        "//(__)\\\\",
        "||    ||"
    ]

    def __init__(self, x, y):
        self.pos = [x, y]
        self.move_timer = 0
        self.move_delay = random.randint(60, 120)
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.alive = True

    def update(self, game_map):
        if not self.alive:
            return
            
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.move_delay = random.randint(60, 120)
            
            new_x = self.pos[0] + self.direction[0] * 0.5
            new_y = self.pos[1] + self.direction[1] * 0.5
            
            if not game_map.is_wall(new_x, self.pos[1]) and not game_map.is_wall(self.pos[0], new_y):
                self.pos[0] = new_x
                self.pos[1] = new_y
            else:
                self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        
        # Verifica se saiu dos limites do mapa (fora das bordas)
        if (self.pos[0] <= 0 or self.pos[0] >= game_map.width - 1 or 
            self.pos[1] <= 0 or self.pos[1] >= game_map.height - 1):
            self.respawn(game_map)

    def respawn(self, game_map):
        """Respawn em posição válida aleatória longe do centro"""
        for attempt in range(100):
            ex = random.uniform(1.5, game_map.width - 1.5)
            ey = random.uniform(1.5, game_map.height - 1.5)
            if not game_map.is_wall(ex, ey):
                self.pos = [ex, ey]
                self.alive = True
                self.move_timer = 0
                self.move_delay = random.randint(60, 120)
                self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                break

    def render(self, screen, player_pos, player_angle, sw, sh, game_map):
        if not self.alive:
            return
            
        dx = self.pos[0] - player_pos[0]
        dy = self.pos[1] - player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        enemy_angle = math.atan2(dy, dx)
        rel_angle = enemy_angle - player_angle
        while rel_angle > math.pi: rel_angle -= 2 * math.pi
        while rel_angle < -math.pi: rel_angle += 2 * math.pi
        
        if abs(rel_angle) >= math.pi / 6:
            return
            
        sin_a = math.sin(enemy_angle)
        cos_a = math.cos(enemy_angle)
        check_dist = 0
        hit_wall = False
        while check_dist < dist:
            check_dist += 0.1
            test_x = player_pos[0] + cos_a * check_dist
            test_y = player_pos[1] + sin_a * check_dist
            if game_map.is_wall(test_x, test_y):
                hit_wall = True
                break
        
        if hit_wall:
            return
        
        screen_x = (0.5 * (rel_angle / (math.pi / 6)) + 0.5) * sw
        font_size = max(8, int(800 / (dist + 0.1)))
        font = pygame.font.SysFont("monospace", font_size, bold=True)
        
        brightness = max(100, min(255, int(255 - (dist * 15))))
        color = (brightness, brightness, 0)
        
        line_height = font_size
        total_height = len(self.SPRITE_LINES) * line_height
        start_y = (sh // 2) - (total_height // 2)
        
        for i, line in enumerate(self.SPRITE_LINES):
            text_surf = font.render(line, True, color)
            text_rect = text_surf.get_rect(center=(screen_x, start_y + i * line_height + line_height // 2))
            screen.blit(text_surf, text_rect)

    def check_hit(self, player_pos, player_angle):
        dx = self.pos[0] - player_pos[0]
        dy = self.pos[1] - player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        enemy_angle = math.atan2(dy, dx)
        rel_angle = enemy_angle - player_angle
        while rel_angle > math.pi: rel_angle -= 2 * math.pi
        while rel_angle < -math.pi: rel_angle += 2 * math.pi
        if abs(rel_angle) < 0.1:
            return True
        return False


class Explosion:
    """Sistema de partículas para explosão em pixels vermelhos GRANDES"""
    def __init__(self, x, y, screen_x, screen_y):
        self.particles = []
        self.lifetime = 40  # frames (mais tempo)
        self.screen_x = screen_x
        self.screen_y = screen_y
        
        # Cria 50-80 partículas MAIORES
        for _ in range(random.randint(50, 80)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)  # Mais rápido
            size = random.randint(6, 14)  # MUITO MAIOR (era 2-5)
            self.particles.append({
                'x': screen_x,
                'y': screen_y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size,
                'color': (255, random.randint(0, 150), 0),
                'life': self.lifetime
            })
    
    def update(self):
        self.lifetime -= 1
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.15  # Gravidade um pouco mais forte
            p['life'] -= 1
            fade = p['life'] / 40.0
            p['color'] = (int(255 * fade), int(100 * fade), 0)
            # Partículas encolhem conforme morrem
            p['size'] = max(1, int(p['size'] * fade))
        self.particles = [p for p in self.particles if p['life'] > 0]
    
    def render(self, screen):
        for p in self.particles:
            pygame.draw.rect(screen, p['color'], 
                           (int(p['x']), int(p['y']), p['size'], p['size']))
    
    def is_dead(self):
        return len(self.particles) == 0


class Crosshair:
    """Mira central estilo ASCII"""
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
    
    def render(self, screen):
        cx, cy = self.sw // 2, self.sh // 2
        color = (0, 255, 0)  # Verde neon
        gap = 8
        length = 12
        thickness = 2
        
        # Linhas horizontais
        pygame.draw.line(screen, color, (cx - gap - length, cy), (cx - gap, cy), thickness)
        pygame.draw.line(screen, color, (cx + gap, cy), (cx + gap + length, cy), thickness)
        
        # Linhas verticais
        pygame.draw.line(screen, color, (cx, cy - gap - length), (cx, cy - gap), thickness)
        pygame.draw.line(screen, color, (cx, cy + gap), (cx, cy + gap + length), thickness)
        
        # Ponto central
        pygame.draw.rect(screen, color, (cx - 1, cy - 1, 3, 3))