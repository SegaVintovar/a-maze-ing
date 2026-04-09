import random
from time import sleep
from functools import wraps
from typing import Callable


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
            self, n: bool, e: bool, s: bool, w: bool, position: tuple[int, int],
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
        self.path = False

    def wall(self, wall: bool, side: str) -> str:
        if not wall:
            return "  "
        if side == "N" or side == "S":
            return "██"
        if side == "E" or side == "W":
            return "██"

    def representation(self):
        return [
            ["██", self.wall(self.n, "N"), "██"],
            [self.wall(self.w, "W"), self.special, self.wall(self.e, "E")],
            ["██", self.wall(self.s, "S"), "██"]
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

    def print(self):
        ...


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
                    # cell.special = " S"
                    # print("S", end="")
                elif (j, i) == self.exit:
                    cell = Cell(1, 1, 1, 1, (j, i), " E", False)
                    # cell.special = " E"
                else:
                    cell = Cell(1, 1, 1, 1, (j, i), "  ", False)
                    # cell.special = "  "
                row.append(cell)
                j += 1
            # print(random.randint(1, 10), end="")
            # print()
            self.grid.append(row)
            i += 1

    def print_grid(self) -> None:
        for row in self.grid:
            i = 0
            while i < 3:
                for cell in row:
                    k = 0
                    while k < 3:
                        print(cell.representation()[i][k], end="")
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

    def insert_forty2(self, ft: list[list]) -> None:
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
        # j = 0
        # for j, row in enumerate(ft):
        #     i = 0
        #     while i < len(ft[j]):
        #         if ((c_x + i, c_y + j) == self.entry or
        #                 (c_x + i, c_y + j) == self.exit):
        #             if ft[j][i].visited is True:
        #                 raise Exception(
        #                   "Error: Entry and Exit must be appart from 42 logo"
        #                     )
        #         self.grid[c_y + j][c_x + i] = ft[j][i]
        #         i += 1

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

    def get_visited_neighbours(self, cell: Cell) -> dict:
        x, y = cell.position
        result = {}
        # checing from 4 sides
        if x - 1 >= 0:
            if self.grid[y][x - 1].visited is True:
                if self.grid[y][x - 1].special != "42":
                    result.update({"W": self.grid[y][x - 1]})
        if x + 1 < self.width:
            if self.grid[y][x + 1].visited is True:
                if self.grid[y][x + 1].special != "42":
                    result.update({"E": self.grid[y][x + 1]})
        if y - 1 >= 0:
            if self.grid[y - 1][x].visited is True:
                if self.grid[y - 1][x].special != "42":
                    result.update({"N": self.grid[y - 1][x]})
        if y + 1 < self.height:
            if self.grid[y + 1][x].visited is True:
                if self.grid[y + 1][x].special != "42":
                    result.update({"S": self.grid[y + 1][x]})
        return result

    def finalize_v1(self) -> None:
        for row in self.grid:
            for cell in row:
                if cell.visited is False and cell.special != "42":
                    neighbours = self.get_visited_neighbours(cell)
                    print(neighbours, cell.position)
                    if len(neighbours) > 0:
                        direction, next_cell = random.choice(
                            list(neighbours.items()))
                        Maze.remove_walls_in_between(
                            cell, direction, next_cell)
                        cell.visited = True

    def finalize_v2(self) -> None:
        # in case we want to loop from the end
        for cell in reversed(self.stack):
            # for cell in self.stack:
            neighbours = self.get_neighbours(cell)
            print(neighbours, cell.position)
            if len(neighbours) > 0:
                direction, next_cell = random.choice(
                    list(neighbours.items()))
                Maze.remove_walls_in_between(
                    cell, direction, next_cell)
                self.dig_into_depth(next_cell)
                if self.get_neighbours(cell) == 0:
                    self.stack.remove(cell)
                
                # cell.visited = True
    # go till you have where to go
    def dig_into_depth(self, next_cell: Cell) -> None:
        current = None
        # while len(self.get_neighbours(next_cell)) > 0:
        #     ...
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
                    self.stack.append(Cell)
            else:
                break
            

        # for row in self.grid:
        #     for cell in row:
        #         if cell.visited is True and cell.special != "42":
        #             neighbours = self.get_neighbours(cell)
        #             print(neighbours, cell.position)
        #             if len(neighbours) > 0:
        #                 direction, next_cell = random.choice(
        #                     list(neighbours.items()))
        #                 Maze.remove_walls_in_between(
        #                     cell, direction, next_cell)
        #                 cell.visited = True

    def path_gen(self) -> None:
        start = self.grid[self.entry[1]][self.entry[0]]
        
        current = start
        next_cell: Cell = None
        # flag = True
        i = 0
        while i < 5000:
            if next_cell:
                current = next_cell
                if next_cell.special == " E":
                    break
            neighbours = self.get_neighbours(current)
            print(neighbours, current.position)
            if len(neighbours) > 0:
                for cell in neighbours.values():
                    if cell.special == " E":
                        next_cell == cell
                
                direction, next_cell = random.choice(list(neighbours.items()))
                Maze.remove_walls_in_between(current, direction, next_cell)
                current.visited = True
                neighbours.pop(direction)
                if len(neighbours) > 0:
                    print(len(neighbours), end=", ")
                    self.stack.append(current)
                print(i)
                i += 1
                # current = next_cell
            elif len(self.stack) != 0:
                print("we are in dead end, lets take last cell from the stack", len(self.stack))
                next_cell = self.stack[-1]
                self.stack.pop(-1)
            else:
                print("This is a dead end!")
                break
        for cell in self.stack:
            print(cell.position, end=", ")
        print("finalize")
        # self.finalize_v2()

    def another_path_gen(self) -> None:
        start = self.grid[self.entry[1]][self.entry[0]]
        current = start
        next_cell: Cell = None
        