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
#colour_list/////////


main_surface = pygame.display.set_mode(screen)

IP = 'imgs/f16anim'
#ball\\\\\\\\\\\\\\\\\\\\\\\\\

ball_imgs = [pygame.image.load(IP + '/' + file).convert_alpha() for file in listdir(IP)]
ball_rect = ball_imgs[0].get_rect()
scaled_ball_imgs = [pygame.transform.scale(frame, (200, 200)) for frame in ball_imgs]
ball_speed = 7
# Scale the ball sprite

#ball/////////////////////////



#enemy\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def create_enemy():
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

#bonus\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def create_bonus():
    bonus = pygame.image.load('imgs/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(width, random.randint(0, 800), *bonus.get_size())
    bonus_speed = random.randint(4, 8)
    return [bonus, bonus_rect, bonus_speed]
CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 5000)

bonuses =[]
#bonus/////////////////////////////////////////////////


change_img = pygame.USEREVENT + 3
pygame.time.set_timer(change_img, 125)

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == change_img:
            index += 1
            if index == len(scaled_ball_imgs):
                index = 0

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == change_img:
            index += 1
            if index == len(scaled_ball_imgs):
                index = 0
            ball = scaled_ball_imgs[index]



    pressed_keys = pygame.key.get_pressed()

    bgx -= bg_speed
    bgx2 -= bg_speed
    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))

    if bgx < -bg.get_width():
        bgx = bg.get_width()
    if bgx2 < -bg.get_width():
        bgx2 = bg.get_width()

    ball = scaled_ball_imgs[index]
    main_surface.blit(ball, ball_rect)

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(-bonus[2], 0)
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].left < 0:
            bonus.pop(bonus.index(bonus))


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