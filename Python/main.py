import pygame
import sys
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Z-urvival")
clock = pygame.time.Clock()

# Colors
BG = (30, 30, 30)
PLAYER_COLOR = (0, 200, 255)
BULLET_COLOR = (255, 50, 50)

# Player (firkanten)
square_size = 50
square_x = WIDTH // 2
square_y = HEIGHT // 2
speed = 3

# Bullets list
bullets = []
bullet_speed = 8
bullet_radius = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Shoot bullet on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                # Skyt fra midten av firkanten
                player_center_x = square_x + square_size // 2
                player_center_y = square_y + square_size // 2
                
                dx = mouse_x - player_center_x
                dy = mouse_y - player_center_y
                distance = math.hypot(dx, dy)
                if distance == 0:
                    distance = 1
                # Normalize direction
                dx /= distance
                dy /= distance
                bullets.append({"pos": [player_center_x, player_center_y], "dir": (dx, dy)})

    # Key presses - flytt firkanten
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= speed
    if keys[pygame.K_RIGHT]:
        square_x += speed
    if keys[pygame.K_UP]:
        square_y -= speed
    if keys[pygame.K_DOWN]:
        square_y += speed

    # Keep square on screen
    square_x = max(0, min(WIDTH - square_size, square_x))
    square_y = max(0, min(HEIGHT - square_size, square_y))

    # Move bullets
    for bullet in bullets[:]:
        bullet["pos"][0] += bullet["dir"][0] * bullet_speed
        bullet["pos"][1] += bullet["dir"][1] * bullet_speed

        # Remove bullets off-screen
        if (bullet["pos"][0] < 0 or bullet["pos"][0] > WIDTH or
            bullet["pos"][1] < 0 or bullet["pos"][1] > HEIGHT):
            bullets.remove(bullet)

    # Drawing
    screen.fill(BG)
    
    # Tegn firkanten (spilleren)
    pygame.draw.rect(screen, PLAYER_COLOR, (square_x, square_y, square_size, square_size))

    # Tegn kulene
    for bullet in bullets:
        pygame.draw.circle(screen, BULLET_COLOR,
                           (int(bullet["pos"][0]), int(bullet["pos"][1])), bullet_radius)

    pygame.display.flip()
    clock.tick(60)