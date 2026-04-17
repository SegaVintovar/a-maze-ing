import random
from time import sleep
from functools import wraps
from typing import Callable
import math
# from .a_maze_ing import write_into_file

OPPOSSITE_DIR = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E"
}


def time_slower(seconds: int | float):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sleep(seconds)
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


class Cell():
    def __init__(
            self,
            n: bool, e: bool, s: bool, w: bool, position: tuple[int, int],
            special: str, visited: bool
            ) -> None:
        # self.state = 0000
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.special = special
        self.seed: bool = False
        self.position = position
        self.visited = visited
        self.path: bool = False
        self.parent: Cell | None = None
        self.dead: bool = False

    def wall(self, wall: bool, side: str, is_path: bool = False, is_42: bool = False) -> str:
        # if not wall:
        #     return "  "
        # if side == "N" or side == "S":
        #     return "██"
        # if side == "E" or side == "W":
        #     return "██"
        blue_square = "\033[34m██\033[0m"
        white_corridor = "\033[47m  \033[0m"
        yellow_square = "\033[33m██\033[0m"

        if is_42:
            return yellow_square
        
        if not wall:
            if is_path:
                return blue_square
            return white_corridor
        return "██"

    # @time_slower(0.001)
    def representation(self, show_path: bool = False, neigh_path: dict = None, neigh_42: dict = None):
        if neigh_path is None:
            neigh_path = {"N": False, "E": False, "S": False, "W": False}
        
        if neigh_42 is None:
            neigh_42 = {"N": False, "E": False, "S": False, "W": False}
        
        blue_square = "\033[34m██\033[0m"
        white_corridor = "\033[47m  \033[0m"

        if "S" in self.special:
            center = "\033[92;47m██\033[0m"
        elif "E" in self.special:
            center = "\033[91;47m██\033[0m"
        elif show_path and self.path and "\033[" not in self.special: # Тепер це elif!
            center = blue_square
        elif self.special == "  ":
            center = white_corridor
        else:
            center = self.special

        w_char = "██"

        return [
            [w_char, self.wall(self.n, "N", show_path and neigh_path["N"], neigh_42["N"]), w_char],
            [self.wall(self.w, "W", show_path and neigh_path["W"], neigh_42["W"]), center, 
             self.wall(self.e, "E", show_path and neigh_path["E"], neigh_42["E"])],
            [w_char, self.wall(self.s, "S", show_path and neigh_path["S"], neigh_42["S"]), w_char]
        ]

    def open_wall(self, wall: str) -> None:
        if wall == "N":
            self.n = False
        if wall == "E":
            self.e = False
        if wall == "S":
            self.s = False
        if wall == "W":
            self.w = False

    def count_open_walls(self) -> int:
        i = 0
        if self.n is False:
            i += 1
        if self.e is False:
            i += 1
        if self.s is False:
            i += 1
        if self.w is False:
            i += 1
        return i


