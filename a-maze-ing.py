import sys
from typing import Dict
# from sys import argv


def parsing(data: str) -> Dict:
    rows = data.split("\n")
    result = {}
    for row in rows:
        entry = row.split("=")
        result.update({entry[0]: entry[1]})
    # check if we have all the parameters and they are correct
    return result


def validation(data: Dict) -> bool:
    ...

def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as config_file:
            config_data = config_file.read()
        try:
            data_4_maze = parsing(config_data)
        except Exception as e:
            print("Parsing error: ", str(e))
            return
        else:
            maze_gen(data_4_maze)
    else:
        print("try again")


if __name__ == "__main__":
    main()
