import pygame
import random
import time
from pygame.locals import *


BLUE   = (0, 0, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
CYAN   = (0, 220, 255)
GRAY   = (160, 160, 160)
DARK_GRAY = (80, 80, 80)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600


def load_image(filename, size, fallback_color=(255, 0, 255)):
    img = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(img, size)



class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="default"):
        super().__init__()
        
        color_name = car_color if car_color in ["default", "blue", "green", "yellow"] else "default"
        filename = f"assets\player_{color_name}.png"
        
        
        self.image = load_image(filename, (40, 60), RED)
        
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)

        self.shield_active = False
        self.nitro_active  = False
        self.nitro_end     = 0
        self.base_speed    = 5

    def move(self):
        speed = 7 if self.nitro_active else self.base_speed
        pressed = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if self.rect.right < SCREEN_WIDTH and pressed[K_RIGHT]:
            self.rect.move_ip(speed, 0)

    def update_powerups(self):
        if self.nitro_active and time.time() > self.nitro_end:
            self.nitro_active = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        
        filename = "assets\enemy_car.png"
        
        self.image = load_image(filename, (40, 60), DARK_GRAY)
        self.rect  = self.image.get_rect()
        self.speed = speed
        self._place_top()

    def _place_top(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -60)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self._place_top()

    def safe_spawn(self, player_rect):
        """Respawn away from player."""
        for _ in range(20):
            x = random.randint(40, SCREEN_WIDTH - 40)
            self.rect.center = (x, -60)
            if not self.rect.colliderect(player_rect.inflate(80, 80)):
                return
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -120)


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.speed  = speed
        self.weight = 1
        self.reset()

    def reset(self):
        self.weight = random.choice([1, 2, 3])
        filenames = {1: r"assets\coin.png", 2: r"assets\coin2.png", 3: r"assets\coin3.png"}
        filename = filenames[self.weight]
        self.image = load_image(filename, (24, 24), YELLOW)
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -30)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self.reset()


class OilSpill(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.speed = speed
        self.image = load_image("assets\oil_spill.png", (56, 28), BLACK)
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), -30)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.speed = speed
        self.image = load_image(r"assets\barrier.png", (40, 40), ORANGE)
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(60, SCREEN_WIDTH - 60), -30)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self.kill()


class NitroStrip(pygame.sprite.Sprite):
    """A road event strip — touching it applies nitro boost to the player."""
    def __init__(self, speed=5):
        super().__init__()
        self.speed = speed
        self.image = load_image(r"assets\nitro_strip.png", (SCREEN_WIDTH - 80, 20), CYAN)
        self.rect  = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = -30

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self.kill()


class Powerup(pygame.sprite.Sprite):
    TIMEOUT = 8  
    def __init__(self, kind, speed=5):
        super().__init__()
        self.kind  = kind  
        self.speed = speed
        
        filename = f"assets\powerup_{kind}.png"
        self.image = load_image(filename, (36, 36), GREEN)
        
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -40)
        self.spawn_time = time.time()

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self.kill()
        
        if time.time() - self.spawn_time > self.TIMEOUT:
            self.kill()