import pygame
import math

def get_color(mode):
    if mode == 'red': return (255, 0, 0)
    elif mode == 'green': return (0, 255, 0)
    elif mode == 'white': return (255, 255, 255)
    elif mode == 'yellow': return (255, 255, 0)
    elif mode == 'black': return (0, 0, 0)
    return (0, 0, 255) 

def fill(surface, x, y, fill_color):
    w, h = surface.get_size()
    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(*fill_color)
    
    if target_color == fill_color:
        return
        
    stack = [(x, y)]
    while stack:
        nx, ny = stack.pop()
        if surface.get_at((nx, ny)) == target_color:
            surface.set_at((nx, ny), fill_color)
            if nx + 1 < w: stack.append((nx + 1, ny))
            if nx - 1 >= 0: stack.append((nx - 1, ny))
            if ny + 1 < h: stack.append((nx, ny + 1))
            if ny - 1 >= 0: stack.append((nx, ny - 1))

def draw_shape(surface, tool, sx, sy, ex, ey, c, width):
    if tool == 'line':
        pygame.draw.line(surface, c, (sx, sy), (ex, ey), width)
    elif tool == 'rect':
        pygame.draw.rect(surface, c, (min(sx, ex), min(sy, ey), abs(ex-sx), abs(ey-sy)), width)
    elif tool == 'circle':
        r_circ = int(math.hypot(ex-sx, ey-sy))
        pygame.draw.circle(surface, c, (sx, sy), r_circ, width)
    elif tool == 'square':
        side = min(abs(ex-sx), abs(ey-sy))
        pygame.draw.rect(surface, c, (min(sx, ex), min(sy, ey), side, side), width)
    elif tool == 'right_tri':
        
        pygame.draw.polygon(surface, c, [(sx, sy), (sx, ey), (ex, ey)], width)
    elif tool == 'eq_tri':
        w = abs(ex-sx)
        h = abs(ey-sy)
        max_s = int(h * 2 / math.sqrt(3))
        s = min(w, max_s)
        if s > 0:
            h_tri = int(s * math.sqrt(3) / 2)
            left = min(sx, ex)
            top = min(sy, ey)
            pygame.draw.polygon(surface, c, [(left + s//2, top), (left, top+h_tri), (left+s, top+h_tri)], width)
    elif tool == 'rhombus':
        cx = (sx + ex) // 2
        cy = (sy + ey) // 2
        pygame.draw.polygon(surface, c, [(cx, min(sy,ey)), (max(sx,ex), cy), (cx, max(sy,ey)), (min(sx,ex), cy)], width)