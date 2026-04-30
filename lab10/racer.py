import pygame, sys, random, time
from pygame.locals import *

pygame.init()
pygame.mixer.music.load("background.wav") 
pygame.mixer.music.set_volume(0.5)      
pygame.mixer.music.play(-1)           

FPS = 60
fps_clock = pygame.time.Clock()
BLUE, RED, GREEN, BLACK, WHITE = (0,0,255), (255,0,0), (0,255,0), (0,0,0), (255,255,255)

SPEED = 5
points = 0
coin_count = 0  # переименовал чтобы не конфликтовало

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_txt = font.render("Game Over", True, BLACK)

bg = pygame.image.load("AnimatedStreet.png")
screen = pygame.display.set_mode((400,600))
pygame.display.set_caption("My Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)  

    def move(self):
        global points
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            points += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < 400 and keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, 360), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.reset()

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coin_sprites = pygame.sprite.Group()  # переименовал группу
coin_sprites.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg, (0,0))
    screen.blit(font_small.render("Score: " + str(points), True, BLACK), (10,10))
    screen.blit(font_small.render("Coins: " + str(coin_count), True, BLACK), (250,10))

    for obj in all_sprites:
        screen.blit(obj.image, obj.rect)
        obj.move()

    # Collect coins
    if pygame.sprite.spritecollideany(P1, coin_sprites):
        for c in pygame.sprite.spritecollide(P1, coin_sprites, False):
            coin_count += 1
            c.reset()

    # Enemy collision
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        screen.fill(RED)
        screen.blit(game_over_txt, (30,250))
        pygame.display.update()
        for obj in all_sprites:
            obj.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    fps_clock.tick(FPS)