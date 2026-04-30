import pygame
from datetime import datetime
from tools import get_color, fill, draw_shape


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24) 
    
    
    brush_size = 2 
    mode = 'red'
    tool = 'pencil' 

    canvas = pygame.Surface((800, 600))
    canvas.fill((0, 0, 0))
    
    
    history = []
    
    def save_state():
        history.append(canvas.copy())
        if len(history) > 20:
            history.pop(0)

    drawing = False
    start_pos = (0, 0)
    last_pos = (0, 0)

    typing = False
    text_input = ""
    text_pos = (0, 0)

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and alt_held:
                    pygame.quit()
                    return
                if event.key == pygame.K_ESCAPE and not typing:
                    pygame.quit()
                    return
                
                if event.key == pygame.K_s and ctrl_held:
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"canvas_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Canvas saved as {filename}")
                    continue

                
                if event.key == pygame.K_z and ctrl_held:
                    if history: 
                        canvas.blit(history.pop(), (0, 0))
                    continue

                if typing:
                    if event.key == pygame.K_RETURN:
                        save_state() 
                        txt_surface = font.render(text_input, True, get_color(mode))
                        canvas.blit(txt_surface, text_pos)
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                    continue 

                if event.key == pygame.K_r: mode = 'red'
                elif event.key == pygame.K_g: mode = 'green'
                elif event.key == pygame.K_b: mode = 'blue'
                elif event.key == pygame.K_w: mode = 'white'
                elif event.key == pygame.K_y: mode = 'yellow'
                
                
                elif event.key == pygame.K_z and not ctrl_held: brush_size = 2
                elif event.key == pygame.K_x: brush_size = 5
                elif event.key == pygame.K_c: brush_size = 10

                elif event.key == pygame.K_1: tool = 'rect'
                elif event.key == pygame.K_2: tool = 'circle'
                elif event.key == pygame.K_3: tool = 'square'
                elif event.key == pygame.K_4: tool = 'right_tri'
                elif event.key == pygame.K_5: tool = 'eq_tri'
                elif event.key == pygame.K_6: tool = 'rhombus'
                
                elif event.key == pygame.K_p: tool = 'pencil'
                elif event.key == pygame.K_l: tool = 'line'
                elif event.key == pygame.K_f: tool = 'fill'
                elif event.key == pygame.K_t: tool = 'text'
                elif event.key == pygame.K_e: tool = 'eraser'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if tool == 'text':
                        typing = True
                        text_pos = event.pos
                        text_input = ""
                    elif tool == 'fill':
                        save_state() 
                        fill(canvas, event.pos[0], event.pos[1], get_color(mode))
                    else:
                        typing = False
                        save_state() 
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    end_pos = event.pos
                    
                    if tool not in ['pencil', 'eraser']:
                        draw_shape(canvas, tool, start_pos[0], start_pos[1], end_pos[0], end_pos[1], get_color(mode), brush_size)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'pencil':
                        pygame.draw.line(canvas, get_color(mode), last_pos, event.pos, brush_size)
                    elif tool == 'eraser':
                        pygame.draw.line(canvas, get_color('black'), last_pos, event.pos, brush_size * 2)
                    last_pos = event.pos

        screen.blit(canvas, (0, 0))
        
        if drawing and tool not in ['pencil', 'eraser', 'fill', 'text']:
            mx, my = pygame.mouse.get_pos()
            draw_shape(screen, tool, start_pos[0], start_pos[1], mx, my, get_color(mode), brush_size)
            
        if typing:
            txt_surf = font.render(text_input + "|", True, get_color(mode))
            screen.blit(txt_surf, text_pos)

        ui_bg = pygame.Surface((800, 75))
        ui_bg.set_alpha(180)
        screen.blit(ui_bg, (0, 0))
        
        color_text = "R/G/B/W/Y"
        size_text = "Z(2), X(5), C(10)"
        tools_1 = "P:Pencil L:Line E:Eraser F:Fill T:Text"
        tools_2 = "1:Rect 2:Circ 3:Sq 4:RTri 5:EqTri 6:Rhomb"
        
        screen.blit(font.render(f"Mode: {tool.upper()} | Color: {mode.upper()} | Size: {brush_size}", True, (255, 255, 0)), (10, 5))
        screen.blit(font.render(f"Colors: {color_text} | Sizes: {size_text} | Save: Ctrl+S | Undo: Ctrl+Z", True, (255, 255, 255)), (10, 30))
        screen.blit(font.render(f"Tools: {tools_1} | {tools_2}", True, (200, 200, 200)), (10, 55))
        
        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()