import src.fltk as fltk
from src.board import Cell, Board
from src.tools import distance
from src.color import Color
from src.settings import BLOCK_SIZE, RADIUS

PRADIUS = 5

COLORS = {
    '#': "green",
    '>': "darkcyan",
    '*': "grey"
}

GRADIENTS = Color.BLUE.gradient(Color.RED, 30)

def map_coordinates(x, y) -> tuple[int, int]:
    return x*BLOCK_SIZE, y*BLOCK_SIZE

def draw_board(board: list[str]) -> None:
    for y, line in enumerate(board):
        for x, char in enumerate(line):
            if char in COLORS:
                color = COLORS[char]
                fltk.cercle(x*BLOCK_SIZE,
                            y*BLOCK_SIZE,
                            RADIUS,
                            couleur=color,
                            remplissage=color)

def draw_grid(board: list[str]) -> None:
    height = len(board)
    width = len(board[0])
    
    for y in range(height):
        fltk.ligne(0, y*BLOCK_SIZE, width*BLOCK_SIZE, y*BLOCK_SIZE)
    
    for x in range(width):
        fltk.ligne(x*BLOCK_SIZE, 0, x*BLOCK_SIZE, height*BLOCK_SIZE)

def wait_next_event():
    ev = None
    tev = None
    while not tev:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        fltk.mise_a_jour()
    return tev

def get_spacing(board: Board) -> int:
    if board.image:
        return board.spacing
    else:
        return BLOCK_SIZE

def next_event() -> str:
    ev = None
    tev = None
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev is not None:
            if tev == "Touche":
                return fltk.touche(ev)
            return tev
        fltk.mise_a_jour()

def draw_points(points: set[Cell], board: Board) -> list[int]:
    spacing = get_spacing(board)
    return [fltk.cercle(cell.x*spacing, cell.y*spacing, PRADIUS,
                        remplissage="white")
            for cell in points]

def get_cell_from_click(points: set[Cell], board: Board) -> Cell:
    spacing = get_spacing(board)
    cell = Cell(fltk.abscisse_souris(), fltk.ordonnee_souris())
    
    for point in points:
        p = Cell(point.x*spacing, point.y*spacing)
        if distance(p, cell) < 5:
            return point

def erase_tags(tags: list[int]):
    for tag in tags:
        fltk.efface(tag)

def get_color(a: Cell, b: Cell) -> Color:
    dist = int(distance(a, b))*10
    if dist >= len(GRADIENTS):
        return Color.RED
    return GRADIENTS[dist]

def draw_trajectory(trajectory: list[Cell], board: Board):
    spacing = get_spacing(board)
    
    if len(trajectory) == 1:
        point = trajectory[0]
        return [fltk.cercle(point.x*spacing, point.y*spacing, PRADIUS,
                            remplissage="blue")]
    
    points = zip(trajectory, trajectory[1:])
    tags = []
    for a, b in points:
        color = get_color(a, b).hex()
        ax, ay = a.x*spacing, a.y*spacing
        bx, by = b.x*spacing, b.y*spacing
        tags.append(fltk.cercle(ax, ay, PRADIUS, remplissage=color))
        tags.append(fltk.cercle(bx, by, PRADIUS, remplissage=color))
        tags.append(fltk.ligne(ax, ay, bx, by, epaisseur=2, couleur=color))
    return tags

def create_window_board(board: list[str]):
    fltk.cree_fenetre(*map_coordinates(len(board[0]) - 2, len(board) - 1))
