from collections import deque
from time import time
from typing import Generator

import src.fltk as fltk
import src.graphic as graphic
from src.board import Cell, Board
from src.settings import LAX_RULE
from src.tools import filter_positions

def indepth_search(board: Board, rule: str) -> Generator[list[Cell], None, list[Cell]]:
    stack = deque([[coord] for coord in board.next_coords()])
    done = set()
    while stack and not board.win():
        board.trajectory = stack.pop()
        
        t_traj = tuple(board.trajectory)
        if t_traj in done:
            continue
        done.add(t_traj)
        
        if rule == LAX_RULE:
            next_coords = board.next_coords()
        else:
            next_coords = filter_positions(board)
            
        for coord in next_coords:
            new_traj = board.trajectory + [coord]
            if tuple(new_traj) not in done:
                yield new_traj
                stack.append(new_traj)
    return board.trajectory

def breadth_search(board: Board, rule: str) -> Generator[list[Cell], None, list[Cell]]:
    stack = deque([[coord] for coord in board.next_coords()])
    done = set()
    while stack and not board.win():
        board.trajectory = stack.popleft()
        t_traj = tuple(board.trajectory)
        if t_traj in done:
            continue
        done.add(t_traj)
        
        if rule == LAX_RULE:
            next_coords = board.next_coords()
        else:
            next_coords = filter_positions(board)
        
        for coord in next_coords:
            new_traj = board.trajectory + [coord]
            if tuple(new_traj) not in done:
                yield new_traj
                stack.append(new_traj)
    
    return board.trajectory

SOLVERS = {
    "indepth": indepth_search,
    "breadth": breadth_search
}

def solve(board: Board, solver: callable, c_time: bool, rule: str) -> None:
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

def fast_solve(board: Board, solver: callable, c_time: bool, rule: str) -> None:
    gen = solver(board, rule)
    trajectory = []
    
    start = time()
    
    while not board.win(trajectory): trajectory = next(gen)
        
    if c_time:    
        print(f"Solved in {time() - start:0.2}s")

    graphic.draw_trajectory(trajectory, board)
    graphic.wait_exit()
