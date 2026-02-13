import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_RED = (139, 0, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.angle = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.3
        self.rotation_speed = 4
        self.health = 100
        self.max_health = 100
        self.score = 0
        
    def update(self, keys):
        # Rotation
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.rotation_speed
            
        # Acceleration
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        else:
            # Friction
            if self.speed > 0:
                self.speed = max(0, self.speed - 0.1)
            elif self.speed < 0:
                self.speed = min(0, self.speed + 0.1)
        
        # Move in direction of angle
        rad = math.radians(self.angle)
        self.x += self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)
        
        # Keep player on screen
        self.x = max(self.width/2, min(SCREEN_WIDTH - self.width/2, self.x))
        self.y = max(self.height/2, min(SCREEN_HEIGHT - self.height/2, self.y))
    
    def draw(self, screen):
        # Create jeep shape
        points = [
            (-self.width/2, -self.height/2),
            (self.width/2, -self.height/2),
            (self.width/3, self.height/2),
            (-self.width/3, self.height/2)
        ]
        
        # Rotate points
        rotated_points = []
        rad = math.radians(self.angle)
        for px, py in points:
            rx = px * math.cos(rad) - py * math.sin(rad)
            ry = px * math.sin(rad) + py * math.cos(rad)
            rotated_points.append((self.x + rx, self.y + ry))
        
        # Draw jeep body
        pygame.draw.polygon(screen, DARK_GREEN, rotated_points)
        pygame.draw.polygon(screen, BLACK, rotated_points, 2)
        
        # Draw gun turret
        gun_length = 30
        gun_x = self.x + gun_length * math.sin(rad)
        gun_y = self.y - gun_length * math.cos(rad)
        pygame.draw.line(screen, GRAY, (self.x, self.y), (gun_x, gun_y), 5)
        
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = random.uniform(0.8, 1.5)
        self.health = 50
        self.max_health = 50
        self.damage = 10
        self.attack_cooldown = 0
        
    def update(self, player):
        # Move towards player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        
        # Attack player if close enough
        if dist < 40:
            if self.attack_cooldown <= 0:
                player.take_damage(self.damage)
                self.attack_cooldown = 60  # 1 second cooldown
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
    def draw(self, screen):
        # Draw zombie body
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.width//2)
        pygame.draw.circle(screen, DARK_GREEN, (int(self.x), int(self.y)), self.width//2, 2)
        
        # Draw eyes
        eye_offset = 8
        pygame.draw.circle(screen, RED, (int(self.x - eye_offset), int(self.y - 5)), 4)
        pygame.draw.circle(screen, RED, (int(self.x + eye_offset), int(self.y - 5)), 4)
        
        # Draw health bar
        bar_width = self.width
        bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - bar_width/2, self.y - self.height, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x - bar_width/2, self.y - self.height, bar_width * health_ratio, bar_height))
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = angle
        self.damage = 25
        self.radius = 4
        
    def update(self):
        rad = math.radians(self.angle)
        self.x += self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)
        
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius - 1)

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # 'health', 'speed', 'damage'
        self.radius = 15
        self.collected = False
        
    def draw(self, screen):
        if self.type == 'health':
            color = GREEN
        elif self.type == 'speed':
            color = BLUE
        else:
            color = RED
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 3)
        
    def check_collision(self, player):
        dist = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
        return dist < self.radius + player.width/2

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jackal Zombie Survival")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.zombies = []
        self.bullets = []
        self.powerups = []
        
        # Game state
        self.wave = 1
        self.zombies_per_wave = 5
        self.zombies_spawned = 0
        self.spawn_timer = 0
        self.shoot_cooldown = 0
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def spawn_zombie(self):
        # Spawn zombie at random edge of screen
        side = random.randint(0, 3)
        if side == 0:  # Top
            x, y = random.randint(0, SCREEN_WIDTH), -30
        elif side == 1:  # Right
            x, y = SCREEN_WIDTH + 30, random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Bottom
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 30
        else:  # Left
            x, y = -30, random.randint(0, SCREEN_HEIGHT)
        
        self.zombies.append(Zombie(x, y))
        
    def spawn_powerup(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        type = random.choice(['health', 'speed', 'damage'])
        self.powerups.append(PowerUp(x, y, type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.shoot_cooldown <= 0:
                    # Shoot bullet
                    bullet = Bullet(self.player.x, self.player.y, self.player.angle)
                    self.bullets.append(bullet)
                    self.shoot_cooldown = 15  # Cooldown between shots
                elif event.key == pygame.K_r and self.game_over:
                    # Restart game
                    self.__init__()
    
    def update(self):
        if self.game_over:
            return
        
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys)
        
        # Shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Spawn zombies
        if self.zombies_spawned < self.zombies_per_wave:
            self.spawn_timer += 1
            if self.spawn_timer > 60:  # Spawn every second
                self.spawn_zombie()
                self.zombies_spawned += 1
                self.spawn_timer = 0
        elif len(self.zombies) == 0:
            # Next wave
            self.wave += 1
            self.zombies_per_wave += 3
            self.zombies_spawned = 0
            
            # Spawn a powerup
            if random.random() < 0.5:
                self.spawn_powerup()
        
        # Update zombies
        for zombie in self.zombies[:]:
            zombie.update(self.player)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                continue
            
            # Check bullet collision with zombies
            for zombie in self.zombies[:]:
                dist = math.sqrt((bullet.x - zombie.x)**2 + (bullet.y - zombie.y)**2)
                if dist < zombie.width/2 + bullet.radius:
                    if zombie.take_damage(bullet.damage):
                        self.zombies.remove(zombie)
                        self.player.score += 10
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
        
        # Check powerup collection
        for powerup in self.powerups[:]:
            if powerup.check_collision(self.player):
                if powerup.type == 'health':
                    self.player.health = min(self.player.max_health, self.player.health + 30)
                elif powerup.type == 'speed':
                    self.player.max_speed += 0.5
                self.powerups.remove(powerup)
        
        # Check game over
        if self.player.health <= 0:
            self.game_over = True
    
    def draw(self):
        # Background
        self.screen.fill((40, 40, 40))
        
        # Draw grid pattern
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
        
        # Draw game objects
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        self.player.draw(self.screen)
        
        # Draw HUD
        # Health bar
        bar_width = 200
        bar_height = 20
        health_ratio = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, RED, (20, 20, bar_width, bar_height))
        pygame.draw.rect(self.screen, GREEN, (20, 20, bar_width * health_ratio, bar_height))
        pygame.draw.rect(self.screen, WHITE, (20, 20, bar_width, bar_height), 2)
        
        health_text = self.small_font.render(f"Health: {int(self.player.health)}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (25, 22))
        
        # Score
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (20, 60))
        
        # Wave
        wave_text = self.font.render(f"Wave: {self.wave}", True, WHITE)
        self.screen.blit(wave_text, (20, 100))
        
        # Zombies remaining
        zombies_left = self.zombies_per_wave - self.zombies_spawned + len(self.zombies)
        zombie_text = self.small_font.render(f"Zombies: {len(self.zombies)}", True, WHITE)
        self.screen.blit(zombie_text, (20, 140))
        
        # Controls
        controls_text = self.small_font.render("WASD/Arrows: Move | SPACE: Shoot", True, WHITE)
        self.screen.blit(controls_text, (SCREEN_WIDTH - 350, 20))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
            wave_text = self.font.render(f"Survived to Wave: {self.wave}", True, WHITE)
            restart_text = self.small_font.render("Press R to Restart", True, GREEN)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(wave_text, (SCREEN_WIDTH//2 - wave_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
