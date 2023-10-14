import pygame
import random
from pygame. constants import QUIT, K_s, K_w, K_a, K_d, K_SPACE
from os import listdir
#general\\\\\\\\\\\\\\\\\\\\\\\\\\\
pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1920, 1000

font = pygame.font.SysFont('Verdana', 20)
#general///////////////////////////

#colour_list\\\\\\\\\
WHITE = 255, 255, 255
BLACK = 0, 0, 0
#colour_list/////////

return_to_menu = False
main_surface = pygame.display.set_mode(screen)

IP = 'imgs/f16anim'
#ball\\\\\\\\\\\\\\\\\\\\\\\\\

ball_imgs = [pygame.image.load(IP + '/' + file).convert_alpha() for file in listdir(IP)]
ball_rect = pygame.Rect(0, 0, 200, 200)
scaled_ball_imgs = [pygame.transform.scale(frame, (200, 200)) for frame in ball_imgs]
ball_speed = 8
# Scale the ball sprite

#ball/////////////////////////



# Game state
game_state = "menu"


#enemy\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def create_enemy():
    enemy = pygame.image.load('imgs/enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint(0, 800), *enemy.get_size())
    enemy_speed = random.randint(4, 7)
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



change_img = pygame.USEREVENT + 3
pygame.time.set_timer(change_img, 125)

#Game variables\\\\\\\\\
is_working = True
projectiles = []
last_shot_time = 0
score = 0
#//////////////////////

start_button = pygame.Rect(width // 2 - 100, height // 2, 200, 50)
quit_button = pygame.Rect(width // 2 - 100, height // 2 + 60, 200, 50)

# Define button colors
button_color = (100, 100, 100)
hover_color = (150, 150, 150)
click_color = (50, 50, 50)

button_font = pygame.font.Font(None, 36)
start_text = button_font.render("Start Game", True, (255, 255, 255))
quit_text = button_font.render("Quit", True, (255, 255, 255))
start_button_color = (255, 0, 0)
quit_button_color = (255, 0, 0)

menu_button = pygame.Rect(width // 2 - 100, height // 2 + 120, 200, 50)
menu_button_color = (255, 0, 0)
menu_text = button_font.render("Menu", True, (255, 255, 255))

while True:
    while is_working:

        FPS.tick(60)

        current_time = pygame.time.get_ticks()  # Get the current times

        for event in pygame.event.get():
            if event.type == QUIT:
                is_working = False
            if event.type == change_img:
                index += 1
                if index == len(scaled_ball_imgs):
                    index = 0

            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())

            if event.type == change_img:
                index += 1
                if index == len(scaled_ball_imgs):
                    index = 0
                ball = scaled_ball_imgs[index]

        pressed_keys = pygame.key.get_pressed()

        if game_state == "menu":
            # Draw buttons
            pygame.draw.rect(main_surface, start_button_color, start_button)
            main_surface.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 + 10))
            pygame.draw.rect(main_surface, quit_button_color, quit_button)
            main_surface.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 70))

            if event.type == pygame.MOUSEMOTION:
                # Change button color when mouse hovers over
                if start_button.collidepoint(event.pos):
                    start_button_color = hover_color
                else:
                    start_button_color = button_color

                if quit_button.collidepoint(event.pos):
                    quit_button_color = hover_color
                else:
                    quit_button_color = button_color

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_state = "playing"
                    # Initialize game variables (e.g., reset score, enemies, etc.)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        elif game_state == "playing":


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
            #gpt\\\\\\\\\\\\
            for projectile in projectiles:
                projectile.x += 10  # Adjust the speed and direction of projectiles
                pygame.draw.rect(main_surface, WHITE, projectile)  # Draw the projectiles
            #gpt////////////
            for enemy in enemies:
                enemy[1] = enemy[1].move(-enemy[2], 0)
                main_surface.blit(enemy[0], enemy[1])
                if enemy[1].left < 0:
                    enemies.pop(enemies.index(enemy))

                if ball_rect.colliderect(enemy[1]):
                    is_working = False

            projectiles = [p for p in projectiles if p.right <= width]

            updated_enemies = []
            for enemy in enemies:
                enemy[1] = enemy[1].move(-enemy[2], 0)
                main_surface.blit(enemy[0], enemy[1])
                if enemy[1].left >= 0:
                    updated_enemies.append(enemy)


            #controles\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            if pressed_keys[K_s] and not ball_rect.bottom >= height:
                ball_rect = ball_rect.move(0, ball_speed)

            if pressed_keys[K_w] and not ball_rect.top <= 0:
                ball_rect = ball_rect.move(0, -ball_speed)

            if pressed_keys[K_a] and not ball_rect.left <= 0:
                ball_rect = ball_rect.move(-ball_speed, 0)

            if pressed_keys[K_d] and not ball_rect.right >= width:
                ball_rect = ball_rect.move(ball_speed, 0)

            if pressed_keys[K_SPACE]:
                # Calculate the time since the last shot
                time_since_last_shot = current_time - last_shot_time

                # If enough time has passed (around 2000 ms for 2 seconds), allow shooting
                if time_since_last_shot >= 700:
                    # Create a projectile at the player's current position
                    projectile = pygame.Rect(ball_rect.centerx, ball_rect.centery, 10, 5)
                    projectiles.append(projectile)

                    # Update the last shot time
                    last_shot_time = current_time

            #controles//////////////////////////////////////

        if game_state == "menu":
            # Draw buttons
            pygame.draw.rect(main_surface, start_button_color, start_button)
            pygame.draw.rect(main_surface, quit_button_color, quit_button)

        pygame.display.flip()

#DO NOT TOUCH!!!!!!!!!!!!!!!!!!!!!!!
    while True:
        main_surface.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render("Score: " + str(score), True, WHITE)

        main_surface.blit(game_over_text, (
        width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
        main_surface.blit(score_text,
                          (width // 2 - score_text.get_width() // 2, height // 2 + game_over_text.get_height() // 2))

        # Draw the "Menu" button
        pygame.draw.rect(main_surface, menu_button_color, menu_button)
        main_surface.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 2 + 130))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if menu_button.collidepoint(event.pos):
                    menu_button_color = hover_color
                else:
                    menu_button_color = button_color

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    # If the "Menu" button is clicked, set the flag to return to the main menu
                    return_to_menu = True

        if return_to_menu:
            # Reset game-related variables and return to the main menu
            # This block will only execute after the button click
            return_to_menu = False  # Reset the flag
            game_state = "menu"
            projectiles = []
            enemies = []
            score = 0  # Reset the score or any other relevant game variables
            ball_rect = pygame.Rect(0, 0, 200, 200)
            is_working = True

            # Additional initialization as needed

            # Break out of the game over loop to return to the main menu
            break


