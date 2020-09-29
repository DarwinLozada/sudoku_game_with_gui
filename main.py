import tkinter as tk
from parent_widgets import NewRoot, TopLevelWindow
from sudoku_solver import Sudoku
import platform


def main():
    from menu import MenuWindow
    from title_bar import TitleBar

    if platform.system() == 'Windows':
        root = NewRoot()
        app = TopLevelWindow(root)
        menu = MenuWindow(app)
        root.title('Sudoku')
        bar = TitleBar(app, root)
        bar.grid(row=0, column=0, sticky='NSEW')
        menu.grid(sticky='NSEW')
        root.bind('<FocusIn>', lambda event: app.attributes('-topmost', True))
        root.bind('<FocusOut>', lambda event: app.attributes('-topmost', False))
        app.grid_rowconfigure(1, weight=2)
        app.grid_columnconfigure(0, weight=1)
        app.grid_rowconfigure(1, weight=2, minsize=500)
        app.grid_columnconfigure(0, weight=1, minsize=100)

        app.mainloop()
 
    elif platform.system() == 'Linux':
        root = tk.Tk()
        root.title('Sudoku')
        
        root.minsize(550, 550)
        root.maxsize(550, 550)
        menu = MenuWindow(root)
        menu.grid(sticky='NSEW')
        root.grid_rowconfigure(0, weight=1, minsize=550)
        root.grid_columnconfigure(0, weight=1)
        root.icon = tk.PhotoImage(file='Images/sudoku_icon.png')
        root.mainloop()
  
 

if __name__ == '__main__':
    main()
    