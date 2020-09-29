import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
from tkinter import FLAT
from select_difficult import SelectDifficult
from play_window import PlayWindow


def declare_an_image_for_a_widget(object, image_route, size, name):
    image = Image.open(image_route)
    image = image.resize((size[0], size[1]))
    image = ImageTk.PhotoImage(image)
    setattr(object, name, image)


def bind_events_for_widget(widget, functions, label_name):
    setattr(widget, 'is_cursor_on', False)
    widget.bind('<Enter>', lambda event, label=label_name: functions[0](label))
    widget.bind('<Leave>', lambda event, label=label_name: functions[1](label))
    widget.bind('<Button-1>', lambda event,
                label=label_name: functions[2](label))
    widget.bind('<ButtonRelease-1>', lambda event,
                label=label_name: functions[3](label))


class MenuWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.bg_color = '#363747'
        self.parent = parent
        self.config(bg=self.bg_color)
        
        def enter_to_label(label):
            if label == 'play':
                self.play_label.config(image=self.play_button_cursor_on_image)
                self.play_label.is_cursor_on = True

            elif label == 'sandbox':
                self.sandbox_label.config(image=self.sandbox_cursor_on_image)
                self.sandbox_label.is_cursor_on = True
            elif label == 'github':
                self.is_cursor_on_github_button = True
                self.github_label.config(image=self.github_image_cursor_on)

        def leave_label(label):
            if label == 'play':
                self.play_label.config(image=self.play_button_image)
                self.play_label.is_cursor_on = False
            elif label == 'sandbox':
                self.sandbox_label.config(image=self.sandbox_image)
                self.sandbox_label.is_cursor_on = False
            elif label == 'github':
                self.is_cursor_on_github_button = False
                self.github_label.config(image=self.github_image)

        def press_label(label):
            if label == 'play':
                self.play_label.config(image=self.play_button_pressed_image)
            elif label == 'sandbox':
                self.sandbox_label.config(image=self.sandbox_pressed_image)
            elif label == 'github':        
                self.github_label.config(image=self.github_image_pressed)        

        def release_label(label):
            if label == 'play':
                if self.play_label.is_cursor_on:
                    self.start_difficultie_selection()
            elif label == 'sandbox':
                if self.sandbox_label.is_cursor_on:
                    self.start_game()
            elif label == 'github':
                if self.is_cursor_on_github_button:
                    self.open_github_repository()         

    # List of all the images used in this widget, 'image route', 'size', atributte name'

        images = [['Images/sudoku_title.png', (580, 110), 'sudoku_title_image'],
                  ['Images/sandbox_image.png', (200, 80), 'sandbox_image'],
                  ['Images/sandbox_cursor_on.png',
                      (200, 80), 'sandbox_cursor_on_image'],
                  ['Images/sandbox_pressed.png',
                      (200, 80), 'sandbox_pressed_image'],
                  ['Images/play_button.png', (290, 110), 'play_button_image'],
                  ['Images/play_button_cursor_on.png',
                      (290, 110), 'play_button_cursor_on_image'],
                  ['Images/play_button_pressed.png',
                      (290, 110), 'play_button_pressed_image'],
                  ['Images/github_icon.png', (60, 60), 'github_image'],
                  ['Images/github_icon_cursor_on.png', (60, 60), 'github_image_cursor_on'],
                  ['Images/github_icon_pressed.png', (60, 60), 'github_image_pressed']]

        for image in images:
            declare_an_image_for_a_widget(self, image[0], image[1], image[2])

        self.functions = [enter_to_label,
                          leave_label, press_label, release_label]

        self.sudoku_title = tk.Label(
            self, bg=self.bg_color, image=self.sudoku_title_image)
        self.sudoku_title.grid(columnspan=2, padx=(0, 10))

        self.play_label = tk.Label(
            self, bg=self.bg_color, relief=FLAT, image=self.play_button_image)
        self.play_label.grid(row=1, column=0, padx=(50, 0), pady=(30, 0))
        bind_events_for_widget(self.play_label, self.functions, 'play')

        self.sandbox_label = tk.Label(
            self, text='BEGIN', bg=self.bg_color, relief=FLAT, image=self.sandbox_image)
        self.sandbox_label.grid(row=2, column=0, padx=(50, 0), pady=(40, 0))
        bind_events_for_widget(self.sandbox_label, self.functions, 'sandbox')

        # Navegation button to go to the Github Repository

        self.github_label = tk.Label(self, bg=self.bg_color,
                                       relief=FLAT, image=self.github_image)
        self.github_label.grid(row=3, column=0, padx=(0, 400), pady=(40, 0))
        bind_events_for_widget(self.github_label, self.functions, 'github')


    def open_github_repository(self):
        webbrowser.open('https://github.com/DarwinLozada/sudoku_game_with_gui')

    def start_difficultie_selection(self):
        self.destroy()
        selection = SelectDifficult(self.parent)
        selection.grid(sticky='NSEW')

    def start_game(self):
        self.destroy()
        game = PlayWindow(self.parent, True)
        game.grid(sticky='NSEW')
       

