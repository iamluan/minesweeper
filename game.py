from tkinter import Tk, Frame, PhotoImage, RAISED
from control import generate_matrix, print_matrix, assign_bom, assign_bom_num
from control import WIDTH
from components import Grid

window = Tk()
window.title('Minesweeper')

# change icon image of the window
icon = PhotoImage(file='images//bomb.png')
window.iconphoto(True, icon)

# to wrap the grid of cell
frame = Frame(window, bd=5, relief=RAISED)
frame.pack()

matrix = generate_matrix(WIDTH, None)
assign_bom(matrix)
assign_bom_num(matrix)
print_matrix(matrix)

grid = Grid(data=matrix, wrapper=frame)

window.mainloop()
