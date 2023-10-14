import pygame
import random
from pygame. constants import QUIT, K_s, K_w, K_a, K_d, K_SPACE, K_q
from os import listdir
import pygame.mixer

#general\\\\\\\\\\\\\\\\\\\\\\\\\\\
pygame.init()
pygame.mixer.init()
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
ball_rect = pygame.Rect(80, 500, 150, 150)
scaled_ball_imgs = [pygame.transform.scale(frame, (150, 150)) for frame in ball_imgs]
ball_speed = 8
# Scale the ball sprite

#ball/////////////////////////

start_button_images = pygame.image.load('imgs/buttons/menub.png').convert_alpha()
start_button_image = pygame.transform.scale(start_button_images, (200, 60))
stop_button_images = pygame.image.load('imgs/buttons/Stop.png').convert_alpha()
stop_button_image = pygame.transform.scale(stop_button_images, (200, 60))
menu_button_images = pygame.image.load('imgs/buttons/menub.png').convert_alpha()
menu_button_image = pygame.transform.scale(menu_button_images, (200, 60))
# Game state
game_state = "menu"


last_eng = 0


#\\\\\\\\\\\\\\\\\\\\\\\\\
#sound
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
eng_sound = pygame.mixer.Sound('sounds/engine.mp3')
exp_sound = pygame.mixer.Sound('sounds/hq-explosion-6288.mp3')
kill_sound = pygame.mixer.Sound('sounds/kill.mp3')
shoot_sound.set_volume(0.25)
eng_sound.set_volume(0.25)
exp_sound.set_volume(0.5)
#/////////////////////////


#enemy\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def create_enemy():
    enemy = pygame.image.load('imgs/enemy.png').convert_alpha()

    # Scale the enemy image to your desired dimensions (e.g., 50x50 pixels)
    scaled = random.randint(195, 200)
    enemy = pygame.transform.scale(enemy, (scaled, scaled))

    enemy_rect = pygame.Rect(width, random.randint(0, 900), *enemy.get_size())
    enemy_speed = random.randint(2, 3)

    return [enemy, enemy_rect, enemy_speed]

enemy_creation_interval = random.randint(1500, 1800)  # Initial interval, in milliseconds

ENEMY_CREATION_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(ENEMY_CREATION_EVENT, enemy_creation_interval)

enemies =[]
#enemy/////////////////////////////////////////////////

#background\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
bg = pygame.transform.scale(pygame.image.load('imgs/background.png').convert(), screen)
bgx = 0
bgx2 = bg.get_width()
bg_speed = 3
menubg = pygame.transform.scale(pygame.image.load('imgs/menu.png').convert(), screen)
index = 0
score = 0
timse_since_last_shot_sound = 1000
exps = 1
#background////////////////////////////////////////////////////////////////////////////////



change_img = pygame.USEREVENT + 3
pygame.time.set_timer(change_img, 125)

#Game variables\\\\\\\\\
is_working = True
projectiles = []
last_shot_time = 0
score = 0
enemy_hit_count = {}

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
    main_surface.blit(menubg, (0, 0))
    while is_working:
        FPS.tick(60)

        current_time = pygame.time.get_ticks()  # Get the current times

        if score >= 15:
            if score < 30:
                enemy_creation_interval = 2500  # Initial interval, in milliseconds
            else:
                if score < 45:
                    enemy_creation_interval = 2000  # Initial interval, in milliseconds
                else:
                    if score < 60:
                        enemy_creation_interval = 1500  # Initial interval, in milliseconds
                    else:
                        enemy_creation_interval = 1000  # Initial interval, in milliseconds

        for event in pygame.event.get():
            if event.type == QUIT:
                is_working = False
            if event.type == change_img:
                index += 1
                if index == len(scaled_ball_imgs):
                    index = 0

            if event.type == ENEMY_CREATION_EVENT:
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

            time_since_eng = current_time - last_eng
            if time_since_eng >= 4000:
                # Create a projectile at the player's current position
                eng_sound.play()


                # Update the last shot time
                last_eng = current_time

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

            for i, enemy in enumerate(enemies):
                enemy[1] = enemy[1].move(-enemy[2], 0)
                main_surface.blit(enemy[0], enemy[1])

            #gpt\\\\\\\\\\\\
            for projectile in projectiles:
                projectile.x += 10  # Adjust the speed and direction of projectiles
                pygame.draw.rect(main_surface, WHITE, projectile)  # Draw the projectiles

            for i, enemy in enumerate(enemies.copy()):
                # If this enemy is not in the hit count dictionary, add it
                if i not in enemy_hit_count:
                    enemy_hit_count[i] = 0

                enemy[1] = enemy[1].move(-enemy[2], 0)
                main_surface.blit(enemy[0], enemy[1])

                # Check for collisions with shots and update hit counts
                for projectile in projectiles:
                    if enemy[1].colliderect(projectile):
                        # Increment the hit count for the enemy and remove the projectile
                        enemy_hit_count[i] += 1
                        projectiles.remove(projectile)

                # Check if the enemy has been hit twice and mark it for removal
                if enemy_hit_count[i] >= 2:
                    enemies.remove(enemy)
                    del enemy_hit_count[i]
                    score += 1
                    kill_sound.play()


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

            if pressed_keys[K_a] and not ball_rect.left <= 79:
                ball_rect = ball_rect.move(-ball_speed, 0)

            if pressed_keys[K_d] and not ball_rect.right >= width:
                ball_rect = ball_rect.move(ball_speed, 0)

            if pressed_keys[K_SPACE]:
                # Calculate the time since the last shot
                time_since_last_shot = current_time - last_shot_time

                # If enough time has passed (around 2000 ms for 2 seconds), allow shooting
                if time_since_last_shot >= 520:
                    # Create a projectile at the player's current position
                    projectile = pygame.Rect(ball_rect.centerx, ball_rect.centery, 10, 5)
                    projectiles.append(projectile)
                    if  timse_since_last_shot_sound >= 1000:
                        shoot_sound.play()
                        timse_since_last_shot_sound = current_time
                    # Update the last shot time
                    last_shot_time = current_time
            #if pressed_keys[K_q]:
            #    score +=1

            #controles//////////////////////////////////////

        if game_state == "menu":
            # Draw buttons
            main_surface.blit(start_button_image, start_button)
            main_surface.blit(stop_button_image, quit_button)

        pygame.display.flip()

#DO NOT TOUCH!!!!!!!!!!!!!!!!!!!!!!!
    while True:
        eng_sound.stop()
        shoot_sound.stop()
        if exps == 1:
            exp_sound.play()
            exps = 0
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render("Score: " + str(score), True, WHITE)

        main_surface.blit(game_over_text, (
        width // 2 - game_over_text.get_width() // 2, height // 2.35 - game_over_text.get_height() // 2))
        main_surface.blit(score_text,
                          (width // 2 - score_text.get_width() // 2, height // 2.35 + game_over_text.get_height() // 2))

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
            ball_rect = pygame.Rect(80, 100, 200, 200)
            is_working = True
            exps = 1
            # Additional initialization as needed

            # Break out of the game over loop to return to the main menu
            break