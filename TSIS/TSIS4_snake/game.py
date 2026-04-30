import pygame
import random
from config import *


class Food:
    def __init__(self, snake_body, obstacles):
        self.size = FOOD_SIZE
        self.respawn(snake_body, obstacles)

    def respawn(self, snake_body, obstacles):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = [x, y]
            if pos not in snake_body and pos not in obstacles:
                self.pos = pos
                self.weight = random.choice([1, 2, 3])
                self.color = FOOD_COLORS[self.weight]
                self.spawn_time = pygame.time.get_ticks()
                return

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > FOOD_LIFETIME

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.pos[0], self.pos[1], self.size, self.size))


class PoisonFood:
    """Poison food - shrinks snake by 2 segments"""
    def __init__(self, snake_body, obstacles):
        self.size = CELL_SIZE
        self.respawn(snake_body, obstacles)

    def respawn(self, snake_body, obstacles):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = [x, y]
            if pos not in snake_body and pos not in obstacles:
                self.pos = pos
                self.spawn_time = pygame.time.get_ticks()
                return

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > FOOD_LIFETIME

    def draw(self, screen):
        # Draw dark red square with a cross to distinguish from regular food
        pygame.draw.rect(screen, POISON_COLOR,
                         (self.pos[0], self.pos[1], self.size, self.size))
        pygame.draw.line(screen, WHITE,
                         (self.pos[0] + 3, self.pos[1] + 3),
                         (self.pos[0] + self.size - 3, self.pos[1] + self.size - 3), 2)
        pygame.draw.line(screen, WHITE,
                         (self.pos[0] + self.size - 3, self.pos[1] + 3),
                         (self.pos[0] + 3, self.pos[1] + self.size - 3), 2)


class PowerUp:
    """Power-up on the field"""
    def __init__(self, snake_body, obstacles, food_pos, poison_pos):
        self.size = CELL_SIZE
        self.type = random.choice(["speed_boost", "slow_motion", "shield"])
        self.color = POWERUP_COLORS[self.type]
        self.active = False         # activated (affecting snake)
        self.active_start = 0       # activation time
        self.collected = False      # collected by snake

        # Spawn on a free cell
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = [x, y]
            if (pos not in snake_body and pos not in obstacles
                    and pos != food_pos and pos != poison_pos):
                self.pos = pos
                self.spawn_time = pygame.time.get_ticks()
                return

    def is_expired_on_field(self):
        """Has it disappeared from field (if not collected within 8 sec)"""
        if not self.collected:
            return pygame.time.get_ticks() - self.spawn_time > POWERUP_LIFETIME
        return False

    def is_effect_over(self):
        """Has the effect ended"""
        if self.active:
            return pygame.time.get_ticks() - self.active_start > POWERUP_EFFECT_DURATION
        return False

    def activate(self):
        self.collected = True
        self.active = True
        self.active_start = pygame.time.get_ticks()

    def draw(self, screen):
        if not self.collected:
            # Draw a diamond shape
            cx = self.pos[0] + self.size // 2
            cy = self.pos[1] + self.size // 2
            points = [
                (cx, self.pos[1]),
                (self.pos[0] + self.size, cy),
                (cx, self.pos[1] + self.size),
                (self.pos[0], cy)
            ]
            pygame.draw.polygon(screen, self.color, points)


