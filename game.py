from tkinter import Tk, Frame, PhotoImage, RAISED
from control import Controller, WIDTH
from components import Grid

class Game:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.window.title('Minesweeper')

        # change icon image of the window
        icon = PhotoImage(file='images//bomb.png')
        self.window.iconphoto(True, icon)

        # to wrap the grid of cell
        frame = Frame(self.window, bd=5, relief=RAISED)
        frame.pack()

        matrix = self.controller.generate_matrix(WIDTH, None)
        self.controller.assign_bombs(matrix)
        self.controller.assign_bomb_num(matrix)
        self.controller.print_matrix(matrix)

        grid = Grid(data=matrix, wrapper=frame, controller=self.controller)
        self.window.mainloop()

    # to stop the program when the window is closed
    def quit_game(self):
        print('Quit')
        self.window.quit()
        self.window.destroy()

game = Game(controller=Controller())
