import pygame
import math

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)

    radius = 8
    mode = "brush"
    color = (0, 0, 255)

    drawing = False
    start_pos = None
    last_pos = None

    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)


                elif event.key == pygame.K_b:
                    radius = min(50, radius + 2)
                elif event.key == pygame.K_s:
                    radius = max(1, radius - 2)


                elif event.key == pygame.K_1:
                    mode = "brush"
                elif event.key == pygame.K_2:
                    mode = "rect"
                elif event.key == pygame.K_3:
                    mode = "circle"
                elif event.key == pygame.K_4:
                    mode = "eraser"

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

                if mode == "rect" and start_pos:
                    end_pos = event.pos
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(canvas, color, rect, 2)

                elif mode == "circle" and start_pos:
                    end_pos = event.pos
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    r = int((dx*dx + dy*dy) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, r, 2)

                last_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if last_pos is None:
                        last_pos = event.pos

                    dx = event.pos[0] - last_pos[0]
                    dy = event.pos[1] - last_pos[1]
                    distance = int(math.hypot(dx, dy))

                    for i in range(distance):
                        x = int(last_pos[0] + dx * i / distance)
                        y = int(last_pos[1] + dy * i / distance)

                        if mode == "brush":
                            pygame.draw.circle(canvas, color, (x, y), radius)
                        elif mode == "eraser":
                            pygame.draw.circle(canvas, (0, 0, 0), (x, y), radius)

                    last_pos = event.pos

        screen.fill((30, 30, 30))
        screen.blit(canvas, (0, 0))


        screen.blit(font.render("1 Brush | 2 Rect | 3 Circle | 4 Eraser", True, (255,255,255)), (10, 10))
        screen.blit(font.render("R Red | G Green | Y Yellow | W White", True, (255,255,255)), (10, 30))
        screen.blit(font.render("B Bigger | S Smaller", True, (255,255,255)), (10, 50))
        screen.blit(font.render(f"Mode: {mode} | Size: {radius}", True, (255,255,255)), (10, 70))

        pygame.display.flip()
        clock.tick(60)

main()