from tkinter import Button, Label, RAISED, Frame, LEFT, PhotoImage, RIGHT, TOP
from threading import Thread

class Cell:

    def __init__(self, wrapper, x, y, value, bom_symbol: str):

        self.bom_symbol = bom_symbol
        self.label = Label(wrapper, bd=5, relief=RAISED, width=4, height=2, bg='white')
        
        self.x = x
        self.y = y
        self.value = value
        self.open = False

        self.state_list = []

    def reveal(self):
        
        self.state_list.append((self.open, self.label['bg'], self.label['text']))
        # print(self.state_list)

        self.open = True
        if self.value == '0':
            self.label['bg'] = 'yellow'
        elif self.value == self.bom_symbol:
            self.label.config(text=self.value, bg='black')
        else:    
            self.label.config(text=self.value, bg='yellow')

        self.unbind_event()
        

    def flagged(self):
        if self.label['bg'] == 'red':
            self.label['bg'] = 'white'
        else:
            self.label.config(bg='red')
    
    def unbind_event(self):
        self.label.unbind('<Button-1>')
        self.label.unbind('<Button-3>')

    def back(self):
        if len(self.state_list) > 0:
            open, bg, text = self.state_list.pop()
            print(f'{open}, {bg}, {text}')
            self.open = open
            self.label['bg'] = bg
            self.label['text'] = text
    

class Panel:
    def __init__(self, window, total_bom_num: int):
        self.total_bom_num = total_bom_num
        self.panel = Frame(window)

        self.flag_container = Frame(self.panel)
        

        self.flag_icon = PhotoImage(file='images\\flag_icon.png')
        self.flag_display = Label(self.flag_container, text="flag number", image=self.flag_icon)
        self.flag_display.pack(side=LEFT)
        
        self.display_num = Label(self.flag_container, text=f'{self.total_bom_num}', font=100, relief=RAISED)
        self.display_num.pack(side=RIGHT)

        self.flag_container.pack(side=LEFT)

        self.undo_button = Button(self.panel, text='Undo')
        self.undo_button.pack(side=RIGHT)
        
        self.panel.pack(side=TOP)
        
    
    def change_display_num(self, num):
        self.display_num['text'] = f'{num}'

    

class Grid:
    def __init__(self, wrapper, width: int):
        self.width = width
        self.cells = [[None for i in range(width)] for j in range(width)]
        self.wrapper = wrapper

    def add_cell(self, cell: Cell, x: int, y: int):
        self.cells[x][y] = cell
        cell.label.grid(row=x, column=y)

    def is_opened(self, x: int, y: int):
        return self.cells[x][y].open

    def get_cell_value(self, x, y):
        return self.cells[x][y].value

    def get_cell(self, x: int, y: int):
        return self.grid[x][y]

    def remove_all_events(self):
        """
            remove events of each cell
        """
        for i in range(self.width):
            for j in range(self.width):
                self.cells[i][j].unbind_event()
    