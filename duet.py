import pygame
import os
import random
import math

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def generate(ammount):
    global blocks
    blocks = [0, 0, 0]
    # 0 - no block
    # 1 - ====
    # 2 -   ====
    # 3 - ==
    # 4 -     ==
    # 5 -   ==
    # 6 -   ##
    # 7 - =-=-=
    # 8 -  =-=-=
    for i in range(ammount):
        if blocks[-1] in [1, 2] and random.randint(0, 2):
            blocks.append(random.randint(1, 2))
        if blocks[-1] in [7, 8] and random.randint(0, 2):
            blocks.append(random.randint(7, 8))
        else:
            blocks.append(random.randint(1, 8))

def restart():
    global score
    global angle
    score = 0
    angle = 0

def fullRestart():
    global score
    global angle
    global SPEED
    global ANGULAR_SPEED
    global level_count
    global total_score
    global HITPOINTS
    score = 0
    angle = 0
    SPEED = 6
    ANGULAR_SPEED = math.pi * SPEED / INTERVAL
    level_count = 0
    total_score = 0
    HITPOINTS = 3
    generate(10)

def restartMenu():
    restart_menu = True

    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(BLACK)
    surface.set_alpha(127)
    screen.blit(surface, (0, 0))

    pygame.draw.rect(screen, WHITE, (0, HEIGHT // 2 - 80, WIDTH, 160))
    score_rendered = font.render("счёт: " + str(int((total_score + score) / 20)), False, BLACK)
    screen.blit(score_rendered, (WIDTH // 2 - 40, HEIGHT // 2 - 40))

    global HIGHSCORE
    HIGHSCORE = max(total_score + score, HIGHSCORE)

    highscore_rendered = font.render("рекорд: " + str(int((HIGHSCORE) / 20)), False, BLACK)
    screen.blit(highscore_rendered, (WIDTH // 2 - 50, HEIGHT // 2 + 20))

    screen.blit(restart_image, ((WIDTH - restart_width) // 2, HEIGHT - 300))

    pygame.display.flip()
    while restart_menu:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart_menu = False
                global done
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if x > (WIDTH - restart_width) // 2 and \
                       x < (WIDTH + restart_width) // 2 and \
                       y > (HEIGHT - 300 - restart_height // 2) and \
                       y < (HEIGHT - 300 + restart_height // 2):
                       restart_menu = False
                       break
        fullRestart()

pygame.init()

BLACK =  (  0,   0,   0)
GREY  =  (100, 100, 100)
WHITE =  (255, 255, 255)
RED   =  (255,   0,   0)
BLUE  =  ( 50, 150, 255)

WIDTH, HEIGHT = (540, 960)

FPS = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)

pygame.display.set_caption("Duet")

hearts_width, hearts_height = 120, 40
hearts = pygame.transform.scale(load_image("hearts.png"), (hearts_width, hearts_height))
restart_width, restart_height = 90, 80
restart_image = pygame.transform.scale(load_image("restart.png"), (restart_width, restart_height))

done = False
clock = pygame.time.Clock()

angle = 0
SPEED = 6
INTERVAL = 360
BLOCK_WIDTH = 320
ANGULAR_SPEED = math.pi * SPEED / INTERVAL
score = 0
level_count = 0
total_score = 0
font = pygame.font.Font(None, 30)
HITPOINTS = 3
HIGHSCORE = 0

blocks = []
generate(10)

while not done:
 
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        angle -= ANGULAR_SPEED
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        angle += ANGULAR_SPEED

    screen.fill(BLACK)
    pygame.draw.circle(screen, GREY, (270, 750), 160, 3)
    
    for i in range(len(blocks)):
        if blocks[i] == 0:
            continue
        y = INTERVAL * i - score
        if y > -100 and y < HEIGHT + 100:
            if blocks[i] == 1:
                rect = pygame.Rect(0, int(HEIGHT-y), BLOCK_WIDTH, 60)
                pygame.draw.rect(screen, WHITE, rect)
            elif blocks[i] == 2:
                rect = pygame.Rect(WIDTH-BLOCK_WIDTH, int(HEIGHT-y), BLOCK_WIDTH, 60)
                pygame.draw.rect(screen, WHITE, rect)
            elif blocks[i] == 3:
                rect = pygame.Rect(0, int(HEIGHT-y), BLOCK_WIDTH//2, 60)
                pygame.draw.rect(screen, WHITE, rect)
            elif blocks[i] == 4:
                rect = pygame.Rect(WIDTH-BLOCK_WIDTH//2, int(HEIGHT-y), BLOCK_WIDTH//2, 60)
                pygame.draw.rect(screen, WHITE, rect)
            elif blocks[i] == 5:
                rect = pygame.Rect(WIDTH // 2 - BLOCK_WIDTH//4, int(HEIGHT-y), BLOCK_WIDTH//2, 60)
                pygame.draw.rect(screen, WHITE, rect)
            elif blocks[i] == 6:
                rect = pygame.Rect(WIDTH // 2 - BLOCK_WIDTH//4, int(HEIGHT-y), BLOCK_WIDTH//2, BLOCK_WIDTH//2)
                pygame.draw.rect(screen, WHITE, rect)
            elif blocks[i] == 7:
                rect = pygame.Rect(0, int(HEIGHT-y), BLOCK_WIDTH, 60)
                surface = pygame.Surface((BLOCK_WIDTH, 60))
                surface.fill(WHITE)
                surface.set_alpha(max(0, min(255, int(255 * (y - HEIGHT / 2) / (HEIGHT / 2)))))
                screen.blit(surface, (0, int(HEIGHT-y)))
            elif blocks[i] == 8:
                rect = pygame.Rect(WIDTH-BLOCK_WIDTH, int(HEIGHT-y), BLOCK_WIDTH, 60)
                surface = pygame.Surface((BLOCK_WIDTH, 60))
                surface.fill(WHITE)
                surface.set_alpha(max(0, min(255, int(255 * (y - HEIGHT / 2) / (HEIGHT / 2)))))
                screen.blit(surface, (WIDTH-BLOCK_WIDTH, int(HEIGHT-y)))

            ball = pygame.Rect(0, 0, 20, 20)
            ball.center = (int(270 + 160 * math.cos(angle)), int(750 - 160 * math.sin(angle)))
            if rect.colliderect(ball):
                HITPOINTS -= 1
                if HITPOINTS > 0:
                    restart()
            ball.center = (int(270 - 160 * math.cos(angle)), int(750 + 160 * math.sin(angle)))
            if rect.colliderect(ball):
                HITPOINTS -= 1
                if HITPOINTS > 0:
                    restart()

    pygame.draw.circle(screen, BLUE, (int(270 + 160 * math.cos(angle)), int(750 - 160 * math.sin(angle))), 25)
    pygame.draw.circle(screen, RED, (int(270 - 160 * math.cos(angle)), int(750 + 160 * math.sin(angle))), 25)
    
    if HITPOINTS <= 0:
        restartMenu()
        continue

    screen.blit(font.render(str(int((total_score + score) / 20)), False, GREY), (WIDTH - 50, 20))

    if score > len(blocks) * INTERVAL + HEIGHT // 4:
        total_score += score
        level_count += 1
        score = 0
        SPEED += 0.2
        ANGULAR_SPEED = math.pi * SPEED / INTERVAL
        generate(random.randint(10 + 3 * level_count, 10 + 5 * level_count))
        restart()

    HITPOINTS = min(3, HITPOINTS + 0.002)
    hearts_current = hearts.subsurface((0, 0, int(hearts_width * HITPOINTS / 3), hearts_height))
    screen.blit(hearts_current, (20, 20))

    pygame.display.flip()
    score += SPEED

pygame.quit()
