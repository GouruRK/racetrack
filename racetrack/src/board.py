from src.fltk import PhotoImage
from src.color import Color


class Cell:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Cell):
            return Cell(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def neighbour(self):
        return {self + c for c in neighbour}
    
    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Cell(x: {self.x}, y: {self.y})"

neighbour = {Cell(-1, -1), Cell(0, -1), Cell(1, -1), Cell(1, 0),
             Cell(1, 1),   Cell(0, 1),  Cell(-1, 1), Cell(-1, 0),
             Cell(0, 0)}

class Board:
    
    def __init__(self, image: PhotoImage = None, spacing: int = 0, block_size: int = 0) -> None:
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
        if not len(trajectory):
            targets = self.start
        elif len(trajectory) == 1:
            targets = trajectory[-1].neighbour()
        else:
            a = trajectory[-1]
            b = trajectory[-2]
            vector = Cell(a.x - b.x, a.y - b.y)
            targets = (trajectory[-1] + vector).neighbour()
        return (targets & self.legal) - set(trajectory)

    def filter_image_obstacles(self, start: Cell, dest: Cell) -> bool:
        return True

    def filter_obstacles(self, start: Cell, dest: Cell) -> bool:
        if self.image:
            return self.filter_image_obstacles(start, dest)
        return True

    def append(self, cell: Cell):
        self.trajectory.append(cell)

    def pop(self):
        if self.trajectory:
            cell = self.trajectory.pop()
            return cell

    def win(self, trajectory: list[Cell] = None):
        if trajectory is None:
            trajectory = self.trajectory
        return len(trajectory) and trajectory[-1] in self.end

    def load_board(board: list[str], block_size: int) -> 'Board':
        res = Board(block_size=block_size)
        for y, line in enumerate(board):
            for x, char in enumerate(line):
                if char == '>':
                    res.start.add(Cell(x, y))
                elif char == '*':
                    res.end.add(Cell(x, y))
                elif char == '#':
                    res.obstacles.add(Cell(x, y))
                if char != '#':
                    res.legal.add(Cell(x, y))
        return res
    
    def load_image(image: object, spacing: int) -> 'Board':
        res = Board(image, spacing)
        for y in range(image.height() // spacing):
            for x in range(image.width() // spacing):
                color = image.get(x*spacing, y*spacing)
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
    