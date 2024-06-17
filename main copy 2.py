import pygame
import time
import random
import os
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sounds

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lightning Dodge - Minor - JB")

BG = pygame.image.load("Bliksem BG.jpg")

# Laden van de afbeeldingen
player_img = pygame.image.load("Ufo.png")
rock_img = pygame.image.load("Bliksem.png")
powerup_invincible_img = pygame.image.load("powerup_invincible.png")
powerup_slowdown_img = pygame.image.load("powerup_slowdown.png")

# Definiëren van de grootte van de speler, rotsen en power-ups
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
ROCK_WIDTH = 30
ROCK_HEIGHT = 30
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30

# Schaal de afbeeldingen naar de gewenste grootte
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
rock_img = pygame.transform.scale(rock_img, (ROCK_WIDTH, ROCK_HEIGHT))
powerup_invincible_img = pygame.transform.scale(powerup_invincible_img, (POWERUP_WIDTH, POWERUP_HEIGHT))
powerup_slowdown_img = pygame.transform.scale(powerup_slowdown_img, (POWERUP_WIDTH, POWERUP_HEIGHT))

PLAYER_VELOCITY = 5
ROCK_VELOCITY = 5
FONT = pygame.font.SysFont("Arial", 30)

HIGHSCORE_FILE = "highscore.txt"

# Geluiden laden
pygame.mixer.music.load("BG music.mp3")  # Achtergrondmuziek
game_over_sound = pygame.mixer.Sound("Game Over.mp3")  # Game-over geluid

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            return float(file.read().strip())
    return 0.0

def save_highscore(highscore):
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(highscore))

def draw(player, elapsed_time, rocks, level, highscore, powerups, active_powerup, powerup_time_left, score, lives):
    WIN.blit(BG, (0, 0))
    
    level_text = FONT.render(f"Level: {level}", 1, (255, 255, 255))
    WIN.blit(level_text, (10, 10))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))
    
    score_text = FONT.render(f"Highscore: {score}", 1, (255, 255, 255))
    WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 10))
    
    if active_powerup:
        powerup_text = FONT.render(f"Power-up: {active_powerup} ({round(powerup_time_left)}s)", 1, (255, 255, 255))
        WIN.blit(powerup_text, (10, 50))

    lives_text = FONT.render(f"Lives: {lives}", 1, (255, 255, 255))
    WIN.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 90))

    WIN.blit(player_img, (player.x, player.y))

    for rock in rocks:
        WIN.blit(rock_img, (rock.x, rock.y))

    for powerup in powerups:
        if powerup[1] == "invincible":
            WIN.blit(powerup_invincible_img, (powerup[0].x, powerup[0].y))
        elif powerup[1] == "slowdown":
            WIN.blit(powerup_slowdown_img, (powerup[0].x, powerup[0].y))

    pygame.display.update()

def increase_difficulty(level):
    global ROCK_VELOCITY, rock_add_increment
    ROCK_VELOCITY += level * 0.5
    rock_add_increment = max(200, rock_add_increment - level * 10)

