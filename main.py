#This is the file that I created by completing the tutorial

import pygame
import time
import random
pygame.font.init()

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lightning Dodge - Minor - JB")

BG = pygame.image.load("Bliksem BG.jpg")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5

ROCK_WIDTH = 10
ROCK_HEIGHT = 20
ROCK_VELOCITY = 5

FONT = pygame.font.SysFont("Arial", 50)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "Black")
    WIN.blit(time_text, (580, 10))
    
    pygame.draw.rect(WIN, "Red", player)

    for rock in stars:
        pygame.draw.rect(WIN, "Yellow", rock)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    rock_add_increment = 2000 
    rock_count = 0 

    rocks = []
    hit = False

    while run: 
        rock_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if rock_count > rock_add_increment:
            for _ in range(3):
                rock_x = random.randint(0, WIDTH - ROCK_WIDTH)
                rock = pygame.Rect(rock_x, -ROCK_HEIGHT, ROCK_WIDTH, ROCK_HEIGHT)
                rocks.append(rock)

            rock_add_increment = max(200, rock_add_increment - 50)
            rock_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Move player based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >=0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        for rock in rocks[:]:
            rock.y += ROCK_VELOCITY 
            if rock.y > HEIGHT:
                rocks.remove(rock)
            elif rock.y + rock.height >= player.y and rock.colliderect(player):
                rocks.remove(rock)
                hit = True
                break

        if hit: 
            lost_text = FONT.render("GAME OVER!", 1, "White")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break


        draw(player, elapsed_time, rocks)

    pygame.quit()

if __name__ == "__main__":
    main()

