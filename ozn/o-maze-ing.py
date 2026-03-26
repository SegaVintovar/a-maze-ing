class Cell:
    def __init__(self) -> None:
        self.walls = 0000


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell())
            self.grid.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]


def main() -> None:
    maze = MazeGenerator(3, 4)
    print(maze.get_cell(0, 0).walls)
    print(maze.get_cell(2, 3).walls)
    # print(maze.get_cell(3, 4).walls) Error!
    print(len(maze.grid[0]))
    print(len(maze.grid))


if __name__ == "__main__":
    main()
