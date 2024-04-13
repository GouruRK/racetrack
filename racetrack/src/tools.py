from src.board import Cell, Board
from math import sqrt
from src.color import Colors, Color
from src.settings import RRADIUS

import src.fltk as fltk

VALID_TEXTURES = {Color.WHITE, Color.DARKCYAN, Color.GREY}

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
    # https://gist.github.com/bert/1085538
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

def filter_imagebased_position(board: Board, positions: set[Cell]) -> set[Cell]:
    new_coords = set()
    start = map_cell(board.trajectory[-1], board.spacing)
    for coord in positions:
        rejected = False
        for in_between in bresenham(start.copy(), map_cell(coord, board.spacing)):
            if board.image.get(*in_between) not in VALID_TEXTURES:
                rejected = True
                break
        if not rejected:
            new_coords.add(coord)
    return new_coords

def filter_textbased_postion(board: Board, positions: set[Cell]) -> set[Cell]:
    # https://mathworld.wolfram.com/Circle-LineIntersection.html
    new_coords = set()
    start = map_cell(board.trajectory[-1], board.block_size)
    for coord in positions:
        rejected = False
        for obstacles in board.obstacles:
            x1, y1 = start
            x2, y2 = map_cell(coord, board.block_size)
            cx, cy = map_cell(obstacles, board.block_size)
            
            x1 -= cx
            y1 -= cy
            x2 -= cx
            y2 -= cy
            
            dr = sqrt((x1*y2)**2 - (x2*y1)**2)
            D = x1*y2 - x2*y1
            
            discrim = (board.block_size*RRADIUS)**2 * dr**2 - D**2
            if discrim > 0:
                print("coord", coord, "blocked by", obstacles)
                fltk.cercle(cx, cy, board.block_size*RRADIUS)
                rejected = True
                break
        if not rejected:
            new_coords.add(coord)
    return new_coords


def filter_positions(board: Board):
    positions = board.next_coords()
        
    if not len(board.trajectory):
        return positions
    
    if board.image is not None:
        return filter_imagebased_position(board, positions)
    return filter_textbased_postion(board, positions)