class Snake:
    def __init__(self, settings):
        self.body = [[100, 60], [80, 60], [60, 60]]
        self.dx = CELL_SIZE
        self.dy = 0
        self.color = tuple(settings["snake_color"])
        self.shield_active = False

    def change_direction(self, key):
        if key == pygame.K_UP and self.dy == 0:
            self.dx = 0
            self.dy = -CELL_SIZE
        elif key == pygame.K_DOWN and self.dy == 0:
            self.dx = 0
            self.dy = CELL_SIZE
        elif key == pygame.K_LEFT and self.dx == 0:
            self.dx = -CELL_SIZE
            self.dy = 0
        elif key == pygame.K_RIGHT and self.dx == 0:
            self.dx = CELL_SIZE
            self.dy = 0

    def move(self):
        head = [self.body[0][0] + self.dx, self.body[0][1] + self.dy]
        self.body.insert(0, head)

    def remove_tail(self):
        self.body.pop()

    def get_head(self):
        return self.body[0]

    def check_wall_collision(self):
        head = self.get_head()
        return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT

    def check_self_collision(self):
        head = self.get_head()
        return head in self.body[1:]

    def draw(self, screen):
        for i, block in enumerate(self.body):
            # Head is slightly lighter
            color = self.color if i > 0 else tuple(min(c + 50, 255) for c in self.color)
            pygame.draw.rect(screen, color, (block[0], block[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (block[0], block[1], CELL_SIZE, CELL_SIZE), 1)


class Game:
    def __init__(self, screen, settings, username, personal_best):
        self.screen = screen
        self.settings = settings
        self.username = username
        self.personal_best = personal_best
        self.font = pygame.font.SysFont(None, 25)
        self.big_font = pygame.font.SysFont(None, 40)

        self.snake = Snake(settings)
        self.score = 0
        self.level = 1
        self.speed = START_SPEED
        self.obstacles = []

        self.food = Food(self.snake.body, self.obstacles)
        self.poison = PoisonFood(self.snake.body, self.obstacles)
        self.powerup = None
        self.powerup_spawn_timer = pygame.time.get_ticks()
        self.powerup_spawn_delay = 10000  # spawn power-up every 10 sec

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

    def spawn_obstacles(self):
        """Add obstacles when reaching a new level"""
        count = OBSTACLE_COUNT_PER_LEVEL
        attempts = 0
        while count > 0 and attempts < 200:
            attempts += 1
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            pos = [x, y]

            # Don't place near snake (5 cells around head)
            head = self.snake.get_head()
            too_close = (abs(pos[0] - head[0]) < CELL_SIZE * 5 and
                         abs(pos[1] - head[1]) < CELL_SIZE * 5)

            if (pos not in self.snake.body and
                    pos not in self.obstacles and
                    pos != self.food.pos and
                    not too_close):
                self.obstacles.append(pos)
                count -= 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                self.snake.change_direction(event.key)
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        return None

    def update(self):
        current_time = pygame.time.get_ticks()

        # Food expired - respawn
        if self.food.is_expired():
            self.food.respawn(self.snake.body, self.obstacles)

        if self.poison.is_expired():
            self.poison.respawn(self.snake.body, self.obstacles)

        # Spawn power-up every 10 sec if none active
        if self.powerup is None and current_time - self.powerup_spawn_timer > self.powerup_spawn_delay:
            self.powerup = PowerUp(
                self.snake.body, self.obstacles,
                self.food.pos, self.poison.pos
            )
            self.powerup_spawn_timer = current_time

        # Power-up on field expired
        if self.powerup and self.powerup.is_expired_on_field():
            self.powerup = None
            self.powerup_spawn_timer = current_time

        # Power-up effect ended
        if self.powerup and self.powerup.is_effect_over():
            self._remove_powerup_effect()

        # Move snake
        self.snake.move()
        head = self.snake.get_head()

        # Check collisions
        wall_hit = self.snake.check_wall_collision()
        self_hit = self.snake.check_self_collision()
        obstacle_hit = head in self.obstacles

        if wall_hit or self_hit or obstacle_hit:
            if self.snake.shield_active and (wall_hit or self_hit):
                # Shield absorbs one hit (does not protect from obstacles)
                self.snake.shield_active = False
                # Teleport to safe position if went out of bounds
                if wall_hit:
                    self.snake.body[0][0] = max(0, min(head[0], WIDTH - CELL_SIZE))
                    self.snake.body[0][1] = max(0, min(head[1], HEIGHT - CELL_SIZE))
            else:
                self.game_over = True
                return

        # Ate regular food
        if head == self.food.pos:
            self.score += self.food.weight
            self._check_level_up()
            self.food.respawn(self.snake.body, self.obstacles)
        else:
            self.snake.remove_tail()

        # Ate poison
        if head == self.poison.pos:
            # Shrink by 2 segments
            for _ in range(2):
                if len(self.snake.body) > 1:
                    self.snake.body.pop()
            if len(self.snake.body) <= 1:
                self.game_over = True
                return
            self.poison.respawn(self.snake.body, self.obstacles)

        # Collected power-up
        if self.powerup and not self.powerup.collected and head == self.powerup.pos:
            self._apply_powerup()

    def _check_level_up(self):
        if self.score % 3 == 0 and self.score > 0:
            self.level += 1
            self.speed += 2
            if self.level >= OBSTACLE_START_LEVEL:
                self.spawn_obstacles()

    def _apply_powerup(self):
        self.powerup.activate()
        ptype = self.powerup.type
        if ptype == "speed_boost":
            self.speed += 5
        elif ptype == "slow_motion":
            self.speed = max(3, self.speed - 5)
        elif ptype == "shield":
            self.snake.shield_active = True

    def _remove_powerup_effect(self):
        if self.powerup:
            ptype = self.powerup.type
            if ptype == "speed_boost":
                self.speed -= 5
            elif ptype == "slow_motion":
                self.speed += 5
            # shield is removed when used
            self.powerup = None
            self.powerup_spawn_timer = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill(BLACK)

        # Grid overlay if enabled
        if self.settings.get("grid_overlay"):
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))

        # Obstacles
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (obs[0], obs[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, LIGHT_GRAY, (obs[0], obs[1], CELL_SIZE, CELL_SIZE), 1)

        # Food
        self.food.draw(self.screen)
        self.poison.draw(self.screen)

        # Power-up
        if self.powerup and not self.powerup.collected:
            self.powerup.draw(self.screen)

        # Snake
        self.snake.draw(self.screen)

        # Shield highlight around head
        if self.snake.shield_active:
            head = self.snake.get_head()
            pygame.draw.rect(self.screen, PURPLE,
                             (head[0] - 2, head[1] - 2, CELL_SIZE + 4, CELL_SIZE + 4), 2)

        # UI
        score_text = self.font.render(
            f"Score: {self.score}  Level: {self.level}  Best: {self.personal_best}",
            True, WHITE
        )
        self.screen.blit(score_text, (10, 10))

        # Active power-up
        if self.powerup and self.powerup.active:
            ptype = self.powerup.type
            elapsed = pygame.time.get_ticks() - self.powerup.active_start
            remaining = max(0, (POWERUP_EFFECT_DURATION - elapsed) // 1000)
            label = {"speed_boost": "SPEED+", "slow_motion": "SLOW", "shield": "SHIELD"}
            pu_text = self.font.render(
                f"{label.get(ptype, ptype)}: {remaining}s",
                True, POWERUP_COLORS.get(ptype, WHITE)
            )
            self.screen.blit(pu_text, (WIDTH - 130, 10))

        # ESC hint
        hint = self.font.render("ESC - menu", True, GRAY)
        self.screen.blit(hint, (10, HEIGHT - 25))

        pygame.display.update()

    def run(self):
        """Main game loop. Returns ('game_over', score, level) or 'quit'/'menu'"""
        while self.running:
            result = self.handle_events()
            if result:
                return result

            self.update()

            if self.game_over:
                return ("game_over", self.score, self.level)

            self.draw()
            self.clock.tick(self.speed)