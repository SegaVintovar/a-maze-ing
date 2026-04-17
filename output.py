# from . import Cell


# def decode(cell: Cell) -> str:
#     result = ""
#     north = int(cell.n)
#     east = int(cell.e)
#     south = int(cell.s)
#     west = int(cell.w)
#     result = str(west) + str(south) + str(east) + str(north)
#     return result


# def write_into_file(grid: list[list[Cell]], output_file) -> None:
#     result = ""
#     for row in grid:
#         for cell in row:
#             string = decode(cell)
#             result += str(int(string, base=16))
#         result += "\n"
#     try:
#         with open("output_file", mode="w") as f:
#             f.write(result)
#     except Exception as e:
#         raise e

