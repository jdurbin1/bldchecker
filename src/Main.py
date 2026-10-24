import pygame
import pygame_gui
import sys
from math import *
import Checker
from Checker import Cube as Backend_Cube
import Gui
import Renderer
import webbrowser

Window_x = 1280
Window_y = 720
Rotate_speed = 0.1

def main():
    angle_x = 0
    angle_y = 0
    angle_z = 0
    pygame.init()
    window = pygame.display.set_mode((Window_x,Window_y))
    gui = Gui.Gui(window, Window_x, Window_y)
    clock = pygame.time.Clock()
    cube = Renderer.Cube(window)
    back_cube = Backend_Cube()
    while True:
        clock.tick(60)
        time_delta = clock.tick(60)/1000.0
        window.fill((0,0,0))
        rotation_x = [[1, 0, 0],
                        [0, cos(angle_x), -sin(angle_x)],
                        [0, sin(angle_x), cos(angle_x)]]

        rotation_y = [[cos(angle_y), 0, sin(angle_y)],
                        [0, 1, 0],
                        [-sin(angle_y), 0, cos(angle_y)]]

        rotation_z = [[cos(angle_z), -sin(angle_z), 0],
                        [sin(angle_z), cos(angle_z), 0],
                        [0, 0, 1]]
        
        cube.RenderCube(rotation_x, rotation_y, rotation_z)
        
        for event in pygame.event.get():
            in_menu = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gui.scramble_button:
                    Checker.scrambleCube(back_cube, gui.scramble_entry.get_text())
                    cube.set_state(back_cube)
                elif event.ui_element == gui.solution_button:
                    solution = gui.solution_entry.get_text()
                    valid = Checker.isValidSolution(solution)
                    if valid == 0:
                        Checker.executeSolution(back_cube, solution)
                        cube.set_state(back_cube)
                    else:
                        print(valid)
                elif event.ui_element == gui.reset_button:
                    back_cube = Checker.Cube()
                    cube.set_state(back_cube)
            elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                webbrowser.open(event.link_target)


            if gui.scramble_entry.is_focused:
                in_menu = True
            if not in_menu:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    angle_x=angle_y=angle_z=0
                if keys[pygame.K_d]:
                    angle_y += Rotate_speed
                if keys[pygame.K_a]:
                    angle_y -= Rotate_speed
                if keys[pygame.K_s]:
                    angle_x += Rotate_speed
                if keys[pygame.K_w]:
                    angle_x -= Rotate_speed
                if keys[pygame.K_q]:
                    angle_z -= Rotate_speed
                if keys[pygame.K_e]:
                    angle_z += Rotate_speed
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
            
            gui.manager.process_events(event)

        gui.manager.update(time_delta)
        gui.manager.draw_ui(window)

        pygame.display.update()

if __name__ == "__main__":
    main()
