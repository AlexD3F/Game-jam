import pygame
import random
from pygame. constants import QUIT, K_s, K_w, K_a, K_d
from os import listdir
#general\\\\\\\\\\\\\\\\\\\\\\\\\\\
pygame.init()

FPS = pygame.time.Clock()

screen = width, heigth = 1920, 1000

font = pygame.font.SysFont('Verdana', 20)
#general///////////////////////////

#colour_list\\\\\\\\\
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 0, 255
BLUE = 0, 0, 255
#colour_list/////////


main_surface = pygame.display.set_mode(screen)

IP = 'imgs/f16anim'
#ball\\\\\\\\\\\\\\\\\\\\\\\\\
ball_imgs = [pygame.image.load(IP + '/' + file).convert_alpha() for file in listdir(IP)]
ball = ball_imgs[0]
ball_rect = ball.get_rect()
ball_speed = 7
#ball/////////////////////////

#enemy\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def create_enemy():
    #enemy = pygame.Surface((20, 20))
    #enemy.fill(RED)
    enemy = pygame.image.load('imgs/enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint(0, 800), *enemy.get_size())
    enemy_speed = random.randint(4, 8)
    return [enemy, enemy_rect, enemy_speed]
CREATE_ENEMY = pygame.USEREVENT +1
pygame.time.set_timer(CREATE_ENEMY, 3000)

enemies =[]
#enemy/////////////////////////////////////////////////

#background\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
bg = pygame.transform.scale(pygame.image.load('imgs/background.png').convert(), screen)
bgx = 0
bgx2 = bg.get_width()
bg_speed = 3

index = 0
score = 0
#background////////////////////////////////////////////////////////////////////////////////

change_img = pygame.USEREVENT +3
pygame.time.set_timer(change_img, 125)

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == change_img:
             index += 1
             if index == len(ball_imgs):
                 index = 0
             ball = ball_imgs[index]

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

    pressed_keys = pygame.key.get_pressed()

    bgx -= bg_speed
    bgx2 -= bg_speed
    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))

    if bgx < -bg.get_width():
        bgx = bg.get_width()
    if bgx2 < -bg.get_width():
        bgx2 = bg.get_width()

    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(str(score), True, BLACK), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False


    #controles\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    if pressed_keys[K_s] and not ball_rect.bottom >= heigth:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_keys[K_w] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_keys[K_a] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    if pressed_keys[K_d] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)
    #controles//////////////////////////////////////




    pygame.display.flip()