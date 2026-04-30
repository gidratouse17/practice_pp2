import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("snake")
fps_clock = pygame.time.Clock()
my_font = pygame.font.SysFont(None, 25)

snake = [[100, 60], [80, 60], [60, 60]]


direct_x = 20
direct_y = 0

points = 0
lvl = 1
speed = 10

eda_x = 0
eda_y = 0

def make_food():
    global eda_x, eda_y
    
    while True:
        eda_x = random.randint(0, 29) * 20
        eda_y = random.randint(0, 19) * 20
        

        collision = False
        for z in snake:
            if z[0] == eda_x and z[1] == eda_y:
                collision = True
        
        if collision == False:
            break

make_food() 

run = True
while run:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
            
        if ev.type == pygame.KEYDOWN:

            if ev.key == pygame.K_UP:
                if direct_y == 0:
                    direct_x = 0
                    direct_y = -20
            if ev.key == pygame.K_DOWN:
                if direct_y == 0:
                    direct_x = 0
                    direct_y = 20
            if ev.key == pygame.K_LEFT:
                if direct_x == 0:
                    direct_x = -20
                    direct_y = 0
            if ev.key == pygame.K_RIGHT:
                if direct_x == 0:
                    direct_x = 20
                    direct_y = 0


    head_x = snake[0][0] + direct_x
    head_y = snake[0][1] + direct_y
    
  
    snake.insert(0, [head_x, head_y])

    if head_x == eda_x and head_y == eda_y:
        points = points + 1
        
 
        if points % 3 == 0:
            lvl = lvl + 1
            speed = speed + 2
            
        make_food()
    else:

        snake.pop()


    if head_x < 0 or head_x > 580 or head_y < 0 or head_y > 380:
        print("Hit the wall. Points:", points)
        run = False


    for i in range(1, len(snake)):
        if head_x == snake[i][0] and head_y == snake[i][1]:
            print("Hit onto itself")
            run = False

 
    screen.fill((0, 0, 0))


    pygame.draw.rect(screen, (255, 0, 0), (eda_x, eda_y, 20, 20))

    
    for body in snake:
        pygame.draw.rect(screen, (0, 255, 0), (body[0], body[1], 20, 20))

    t = my_font.render("Score: " + str(points) + "  Level: " + str(lvl), True, (255, 255, 255))
    screen.blit(t, (10, 10))

    pygame.display.update()
    fps_clock.tick(speed)

pygame.quit()
sys.exit()