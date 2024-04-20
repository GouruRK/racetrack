from collections import deque
from time import time
from typing import Generator
from heapq import heappush, heappop

from lib import fltk
from src import graphic
from src.board import Cell, Board
from src.settings import LAX_RULE
from src.tools import filter_positions, distance

SearchType = Generator[list[Cell], None, list[Cell]]


def next_coords(board: Board, rule: str) -> set[Cell]:
    if rule == LAX_RULE:
        return board.next_coords()
    return filter_positions(board)


def indepth_search(board: Board, rule: str) -> SearchType:
    stack = deque([[coord] for coord in board.next_coords()])
    done = set()
    while stack and not board.win():
        board.trajectory = stack.pop()

        t_traj = tuple(board.trajectory)
        if t_traj in done:
            continue
        done.add(t_traj)
        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            if tuple(new_traj) not in done:
                stack.append(new_traj)
    return board.trajectory


def breadth_search(board: Board, rule: str) -> SearchType:
    stack = deque([[coord] for coord in board.next_coords()])
    done = set()
    while stack and not board.win():
        board.trajectory = stack.popleft()
        t_traj = tuple(board.trajectory)
        if t_traj in done:
            continue
        done.add(t_traj)
        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            if tuple(new_traj) not in done:
                stack.append(new_traj)
    return board.trajectory


def average_zone(coords: set[Cell]) -> Cell:
    x, y = 0, 0
    for coord in coords:
        x += coord.x
        y += coord.y
    return Cell(x // len(coords), y // len(coords))


def astar(board: Board, rule: str) -> SearchType:
    done = set()
    heap = []
    average_finish_zone = average_zone(board.end)

    for start in board.start:
        heappush(heap, (distance(start, average_finish_zone), [start]))

    while heap and not board.win():
        _, board.trajectory = heappop(heap)
        t_traj = tuple(board.trajectory)

        if t_traj in done:
            continue
        done.add(t_traj)
        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            if tuple(new_traj) not in done:
                heappush(heap, (distance(coord, average_finish_zone), new_traj))
    return board.trajectory


def greedy(board: Board, rule: str) -> SearchType:
    done = set()
    heap = [(0, [start]) for start in board.start]

    while heap and not board.win():
        _, board.trajectory = heappop(heap)
        t_traj = tuple(board.trajectory)

        if t_traj in done:
            continue
        done.add(t_traj)
        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            if tuple(new_traj) not in done:
                heappush(heap, (-distance(board.trajectory[-1], coord), new_traj))
    return board.trajectory


SOLVERS = {
    "indepth": indepth_search,
    "breadth": breadth_search,
    "astar": astar,
    "greedy": greedy,
}


def solve(board: Board, solver: callable, c_time: bool, rule: str) -> None:
    gen = solver(board, rule)
    trajectory, tags = [], []
    tev = None
    pause, step = False, False
    start, sum_time, attempt = time(), 0, 0
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
                attempt += 1
            except StopIteration:
                ...

        step = False
        graphic.erase_tags(tags)
        tags = graphic.draw_trajectory(trajectory, board)
        fltk.mise_a_jour()
    if tev == "Quitte":
        return
    if c_time:
        print(f"Solved in {time() - start + sum_time:0.2}s in {attempt} attempts")

    graphic.wait_exit()


def fast_solve(board: Board, solver: callable, c_time: bool, rule: str) -> None:
    gen = solver(board, rule)
    trajectory = []

    start = time()
    attempt = 0

    while not board.win(trajectory):
        trajectory = next(gen)
        attempt += 1

    if c_time:
        print(f"Solved in {time() - start:0.2}s in {attempt} attempts")

    graphic.draw_trajectory(trajectory, board)
    graphic.wait_exit()
