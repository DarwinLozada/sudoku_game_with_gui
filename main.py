import tkinter as tk
from parent_widgets import NewRoot, TopLevelWindow
from sudoku_solver import Sudoku


def main():
    from menu import MenuWindow
    from title_bar import TitleBar

    root = NewRoot()
    app = TopLevelWindow(root)
    menu = MenuWindow(app)
    root.title('Sudoku')
    bar = TitleBar(app, root)
    root.bind('<FocusIn>', lambda event: app.attributes('-topmost', True))
    root.bind('<FocusOut>', lambda event: app.attributes('-topmost', False))

    bar.grid(row=0, column=0, sticky='NSEW')
    menu.grid(sticky='NSEW')

    app.grid_rowconfigure(1, weight=2)
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=2, minsize=500)
    app.grid_columnconfigure(0, weight=1, minsize=100)

    app.mainloop()
 

if __name__ == '__main__':
    main()
    