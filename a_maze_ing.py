import sys
from typing import Dict
from pydantic import BaseModel, model_validator
# from sys import argv
import random
from enum import Enum


# Bit Direction
# 0 (LSB) North
# 1 East
# 2 South
# 3 West
# 0101 example of horisontal path
# 1010 example of vertical path
# ###
# #0#
# ###
# 0111


# class CellVariants(Enum):
#     NULL = (0, 0, 0, 0)
#     "1" = (0, 0, 0, 1)

#     0x1: "╵",
#     0x2: "╶",
#     0x3: "└",
#     0x4: "╷",
#     0x5: "│",
#     0x6: "┌",
#     0x7: "├",
#     0x8: "╴",
#     0x9: "┘",
#     0xA: "─",
#     0xB: "┴",
#     0xC: "┐",
#     0xD: "┤",
#     0xE: "┬",
#     0xF: "┼",


class ClosedCell():
    ...


class Cell():
    def __init__(self, position: tuple):
        self.x = position[0]
        self.y = position[1]
        self.state = 0000
        self.special: str | None = None
        self.seed: bool = False
        self.position: tuple[int, int]
    
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
        self.grid = []
        random.seed(seed)

    def create_grid(self):
        x1, y1 = self.entry
        x2, y2 = self.exit
        i = 0
        while i < self.height:
            j = 0
            while j < self.width:
                if (j, i) == self.entry:
                    print("S", end="")
                elif (j, i) == self.exit:
                    print("E", end="")
                else:
                    print("┼", end="")
                j += 1
            # print(random.randint(1, 10), end="")
            print()
            i += 1

    def create_forty2(self) -> None:
        ...


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


class Cell_Variants():
    ...


# class Cell():
#     def __init__(self, north, south, west, east)
#         self.

class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def parsing(data: str) -> Dict:
    rows = data.split("\n")
    result = {}
    for row in rows:
        if row.startswith("#") or row == "":
            continue
        else:
            entry = row.split("=")
            if len(entry) == 2:
                if (
                    entry[0] == "WIDTH" or
                    entry[0] == "HEIGHT"
                        ):
                    result.update({entry[0].lower(): int(entry[1])})
                elif (
                        entry[0] == "ENTRY" or
                        entry[0] == "EXIT"
                        ):
                    ponit_pair = entry[1].split(",")
                    result.update(
                        {entry[0].lower(): (int(ponit_pair[0]),
                                            int(ponit_pair[1]))}
                        )
                elif entry[0] == "OUTPUT_FILE":
                    result.update({entry[0].lower(): entry[1]})
                elif entry[0] == "PERFECT":
                    if entry[1] == "True":
                        result.update({entry[0].lower(): True})
                    elif entry[1] == "False":
                        result.update({entry[0].lower(): False})
                else:
                    raise ParsingError(f"Unknown parameter: {row}")
            else:
                raise ParsingError(f"ParsingError: {row} entry is invalid")

    # check if we have all the parameters and they are correct
    # validation
    return result


def validation(data: Dict) -> bool:
    ...


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
        my_maze = Maze(**data_4_maze)
        my_maze.create_grid()
        # maze_gen(data_4_maze)
    else:
        print("The Amazing reqiuers '' as a given parameter")


if __name__ == "__main__":
    main()
