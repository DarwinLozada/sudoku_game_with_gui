import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
from menu import declare_an_image_for_a_widget, bind_events_for_widget


class TitleBar(tk.Frame):
    def close_app(self):
        if self.close_circle.is_cursor_on:
            self.parent.overrideredirect(0)
            self.parent.destroy()
            self.master.destroy()

    def check_if_zoomed(self):
        if 'normal' == self.parent.wm_state() and not self.parent.overrideredirect():
            self.parent.overrideredirect(1)
            self.master.overrideredirect(0)
        self.parent.after(5, func=lambda: self.check_if_zoomed())

    def minimize_window(self):
        if self.minimize_circle.is_cursor_on:
            self.parent.overrideredirect(0)
            self.parent.wm_state('iconic')
            self.master.overrideredirect(1)

    def drag_window(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.parent.geometry('+{x}+{y}'.format(x=x, y=y))

    def click_win(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def __init__(self, parent, master):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.master = master
        self.font = Font(family='Small Fontz', size=10)
        self.bg_color = '#282c34'
        self.config(bg=self.bg_color)

        def leave_circle(circle):
            if circle == 'close':
                self.close_circle.config(image=self.close_circle_off_image)
                self.close_circle.is_cursor_on = False

            elif circle == 'minimize':
                self.minimize_circle.config(image=self.minimize_off_image)
                self.minimize_circle.is_cursor_on = False

        def enter_to_circle(circle):
            if circle == 'close':
                self.close_circle.config(image=self.close_circle_on_image)
                self.close_circle.is_cursor_on = True
            elif circle == 'minimize':
                self.minimize_circle.config(image=self.minimize_on_image)
                self.minimize_circle.is_cursor_on = True

        def press_circle(circle):
            if circle == 'close':
                self.close_circle.config(image=self.close_circle_pressed_image)
            elif circle == 'minimize':
                self.minimize_circle.config(
                    image=self.minimize_circle_pressed_image)

        def release_circle(circle):
            if circle == 'close':
                self.close_app()
            elif circle == 'minimize':
                self.minimize_window()

    # List of all the images used in this widget, 'image route', 'size', atributte name'

        images = [['Images/close_circle_off.png', (20, 20), 'close_circle_off_image'],
                  ['Images/close_circle_on.png',
                      (20, 20), 'close_circle_on_image'],
                  ['Images/close_circle_pressed.png',
                      (20, 20), 'close_circle_pressed_image'],
                  ['Images/minimize_circle_off.png',
                      (20, 20), 'minimize_off_image'],
                  ['Images/minimize_circle_on.png',
                      (20, 20), 'minimize_on_image'],
                  ['Images/minimize_circle_pressed.png', (20, 20), 'minimize_circle_pressed_image']]

        for image in images:
            declare_an_image_for_a_widget(self, image[0], image[1], image[2])

        self.functions = [enter_to_circle,
                          leave_circle, press_circle, release_circle]

        # Minimize circle

        self.minimize_circle = tk.Label(
            self, image=self.minimize_off_image, bg=self.bg_color, height=25)
        self.minimize_circle.grid(row=0, column=1, sticky='NSEW')
        bind_events_for_widget(self.minimize_circle,
                               self.functions, 'minimize')

        # Close circle

        self.close_circle = tk.Label(
            self, image=self.close_circle_off_image, bg=self.bg_color, height=25, width=40)
        self.close_circle.grid(row=0, column=2, sticky='E')
        bind_events_for_widget(self.close_circle, self.functions, 'close')

        self.grid_columnconfigure(0, weight=2)

        self.bind('<Button-1>', self.click_win)
        self.bind('<B1-Motion>', self.drag_window)
        self.parent.after(5, func=lambda: self.check_if_zoomed())
