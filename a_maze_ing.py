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
    # print(west)
    result = str(west) + str(south) + str(east) + str(north)
    # print(result)
    return result


def get_right_dir(cell: Cell, maze: Maze) -> tuple[str, Cell] | None:
    x, y = cell.position
    # result = ()
    # checing from 4 sides
    if x - 1 >= 0:
        if (maze.grid[y][x - 1].path is True and
                cell.parent != maze.grid[y][x - 1]):
            if maze.grid[y][x - 1].e is False and cell.w is False:
                return ("W", maze.grid[y][x - 1])
    if x + 1 < maze.width:
        if (maze.grid[y][x + 1].path is True and
                cell.parent != maze.grid[y][x + 1]):
            if maze.grid[y][x + 1].w is False and cell.e is False:
                return ("E", maze.grid[y][x + 1])
    if y - 1 >= 0:
        if (maze.grid[y - 1][x].path is True and
                cell.parent != maze.grid[y - 1][x]):
            if maze.grid[y - 1][x].s is False and cell.n is False:
                return ("N", maze.grid[y - 1][x])
    if y + 1 < maze.height:
        if (maze.grid[y + 1][x].path is True and
                cell.parent != maze.grid[y + 1][x]):
            if maze.grid[y + 1][x].n is False and cell.s is False:
                return ("S", maze.grid[y + 1][x])
    return None
    # print(result, cell.position)
    # return result


def get_directions(maze: Maze) -> str:
    current = maze.grid[maze.entry[1]][maze.entry[0]]
    result = ""
    next_cell: Cell = None
    # print("get dir")
    while True:
        right_dir = get_right_dir(current, maze)
        if right_dir:
            dir, next_cell = right_dir
            # print(dir, next_cell.position)
        # print(right_dir)
        # print(right_dir)
        # for d, cell in right_dir.items():
        #     dir = d
        #     next_cell = cell
        # dir = right_dir.keys()
        # print(dir)
        # dir, next_cell = get_right_dir(current, maze).items()
        result += dir
        next_cell.parent = current
        current = next_cell
        # print(result)
        if next_cell.special == " E":
            break
    return result


def write_into_file(maze: Maze) -> None:
    result = ""
    for row in maze.grid:
        for cell in row:
            string = decode(cell)

            to_add = str(hex(int(string, base=2)))

            result += to_add.removeprefix("0x").capitalize()
        result += "\n"
    result += "\n"
    entry = str(maze.entry).removeprefix("(")
    result += entry.removesuffix(")") + "\n"
    finish = str(maze.exit).removeprefix("(")
    # print(finish)
    result += finish.removesuffix(")") + "\n"
    result += get_directions(maze)
    try:
        with open(maze.output_file, mode="w") as f:
            f.write(result)
    except Exception:
        raise Exception


def run_menu(my_maze: Maze) -> None:
    show_path = False

    colors = ["\033[0m", "\033[31m", "\033[32m", "\033[33m", "\033[34m"]
    #          default       red          green       yellow      blue
    color_index = 0

    while True:
        """Escape sequence to clean terminal screen"""
        print("\033[H\033[J", end="")
        # system("clear")
        my_maze.print_grid(show_path, colors[color_index])

        print("\n=== A-Maze-ing ===")
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
            write_into_file(my_maze)
        elif choice == "2":
            if show_path is False:
                show_path = True
            else:
                show_path = False
            # show_path = not show_path
            print("In progress...")
        elif choice == "3":
            color_index = (color_index + 1) % len(colors)
        elif choice == "4" or choice == "q":
            break


def print_grid_of_path(maze: list[list[Cell]]):
    for row in maze:
        for cell in row:
            if cell.path is True:
                print("1", end="")
            else:
                print("0", end="")
        print()

def main() -> None:
    if len(sys.argv) == 2:
        # it can be any file, maybe that ends up on .txt
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
            my_maze.create_grid()
            my_maze.insert_forty2(my_maze.ft())
            my_maze.path_gen()
            # print_grid_of_path(my_maze.grid)
            # print_grid(my_maze.grid)
            write_into_file(my_maze)
            # my_maze.print_grid()
            run_menu(my_maze)

        except Exception as e:
            print(str(e))
            exit(1)
    else:
        print("The Amazing reqiuers 'config.txt' as a given parameter")


if __name__ == "__main__":
    main()
