from pydantic import BaseModel, model_validator, Field
import sys
import os

terminal_width = os.get_terminal_size()
print(terminal_width)


class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def parsing(data: str) -> dict:
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


def input_check(BaseModel):
    width: int = Field(gt=0, lt=terminal_width)