"""
Configuration parsing and validation for A-Maze-ing.

Parses a plain-text config file into a dict of maze parameters and
validates types, ranges, and file-name patterns via a Pydantic model.
"""

from pydantic import BaseModel, model_validator, Field
# import sys
# import os

# terminal_width = os.get_terminal_size()
# print(terminal_width)


class ParsingError(Exception):
    """Raised when a config file line cannot be parsed or has an unknown key."""
    def __init__(self, message: str) -> None:
        self.message = message


def parsing(data: str) -> dict:
    """
    Parse the raw text of a config file into a dict of maze parameters.

    Each non-empty, non-comment line must have the form KEY=VALUE.
    Recognised keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, SEED.
    Keys are lowercased in the returned dict so they map directly onto the
    Maze / InputCheck constructors.

    ParsingError: If a line is malformed or contains an unknown key.
    """
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
                elif entry[0] == "SEED":
                    result.update({entry[0].lower(): entry[1]})
                else:
                    raise ParsingError(f"Unknown parameter: {row}")
            else:
                raise ParsingError(f"ParsingError: {row} entry is invalid")

    # check if we have all the parameters and they are correct
    # validation
    return result


class InputCheck(BaseModel):
    """
    Pydantic schema that validates parsed config values.

    Ensures width/height are positive, the output file ends in '.txt',
    and seed, if given, is non-negative. Entry and exit ranges relative
    to the grid are not yet validated here.
    """
    # we do not run the amazing if the terminal width is not big enough
    # cell is represented as 6 colomns
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: tuple[int, int]
    exit: tuple[int, int]
    # r is raw string, because regex uses a lot of backslashes
    # without r Python would treat those as escape char
    # ^ is start of the string, $ is the end
    # . is any char, + is one or more previous token
    # \. is literal
    output_file: str = Field(min_length=5, pattern=r"^.+\.txt$")
    perfect: bool
    seed: int | None = Field(ge=0)

    # i can check if the entry and exit are in the grid
    # @model_validator
    # def validator(self):
    #     if self.width * 6 < terminal_width:
    #         raise ValueError
    #     return self
