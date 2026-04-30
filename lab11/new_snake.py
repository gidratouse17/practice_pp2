import pygame
import sys
import random

pygame.init()

# Window size
WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)


snake = [[100, 60], [80, 60], [60, 60]]


dx = 20
dy = 0


score = 0
level = 1
speed = 10


FOOD_SIZE = 20
FOOD_LIFETIME = 5000  

FOOD_COLORS = {
    1: (255, 0, 0),    
    2: (255, 255, 0),  
    3: (255, 255, 255)  
}


def create_food():
    while True:
        x = random.randrange(0, WIDTH, FOOD_SIZE)
        y = random.randrange(0, HEIGHT, FOOD_SIZE)
        pos = [x, y]


        if pos not in snake:
            weight = random.choice([1, 2, 3])  
            color = FOOD_COLORS[weight]
            spawn_time = pygame.time.get_ticks()  
            return {
                "pos": pos,
                "weight": weight,
                "color": color,
                "spawn_time": spawn_time
            }


food = create_food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -20
            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = 20
            elif event.key == pygame.K_LEFT and dx == 0:
                dx = -20
                dy = 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = 20
                dy = 0


    current_time = pygame.time.get_ticks()
    if current_time - food["spawn_time"] > FOOD_LIFETIME:
        food = create_food()

 
    head = [snake[0][0] + dx, snake[0][1] + dy]
    snake.insert(0, head)


    if head == food["pos"]:
        score += food["weight"] 

  
        if score % 3 == 0:
            level += 1
            speed += 2

        food = create_food()
    else:
    
        snake.pop()


    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        print("Game Over")
        pygame.quit()
        sys.exit()

   
    if head in snake[1:]:
        print("Game Over")
        pygame.quit()
        sys.exit()

 
    screen.fill((0, 0, 0))


    pygame.draw.rect(
        screen,
        food["color"],
        (food["pos"][0], food["pos"][1], FOOD_SIZE, FOOD_SIZE)
    )

 
    for block in snake:
        pygame.draw.rect(screen, (0, 255, 0), (block[0], block[1], 20, 20))

   
    text = font.render("Score: " + str(score) + "  Level: " + str(level), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)