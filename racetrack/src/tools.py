from math import sqrt

from src.color import Color
from src.board import Cell, Board
from src.settings import RRADIUS

__all__ = ["distance", "map_cell", "filter_positions"]

VALID_TEXTURES = {Color.WHITE, Color.DARKCYAN, Color.GREY}


def distance(a: Cell, b: Cell) -> float:
    x = a.x - b.x
    y = a.y - b.y
    return sqrt(x * x + y * y)


def map_cell(cell: Cell, ratio: int) -> Cell:
    return Cell(cell.x * ratio, cell.y * ratio)


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

    count = 0

    while start.x != end.x and start.y != end.y:
        t_err = 2 * err
        if t_err >= dy:
            err += dy
            start.x += xslope
        if t_err <= dx:
            err += dx
            start.y += yslope

        count += 1
        if count % 3 == 0:
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
    new_coords = set()
    start = map_cell(board.trajectory[-1], board.block_size)
    for coord in positions:
        t_coord = map_cell(coord, board.block_size)
        rejected = False
        for in_between in bresenham(start.copy(), t_coord.copy()):
            for obstacles in board.obstacles:
                obstacles = map_cell(obstacles, board.block_size)
                if distance(in_between, obstacles) <= board.block_size * RRADIUS:
                    rejected = True
                    break
            if rejected:
                break
        if not rejected:
            new_coords.add(coord)
    return new_coords


def filter_positions(board: Board) -> set[Cell]:
    positions = board.next_coords()

    if not board.trajectory:
        return positions

    if board.image is not None:
        return filter_imagebased_position(board, positions)
    return filter_textbased_postion(board, positions)
