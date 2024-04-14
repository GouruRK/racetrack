from src.board import Board
import src.graphic as graphic
import src.fltk as fltk
from collections import deque
from src.settings import LAX_RULE
from src.tools import filter_positions
from time import time

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

def solve(board: Board, solver: callable, fast: bool, c_time: bool, rule: str):
    if fast:
        return fast_solve(board, solver, c_time, rule)
    gen = solver(board, rule)
    trajectory, tags = [], []
    tev = None
    pause, step = False, False
    start, sum_time = time(), 0
    while tev != "Quitte" and not board.win(trajectory):
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "Touche":
            touche = fltk.touche(ev)
            if touche == "space":
                pause = not pause
                if pause:
                    sum_time = time() - start
                else:
                    start = time()
            elif touche == "Return":
                step = True
        
        if step or not pause:
            try:
                trajectory = next(gen)
            except StopIteration:
                ...

        step = False
        graphic.erase_tags(tags)
        tags = graphic.draw_trajectory(trajectory, board)
        fltk.mise_a_jour()
    if tev == "Quitte":
        return
    if c_time:
        print(f"Solved in {time() - start + sum_time:0.2}s")
    
    graphic.wait_exit()

def fast_solve(board: Board, solver: callable, c_time: bool, rule: str):
    gen = solver(board, rule)
    attempts = 0
    trajectory = []
    
    start = time()
    while not board.win(trajectory):
        trajectory = next(gen)
        attempts += 1
    
    if c_time:    
        print(f"Solved in {time() - start:0.2}s")

    graphic.draw_trajectory(trajectory, board)
    graphic.wait_exit()
