import pygame
from pygame.locals import *
from persistence import load_leaderboard, save_settings

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
GRAY   = (160, 160, 160)
DARK   = (30,  30,  50)
RED    = (220,  40,  40)
GREEN  = (40,  200,  80)
YELLOW = (240, 210,   0)
CYAN   = (0,   200, 240)
ORANGE = (255, 140,   0)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600


# ── tiny helper ───────────────────────────────────────────────────────────────
def draw_button(surf, text, rect, color, hover_color, font, mouse_pos, text_color=BLACK):
    col = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(surf, col, rect, border_radius=10)
    pygame.draw.rect(surf, WHITE, rect, 2, border_radius=10)
    label = font.render(text, True, text_color)
    surf.blit(label, (rect.centerx - label.get_width() // 2,
                      rect.centery - label.get_height() // 2))


def draw_panel(surf, rect, alpha=200):
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    panel.fill((10, 10, 30, alpha))
    surf.blit(panel, rect.topleft)
    pygame.draw.rect(surf, (80, 80, 120), rect, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Main Menu
# ─────────────────────────────────────────────────────────────────────────────
def main_menu(screen, clock, background):
    font_title = pygame.font.SysFont("Verdana", 44, bold=True)
    font_btn   = pygame.font.SysFont("Verdana", 22)

    buttons = {
        "play":        pygame.Rect(120, 200, 160, 48),
        "leaderboard": pygame.Rect(90,  265, 220, 48),
        "settings":    pygame.Rect(120, 330, 160, 48),
        "quit":        pygame.Rect(140, 395, 120, 48),
    }

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for action, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return action

        screen.blit(background, (0, 0))
        draw_panel(screen, pygame.Rect(60, 80, 280, 90))
        title = font_title.render("RACER", True, YELLOW)
        sub   = pygame.font.SysFont("Verdana", 16).render("Street Racing Game", True, GRAY)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 92))
        screen.blit(sub,   (SCREEN_WIDTH // 2 - sub.get_width() // 2,   145))

        draw_button(screen, "PLAY",        buttons["play"],        GREEN,  (80, 240, 120), font_btn, mouse)
        draw_button(screen, "LEADERBOARD", buttons["leaderboard"], CYAN,   (80, 220, 255), font_btn, mouse)
        draw_button(screen, "SETTINGS",    buttons["settings"],    ORANGE, (255, 180, 60), font_btn, mouse)
        draw_button(screen, "QUIT",        buttons["quit"],        RED,    (255, 80, 80),  font_btn, mouse, WHITE)

        pygame.display.update()


# ─────────────────────────────────────────────────────────────────────────────
# Username Entry
# ─────────────────────────────────────────────────────────────────────────────
def username_screen(screen, clock, background):
    font_title = pygame.font.SysFont("Verdana", 28, bold=True)
    font_input = pygame.font.SysFont("Verdana", 26)
    font_hint  = pygame.font.SysFont("Verdana", 16)
    font_btn   = pygame.font.SysFont("Verdana", 22)

    name    = ""
    box     = pygame.Rect(80, 280, 240, 44)
    ok_btn  = pygame.Rect(130, 360, 140, 44)
    active  = True

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name.strip():
                    return name.strip()
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 16 and event.unicode.isprintable():
                    name += event.unicode
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if ok_btn.collidepoint(event.pos) and name.strip():
                    return name.strip()

        screen.blit(background, (0, 0))
        draw_panel(screen, pygame.Rect(60, 160, 280, 260))

        title = font_title.render("Enter Your Name", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))

        hint = font_hint.render("Type your name and press Enter", True, GRAY)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 240))

        # input box
        pygame.draw.rect(screen, WHITE, box, border_radius=8)
        pygame.draw.rect(screen, CYAN,  box, 2,  border_radius=8)
        txt_surf = font_input.render(name + "|", True, BLACK)
        screen.blit(txt_surf, (box.x + 8, box.y + 8))

        draw_button(screen, "START", ok_btn,
                    GREEN if name.strip() else GRAY,
                    (80, 240, 120), font_btn, mouse)

        pygame.display.update()


