from tkinter import Tk, Frame, PhotoImage, RAISED
from control import generate_matrix, print_matrix, assign_bombs, assign_bomb_num
from control import WIDTH
from components import Grid


# to stop the program when the window is closed
def quit_game():
    print('Quit')
    window.quit()
    window.destroy()


window = Tk()
window.protocol("WM_DELETE_WINDOW", quit_game)
window.title('Minesweeper')

# change icon image of the window
icon = PhotoImage(file='images//bomb.png')
window.iconphoto(True, icon)

# to wrap the grid of cell
frame = Frame(window, bd=5, relief=RAISED)
frame.pack()

matrix = generate_matrix(WIDTH, None)
assign_bombs(matrix)
assign_bomb_num(matrix)
print_matrix(matrix)

grid = Grid(data=matrix, wrapper=frame)

window.mainloop()
