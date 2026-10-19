import pygame
import random
import math
import os

# --- Configurações Iniciais ---
pygame.init()
pygame.mixer.init() # Inicializa o sistema de som

# Tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders - Nebula Edition")

# Cores (Cyberpunk Palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

# --- Gestão de Áudio ---
def load_sound(file_name):
    path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    else:
        print(f"⚠️ Aviso: Arquivo de som {file_name} não encontrado. O jogo rodará em silêncio.")
        return None

# Carregando sons (Você precisa colocar esses arquivos na pasta ~/invaders/)
snd_laser = load_sound("laser.wav")
snd_explosion = load_sound("explosion.wav")

# --- Classes do Jogo ---

class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 60
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, CYAN, self.rect)
        pygame.draw.rect(screen, CYAN, (self.rect.x + 20, self.rect.y - 10, 10, 10))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -7
        self.rect = pygame.Rect(x, y, 5, 15)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Alien:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direction = 1

    def update(self, speed):
        self.rect.x += speed * self.direction

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)
        pygame.draw.rect(screen, BLACK, (self.rect.x + 8, self.rect.y + 8, 5, 5))
        pygame.draw.rect(screen, BLACK, (self.rect.x + 27, self.rect.y + 8, 5, 5))

# --- Lógica Principal ---

def main():
    player = Player()
    bullets = []
    aliens = []
    
    alien_rows = 5
    alien_cols = 10
    alien_width = 50
    alien_height = 40
    for row in range(alien_rows):
        for col in range(alien_cols):
            aliens.append(Alien(col * alien_width + 50, row * alien_height + 50))

    alien_speed = 2
    score = 0
    font = pygame.font.SysFont("monospace", 25, bold=True)
    game_over = False

    running = True
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.rect.centerx - 2, player.rect.top))
                    if snd_laser: snd_laser.play() # Som de tiro

        if not game_over:
            player.move(keys)

            for bullet in bullets[:]:
                bullet.update()
                if bullet.rect.bottom < 0:
                    bullets.remove(bullet)

            move_down = False
            for alien in aliens:
                alien.update(alien_speed)
                if alien.rect.right >= WIDTH or alien.rect.left <= 0:
                    move_down = True
            
            if move_down:
                alien_speed *= -1.1
                for alien in aliens:
                    alien.rect.y += 10

            for bullet in bullets[:]:
                for alien in aliens[:]:
                    if bullet.rect.colliderect(alien.rect):
                        if snd_explosion: snd_explosion.play() # Som de explosão
                        bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 10
                        break

            for alien in aliens:
                if alien.rect.colliderect(player.rect) or alien.rect.bottom >= player.rect.top:
                    game_over = True

            if not aliens:
                game_over = True

        player.draw()
        for bullet in bullets: bullet.draw()
        for alien in aliens: alien.draw()

        score_text = font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            msg = "GAME OVER" if aliens else "YOU WIN!"
            end_text = font.render(msg, True, RED)
            screen.blit(end_text, (WIDTH//2 - 80, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
