from src.board import Cell, Board
from math import sqrt
from src.color import Colors, Color

def parse_map(filepath: str) -> list[str]:
    with open(filepath, "r") as file:
        return [line for line in file]
    
def distance(a: Cell, b: Cell) -> float:
    x = a.x - b.x
    y = a.y - b.y
    return sqrt(x*x + y*y)

def map_cell(cell: Cell, ratio: int) -> Cell:
    return Cell(cell.x*ratio, cell.y*ratio)

def bresenham(start: Cell, end: Cell) -> list[Cell]:
    dx, dy = abs(end.x - start.x), -abs(end.y - start.y)
    xslope = 1 if start.x < end.x else -1
    yslope = 1 if start.y < end.y else -1
    err = dx + dy
    res = [start.copy()]
    
    if start.x == end.x:
        end.x += 1
    if start.y == end.y:
        end.y += 1
    
    while start.x != end.x and start.y != end.y:
        t_err = 2*err
        if t_err >= dy:
            err += dy
            start.x += xslope
        if t_err <= dx:
            err += dx
            start.y += yslope
        res.append(start.copy())
    return res

def filter_positions(board: Board):
    positions = board.next_coords()
        
    if not len(board.trajectory):
        return positions
    
    textures = {Color.WHITE, Color.DARKCYAN, Color.GREY}
    
    new_coords = set()
    if board.image is not None:
        start = map_cell(board.trajectory[-1], board.spacing)
        for coord in positions:
            rejected = False
            for in_between in bresenham(start.copy(), map_cell(coord, board.spacing)):
                if board.image.get(*in_between) not in textures:
                    rejected = True
                    break
            if not rejected:
                new_coords.add(coord)
        return new_coords
    return positions
