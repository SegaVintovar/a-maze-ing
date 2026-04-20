from pydantic import BaseModel, model_validator, Field
# import sys
# import os

# terminal_width = os.get_terminal_size()
# print(terminal_width)


class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def parsing(data: str) -> dict:
    rows = data.split("\n")
    result = {"seed": None}
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
                    result.update({entry[0].lower(): int(entry[1])})
                else:
                    raise ParsingError(f"Unknown parameter: {row}")
            else:
                raise ParsingError(f"ParsingError: {row} entry is invalid")

    return result


class InputCheck(BaseModel):
    width: int
    height: int
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
    @model_validator(mode="after")
    def validator(self):
        if self.entry == self.exit:
            raise ValueError("Entry and Exit has to be different")
        if self.width < 1 or self.height < 1:
            raise ValueError("Size parameters have to be greater then ZERO")
        if (self.entry[0] < 0 or
                self.entry[1] < 0 or
                self.exit[0] < 0 or
                self.exit[1] < 0):
            raise ValueError(
                "Entry/Exit coordinates have to be positive integers"
                )
        # check start and entry
        if (self.entry[0] >= self.width or self.entry[1] >= self.height or
                self.entry[0] < 0 or self.entry[1] < 0):
            raise ValueError("Entry point is out of Maze bounds")
        if (self.exit[0] >= self.width or self.exit[1] >= self.height or
                self.entry[0] < 0 or self.entry[1] < 0):
            raise ValueError("Exit point is out of Maze bounds")
        # if self.width < 9 or self.height < 7:
        #     raise ValueError("Maze size is too small to",
        #                      "create a labirynth with '42' logo."
        #                      "\nMin size is 9 x 7")
        return self
