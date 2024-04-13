from src.board import Board
import src.graphic as graphic
import src.fltk as fltk
from collections import deque
from src.settings import LAX_RULE
from src.tools import filter_positions

def indepth_search(board: Board, rule: str):
    stack = deque([[coord] for coord in board.next_coords()])
    
    while stack and not board.win():
        board.trajectory = stack.pop()
        
        if rule == LAX_RULE:
            next_coords = board.next_coords()
        else:
            next_coords = filter_positions(board)
            
        for coord in next_coords:
            yield board.trajectory + [coord]
            stack.append(board.trajectory + [coord])
    return board.trajectory

def breadth_search(board: Board, rule: str):
    stack = deque([[coord] for coord in board.next_coords()])
    
    while stack and not board.win():
        board.trajectory = stack.popleft()
        
        if rule == LAX_RULE:
            next_coords = board.next_coords()
        else:
            next_coords = filter_positions(board)
        
        for coord in next_coords:
            yield board.trajectory + [coord]
            stack.append(board.trajectory + [coord])
    
    return board.trajectory

SOLVERS = {
    "indepth": indepth_search,
    "breadth": breadth_search
}

def solve(board: Board, solver: callable, fast: bool, rule: str):
    if fast:
        return fast_solve(board, solver, rule)
    gen = solver(board, rule)
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
            graphic.draw_trajectory(trajectory, board)
        graphic.erase_tags(tags)
        tags = graphic.draw_trajectory(trajectory, board)
        
        fltk.mise_a_jour()

def fast_solve(board: Board, solver: callable, rule: str):
    gen = solver(board, rule)
    attempts = 0
    trajectory = []
    
    while not board.win(trajectory):
        trajectory = next(gen)
        attempts += 1

    graphic.draw_trajectory(trajectory, board)
    event = None
    while event != "Quitte":
        event = graphic.wait_event()