# ─────────────────────────────────────────────────────────────────────────────
# Settings Screen
# ─────────────────────────────────────────────────────────────────────────────
def settings_screen(screen, clock, background, settings):
    font_title = pygame.font.SysFont("Verdana", 28, bold=True)
    font       = pygame.font.SysFont("Verdana", 18)
    font_btn   = pygame.font.SysFont("Verdana", 20)

    back_btn = pygame.Rect(130, 510, 140, 44)
    colors   = ["default", "blue", "green", "yellow"]
    diffs    = ["easy", "normal", "hard"]

    col_btns  = [pygame.Rect(40 + i * 82, 310, 74, 36) for i in range(4)]
    diff_btns = [pygame.Rect(40 + i * 110, 400, 100, 36) for i in range(3)]
    sound_btn = pygame.Rect(150, 220, 100, 36)

    col_colors_map = {
        "default": (220, 30, 30),
        "blue":    (30, 80, 220),
        "green":   (30, 180, 60),
        "yellow":  (220, 200, 0),
    }

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                save_settings(settings)
                return settings
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return settings
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    if settings["sound"]:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                for i, btn in enumerate(col_btns):
                    if btn.collidepoint(event.pos):
                        settings["car_color"] = colors[i]
                for i, btn in enumerate(diff_btns):
                    if btn.collidepoint(event.pos):
                        settings["difficulty"] = diffs[i]

        screen.blit(background, (0, 0))
        draw_panel(screen, pygame.Rect(20, 80, 360, 460))

        title = font_title.render("SETTINGS", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Sound toggle
        sound_lbl = font.render("Sound:", True, WHITE)
        screen.blit(sound_lbl, (50, 228))
        s_color = GREEN if settings["sound"] else RED
        s_text  = "ON" if settings["sound"] else "OFF"
        draw_button(screen, s_text, sound_btn, s_color, s_color, font_btn, mouse)

        # Car color
        col_lbl = font.render("Car color:", True, WHITE)
        screen.blit(col_lbl, (50, 285))
        for i, btn in enumerate(col_btns):
            c = col_colors_map[colors[i]]
            sel = settings["car_color"] == colors[i]
            pygame.draw.rect(screen, c, btn)
            if sel:
                pygame.draw.rect(screen, WHITE, btn, 3)
            else:
                pygame.draw.rect(screen, GRAY, btn, 1)
            lbl = pygame.font.SysFont("Verdana", 11).render(colors[i].capitalize(), True, WHITE)
            screen.blit(lbl, (btn.centerx - lbl.get_width() // 2, btn.centery - lbl.get_height() // 2))

        # Difficulty
        diff_lbl = font.render("Difficulty:", True, WHITE)
        screen.blit(diff_lbl, (50, 375))
        diff_cols = [GREEN, YELLOW, RED]
        for i, btn in enumerate(diff_btns):
            sel  = settings["difficulty"] == diffs[i]
            bcol = diff_cols[i]
            draw_button(screen, diffs[i].capitalize(), btn, bcol if sel else DARK, bcol, font_btn, mouse, WHITE)

        draw_button(screen, "BACK", back_btn, ORANGE, (255, 180, 60), font_btn, mouse)
        pygame.display.update()


# ─────────────────────────────────────────────────────────────────────────────
# Game Over Screen
# ─────────────────────────────────────────────────────────────────────────────
def game_over_screen(screen, clock, background, score, distance, coins):
    font_title = pygame.font.SysFont("Verdana", 40, bold=True)
    font_stat  = pygame.font.SysFont("Verdana", 20)
    font_btn   = pygame.font.SysFont("Verdana", 22)

    retry_btn = pygame.Rect(60,  440, 120, 46)
    menu_btn  = pygame.Rect(220, 440, 120, 46)

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if retry_btn.collidepoint(event.pos):
                    return "retry"
                if menu_btn.collidepoint(event.pos):
                    return "menu"

        screen.blit(background, (0, 0))
        draw_panel(screen, pygame.Rect(40, 100, 320, 380))

        title = font_title.render("GAME OVER", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        pygame.draw.line(screen, GRAY, (60, 175), (340, 175), 1)

        stats = [
            ("Score",    str(score)),
            ("Distance", f"{int(distance)} m"),
            ("Coins",    str(coins)),
        ]
        for i, (label, val) in enumerate(stats):
            lbl_s = font_stat.render(label + ":", True, GRAY)
            val_s = font_stat.render(val, True, WHITE)
            y = 195 + i * 50
            screen.blit(lbl_s, (80, y))
            screen.blit(val_s, (300 - val_s.get_width(), y))

        draw_button(screen, "RETRY",     retry_btn, GREEN,  (80, 240, 120), font_btn, mouse)
        draw_button(screen, "MAIN MENU", menu_btn,  ORANGE, (255, 180, 60), font_btn, mouse)

        pygame.display.update()


# ─────────────────────────────────────────────────────────────────────────────
# Leaderboard Screen
# ─────────────────────────────────────────────────────────────────────────────
def leaderboard_screen(screen, clock, background):
    font_title = pygame.font.SysFont("Verdana", 28, bold=True)
    font_row   = pygame.font.SysFont("Verdana", 17)
    font_hdr   = pygame.font.SysFont("Verdana", 15, bold=True)
    font_btn   = pygame.font.SysFont("Verdana", 22)

    back_btn = pygame.Rect(130, 540, 140, 44)
    board    = load_leaderboard()

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    return

        screen.blit(background, (0, 0))
        draw_panel(screen, pygame.Rect(20, 70, 360, 490))

        title = font_title.render("LEADERBOARD", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 82))

        # header row
        hdr_y = 122
        for text, x in [("#", 40), ("Name", 80), ("Score", 220), ("Dist", 320)]:
            h = font_hdr.render(text, True, CYAN)
            screen.blit(h, (x, hdr_y))
        pygame.draw.line(screen, GRAY, (30, 144), (370, 144), 1)

        if not board:
            msg = font_row.render("No scores yet!", True, GRAY)
            screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 280))
        else:
            medal_colors = [YELLOW, GRAY, (180, 100, 40)]
            for i, entry in enumerate(board[:10]):
                y = 154 + i * 34
                col = medal_colors[i] if i < 3 else WHITE
                rank  = font_row.render(str(i + 1), True, col)
                name  = font_row.render(str(entry.get("name", "?"))[:12], True, col)
                score = font_row.render(str(entry.get("score", 0)), True, col)
                dist  = font_row.render(str(entry.get("distance", 0)) + "m", True, col)
                screen.blit(rank,  (40, y))
                screen.blit(name,  (70, y))
                screen.blit(score, (220, y))
                screen.blit(dist,  (310, y))

        draw_button(screen, "BACK", back_btn, ORANGE, (255, 180, 60), font_btn, mouse)
        pygame.display.update()