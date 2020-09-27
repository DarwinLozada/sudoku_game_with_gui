import tkinter as tk
from tkinter.font import Font
import multiprocessing
from tkinter import FLAT, messagebox
from PIL import Image, ImageTk
from sudoku_games import easy_sudokus, medium_sudokus, hard_sudokus
import random
from key_highlighting import highlight_keys
from sudoku_solver import Sudoku
from main import main


class PlayWindow(tk.Frame):
    empty_sudoku_board = [['' for i in range(9)] for j in range(9)]

    def __init__(self, parent, is_a_sandbox_sudoku, sudoku=empty_sudoku_board):
        tk.Frame.__init__(self, parent)
        from menu import declare_an_image_for_a_widget, bind_events_for_widget
        from menu import MenuWindow
        from select_difficult import SelectDifficult

        self.empty_sudoku_board = [['' for i in range(9)] for j in range(9)]
        self.TEXT_COLOR = '#05619a'
        self.parent = parent
        self.BG = '#42445e'
        self.config(bg=self.BG)

        self.font = Font(family='Dubai Light bold', size=18)
        self.is_there_focused_label = False
        self.previous_label = None
        self.labels = [[] for _ in range(9)]
        self.text_variables = [[] for _ in range(9)]

        self.stopped_timer = False
        self.is_in_play_mode = False
        self.is_window_blocked = False

        self._offsetx = 0
        self._offsety = 0

        # Time variables

        self.seconds = 0
        self.minutes = 0

        def announce_win():
            self.is_window_blocked = True
            play_again = tk, messagebox.askyesno(message=f'Congratulations, you did it in {self.minutes}:{self.seconds}! Do you want to play again?',
                                                 title='Congrats!')
            if play_again:
                self.destroy()
                game = PlayWindow(self.parent, False, sudoku)
                game.grid()
            else:
                return_to_menu()

        def update_time():
            if not self.is_window_blocked:
                if self.is_in_play_mode:
                    if self.seconds == 59:
                        self.minutes += 1
                        self.seconds = 0

                    else:
                        self.seconds += 1
                    new_time = f'{str(self.minutes)}:{str(self.seconds)}'
                    self.time.set(new_time)
                    self.timer.after(1000, update_time)
            else:
                self.timer.after(1000, update_time)

        def desselect_label():
            self.is_there_focused_label = False
            self.previous_label.is_locked = True

        def start_play_mode():
            self.start_label.destroy()
            clean_highlighted_labels()
            self.is_in_play_mode = True
            for l, _ in enumerate(self.board):
                for k, _ in enumerate(self.board[l]):
                    if type(self.board[l][k]) == int:
                        self.labels[l][k].is_locked = True

            if is_a_sandbox_sudoku:
                self.solve_label = tk.Label(
                    self, relief=FLAT, bg=self.BG, image=self.solve_button_off_image)
                self.solve_label.grid(row=10, column=1, sticky='NSEW',
                                      columnspan=3, padx=(20, 0), pady=(0, 10))
                bind_events_for_widget(
                    self.solve_label, self.binding_functions, 'solve')

            # Timer widget

            timer_font = Font(family='Dubai', size=18)

            self.time = tk.StringVar()
            self.timer = tk.Label(self, textvariable=self.time,
                                  font=timer_font, relief=FLAT, bg=self.BG, fg='#a2a3b7')

            self.timer.grid(row=10, column=4, sticky='NSEW',
                            columnspan=9, padx=(100, 0), pady=(5, 15))
            self.time.set(f'{self.minutes}:{self.seconds}')
            self.after(
                1000, update_time)

        def change_focused_label_with_key(key, position):
            if key == 'Up':
                next_label = position[0] - 1
                if next_label < 0:
                    next_label = 8
                while self.labels[next_label][position[1]].is_locked:
                    next_label -= 1
                    if next_label < 0:
                        next_label = 8
                position = (next_label, position[1])
                label_to_go = self.labels[position[0]][position[1]]
                var = self.text_variables[position[0]][position[1]]
                focus_label((position[0], position[1]), label_to_go, var)

            elif key == 'Down':
                next_label = position[0] + 1
                if next_label > 8:
                    next_label = 0
                while self.labels[next_label][position[1]].is_locked:
                    next_label += 1
                    if next_label > 8:
                        next_label = 0
                position = (next_label, position[1])

                label_to_go = self.labels[position[0]][position[1]]
                var = self.text_variables[position[0]][position[1]]
                focus_label((position[0], position[1]), label_to_go, var)

            elif key == 'Left':
                next_label = position[1] - 1
                if next_label < 0:
                    next_label = 8
                while self.labels[position[0]][next_label].is_locked:
                    next_label -= 1
                    if next_label < 0:
                        next_label = 8
                position = (position[0], next_label)
                label_to_go = self.labels[position[0]][position[1]]
                var = self.text_variables[position[0]][position[1]]
                focus_label((position[0], position[1]), label_to_go, var)

            elif key == 'Right':
                next_label = position[1] + 1
                if next_label > 8:
                    next_label = 0
                while self.labels[position[0]][next_label].is_locked:
                    next_label += 1
                    if next_label > 8:
                        next_label = 0
                position = (position[0], next_label)

                label_to_go = self.labels[position[0]][position[1]]
                var = self.text_variables[position[0]][position[1]]
                focus_label((position[0], position[1]), label_to_go, var)

        def update_the_board():
            for index, list in enumerate(self.labels):
                for sub_index, sub_list in enumerate(list):
                    variable = tk.StringVar(value=self.board[index][sub_index])
                    label = self.labels[index][sub_index]
                    label.configure(textvariable=variable)

        def solve_the_sudoku():
            self.is_in_play_mode = False
            board = Sudoku(self.board)
            solve_sudoku = multiprocessing.Process(
                target=board.return_the_solution)
            solve_sudoku.start()
            solve_sudoku.join(4)
            if solve_sudoku.is_alive():
                solve_sudoku.terminate()
                tk.messagebox.showinfo(
                    message='There is no solution for this sudoku', title='Advice')

            else:
                self.board = board.return_the_solution()
                update_the_board()

            # Lock all the labels

                for i, _ in enumerate(self.labels):
                    for l, _ in enumerate(self.labels):
                        self.labels[i][l].is_locked = True

                clean_highlighted_labels()

                tk.messagebox.showinfo(
                    message='This is the solution!', title='Done!')

            # Leave the bord in blank if the user wants to play again

                self.board = self.empty_sudoku_board
                return_to_menu()

        def insert_number(number, variable, position):

            variable.set(number)
            if number.isdigit():
                self.board[position[0]][position[1]] = int(number)

        # If user press the backspace

            else:
                self.board[position[0]][position[1]] = ''

            highlight_keys(self.board, position,
                           self.labels, self.TEXT_COLOR)

            if self.is_in_play_mode:
                board = self.board
                board = Sudoku(board)
                if board.check_if_solved():
                    announce_win()

        def clean_highlighted_labels():
            self.is_there_focused_label = False
            for i, _ in enumerate(self.board):
                for k, _ in enumerate(self.board):
                    self.labels[i][k].is_highlighted = False
                    self.labels[i][k].config(
                        bg=self.BG_LABEL_COLOR, fg=self.TEXT_COLOR)

        def focus_label(position, label, variable):
            if not self.is_window_blocked:
                if not self.is_there_focused_label and not label.is_locked:
                    if self.previous_label:
                        self.previous_label.is_locked = False

                    label.is_locked = True
                    # The focused label is now the previous label
                    self.previous_label = self.labels[position[0]][position[1]]

                    # Set the window focus on the PlayWindow

                    self.focus_set()

                    for num in range(1, 10):
                        self.bind(str(num),
                                  lambda event, number=str(num), var=variable, pos=position: insert_number(
                            number,
                            var, pos))
                    self.bind('<BackSpace>', lambda event, value='', var=variable, pos=position: insert_number(value, var,
                                                                                                               pos))

                    highlight_keys(self.board, position,
                                   self.labels, self.TEXT_COLOR)
                    self.is_there_focused_label = True

                elif self.is_there_focused_label and not label.is_locked:
                    self.previous_label.config(bg='white', fg=self.TEXT_COLOR)
                    self.is_there_focused_label = False
                    focus_label(position, label, variable)

                for key in ['Up', 'Down', 'Left', 'Right']:
                    self.bind('<' + key + '>', lambda event, key=key,
                              pos=position: change_focused_label_with_key(key, position))

        def change_leave_color(label):
            if not self.is_window_blocked:
                if not label.is_locked and not label.is_highlighted:
                    if self.previous_label:
                        if self.previous_label.is_locked:
                            label.config(bg=self.BG_LABEL_COLOR)
                            label.is_highlighted = False
                    else:
                        label.config(bg=self.BG_LABEL_COLOR)
                        label.is_highlighted = False

        def change_enter_color(label):
            if not self.is_window_blocked:
                if not label.is_locked and not label.is_highlighted:
                    label.config(bg='#ffdddd')

        # Label binding functions

        def enter_label(widget):
            if not self.is_window_blocked:
                if widget == 'start':
                    self.start_label.config(image=self.start_button_on_image)
                    self.start_label.is_cursor_on = True
                elif widget == 'exit':
                    self.exit_button.config(image=self.exit_button_on_image)
                    self.exit_button.is_cursor_on = True
                elif widget == 'solve':
                    self.solve_label.config(
                        image=self.solve_button_cursor_on_image)
                    self.solve_button_is_cursor_on = True

        def leave_label(widget):
            if not self.is_window_blocked:
                if widget == 'start':
                    self.start_label.config(image=self.start_button_off_image)
                    self.start_label.is_cursor_on = False
                elif widget == 'exit':
                    self.exit_button.config(image=self.exit_button_off_image)
                    self.exit_button.is_cursor_on = False
                elif widget == 'solve':
                    self.solve_label.config(image=self.solve_button_off_image)
                    self.solve_button_is_cursor_on = False

        def press_label(widget):
            if not self.is_window_blocked:
                if widget == 'start':
                    self.start_label.config(
                        image=self.start_button_pressed_image)
                elif widget == 'exit':
                    self.exit_button.config(
                        image=self.exit_button_pressed_image)
                elif widget == 'solve':
                    self.solve_label.config(
                        image=self.solve_button_pressed_image)

        def release_label(widget):
            if not self.is_window_blocked:
                if widget == 'start':
                    if self.start_label.is_cursor_on:
                        start_play_mode()
                elif widget == 'exit':
                    if self.exit_button.is_cursor_on:
                        ask_if_exit()
                elif widget == 'solve':
                    if self.solve_button_is_cursor_on:
                        solve_the_sudoku()

        def return_to_menu():
            self.destroy()
            menu = MenuWindow(parent)
            menu.grid(sticky='NSEW')

        def ask_if_exit():
            # Block all the app's functions

            self.is_window_blocked = True

            exit_to_menu = tk, messagebox.askyesno(message='Are you sure you want to exit? You will lose all your progress',
                                                   title='Warning')

            # messagebox.askyesno returns a tuple, the first element is the route of the tkinter module (I don't know why)
            # and the second element is the boolean value, True or False

            if exit_to_menu[1] == True:
                return_to_menu()
            elif exit_to_menu[1] == False:
                self.is_window_blocked = False

                # List of all the images used in this widget, 'image route', 'size', atributte name'

        images = [['Images/Start_button_off.png', (140, 65), 'start_button_off_image'],
                  ['Images/Start_button_on.png',
                      (140, 65), 'start_button_on_image'],
                  ['Images/Start_button_pressed.png',
                      (140, 65), 'start_button_pressed_image'],
                  ['Images/leave_button.png',
                      (40, 40), 'exit_button_off_image'],
                  ['Images/leave_button_cursor_on.png',
                   (40, 40), 'exit_button_on_image'],
                  ['Images/leave_button_pressed.png',
                      (40, 40), 'exit_button_pressed_image'],
                  ['Images/solve_button.png',
                      (140, 65), 'solve_button_off_image'],
                  ['Images/solve_button_cursor_on.png',
                      (140, 65), 'solve_button_cursor_on_image'],
                  ['Images/solve_button_pressed.png', (140, 65), 'solve_button_pressed_image']]

        for image in images:
            declare_an_image_for_a_widget(self, image[0], image[1], image[2])

        self.binding_functions = [enter_label, leave_label,
                                  press_label, release_label]

        #  Configuring the button that starts the game and the timer

        self.start_label = tk.Label(self, relief=FLAT, bg=self.BG, width=140, height=65,
                                    image=self.start_button_off_image)

        self.start_label.grid(row=10, column=6, sticky='NSEW',
                              padx=3, pady=(1, 20), columnspan=3)

        bind_events_for_widget(
            self.start_label, self.binding_functions, 'start')

    #  Configuring the button to leave the game and go to the menu

        self.exit_button = tk.Label(
            self, relief=FLAT, bg=self.BG, text='HOLA', image=self.exit_button_off_image)
        self.exit_button.grid(row=10, sticky='NSEW', column=0,
                              padx=(20, 0), pady=(0, 10))
        bind_events_for_widget(
            self.exit_button, self.binding_functions, 'exit')

        if sudoku == 'easy':
            self.board = random.choice(easy_sudokus)
        elif sudoku == 'medium':
            self.board = random.choice(medium_sudokus)
        elif sudoku == 'hard':
            self.board = random.choice(hard_sudokus)
        else:
            self.board = self.empty_sudoku_board

        self.BG_LABEL_COLOR = '#ffffff'

        for row, sublist in enumerate(self.board):
            for column, sub_value in enumerate(sublist):
                label_variable = tk.StringVar(value=self.board[row][column])
                new_label = tk.Label(self, relief=FLAT, bg=self.BG_LABEL_COLOR, font=self.font,
                                     width=40, height=40, fg=self.TEXT_COLOR, textvariable=label_variable)

                setattr(new_label, 'is_highlighted', False)
                setattr(new_label, 'is_locked', False)

                b_padx = 1
                b_pady = 1

                if row == 0:
                    b_pady = (7, 1)

                if row == 8:
                    b_pady = (1, 10)

                if row == 3 or row == 6:
                    b_pady = (3, 1)

                if row == 2 or row == 5:
                    b_pady = (1, 3)

                if column == 0:
                    b_padx = (3, 1)

                if column == 8:
                    b_padx = (1, 3)

                if column == 2 or column == 5:
                    b_padx = (1, 3)

                if column == 3 or column == 6:
                    b_padx = (3, 1)

                new_label.grid(row=row, column=column,
                               sticky='NSEW', padx=b_padx, pady=b_pady)

                new_label.bind('<Button-1>', lambda event, position=(row, column), label=new_label,
                               variable=label_variable: focus_label(position, label,
                                                                    variable))
                new_label.bind('<Enter>', lambda event,
                               label=new_label: change_enter_color(label))
                new_label.bind('<Leave>', lambda event,
                               label=new_label: change_leave_color(label))

                self.labels[row].append(new_label)
                self.text_variables[row].append(label_variable)

        for i in range(10):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        if not self.board == self.empty_sudoku_board:
            start_play_mode()
