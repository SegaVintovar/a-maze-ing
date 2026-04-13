import sys
from maze import Maze, Cell
from parsing import parsing
from os import system

# Bit Direction
# 0 (LSB) North
# 1 East
# 2 South
# 3 West

def decode(cell: Cell) -> str:
    result = ""
    north = int(cell.n)
    east = int(cell.e)
    south = int(cell.s)
    west = int(cell.w)
    result = str(west) + str(south) + str(east) + str(north)
    return result


def write_into_file(grid: list[list[Cell]], output_file) -> None:
    result = ""
    for row in grid:
        for cell in row:
            string = decode(cell)
            result += str(int(string, base=16))
        result += "\n"
    try:
        with open("output_file", mode="w") as f:
            f.write(result)
    except Exception as e:
        raise e


def run_menu(my_maze: Maze) -> None:
    show_path = False 

    colors = ["\033[0m", "\033[31m", "\033[32m", "\033[33m", "\033[34m"]
    #          default       red          green       yellow      blue
    color_index = 0

    while True:
        """Escape sequence to clean terminal screen"""
        print("\033[H\033[J", end="")
        system("virt_env/bin/bash clear")
        my_maze.print_grid(show_path, colors[color_index])
        # my_maze.print_grid()

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


def print_grid_of_pos(grid: list[list[Cell]]) -> None:
    for row in grid:
        for cell in row:
            print(cell.position, end="")
        print()


def main() -> None:
    if len(sys.argv) == 2:
        if sys.argv[1] == "config.txt":
            with open(sys.argv[1], "r") as config_file:
                config_data = config_file.read()
            # try:
                data_4_maze = parsing(config_data)
                # print(data_4_maze)
            # except Exception as e:
            #     print("Parsing error: ", str(e))
            #     return
            # else:
        else:
            raise Exception("We are expecting config.txt as an argument")
        try:
            my_maze = Maze(**data_4_maze)
            cols = my_maze.width * 6
            lines = my_maze.height
            system(f"mode con: cols={cols} lines={lines}")
            my_maze.create_grid()
            my_maze.insert_forty2(my_maze.ft())
            my_maze.path_gen()
            write_into_file(my_maze.grid, my_maze.output_file)
            my_maze.print_grid()
            run_menu(my_maze)

        except Exception as e:
            print(str(e))
            exit(1)
    else:
        print("The Amazing reqiuers 'config.txt' as a given parameter")


if __name__ == "__main__":
    main()
