import pygame
import sys
from config import *
from game import Game
from db import create_tables, save_game_result, get_top10, get_personal_best
from settings import load_settings, save_settings


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
font_small = pygame.font.SysFont(None, 25)
font_mid = pygame.font.SysFont(None, 35)
font_big = pygame.font.SysFont(None, 55)


def draw_button(surface, text, x, y, w, h, color, hover_color, font):
    """Draw a button and return True if clicked"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mouse)
    bg = hover_color if is_hover else color

    pygame.draw.rect(surface, bg, rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, rect, 1, border_radius=6)

    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    surface.blit(label, label_rect)

    if is_hover and click[0]:
        pygame.time.delay(120)  # small delay to avoid double click
        return True
    return False


def screen_main_menu():
    username = ""
    error_msg = ""
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        # Title
        title = font_big.render("SNAKE", True, GREEN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 55)))

        # Name input
        prompt = font_mid.render("Write your name:", True, WHITE)
        screen.blit(prompt, (WIDTH // 2 - 110, 105))

        input_rect = pygame.Rect(WIDTH // 2 - 110, 140, 220, 35)
        pygame.draw.rect(screen, DARK_GRAY, input_rect, border_radius=4)
        pygame.draw.rect(screen, LIGHT_GRAY, input_rect, 1, border_radius=4)
        name_surf = font_mid.render(username + "|", True, WHITE)
        screen.blit(name_surf, (input_rect.x + 8, input_rect.y + 5))

        if error_msg:
            err = font_small.render(error_msg, True, RED)
            screen.blit(err, err.get_rect(center=(WIDTH // 2, 185)))

        # Buttons
        btn_y = 210
        btn_w, btn_h = 180, 38
        btn_x = WIDTH // 2 - btn_w // 2

        play_clicked = draw_button(screen, "Play", btn_x, btn_y, btn_w, btn_h,
                                   DARK_GRAY, (0, 150, 0), font_mid)
        lb_clicked = draw_button(screen, "Leaderboard", btn_x, btn_y + 50, btn_w, btn_h,
                                 DARK_GRAY, GRAY, font_small)
        settings_clicked = draw_button(screen, "Settings", btn_x, btn_y + 100, btn_w, btn_h,
                                       DARK_GRAY, GRAY, font_mid)
        quit_clicked = draw_button(screen, "Quit", btn_x, btn_y + 150, btn_w, btn_h,
                                   DARK_GRAY, (150, 0, 0), font_mid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username.strip():
                        return "play", username.strip()
                    else:
                        error_msg = "Write something as a name"
                elif len(username) < 20:
                    if event.unicode.isprintable():
                        username += event.unicode

        if play_clicked:
            if username.strip():
                return "play", username.strip()
            else:
                error_msg = "Write a name!"

        if lb_clicked:
            return "leaderboard", username.strip()

        if settings_clicked:
            return "settings", username.strip()

        if quit_clicked:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(30)


def screen_leaderboard():
    clock = pygame.time.Clock()
    top10 = get_top10()

    while True:
        screen.fill(BLACK)

        title = font_big.render("Leaders", True, YELLOW)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 30)))

        # Table headers
        header_surf = font_small.render(
            f"{'#':<3} {'Player':<22} {'Score':<8} {'Lvl':<5} {'Date'}",
            True, LIGHT_GRAY
        )
        screen.blit(header_surf, (20, 65))
        pygame.draw.line(screen, GRAY, (15, 82), (WIDTH - 15, 82), 1)

        if not top10:
            no_data = font_mid.render("No data", True, GRAY)
            screen.blit(no_data, no_data.get_rect(center=(WIDTH // 2, 200)))
        else:
            for i, (name, score, level, date) in enumerate(top10):
                color = YELLOW if i == 0 else (LIGHT_GRAY if i < 3 else WHITE)
                row = f"{i + 1:<3} {name[:20]:<22} {score:<8} {level:<5} {date}"
                row_surf = font_small.render(row, True, color)
                screen.blit(row_surf, (20, 90 + i * 24))

        back_clicked = draw_button(screen, "Back", WIDTH // 2 - 70, HEIGHT - 50, 140, 35,
                                   DARK_GRAY, GRAY, font_mid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        if back_clicked:
            return

        pygame.display.update()
        clock.tick(30)


def screen_settings(settings):
    clock = pygame.time.Clock()
    local = settings.copy()
    local["snake_color"] = list(local["snake_color"])

    color_options = [
        ([0, 255, 0], "GREEN"),
        ([0, 100, 255], "BLUE"),
        ([255, 165, 0], "ORANGE"),
        ([255, 0, 255], "PINK"),
        ([255, 255, 255], "WHITE"),
    ]

    while True:
        screen.fill(BLACK)

        title = font_big.render("Settings", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 35)))

        # Grid toggle
        grid_label = font_mid.render("Grid:", True, WHITE)
        screen.blit(grid_label, (60, 95))
        grid_btn_text = "ON" if local["grid_overlay"] else "OFF"
        grid_color = (0, 150, 0) if local["grid_overlay"] else (150, 0, 0)
        grid_clicked = draw_button(screen, grid_btn_text, 220, 90, 80, 30,
                                   grid_color, GRAY, font_mid)
        if grid_clicked:
            local["grid_overlay"] = not local["grid_overlay"]

        # Sound toggle
        sound_label = font_mid.render("Sound:", True, WHITE)
        screen.blit(sound_label, (60, 140))
        sound_btn_text = "ON" if local["sound"] else "OFF"
        sound_color = (0, 150, 0) if local["sound"] else (150, 0, 0)
        sound_clicked = draw_button(screen, sound_btn_text, 220, 135, 80, 30,
                                    sound_color, GRAY, font_mid)
        if sound_clicked:
            local["sound"] = not local["sound"]

        # Snake color
        color_label = font_mid.render("Color:", True, WHITE)
        screen.blit(color_label, (60, 185))
        for i, (rgb, name) in enumerate(color_options):
            cx = 60 + i * 100
            btn_rect = pygame.Rect(cx, 215, 90, 28)
            is_selected = local["snake_color"] == rgb
            bg = tuple(rgb) if is_selected else DARK_GRAY
            pygame.draw.rect(screen, bg, btn_rect, border_radius=4)
            pygame.draw.rect(screen, WHITE if is_selected else GRAY, btn_rect, 1, border_radius=4)
            lbl = font_small.render(name, True, WHITE)
            screen.blit(lbl, lbl.get_rect(center=btn_rect.center))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if btn_rect.collidepoint(mouse) and click[0]:
                local["snake_color"] = rgb
                pygame.time.delay(150)

        # Save button
        save_clicked = draw_button(screen, "Save and quit",
                                   WIDTH // 2 - 110, HEIGHT - 60, 220, 38,
                                   (0, 100, 0), (0, 160, 0), font_mid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return settings  # without saving

        if save_clicked:
            save_settings(local)
            return local

        pygame.display.update()
        clock.tick(30)


def screen_game_over(score, level, personal_best):
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        go_title = font_big.render("GAME OVER", True, RED)
        screen.blit(go_title, go_title.get_rect(center=(WIDTH // 2, 70)))

        info = [
            f"Score: {score}",
            f"Level: {level}",
            f"Best score: {personal_best}",
        ]
        for i, line in enumerate(info):
            surf = font_mid.render(line, True, WHITE)
            screen.blit(surf, surf.get_rect(center=(WIDTH // 2, 150 + i * 45)))

        btn_w, btn_h = 180, 40
        btn_x = WIDTH // 2 - btn_w // 2

        retry_clicked = draw_button(screen, "Try again", btn_x, 300, btn_w, btn_h,
                                    DARK_GRAY, (0, 130, 0), font_mid)
        menu_clicked = draw_button(screen, "Menu", btn_x, 350, btn_w, btn_h,
                                   DARK_GRAY, GRAY, font_mid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if retry_clicked:
            return "retry"
        if menu_clicked:
            return "menu"

        pygame.display.update()
        clock.tick(30)


def main():
    # Create DB tables if they don't exist
    create_tables()

    settings = load_settings()
    username = ""

    state = "menu"

    while True:
        if state == "menu":
            action, username = screen_main_menu()
            if action == "play":
                state = "play"
            elif action == "leaderboard":
                screen_leaderboard()
            elif action == "settings":
                settings = screen_settings(settings)

        elif state == "play":
            personal_best = get_personal_best(username) if username else 0
            game = Game(screen, settings, username, personal_best)
            result = game.run()

            if result == "quit":
                pygame.quit()
                sys.exit()
            elif result == "menu":
                state = "menu"
            elif isinstance(result, tuple) and result[0] == "game_over":
                _, score, level = result
                if score > personal_best:
                    personal_best = score
                if username:
                    save_game_result(username, score, level)
                go_result = screen_game_over(score, level, personal_best)
                if go_result == "retry":
                    state = "play"
                else:
                    state = "menu"


if __name__ == "__main__":
    main()