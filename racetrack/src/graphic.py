"""Contains functions to handle graphic representation of board, including
display of trajectories and event management.
"""

from lib import fltk
from src.board import Cell, Board
from src.color import Color
from src.settings import RRADIUS, PRADIUS
from src.tools import distance

__all__ = [
    "draw_board",
    "draw_grid",
    "wait_event",
    "wait_exit",
    "draw_trajectory",
    "create_window_board",
    "create_window_image",
]

COLORS = {"#": "green", ">": "darkcyan", "*": "grey"}

GRADIENTS = Color.BLUE.gradient(Color.RED, 30)


def draw_board(board: list[str], block_size: int) -> None:
    """Draw text-based board

    Parameters
    ----------
    board : list[str]
        board to draw. Contains list of strings that code the type of tiles
    block_size : int
        padding between each block
    """
    for y, line in enumerate(board):
        for x, char in enumerate(line):
            if char in COLORS:
                color = COLORS[char]
                fltk.cercle(
                    x * block_size,
                    y * block_size,
                    block_size * RRADIUS,
                    couleur=color,
                    remplissage=color,
                )


def draw_grid(width: int, height: int, spacing: int) -> None:
    """Draw grid

    Parameters
    ----------
    width : int
        with of the map to draw the grid
    height : int
        height of the map to draw the grid
    spacing : int
        padding between each dot
    """
    for y in range(height // spacing):
        fltk.ligne(0, y * spacing, width * spacing, y * spacing)

    for x in range(width // spacing):
        fltk.ligne(x * spacing, 0, x * spacing, height * spacing)


def wait_event() -> str:
    """Wait until a fltk's event is triggered. If the evnet is a pressed key,
    `wait_event` returns the pressed key

    Returns
    -------
    str
        event label
    """
    ev, tev = None, None
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev is not None:
            if tev == "Touche":
                return fltk.touche(ev)
            return tev
        fltk.mise_a_jour()


def wait_exit() -> None:
    """Wait until the user quit the window"""
    while wait_event() != "Quitte":
        ...


def draw_points(points: set[Cell], board: Board) -> list[int]:
    """Draw given points. Points will be multiplied by board.padding
    to scale them at the correct proportions

    Parameters
    ----------
    points : set[Cell]
        points to draw
    board : Board

    Returns
    -------
    list[int]
        list of tags used to plot points
    """
    return [
        fltk.cercle(
            cell.x * board.padding, cell.y * board.padding, PRADIUS, remplissage="white"
        )
        for cell in points
    ]


def get_cell_from_click(points: set[Cell], board: Board) -> Cell:
    """Get the nearest clicked cell

    Parameters
    ----------
    points : set[Cell]
        set of possibles cells
    board : Board
        board

    Returns
    -------
    Cell
        clicked cell
    """
    cell = Cell(fltk.abscisse_souris(), fltk.ordonnee_souris())

    for point in points:
        p = Cell(point.x * board.padding, point.y * board.padding)
        if distance(p, cell) < PRADIUS:
            return point
    return None


def erase_tags(tags: list[int]) -> None:
    """Erase all drawn objects from the window based on their given tags

    Parameters
    ----------
    tags : list[int]
        list of tags
    """
    for tag in tags:
        fltk.efface(tag)


def get_color(a: Cell, b: Cell) -> Color:
    """Get a color from two cells. The color is based on the distance
    between them. The furhest their are, the redder the color will be

    Parameters
    ----------
    a : Cell
        first cell
    b : Cell
        second cell

    Returns
    -------
    Color
        associated color
    """
    dist = int(distance(a, b)) * 10
    if dist >= len(GRADIENTS):
        return Color.RED
    return GRADIENTS[dist]


def draw_trajectory(board: Board) -> list[int]:
    """Draw a representation of trajectory (a list of cells)

    Parameters
    ----------
    board : Board
        board

    Returns
    -------
    list[int]
        list of tags needed to draw the trajectory
    """
    if len(board.trajectory) == 1:
        point = board.trajectory[0]
        return [
            fltk.cercle(
                point.x * board.padding,
                point.y * board.padding,
                PRADIUS,
                remplissage="blue",
            )
        ]

    points = zip(board.trajectory, board.trajectory[1:])
    tags = []
    for a, b in points:
        color = get_color(a, b).hex()
        ax, ay = a.x * board.padding, a.y * board.padding
        bx, by = b.x * board.padding, b.y * board.padding
        tags.append(fltk.cercle(ax, ay, PRADIUS, remplissage=color))
        tags.append(fltk.cercle(bx, by, PRADIUS, remplissage=color))
        tags.append(fltk.ligne(ax, ay, bx, by, epaisseur=2, couleur=color))
    return tags


def create_window_board(board: list[str], block_size: int) -> None:
    """Initiate fltk's window in order to correctly display a text-based board

    Parameters
    ----------
    board : list[str]
        board to draw
    block_size : int
        padding between each block
    """
    width = len(board[0]) - 1
    height = len(board) - 1
    fltk.cree_fenetre(width * block_size, height * block_size)


def create_window_image(image_path: str) -> fltk.PhotoImage:
    """Initiate fltk's window in order to correctly display an image-based board

    Parameters
    ----------
    image_path : str
        path to the image

    Returns
    -------
    fltk.PhotoImage
        image object
    """
    fltk.cree_fenetre(500, 500, redimension=True)

    image = fltk.PhotoImage(file=image_path)
    fltk.redimensionne_fenetre(image.width(), image.height())

    fltk.image(0, 0, image_path, ancrage="nw")
    return image
