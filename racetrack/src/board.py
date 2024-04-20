from typing import Iterator

from src.color import Color
from src.fltk import PhotoImage


class Cell:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> "Cell":
        if isinstance(other, Cell):
            return Cell(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def __iter__(self) -> Iterator[tuple[int, int]]:
        return iter((self.x, self.y))

    def neighbour(self) -> set["Cell"]:
        return {self + c for c in neighbour}

    def __lt__(self, other) -> bool:
        if isinstance(other, Cell):
            return (self.x, self.y) < (other.x, other.y)
        if isinstance(other, tuple):
            return (self.x, self.y) < other
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Cell(x: {self.x}, y: {self.y})"

    def copy(self) -> "Cell":
        return Cell(self.x, self.y)


neighbour = {
    Cell(-1, -1),
    Cell(0, -1),
    Cell(1, -1),
    Cell(1, 0),
    Cell(1, 1),
    Cell(0, 1),
    Cell(-1, 1),
    Cell(-1, 0),
    Cell(0, 0),
}


class Board:

    def __init__(
        self, image: PhotoImage = None, spacing: int = 0, block_size: int = 0
    ) -> None:
        self.trajectory = []
        self.start = set()
        self.end = set()
        self.obstacles = set()
        self.legal = set()
        self.image = image
        self.spacing = spacing
        self.block_size = block_size

    def next_coords(self, trajectory: list[Cell] = None) -> set[Cell]:
        if trajectory is None:
            trajectory = self.trajectory

        targets = set()
        if not trajectory:
            targets = self.start
        elif len(trajectory) == 1:
            targets = trajectory[-1].neighbour()
        else:
            a = trajectory[-1]
            b = trajectory[-2]
            vector = Cell(a.x - b.x, a.y - b.y)
            targets = (trajectory[-1] + vector).neighbour()
        return (targets & self.legal) - set(trajectory)

    def append(self, cell: Cell) -> None:
        self.trajectory.append(cell)

    def pop(self) -> Cell:
        if self.trajectory:
            cell = self.trajectory.pop()
            return cell
        return None

    def win(self, trajectory: list[Cell] = None):
        if trajectory is None:
            trajectory = self.trajectory
        return len(trajectory) and trajectory[-1] in self.end

    @staticmethod
    def load_board(board: list[str], block_size: int) -> "Board":
        res = Board(block_size=block_size)
        for y, line in enumerate(board):
            for x, char in enumerate(line):
                if char == ">":
                    res.start.add(Cell(x, y))
                elif char == "*":
                    res.end.add(Cell(x, y))
                elif char == "#":
                    res.obstacles.add(Cell(x, y))
                if char != "#":
                    res.legal.add(Cell(x, y))
        return res

    @staticmethod
    def load_image(image: object, spacing: int) -> "Board":
        res = Board(image, spacing)
        for y in range(image.height() // spacing):
            for x in range(image.width() // spacing):
                color = image.get(x * spacing, y * spacing)
                cell = Cell(x, y)

                if color == Color.WHITE:
                    res.legal.add(cell)
                elif color == Color.DARKCYAN:
                    res.start.add(cell)
                    res.legal.add(cell)
                elif color == Color.GREY:
                    res.end.add(cell)
                    res.legal.add(cell)
        return res
