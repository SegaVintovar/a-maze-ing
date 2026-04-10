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

def run_menu(my_maze: Maze) -> None:
    show_path = False 

    colors = ["\033[0m", "\033[31m", "\033[32m", "\033[33m", "\033[34m"]
    #          default       red          green       yellow      blue
    color_index = 0

    while True:
        """Escape sequence to clean terminal screen"""
        print("\033[H\033[J", end="")
        
        my_maze.print_grid(show_path, colors[color_index])

        print("\n=== A-Maze-ing===")
        print("1. Regenerate maze")
        print("2. Show/Hide path")
        print("3. Rotate colors")
        print("4. Quit")

        choice = input("Choice? (1-4): ")
        if choice == "1":
            my_maze.grid = []
            my_maze.stack = []

            my_maze.create_grid()
            my_maze.insert_forty2(my_maze.ft())
            my_maze.path_gen()
        elif choice == "2":
            show_path = not show_path
            print("In progress...")
        elif choice == "3":
            color_index = (color_index + 1) % len(colors)
        elif choice == "4":
            break


def main() -> None:
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
        # my_maze.print_grid() -  now in run_menu!!!
        run_menu(my_maze)

        # maze_gen(data_4_maze)
    else:
        print("The Amazing reqiuers 'config.txt' as a given parameter")


if __name__ == "__main__":
    main()
