import pygame, sys, time, random
from pygame.locals import *

from racer      import (Player, Enemy, Coin, OilSpill,
                        Barrier, NitroStrip, Powerup,
                        SCREEN_WIDTH, SCREEN_HEIGHT,
                        BLACK, WHITE, RED, GREEN, YELLOW, CYAN, ORANGE, GRAY)
from ui         import (main_menu, username_screen, settings_screen,
                        game_over_screen, leaderboard_screen, draw_panel)
from persistence import load_settings, save_settings, save_score

pygame.init()

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
FPS   = 60


font_small  = pygame.font.SysFont("Verdana", 14)
font_medium = pygame.font.SysFont("Verdana", 18, bold=True)


background = pygame.image.load("assets\AnimatedStreet.png").convert()


pygame.mixer.music.load(r"assets\background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

crash_sound = pygame.mixer.Sound("assets\crash.wav")



DIFF_CONFIG = {
    "easy":   {"speed": 4, "enemy_count": 1, "obstacle_interval": 280, "powerup_interval": 200},
    "normal": {"speed": 5, "enemy_count": 2, "obstacle_interval": 200, "powerup_interval": 260},
    "hard":   {"speed": 7, "enemy_count": 3, "obstacle_interval": 140, "powerup_interval": 320},
}





def run_game(settings, player_name):
    diff   = settings.get("difficulty", "normal")
    cfg    = DIFF_CONFIG.get(diff, DIFF_CONFIG["normal"])
    SPEED  = cfg["speed"]

    
    all_sprites = pygame.sprite.Group()
    enemies     = pygame.sprite.Group()
    coins_grp   = pygame.sprite.Group()
    obstacles   = pygame.sprite.Group()   
    nitros_grp  = pygame.sprite.Group()
    powerups_grp= pygame.sprite.Group()

    P1 = Player(settings.get("car_color", "default"))
    all_sprites.add(P1)

    for i in range(cfg["enemy_count"]):
        e = Enemy(SPEED)
        e.safe_spawn(P1.rect)
        enemies.add(e)
        all_sprites.add(e)

    for i in range(2):
        c = Coin(SPEED)
        coins_grp.add(c)
        all_sprites.add(c)

    
    score = 0
    moneta = 0
    distance= 0.0        
    lvl_step = 5
    frame_count = 0

    obstacle_timer = 0
    obstacle_interval = cfg["obstacle_interval"]
    powerup_timer  = 0
    powerup_interval = cfg["powerup_interval"]
    nitro_timer    = 0
    nitro_interval = 300      

    active_powerup      = None   
    powerup_end_time    = 0
    POWERUP_DURATION    = {
        "nitro":  4.0,
        "shield": 999.0,   
        "repair": 0.0,     
    }

    
    crashed_once = False

    running = True
    while running:
        clock.tick(FPS)
        frame_count += 1

        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()

        
        P1.update_powerups()

        for e in enemies:
            e.speed = SPEED
            e.move()
        for c in coins_grp:
            c.speed = SPEED
            c.move()
        for o in obstacles:
            o.speed = SPEED
            o.move()
        for n in nitros_grp:
            n.speed = SPEED
            n.move()
        for p in powerups_grp:
            p.speed = SPEED
            p.move()
        P1.move()

        distance += SPEED * 0.05   

        
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacle_timer = 0
            kind = random.choice(["oil", "oil", "barrier"])
            if kind == "oil":
                o = OilSpill(SPEED)
            else:
                o = Barrier(SPEED)
            obstacles.add(o)
            all_sprites.add(o)

        nitro_timer += 1
        if nitro_timer >= nitro_interval:
            nitro_timer = 0
            ns = NitroStrip(SPEED)
            nitros_grp.add(ns)
            all_sprites.add(ns)

        powerup_timer += 1
        if powerup_timer >= powerup_interval:
            powerup_timer = 0
            if active_powerup is None:    
                kind = random.choice(["nitro", "shield", "repair"])
                pu = Powerup(kind, SPEED)
                powerups_grp.add(pu)
                all_sprites.add(pu)

        
        target_enemies = cfg["enemy_count"] + int(distance // 300)
        target_enemies = min(target_enemies, 6)
        while len(enemies) < target_enemies:
            e = Enemy(SPEED)
            e.safe_spawn(P1.rect)
            enemies.add(e)
            all_sprites.add(e)

        
        obstacle_interval = max(60, cfg["obstacle_interval"] - int(distance // 200) * 10)

        
        if moneta > 0 and moneta % lvl_step == 0:
            SPEED = cfg["speed"] + moneta // lvl_step
            SPEED = min(SPEED, 14)

        
        for coin in pygame.sprite.spritecollide(P1, coins_grp, False):
            moneta += coin.weight
            score  += coin.weight * 10
            coin.reset()

        
        if pygame.sprite.spritecollideany(P1, nitros_grp):
            if not P1.nitro_active:
                P1.nitro_active = True
                P1.nitro_end    = time.time() + 3
                active_powerup  = "nitro"
                powerup_end_time= P1.nitro_end
            for ns in pygame.sprite.spritecollide(P1, nitros_grp, True):
                pass

        
        for pu in pygame.sprite.spritecollide(P1, powerups_grp, True):
            k = pu.kind
            if k == "nitro":
                P1.nitro_active = True
                P1.nitro_end    = time.time() + 4
                active_powerup  = "nitro"
                powerup_end_time= P1.nitro_end
                score += 30
            elif k == "shield":
                P1.shield_active = True
                active_powerup   = "shield"
                score += 20
            elif k == "repair":
                crashed_once    = False
                active_powerup  = "repair"
                powerup_end_time= time.time() + 0.01   
                score += 15

        
        if active_powerup == "nitro" and not P1.nitro_active:
            active_powerup = None
        if active_powerup == "repair" and time.time() > powerup_end_time:
            active_powerup = None

        
        hit_obstacle = pygame.sprite.spritecollideany(P1, obstacles)
        if hit_obstacle:
            if P1.shield_active:
                P1.shield_active = False
                active_powerup   = None
                hit_obstacle.kill()   
            else:
                
                if isinstance(hit_obstacle, OilSpill):
                    SPEED = max(2, SPEED - 2)
                    hit_obstacle.kill()
                else:   
                    return _game_over(score, distance, moneta)

        
        if pygame.sprite.spritecollideany(P1, enemies):
            if P1.shield_active:
                P1.shield_active = False
                active_powerup   = None
                
                for e in pygame.sprite.spritecollide(P1, enemies, False):
                    e.rect.y -= 80
            else:
                return _game_over(score, distance, moneta)

        
        if frame_count % 10 == 0:
            score += 1

        
        DISPLAYSURF.blit(background, (0, 0))

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)

        
        if P1.shield_active:
            pygame.draw.circle(DISPLAYSURF, (80, 80, 255),
                               P1.rect.center, 36, 3)

        
        _draw_hud(DISPLAYSURF, score, moneta, distance,
                  active_powerup, powerup_end_time,
                  P1.nitro_active, P1.nitro_end,
                  P1.shield_active)

        pygame.display.update()

    return score, distance, moneta


def _game_over(score, distance, moneta):
    if crash_sound:
        crash_sound.play()
    return score, distance, moneta


def _draw_hud(surf, score, coins, distance,
              active_pu, pu_end, nitro_active, nitro_end, shield):
    
    surf.blit(font_small.render(f"Score: {score}",    True, BLACK), (8, 8))
    surf.blit(font_small.render(f"Coins: {coins}",    True, BLACK), (8, 30))
    surf.blit(font_small.render(f"Dist:  {int(distance)}m", True, BLACK), (8, 52))

    
    if active_pu:
        pu_colors = {"nitro": CYAN, "shield": (100, 100, 255), "repair": GREEN}
        col  = pu_colors.get(active_pu, WHITE)
        icon = font_medium.render(active_pu.upper(), True, col)
        surf.blit(icon, (SCREEN_WIDTH - icon.get_width() - 8, 8))
        
        if active_pu == "nitro" and nitro_active:
            remaining = max(0, nitro_end - time.time())
            bar_w = int((remaining / 4.0) * 100)
            pygame.draw.rect(surf, GRAY, (SCREEN_WIDTH - 108, 36, 100, 10), border_radius=4)
            pygame.draw.rect(surf, CYAN, (SCREEN_WIDTH - 108, 36, bar_w, 10), border_radius=4)





def main():
    settings    = load_settings()
    player_name = "Player"

    if not settings.get("sound", True):
        pygame.mixer.music.pause()

    while True:
        action = main_menu(DISPLAYSURF, clock, background)

        if action == "quit":
            pygame.quit(); sys.exit()

        elif action == "leaderboard":
            leaderboard_screen(DISPLAYSURF, clock, background)

        elif action == "settings":
            settings = settings_screen(DISPLAYSURF, clock, background, settings)

        elif action == "play":
            name = username_screen(DISPLAYSURF, clock, background)
            if name is None:
                continue
            player_name = name

            
            while True:
                result = run_game(settings, player_name)
                if result is None:
                    break
                score, distance, coins = result
                save_score(player_name, score, distance)

                action = game_over_screen(DISPLAYSURF, clock, background,
                                          score, distance, coins)
                if action == "retry":
                    continue
                else:   
                    break


if __name__ == "__main__":
    main()