def main_menu():
    run_menu = True
    player_name = ""

    while run_menu:
        WIN.fill((0, 0, 0))
        menu_font = pygame.font.SysFont("Arial", 40)

        title_text = menu_font.render("Lightning Dodge", True, (255, 255, 255))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        start_text = menu_font.render("Start Game", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(start_text, start_rect)

        highscore_text = menu_font.render("High Scores", True, (255, 255, 255))
        highscore_rect = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        WIN.blit(highscore_text, highscore_rect)

        exit_text = menu_font.render("Exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        WIN.blit(exit_text, exit_rect)

        name_text = menu_font.render("Enter your name:", True, (255, 255, 255))
        WIN.blit(name_text, (WIDTH // 2 - 150, HEIGHT // 2 + 150))

        pygame.draw.rect(WIN, (255, 255, 255), (WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50), 2)

        input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50)
        pygame.draw.rect(WIN, (255, 255, 255), input_rect)
        pygame.draw.rect(WIN, (0, 0, 0), input_rect.inflate(-2, -2))

        name_font = pygame.font.SysFont("Arial", 30)
        name_surface = name_font.render(player_name, True, (255, 255, 255))
        WIN.blit(name_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    run_menu = False
                elif highscore_rect.collidepoint(mouse_pos):
                    # Add code to view high scores
                    pass
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == K_RETURN:
                    run_menu = False
                else:
                    player_name += event.unicode

    return player_name

def main(player_name):
    global ROCK_VELOCITY  # Maak ROCK_VELOCITY globaal zodat het kan worden aangepast in increase_difficulty

    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    global rock_add_increment  # Definieer rock_add_increment als een globale variabele
    rock_add_increment = 2000 
    rock_count = 0 

    rocks = []
    powerups = []
    hit = False
    invincible = False
    invincible_start_time = 0
    invincible_duration = 5  # Invincibility lasts for 5 seconds
    slowdown = False
    slowdown_start_time = 0
    slowdown_duration = 5  # Slowdown lasts for 5 seconds
    original_rock_velocity = ROCK_VELOCITY
    current_level = 1
    level_up_time = 10  # Tijd in seconden om naar het volgende niveau te gaan
    next_level_time = level_up_time

    highscore = load_highscore()
    active_powerup = None
    powerup_time_left = 0
    score = 0
    lives = 3

    pygame.mixer.music.play(-1)  # Start de achtergrondmuziek

    while run: 
        rock_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Verhoog het niveau en pas de moeilijkheidsgraad aan
        if elapsed_time > next_level_time:
            current_level += 1
            next_level_time += level_up_time
            increase_difficulty(current_level)

        if rock_count > rock_add_increment:
            rock_x = random.randint(0, WIDTH - ROCK_WIDTH)
            rock = pygame.Rect(rock_x, -ROCK_HEIGHT, ROCK_WIDTH, ROCK_HEIGHT)
            rocks.append(rock)

            rock_add_increment = max(200, rock_add_increment - 50)
            rock_count = 0

        # Voeg af en toe een power-up toe
        if random.random() < 0.002:  # 0.2% kans per frame om een power-up te genereren
            powerup_x = random.randint(0, WIDTH - POWERUP_WIDTH)
            powerup_type = random.choice(["invincible", "slowdown"])
            powerup = (pygame.Rect(powerup_x, -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT), powerup_type)
            powerups.append(powerup)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Move player based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        for rock in rocks[:]:
            rock.y += ROCK_VELOCITY 
            if rock.y > HEIGHT:
                rocks.remove(rock)
                score += 1  # Verhoog de score als een rots de bodem bereikt
            elif rock.y + rock.height >= player.y and rock.colliderect(player):
                if not invincible:
                    rocks.remove(rock)
                    hit = True
                    lives -= 1  # Verminder een leven bij een botsing
                    if lives <= 0:
                        hit = True
                    break

        for powerup in powerups[:]:
            powerup[0].y += ROCK_VELOCITY
            if powerup[0].y > HEIGHT:
                powerups.remove(powerup)
            elif powerup[0].colliderect(player):
                if powerup[1] == "invincible":
                    invincible = True
                    invincible_start_time = time.time()
                    active_powerup = "Invincibility"
                    powerup_time_left = invincible_duration
                elif powerup[1] == "slowdown":
                    slowdown = True
                    slowdown_start_time = time.time()
                    active_powerup = "Slowdown"
                    powerup_time_left = slowdown_duration
                    original_rock_velocity = ROCK_VELOCITY
                    ROCK_VELOCITY = ROCK_VELOCITY / 2  # Vertraag de snelheid van de rotsen
                powerups.remove(powerup)

        # Check if invincibility has worn off
        if invincible and time.time() - invincible_start_time > invincible_duration:
            invincible = False
            active_powerup = None

        # Check if slowdown has worn off
        if slowdown and time.time() - slowdown_start_time > slowdown_duration:
            slowdown = False
            ROCK_VELOCITY = original_rock_velocity
            active_powerup = None

        # Bereken de resterende tijd voor actieve power-ups
        if active_powerup:
            powerup_time_left -= clock.get_time() / 1000  # Aftrekken van de verstreken tijd in seconden
            if powerup_time_left <= 0:
                active_powerup = None

        # Update highscore
        if elapsed_time > highscore:
            highscore = elapsed_time
            save_highscore(highscore)

        draw(player, elapsed_time, rocks, current_level, highscore, powerups, active_powerup, powerup_time_left, score, lives)

        if hit and lives <= 0:
            pygame.mixer.Sound.play(game_over_sound)  # Speel het game-over geluid
            run = False
            break

    pygame.mixer.music.stop()  # Stop de achtergrondmuziek

    while True:
        game_over_text = FONT.render("Game Over", 1, (255, 0, 0))
        WIN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))
        
        press_enter_text = FONT.render("Press ENTER for Main Menu", 1, (255, 255, 255))
        WIN.blit(press_enter_text, (WIDTH/2 - press_enter_text.get_width()/2, HEIGHT/2 + game_over_text.get_height()))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Ga terug naar het hoofdmenu bij ENTER
                    return

if __name__ == "__main__":
    while True:  # Herhaal om terug te keren naar het hoofdmenu na Game Over
        player_name = main_menu()
        main(player_name)
