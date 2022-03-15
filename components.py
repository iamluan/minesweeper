from control import BOM_SYMBOL, WIDTH, start_flood_fill
from tkinter import Label, RAISED


def stop_game(grid):
    # remove events of each cell
    for i in range(WIDTH):
        for j in range(WIDTH):
            grid.grid[i][j].unbind_event()


class Grid:
    def __init__(self, data, wrapper):
        self.grid = data.copy()
        for i in range(len(data)):
            for j in range(len(data)):
                self.grid[i][j] = Cell(wrapper, i, j, data[i][j], self)
                self.grid[i][j].bind_event()
                
    def open_cell(self, x: int, y: int):
        if self.get_cell_value(x, y) == BOM_SYMBOL:
            self.grid[x][y].reveal()
            # stop game
            stop_game(self)
            return -1
        elif self.get_cell_value(x, y) != '0':
            self.grid[x][y].reveal()
            return 1
        else:
            start_flood_fill(grid=self, selected_loc=(x, y))
            print('click')
            return 1

    def is_opened(self, x: int, y: int):
        return self.grid[x][y].open

    def get_cell_value(self, x, y):
        return self.grid[x][y].value

    def get_cell(self, x: int, y: int):
        return self.grid[x][y]


class Cell:
    def __init__(self, wrapper, x, y, value, grid: Grid):
        self.label = Label(wrapper, bd=5, relief=RAISED, width=4, height=2)
        self.label.grid(row=x, column=y)
        self.x = x
        self.y = y
        self.value = value
        self.open = False
        self.grid = grid

    def reveal(self):
        self.open = True
        if self.value == '0':
            self.label['bg'] = 'yellow'
        elif self.value == BOM_SYMBOL:
            self.label.config(text=self.value, bg='black')
        else:    
            self.label.config(text=self.value, bg='yellow')

    def click(self, event):
        self.grid.open_cell(self.x, self.y)
        """
            if the above statement return -1 => stop game
        """

    def right_click(self, event):
        if self.label['bg'] == 'red':
            self.label['bg'] = 'grey'
        else:
            self.label.config(bg='red')

    def bind_event(self):
        self.label.bind('<Button-1>', self.click)
        self.label.bind('<Button-3>', self.right_click)

    def unbind_event(self):
        self.label.unbind('<Button-1>')
        self.label.unbind('<Button-3>')
