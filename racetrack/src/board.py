"""Contains structures to represent and contains game data

Game's component must be created using both 'load_image' and 'load_board'
static methods of class 'Board'
"""

from typing import Iterator

from src.color import Color
from lib.fltk import PhotoImage

__all__ = ["Cell", "Board"]


class Cell:
    """
    Represent a coordinates on a two-dimension system

    Attributes
    ----------
    x : int
        abscissa of the represented coordinate
    y: int
        ordinate of the represented coordinate
    """

    def __init__(self, x: int, y: int) -> None:
        """Constructor of the 'Cell' object

        Parameters
        ----------
        x : int
            abscissa of the represented coordinate
        y: int
            ordinate of the represented coordinate
        """
        self.x = x
        self.y = y

    def __add__(self, other) -> "Cell":
        if isinstance(other, Cell):
            return Cell(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def __iter__(self) -> Iterator[tuple[int, int]]:
        return iter((self.x, self.y))

    def neighbour(self) -> set["Cell"]:
        """Return a set of all nearby cells

        Returns
        -------
        set[Cell]
            Contains the cells arround
        """
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
        """Creates a new 'Cell' object with the same attributes

        Returns
        -------
        Cell
            copy of current cell
        """
        return Cell(self.x, self.y)


neighbour = {  # set of arrounds coordinates of (0, 0)
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
    """Represent the internal data of a map

    Attributes
    ----------
    trajectory : list[Cell]
        list of coordinates that represent the current trajectory
    start : set[Cell]
        set of coordinates where the player's car begin
    end : set[Cell]
        set of coordinates that the player needs to reach in order to win
    obstacles : set[Cell]
        set of coordinates where the player's car cannot stay
    legal : set[Cell]
        set of coordintes where the player's car can go. This set contains also
        the start and end coordinates
    image : PhotoImage, optional
        in case the game source file is an image, this attribute represent the
        image data, default = None
    spacing : int, optional
        in case the game source file is an image, this attribute represent the
        padding of each block, default = 0
    block_size : int, optional
        in case the game representation is a text file, this attribute represent
        the size of each block, default = 0
    """

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
        """Compte the next coordinates based on the previous ones.
        If there is no trajectory yet, the next coordinates are the starting
        coordinates. If there is only one, the next coordinates are the eigth
        arround

        Parameters
        ----------
        trajectory : list[Cell], optional
            if given, the next coordinates are computed with the given
            trajectory, by default None

        Returns
        -------
        set[Cell]
            set of possible next coordinates
        """
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
        """Add a coordinate to the trajectory

        Parameters
        ----------
        cell : Cell
            coordinate to the current trajectory
        """
        self.trajectory.append(cell)

    def pop(self) -> Cell:
        """Remove the last inserted coordinate

        Returns
        -------
        Cell
            the last coordinate if trajectory isn't empty, else None
        """
        if self.trajectory:
            cell = self.trajectory.pop()
            return cell
        return None

    def win(self, trajectory: list[Cell] = None) -> bool:
        """Check if the trajectory leads to the end coordinates

        Parameters
        ----------
        trajectory : list[Cell], optional
            if given, the next coordinates are computed with the given
            trajectory, by default None

        Returns
        -------
        bool
            True if the trajectory leads to the end, else False
        """
        if trajectory is None:
            trajectory = self.trajectory
        return len(trajectory) and trajectory[-1] in self.end

    @staticmethod
    def load_board(board: list[str], block_size: int) -> "Board":
        """Create a board object based on a list of strings

        Parameters
        ----------
        board : list[str]
            list of strings that codes the board
        block_size : int
            size of each block (only needed when displaying the board)

        Returns
        -------
        Board
            created board
        """
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
    def load_image(image: PhotoImage, spacing: int) -> "Board":
        """Create a board object based on an image

        Parameters
        ----------
        image : PhotoImage
            given image
        spacing : int
            space between each coordinates

        Returns
        -------
        Board
            created board
        """
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
