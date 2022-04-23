import random
from queue import Queue
import threading

WIDTH = 15
TOTAL_BOM_NUM = 3*WIDTH
BOM_SYMBOL = '*'
EMPTY_SYMBOL = ' '

class Controller:

    def generate_matrix(self, width, element):
        return [[element for _ in range(width)] for _ in range(width)]

    def print_matrix(self, matrix):
        for e, row in enumerate(matrix):
            if e == 0:
                print(f" {[str(i) for i in range(WIDTH)]}")
            print(f"{e}{row}")


    def random_bomb(self,bom_num):
        bom_pos = set()
        while len(bom_pos) < bom_num:
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, WIDTH)
            bom_pos.add((x, y))
        return bom_pos


    def locate_surround(self, x, y, width):
        """
            return surround locations of a given location (x,y) in a matrix that has a width of 'width'
        """
        surround_loc = {(x+1, y), (x, y+1), 
                    (x-1, y), (x, y-1), 
                    (x+1, y+1), (x-1, y-1),
                    (x+1, y-1), (x-1, y+1)}
        # when given loc at the first row
        if x == 0:
            surround_loc.discard((x-1, y))
            surround_loc.discard((x-1, y-1))
            surround_loc.discard((x-1, y+1))
        # at the final row
        if x == width - 1:
            surround_loc.discard((x+1, y))
            surround_loc.discard((x+1, y+1))
            surround_loc.discard((x+1, y-1))
        # at the first col
        if y == 0:
            surround_loc.discard((x, y-1))
            surround_loc.discard((x-1, y-1))
            surround_loc.discard((x+1, y-1))
        # at the final col
        if y == width-1:
            surround_loc.discard((x, y+1))
            surround_loc.discard((x+1, y+1))
            surround_loc.discard((x-1, y+1))
        return surround_loc


    def assign_bombs(self, matrix):
        """
            assign bombs to random location of the given matrix
        """
        bom_pos = self.random_bomb(TOTAL_BOM_NUM)
        for pos in list(bom_pos):
            x = pos[0]
            y = pos[1]
            matrix[x][y] = BOM_SYMBOL


    def assign_bomb_num(self, matrix):
        """
            after assigning random bombs, fill the number of surround bombs of each cell in matrix
        """
        for row in range(WIDTH):
            for e in range(WIDTH):
                # skip bom cell
                if matrix[row][e] == BOM_SYMBOL:
                    continue
                bom_num = 0
                for loc in self.locate_surround(row, e, WIDTH):
                    if matrix[loc[0]][loc[1]] == BOM_SYMBOL:
                        bom_num += 1
                matrix[row][e] = str(bom_num)


    def get_orthogonal_neighbor_locations(self, x, y, width):
        """
            return surround locations of a given location (x,y) in a matrix that has a width of 'width'
        """
        surround_loc = {(x+1, y), (x, y+1),
                    (x-1, y), (x, y-1),
                    (x+1, y-1), (x-1, y+1)}
        # when given loc at the first row
        if x == 0:
            surround_loc.discard((x-1, y))
            surround_loc.discard((x-1, y+1))
        # at the final row
        if x == width - 1:
            surround_loc.discard((x+1, y))
            surround_loc.discard((x+1, y-1))
        # at the first col
        if y == 0:
            surround_loc.discard((x, y-1))
            surround_loc.discard((x+1, y-1))
        # at the final col
        if y == width-1:
            surround_loc.discard((x, y+1))
            surround_loc.discard((x-1, y+1))
        return surround_loc


    def open_all_neighbors_of_empty_cell(self, grid, x: int, y: int):
        surround_loc = self.get_orthogonal_neighbor_locations(x, y, WIDTH)
        for loc in surround_loc:
            grid.grid[loc[0]][loc[1]].reveal()


    def flood_fill(self, grid, selected_loc: tuple()):
        """
        using breath first search
        """

        x = selected_loc[0]
        y = selected_loc[1]
        cell_queue = Queue(maxsize=WIDTH**2)
        cell_queue.put((x, y))

        # a 2D matrix that represents opening status of the cells
        visited_cells = self.generate_matrix(WIDTH, False)

        while not cell_queue.empty():

            current_cell = cell_queue.get()
            x, y = current_cell[0], current_cell[1]

            # reveal the current cell
            grid.grid[x][y].reveal()
            # mark current cell as opened
            visited_cells[x][y] = True
            self.open_all_neighbors_of_empty_cell(grid, x, y)
            
            # visit all neighbors of the current cell    
            surround_loc = self.get_orthogonal_neighbor_locations(x, y, WIDTH)
            for loc in surround_loc:
                surround_x, surround_y = loc[0], loc[1]
                # if neighbor is empty and not opened
                if grid.get_cell_value(surround_x, surround_y) == '0' and \
                        visited_cells[surround_x][surround_y] is False:
                    cell_queue.put(loc)

    # using thread to avoid Tkinker freeze
    def start_flood_fill(self, grid, selected_loc: tuple()):
        threading.Thread(target=self.flood_fill, args=(grid, selected_loc)).start()
