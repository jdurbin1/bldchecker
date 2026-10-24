import pygame
import pygame_gui

class Gui:
    def __init__(self, window, Window_x, Window_y):
        self.window = window
        self.Window_x = Window_x
        self.Window_y = Window_y
        self.manager = pygame_gui.UIManager((Window_x, Window_y), "style.json")
        # Rect: left, top, width, height

        # Scramble
        self.scramble_entry = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
                                            relative_rect=self.rect(1,1,30,5),
                                            placeholder_text='Enter your scramble here',
                                            manager=self.manager)
        self.scramble_button = pygame_gui.elements.UIButton(relative_rect=self.rect(1,7,7,5),
                                             text='Scramble',
                                             manager=self.manager)
        # Solution
        self.solution_entry = pygame_gui.elements.ui_text_entry_box.UITextEntryBox(
                                            relative_rect=self.rect(1,19,30,10),
                                            placeholder_text='Enter your solution here',
                                            manager=self.manager)
        self.solution_button = pygame_gui.elements.UIButton(relative_rect=self.rect(1,30,10,5),
                                                     text='Execute Solution',
                                                     manager=self.manager)
        # Reset
        self.reset_button = pygame_gui.elements.UIButton(relative_rect=self.rect(45,92,10,5),
                                                     text='Reset Cube',
                                                     manager=self.manager)

        # Info
        self.version_box = pygame_gui.elements.ui_text_box.UITextBox(relative_rect=self.rect(89,1,9,5),
                                                            html_text="Version 1.0.0",
                                                            manager=self.manager,
                                                            object_id="center")

        self.about_box = pygame_gui.elements.ui_text_box.UITextBox(relative_rect=self.rect(70,7,29,40),
                                                                    manager=self.manager,
                                                                    html_text="<b>Welcome to the blindfolded checker!</b>\n" \
                                                                    "Scrambles must follow the same format as displayed on cstimer.\n" \
                                                                    "Solutions consists of 2 lines and may only contain alphabetical characters. " \
                                                                    "The first line is your edge solution, the second line is your corner solution.\n" \
                                                                    "This application uses the default Speffz lettering notation for solution mapping. " \
                                                                    "Visit <a href='https://www.speedsolving.com/wiki/index.php/Speffz'>The Speedsolving Wiki</a> " \
                                                                    "for more information.")

        self.hotkeys_box = pygame_gui.elements.ui_text_box.UITextBox(relative_rect=self.rect(70,60,29,30),
                                                                     manager=self.manager,
                                                                     object_id="test",
                                                                     html_text="<b>Hotkeys:</b>\n" \
                                                                     "W/S: Rotate around the X axis\n" \
                                                                     "A/D: Rotate around the Y axis\n" \
                                                                     "Q/E: Rotate around the Z axis\n" \
                                                                     "R: Reset camera\n" \
                                                                     "Esc: Quit")
        

    # Percent from the left of the screen
    def x_percent(self, val):
        return val/100 * self.Window_x

    # Percent from the top of the screen
    def y_percent(self, val):
        return val/100 * self.Window_y

    # Custom rectangle maker
    def rect(self, left, top, width, height):
        return pygame.Rect((self.x_percent(left), self.y_percent(top)), (self.x_percent(width), self.y_percent(height)))