class Maze():
    def __init__(
            self,
            height: int,
            width: int,
            perfect: bool,
            entry: tuple,
            exit: tuple,
            output_file: str,
            seed: int | None = None
            ):
        self.height = height
        self.width = width
        self.perfect = perfect
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.seed = seed
        self.grid: list[list[Cell]] = []
        random.seed(seed)
        self.stack: list[Cell] = []

    def create_grid(self):
        x1, y1 = self.entry
        x2, y2 = self.exit
        i = 0
        while i < self.height:
            j = 0
            row = []
            while j < self.width:
                if (j, i) == self.entry:
                    cell = Cell(1, 1, 1, 1, (j, i), " S", True)
                elif (j, i) == self.exit:
                    cell = Cell(1, 1, 1, 1, (j, i), " E", False)
                else:
                    cell = Cell(1, 1, 1, 1, (j, i), "  ", False)
                row.append(cell)
                j += 1
            self.grid.append(row)
            i += 1

    def print_grid(self, show_path: bool = False, color: str = "\033[0m") -> None:
        for y, row in enumerate(self.grid):
            i = 0
            while i < 3:
                for x, cell in enumerate(row):
                    # blue path
                    def is_p(c): 
                        return c.path or "\033[32m" in c.special or "\033[31m" in c.special
                    
                    neighs_path = {
                        "N": (y > 0 and is_p(self.grid[y-1][x]) and is_p(cell)),
                        "S": (y < self.height-1 and is_p(self.grid[y+1][x]) and is_p(cell)),
                        "E": (x < self.width-1 and is_p(self.grid[y][x+1]) and is_p(cell)),
                        "W": (x > 0 and is_p(self.grid[y][x-1]) and is_p(cell))
                    }

                    # 42 logic
                    def is_42(c):
                        return "\033[33m" in c.special

                    neighs_42 = {
                        "N": (y > 0 and is_42(self.grid[y-1][x]) and is_42(cell)),
                        "S": (y < self.height-1 and is_42(self.grid[y+1][x]) and is_42(cell)),
                        "E": (x < self.width-1 and is_42(self.grid[y][x+1]) and is_42(cell)),
                        "W": (x > 0 and is_42(self.grid[y][x-1]) and is_42(cell))
                    }
                    
                    rep = cell.representation(show_path=show_path, neigh_path=neighs_path, neigh_42=neighs_42)
                    
                    k = 0
                    while k < 3:
                        part = rep[i][k]
                        # paint only black walls dont touch color blocks
                        if part == "██" and "\033[" not in part:
                            print(color + part + "\033[0m", end="")
                        else:
                            print(part, end="")
                        k += 1
                print()
                i += 1

    @staticmethod
    def ft() -> list:
        pre_ft = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        result = []
        y = 0
        for row in pre_ft:
            x = 0
            r_row = []
            for tp in row:
                if tp == 1:
                    cell = Cell(
                        1, 1, 1, 1, (0, 0), "42", True)
                if tp == 0:
                    cell = Cell(
                        1, 1, 1, 1, (0, 0), "  ", False)
                cell.position = (x, y)
                r_row.append(cell)
                x += 1
            result.append(r_row)
            y += 1
        return result

    def insert_forty2(self, ft: list[list[Cell]]) -> None:
        # What is the center of the grid
        # and what the start point for the 42
        c_x = int((self.width - 1) / 2) - 3
        c_y = int((self.height - 1) / 2) - 2
        j = 0
        while j < len(ft):
            i = 0
            while i < len(ft[j]):
                if ((c_x + i, c_y + j) == self.entry or
                        (c_x + i, c_y + j) == self.exit):
                    if ft[j][i].visited is True:
                        raise Exception(
                            "Error: Entry and Exit must be appart from 42 logo"
                            )
                self.grid[c_y + j][c_x + i] = ft[j][i]
                self.grid[c_y + j][c_x + i].position = (c_x + i, c_y + j)
                i += 1
            j += 1

    @staticmethod
    def remove_walls_in_between(
            current_cell: Cell, direction: str, next_cell: Cell
            ) -> None:
        current_cell.open_wall(direction)
        next_cell.open_wall(OPPOSSITE_DIR[direction])

    def get_neighbours(self, cell: Cell) -> dict:
        x, y = cell.position
        result = {}
        # checing from 4 sides
        if x - 1 >= 0:
            if self.grid[y][x - 1].visited is False:
                result.update({"W": self.grid[y][x - 1]})
        if x + 1 < self.width:
            if self.grid[y][x + 1].visited is False:
                result.update({"E": self.grid[y][x + 1]})
        if y - 1 >= 0:
            if self.grid[y - 1][x].visited is False:
                result.update({"N": self.grid[y - 1][x]})
        if y + 1 < self.height:
            if self.grid[y + 1][x].visited is False:
                result.update({"S": self.grid[y + 1][x]})
        return result

    # with opened walls and not from the path
    def get_visited_neighbours(self, cell: Cell) -> dict:
        x, y = cell.position
        result = {}
        # checing from 4 sides
        if x - 1 >= 0:
            if self.grid[y][x - 1].visited is True:
                if self.grid[y][x - 1].e is False:
                    result.update({"W": self.grid[y][x - 1]})
        if x + 1 < self.width:
            if self.grid[y][x + 1].visited is True:
                if self.grid[y][x + 1].w is False:
                    result.update({"E": self.grid[y][x + 1]})
        if y - 1 >= 0:
            if self.grid[y - 1][x].visited is True:
                if self.grid[y - 1][x].s is False:
                    result.update({"N": self.grid[y - 1][x]})
        if y + 1 < self.height:
            if self.grid[y + 1][x].visited is True:
                if self.grid[y + 1][x].n is False:
                    result.update({"S": self.grid[y + 1][x]})
        return result

    def stage2(self) -> None:
        while self.stack:
            current = self.stack.pop(-1)
            neighbours = self.get_neighbours(current)
            if len(neighbours) > 0:
                self.dig_into_depth(current)

    def dig_into_depth(self, next_cell: Cell) -> None:
        current = None
        while True:
            # if current is None:
            current = next_cell
            neighbours = self.get_neighbours(current)
            if len(neighbours) > 0:
                direction, next_cell = random.choice(
                     list(neighbours.items()))
                Maze.remove_walls_in_between(
                    current, direction, next_cell)
                current.visited = True
                neighbours.pop(direction)
                if len(neighbours) > 0:
                    self.stack.append(current)
            else:
                current.visited = True
                break

    def stage3(self) -> None:
        for row in reversed(self.grid):
            for cell in reversed(row):
                if cell.visited is True and cell.special != "42":
                    neighbours = self.get_neighbours(cell)
                    if len(neighbours) > 0:
                        direction, next_cell = random.choice(
                            list(neighbours.items()))
                        Maze.remove_walls_in_between(
                            cell, direction, next_cell)
                        next_cell.visited = True
                        self.dig_into_depth(next_cell)

    # for the dead end
    def get_neighbours_of_the_dead_end(self, cell: Cell) -> dict:
        x, y = cell.position
        result = {}
        # checing from 4 sides
        if x - 1 >= 0:
            print(1, end="")
            nb = self.grid[y][x - 1]
            # if nb.special not in (" S", " E", "42", " P"):
            if nb.special == "  ":
            # or nb.special == " P":
                # if nb.e is True:
                result.update({"W": nb})
        if x + 1 < self.width:
            print(2, end="")
            nb = self.grid[y][x + 1]
            if nb.special == "  ":
                result.update({"E": nb})
        if y - 1 >= 0:
            print(3, end="")
            nb = self.grid[y - 1][x]
            if nb.special == "  ":
                result.update({"N": nb})
        if y + 1 < self.height:
            print(4, end="")
            nb = self.grid[y + 1][x]
            if nb.special == "  ":
                result.update({"S": nb})
        return result

    def dead_end_open(self) -> None:
        to_choose = []
        for row in self.grid:
            for cell in row:
                if cell.dead is True or cell.count_open_walls() == 1:
                    if cell.special not in (" S", " E", "42"):
                        to_choose.append(cell)
        i = 0
        while True:
            if len(to_choose) > 0:
                his_choice = random.choice(to_choose)
                neighbours = self.get_neighbours_of_the_dead_end(his_choice)
                if len(neighbours) > 0:
                    direction, next_cell = random.choice(
                        list(neighbours.items()))
                    Maze.remove_walls_in_between(
                        his_choice, direction, next_cell)
                    to_choose.remove(his_choice)
                    i += 1
                else:
                    to_choose.remove(his_choice)
            else:
                break

    def stage1(self) -> None:
        start = self.grid[self.entry[1]][self.entry[0]]
        current = start
        next_cell: Cell = None
        while True:
            if next_cell:
                current = next_cell
                next_cell = None
            neighbours = self.get_neighbours(current)
            if len(neighbours) > 0:
                direction = None
                for dir, cell in list(neighbours.items()):
                    if cell.special == " E":
                        next_cell = cell
                        direction = dir
                        break
                if not next_cell:
                    direction, next_cell = random.choice(
                        list(neighbours.items()))
                Maze.remove_walls_in_between(current, direction, next_cell)
                current.visited = True
                next_cell.parent = current
                if next_cell.special == " E":
                    self.stack.append(current)
                    next_cell.visited = True
                    break
                neighbours.pop(direction)
                if len(neighbours) >= 0:
                    self.stack.append(current)
            elif len(self.stack) != 0:
                cell.dead = True
                next_cell = self.stack.pop(-1)
                current.visited = True
            else:
                current.visited = True
                break
        if self.stack:
            # self.stack[-1].special = " P"
            self.stack[-1].path = True

    # MazeGen actually. my alco algo
    def path_gen(self) -> None:
        self.stage1()
        self.build_the_path()
        self.stage2()
        self.stage3()
        if self.perfect is False:
            self.dead_end_open()
        # write_into_file(
        #     self.grid, self.output_file, self.entry, self.exit. self.path)

    @staticmethod
    def distance(point_a: tuple[int, int], point_b: tuple[int, int]) -> float:
        x1, y1 = point_a
        x2, y2 = point_b
        return math.sqrt(((x2 - x1)**2 + (y2 - y1)**2))

    # using the stack after the first stage
    # we have a path, but there is a possibilty of gaps
    # so i need to track them
    def build_the_path(self):
        i = 0
        next_cell: Cell | None = None
        while i < len(self.stack) - 1:
            if not next_cell:
                cell = self.stack[i]
            next_stack_cell = self.stack[i + 1]
            a = cell.position
            b = next_stack_cell.position
            if abs(b[0] - a[0]) + abs(b[1] - a[1]) == 1:
                # if cell.special != " S":
                #     cell.path = True
                if cell.position != self.entry:
                    cell.special = " P"
                next_cell = None
            else:
                vertical_d = next_stack_cell.position[1] - cell.position[1]
                horisontal_d = next_stack_cell.position[0] - cell.position[0]
                if abs(vertical_d) > abs(horisontal_d):
                    if vertical_d > 0:
                        directon_for_dig = "S"
                    else:
                        directon_for_dig = "N"
                else:
                    if horisontal_d > 0:
                        directon_for_dig = "E"
                    else:
                        directon_for_dig = "W"
                neighbours = self.get_visited_neighbours(cell)
                next_cell = neighbours.get(directon_for_dig)
            if cell.special != " S":
                cell.special = " P"
            cell.path = True
            i += 1
        self.stack[-1].path = True
        neighbours = self.get_visited_neighbours(self.stack[-1])
        for next_cell in neighbours.values():
            if next_cell.special == " E":
                next_cell.path = True
        # if len(self.stack) > 0:
        #     last = self.stack[-1]
