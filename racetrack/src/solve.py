from src.board import Board
import src.graphic as graphic
import src.fltk as fltk
from collections import deque


def indepth_search(board: Board):
    if board.win():
        return board.trajectory
    
    stack = deque([[coord] for coord in board.next_coords()])
    
    while stack and not board.win():
        board.trajectory = stack.pop()
        
        for coord in board.next_coords():
            yield board.trajectory + [coord]
            stack.append(board.trajectory + [coord])
    return board.trajectory

def breadth_search(board: Board):
    if board.win():
        return board.trajectory
    
    stack = deque([[coord] for coord in board.next_coords()])
    
    while stack and not board.win():
        board.trajectory = stack.popleft()
        
        for coord in board.next_coords():
            yield board.trajectory + [coord]
            stack.append(board.trajectory + [coord])
    
    return board.trajectory

SOLVERS = {
    "indepth": indepth_search,
    "breadth": breadth_search
}

def main(board: Board, solver: callable):
    gen = solver(board)
    trajectory, tags = [], []
    tev = None
    ended, pause, step = False, False, False
    while tev != "Quitte":
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        
        if tev == "Touche":
            touche = fltk.touche(ev)
            if touche == "space":
                pause = not pause
            elif touche == "Return":
                step = True
        
        if not (ended or board.win(trajectory)):
            if step or not pause:
                try:
                    trajectory = next(gen)
                except StopIteration:
                    ended = True

        step = False
        if board.win(trajectory):
            ended = True
        
        graphic.erase_tags(tags)
        tags = graphic.draw_trajectory(trajectory, board)
        
        fltk.mise_a_jour()