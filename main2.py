import pygame
import random
from os import listdir
import sys

# General settings
pygame.init()
FPS = pygame.time.Clock()
screen = width, height = 1920, 1000
font = pygame.font.SysFont('Verdana', 20)
WHITE = 255, 255, 255
BLACK = 0, 0, 0
start_button_color = 225, 0, 0
quit_button_color = 225, 0, 0

main_surface = pygame.display.set_mode(screen)

# ... (Other code remains the same)

while is_working:
    FPS.tick(60)
    current_time = pygame.time.get_ticks()

    main_surface.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == change_img:
            index += 1
            if index == len(scaled_ball_imgs):
                index = 0
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_state = "playing"
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if game_state == "playing":
            if event.type == change_img:
                index += 1
                if index == len(scaled_ball_imgs):
                    index = 0

            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())

            if event.type == pygame.KEYDOWN:
                if event.key == K_s and not ball_rect.bottom >= height:
                    ball_rect = ball_rect.move(0, ball_speed)
                if event.key == K_w and not ball_rect.top <= 0:
                    ball_rect = ball_rect.move(0, -ball_speed)
                if event.key == K_a and not ball_rect.left <= 0:
                    ball_rect = ball_rect.move(-ball_speed, 0)
                if event.key == K_d and not ball_rect.right >= width:
                    ball_rect = ball_rect.move(ball_speed, 0)

            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                # Calculate the time since the last shot
                time_since_last_shot = current_time - last_shot_time

                # If enough time has passed (around 2000 ms for 2 seconds), allow shooting
                if time_since_last_shot >= 700:
                    # Create a projectile at the player's current position
                    projectile = pygame.Rect(ball_rect.centerx, ball_rect.centery, 10, 5)
                    projectiles.append(projectile)

                    # Update the last shot time
                    last_shot_time = current_time

        if game_state == "game_over":
            main_surface.fill(BLACK)
            game_over_text = font.render("Game Over", True, WHITE)
            score_text = font.render("Score: " + str(score), True, WHITE)
            main_surface.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
            main_surface.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + game_over_text.get_height() // 2))

    pygame.display.flip()

pygame.quit()