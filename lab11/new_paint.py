import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20) 
    
    radius = 15
    mode = 'blue'
    tool = 'brush'

    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))
    
    drawing = False
    start_pos = (0, 0)
    last_pos = (0, 0)

    while True:
        
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
         
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
               
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                
                elif event.key == pygame.K_w:
                    mode = 'white'
                elif event.key == pygame.K_y:
                    mode = 'yellow'
                    
                
                elif event.key == pygame.K_UP:
                    radius = min(200, radius + 2)
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius - 2)

  
                elif event.key == pygame.K_1: tool = 'brush'
                elif event.key == pygame.K_2: tool = 'rect'
                elif event.key == pygame.K_3: tool = 'circle'
                elif event.key == pygame.K_4: tool = 'eraser'
                elif event.key == pygame.K_5: tool = 'square'
                elif event.key == pygame.K_6: tool = 'right_tri'
                elif event.key == pygame.K_7: tool = 'eq_tri'
                elif event.key == pygame.K_8: tool = 'rhombus'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click
                   
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    

                    ex, ey = end_pos[0], end_pos[1]
                    sx, sy = start_pos[0], start_pos[1]
     
                    c = (0,0,255)
                    if mode == 'red': c = (255,0,0)
                    elif mode == 'green': c = (0,255,0)
                    elif mode == 'white': c = (255,255,255)
                    elif mode == 'yellow': c = (255,255,0)
                    
                    if tool == 'rect':
                        pygame.draw.rect(canvas, c, (min(sx, ex), min(sy, ey), abs(ex-sx), abs(ey-sy)), 2)
                    elif tool == 'circle':
                        r_circ = int(math.hypot(ex-sx, ey-sy))
                        pygame.draw.circle(canvas, c, start_pos, r_circ, 2)
                    elif tool == 'square':
                        side = min(abs(ex-sx), abs(ey-sy))
                        pygame.draw.rect(canvas, c, (min(sx, ex), min(sy, ey), side, side), 2)
                    elif tool == 'right_tri':
                        pygame.draw.polygon(canvas, c, [(min(sx,ex), min(sy,ey)), (min(sx,ex), max(sy,ey)), (max(sx,ex), max(sy,ey))], 2)
                    elif tool == 'eq_tri':
 
                        w = abs(ex-sx)
                        h = abs(ey-sy)
                        max_s = int(h * 2 / math.sqrt(3))
                        s = min(w, max_s)
                        if s > 0:
                            h_tri = int(s * math.sqrt(3) / 2)
                            left = min(sx, ex)
                            top = min(sy, ey)
                            pygame.draw.polygon(canvas, c, [(left + s//2, top), (left, top+h_tri), (left+s, top+h_tri)], 2)
                    elif tool == 'rhombus':
                        cx = (sx + ex) // 2
                        cy = (sy + ey) // 2
                        pygame.draw.polygon(canvas, c, [(cx, min(sy,ey)), (max(sx,ex), cy), (cx, max(sy,ey)), (min(sx,ex), cy)], 2)

            if event.type == pygame.MOUSEMOTION:

                if drawing:
                    if tool == 'brush':
                        drawLineBetween(canvas, 0, last_pos, event.pos, radius, mode)
                    elif tool == 'eraser':
                        drawLineBetween(canvas, 0, last_pos, event.pos, radius, 'black')
                    last_pos = event.pos
                

        screen.blit(canvas, (0, 0))
        

        screen.blit(font.render("Tools: 1:Brush 2:Rect 3:Circ 4:Eraser 5:Sq 6:RTri 7:EqTri 8:Rhomb", True, (255,255,255)), (5, 5))
        screen.blit(font.render("Colors: R, G, B, W(hite), Y(ellow) | Size: UP/DOWN arrows", True, (255,255,255)), (5, 25))
        screen.blit(font.render("Mode: " + tool + " | Color: " + mode + " | Size: " + str(radius), True, (200,200,200)), (5, 45))
        
        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):

    if color_mode == 'blue':
        color = (0, 0, 255)
    elif color_mode == 'red':
        color = (255, 0, 0)
    elif color_mode == 'green':
        color = (0, 255, 0)
    elif color_mode == 'white':
        color = (255, 255, 255)
    elif color_mode == 'yellow':
        color = (255, 255, 0)
    elif color_mode == 'black':
        color = (0, 0, 0)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    if iterations == 0: 
        iterations = 1 
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()