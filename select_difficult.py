import tkinter as tk
from PIL import Image, ImageTk
from tkinter.font import Font
from tkinter import FLAT
from play_window import PlayWindow


class SelectDifficult(tk.Frame):
    def __init__(self, parent):
        from menu import declare_an_image_for_a_widget, bind_events_for_widget
        from menu import MenuWindow

        tk.Frame.__init__(self, parent)
        self.font = Font(family='Small Fontz', size=20)
        self.bg_color = '#363747'
        self.parent = parent
        self.config(bg=self.bg_color)

        def enter_to_label(label):
            if label == 'easy':
                self.easy_mode.config(image=self.easy_mode_cursor_on_image)
                self.easy_mode_label.config(fg='#5ef6c1')
                self.easy_mode.is_cursor_on = True
            elif label == 'medium':
                self.medium_mode.config(image=self.medium_mode_cursor_on_image)
                self.medium_mode_label.config(fg='#f5a77c')
                self.medium_mode.is_cursor_on = True
            elif label == 'hard':
                self.hard_mode.config(image=self.hard_mode_cursor_on_image)
                self.hard_mode_label.config(fg='#fd7e92')
                self.hard_mode.is_cursor_on = True
            elif label == 'go_back':
                self.go_back.config(image=self.go_back_cursor_on_image)
                self.go_back.is_cursor_on = True

        def leave_label(label):
            if label == 'easy':
                self.easy_mode_label.config(fg='#01d185')
                self.easy_mode.config(image=self.easy_mode_image)
                self.easy_mode.is_cursor_on = False
            elif label == 'medium':
                self.medium_mode_label.config(fg='#ee8245')
                self.medium_mode.config(image=self.medium_mode_image)
                self.medium_mode.is_cursor_on = False
            elif label == 'hard':
                self.hard_mode_label.config(fg='#fc607d')
                self.hard_mode.config(image=self.hard_mode_image)
                self.hard_mode.is_cursor_on = False
            elif label == 'go_back':
                self.go_back.config(image=self.go_back_image)
                self.go_back.is_cursor_on = False

        def press_label(label):
            if label == 'easy':
                self.easy_mode.config(image=self.easy_mode_pressed_image)
            elif label == 'medium':
                self.medium_mode.config(image=self.medium_mode_pressed_image)
            elif label == 'hard':
                self.hard_mode.config(image=self.hard_mode_pressed_image)
            elif label == 'go_back':
                self.go_back.config(image=self.go_back_pressed_image)

        def release_label(label):
            if label == 'easy':
                if self.easy_mode.is_cursor_on:
                    start_game(label)
            elif label == 'medium':
                if self.medium_mode.is_cursor_on:
                    start_game(label)
            elif label == 'hard':
                if self.hard_mode.is_cursor_on:
                    start_game(label)
            elif label == 'go_back':
                if self.go_back.is_cursor_on:
                    return_to_menu()

        def start_game(difficulty):
            self.destroy()
            game = PlayWindow(self.parent, False, difficulty)
            game.grid()

        def return_to_menu():
            self.destroy()
            menu = MenuWindow(self.parent)
            menu.grid(sticky='NSEW')

        # List of all the images used in this widget, 'image route', 'size', atributte name'

        images = [['Images/easy_face.png', (110, 110), 'easy_mode_image'],
                  ['Images/easy_face_cursor_on.png',
                      (110, 110), 'easy_mode_cursor_on_image'],
                  ['Images/easy_face_pressed.png',
                      (110, 110), 'easy_mode_pressed_image'],
                  ['Images/medium_face.png', (110, 110), 'medium_mode_image'],
                  ['Images/medium_face_cursor_on.png',
                      (110, 110), 'medium_mode_cursor_on_image'],
                  ['Images/medium_face_pressed.png',
                      (110, 110), 'medium_mode_pressed_image'],
                  ['Images/hard_face.png', (110, 110), 'hard_mode_image'],
                  ['Images/hard_face_cursor_on.png',
                      (110, 110), 'hard_mode_cursor_on_image'],
                  ['Images/hard_face_pressed.png',
                      (110, 110), 'hard_mode_pressed_image'],
                  ['Images/choose_difficulty.png',
                      (500, 80), 'choose_difficulty_image'],
                  ['Images/go_back.png', (80, 80), 'go_back_image'],
                  ['Images/go_back_cursor_on.png',
                      (80, 80), 'go_back_cursor_on_image'],
                  ['Images/go_back_pressed.png',
                      (80, 80), 'go_back_pressed_image'],
                  ]

        for image in images:
            declare_an_image_for_a_widget(self, image[0], image[1], image[2])

        # Widget's cursor functions for binding
        self.binding_functions = [enter_to_label,
                                  leave_label, press_label, release_label]

        # Difficulties title label

        self.difficulties = tk.Label(self, relief=FLAT, bg=self.bg_color,
                                     height=80, width=500, image=self.choose_difficulty_image)
        self.difficulties.grid(row=0, column=0, pady=(
            15, 40), padx=(20, 0), columnspan=3)

        # Easy mode label

        self.easy_mode = tk.Label(
            self, relief=FLAT, bg=self.bg_color, image=self.easy_mode_image, font=self.font)
        self.easy_mode.grid(row=2, column=0, padx=(50, 30))
        bind_events_for_widget(self.easy_mode, self.binding_functions, 'easy')

        self.easy_mode_label = tk.Label(self, relief=FLAT, bg=self.bg_color, fg='#01d185', text='Easy',
                                        font=self.font)
        self.easy_mode_label.grid(row=3, column=0, padx=(20, 0))

        # Medium mode label

        self.medium_mode = tk.Label(
            self, bg=self.bg_color, relief=FLAT, image=self.medium_mode_image, font=self.font)
        self.medium_mode.grid(row=2, column=1, padx=30)
        bind_events_for_widget(
            self.medium_mode, self.binding_functions, 'medium')
        self.medium_mode_label = tk.Label(self, relief=FLAT, bg=self.bg_color, fg='#ee8245', text='Medium',
                                          font=self.font)

        self.medium_mode_label.grid(row=3, column=1, padx=(0, 5))

        # Hard mode label

        self.hard_mode = tk.Label(self, bg=self.bg_color, relief=FLAT, text='Hard', font=self.font,
                                  image=self.hard_mode_image)
        self.hard_mode.grid(row=2, column=2, padx=(20, 40))
        bind_events_for_widget(self.hard_mode, self.binding_functions, 'hard')

        self.hard_mode_label = tk.Label(self, relief=FLAT, bg=self.bg_color, fg='#fc607d', text='Hard',
                                        font=self.font)
        self.hard_mode_label.grid(row=3, column=2, padx=(0, 20))

        # Go back arrow label

        self.go_back = tk.Label(self, bg=self.bg_color,
                                relief=FLAT, image=self.go_back_image)
        self.go_back.grid(row=5, column=0, pady=(0, 20), padx=(0, 60))
        bind_events_for_widget(self.go_back, self.binding_functions, 'go_back')

        self.grid_rowconfigure(4, weight=2)
