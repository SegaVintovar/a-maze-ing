import sys
# from sys import argv
from enum import Enum
from maze import Maze, Cell
from parsing import parsing

# Bit Direction
# 0 (LSB) North
# 1 East
# 2 South
# 3 West



            # loop through the grid, check all visited cells
            # check len(get_neighbours) > 0:
            #   then dig into avaliable cells
            # or look up for all the unvisited cells
            #   and check if they have visited neighbours
            #   and the dig there 
            # self.path_gen()
            # i += 0

        

# 7 x 4
# #_#_###
# ###___#
# __#_#__
# __#_###
# tiles = {
# 0x0: " ",
# 0x1: "╵",
# 0x2: "╶",
# 0x3: "└",
# 0x4: "╷",
# 0x5: "│",
# 0x6: "┌",
# 0x7: "├",
# 0x8: "╴",
# 0x9: "┘",
# 0xA: "─",
# 0xB: "┴",
# 0xC: "┐",
# 0xD: "┤",
# 0xE: "┬",
# 0xF: "┼",
# }

def print_grid_of_pos(grid: list[list[Cell]]) -> None:
    for row in grid:
        for cell in row:
            print(cell.position, end="")
        print()


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "config.txt":
            with open(sys.argv[1], "r") as config_file:
                config_data = config_file.read()
            # try:
                data_4_maze = parsing(config_data)
                print(data_4_maze)
            # except Exception as e:
            #     print("Parsing error: ", str(e))
            #     return
            # else:
        else:
            raise Exception("We are expecting config.txt as an argument")
        try:
            my_maze = Maze(**data_4_maze)
            my_maze.create_grid()
            my_maze.insert_forty2(my_maze.ft())
        except Exception as e:
            print(str(e))
            exit(1)
        my_maze.path_gen()
        my_maze.print_grid()
        
        # maze_gen(data_4_maze)
    else:
        print("The Amazing reqiuers '' as a given parameter")


if __name__ == "__main__":
    main()
