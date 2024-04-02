from src.board import Cell
from math import sqrt

def parse_map(filepath: str) -> list[str]:
    with open(filepath, "r") as file:
        return [line for line in file]
    
def distance(a: Cell, b: Cell) -> float:
    x = a.x - b.x
    y = a.y - b.y
    return sqrt(x*x + y*y)
