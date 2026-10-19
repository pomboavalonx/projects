import pygame
import math
import random
from src.map import GameMap
from src.raycaster import Raycaster
from src.entities import Enemy, Explosion, Crosshair
from src.weapon import Weapon

def create_beep_sound():
    sample_rate = 22050
    duration = 0.1
    frequency = 800
    
    import array
    samples = array.array('h')
    max_amplitude = 32767
    
    for i in range(int(sample_rate * duration)):
        t = i / sample_rate
        value = max_amplitude * (1 if math.sin(2 * math.pi * frequency * t) > 0 else -1)
        envelope = 1.0 - (t / duration)
        samples.append(int(value * envelope * 0.3))
    
    sound = pygame.mixer.Sound(buffer=samples)
    return sound

def spawn_enemy(game_map, player_pos, min_dist=3.0):
    """Helper para spawnar um inimigo em posição válida"""
    for attempt in range(100):
        ex = random.uniform(1.5, game_map.width - 1.5)
        ey = random.uniform(1.5, game_map.height - 1.5)
        if not game_map.is_wall(ex, ey):
            if math.sqrt((ex - player_pos[0])**2 + (ey - player_pos[1])**2) > min_dist:
                return Enemy(ex, ey)
    return None

def main():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    
    sw, sh = 800, 600
    screen = pygame.display.set_mode((sw, sh))
    pygame.display.set_caption("chr$doom - ASCII Raycaster")
    clock = pygame.time.Clock()

    shoot_sound = create_beep_sound()

    game_map = GameMap(31, 31)
    player_pos = game_map.get_spawn_point()
    player_angle = 0.0
    
    raycaster = Raycaster(sw, sh, game_map)
    weapon = Weapon(sw, sh)
    crosshair = Crosshair(sw, sh)
    
    # Inimigos iniciais
    enemies = []
    for _ in range(5):
        enemy = spawn_enemy(game_map, player_pos)
        if enemy:
            enemies.append(enemy)
    
    explosions = []
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    weapon.is_firing = True
                    weapon.fire_timer = 10
                    shoot_sound.play()
                    
                    # Verifica acertos - inimigo respawn em vez de morrer
                    for enemy in enemies:
                        if enemy.alive and enemy.check_hit(player_pos, player_angle):
                            # Calcula posição na tela para explosão
                            dx = enemy.pos[0] - player_pos[0]
                            dy = enemy.pos[1] - player_pos[1]
                            enemy_angle = math.atan2(dy, dx)
                            rel_angle = enemy_angle - player_angle
                            while rel_angle > math.pi: rel_angle -= 2 * math.pi
                            while rel_angle < -math.pi: rel_angle += 2 * math.pi
                            
                            screen_x = (0.5 * (rel_angle / (math.pi / 6)) + 0.5) * sw
                            screen_y = sh // 2
                            
                            explosions.append(Explosion(enemy.pos[0], enemy.pos[1], screen_x, screen_y))
                            enemy.respawn(game_map)  # RESPAWN!
                            break  # Um tiro = um acerto

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: player_angle -= 0.05
        if keys[pygame.K_RIGHT] or keys[pygame.K_e]: player_angle += 0.05
        
        move_step = 0.05
        move_forward = keys[pygame.K_w] or keys[pygame.K_UP]
        move_backward = keys[pygame.K_s] or keys[pygame.K_DOWN]
        
        if move_forward:
            new_x = player_pos[0] + math.cos(player_angle) * move_step
            new_y = player_pos[1] + math.sin(player_angle) * move_step
            if not raycaster.map.is_wall(new_x, player_pos[1]): player_pos[0] = new_x
            if not raycaster.map.is_wall(player_pos[0], new_y): player_pos[1] = new_y
        if move_backward:
            new_x = player_pos[0] - math.cos(player_angle) * move_step
            new_y = player_pos[1] - math.sin(player_angle) * move_step
            if not raycaster.map.is_wall(new_x, player_pos[1]): player_pos[0] = new_x
            if not raycaster.map.is_wall(player_pos[0], new_y): player_pos[1] = new_y

        # Update inimigos (movimento + verificação de bounds)
        for enemy in enemies:
            enemy.update(game_map)
        
        # Update explosões
        for explosion in explosions[:]:
            explosion.update()
            if explosion.is_dead():
                explosions.remove(explosion)

        weapon.update()
        
        # Render
        raycaster.render(screen, player_pos, player_angle)
        for enemy in enemies:
            enemy.render(screen, player_pos, player_angle, sw, sh, game_map)
        for explosion in explosions:
            explosion.render(screen)
        weapon.render(screen)
        crosshair.render(screen)  # MIRA CENTRAL
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()