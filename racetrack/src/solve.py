from collections import deque
from time import time
from typing import Generator
from heapq import heappush, heappop

from lib import fltk
from src import graphic
from src.board import Cell, Board
from src.settings import LAX_RULE
from src.tools import filter_positions, distance

__all__ = ["SOLVERS", "solve", "fast_solve"]

SearchType = Generator[list[Cell], None, list[Cell]]

def format_time(seconds: float):
    if seconds < 60:
        return f"{seconds:.2}s"
    return f"{seconds // 60}m {seconds - 60*(seconds//60):.2}s"

def next_coords(board: Board, rule: str) -> set[Cell]:
    if rule == LAX_RULE:
        return board.next_coords()
    return filter_positions(board)


def indepth_search(board: Board, rule: str) -> SearchType:
    stack = deque([[coord] for coord in board.next_coords()])
    done = set()
    indepth_search.skip = 0
    
    while stack and not board.win():
        board.trajectory = stack.pop()

        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            speed = board.speed(new_traj)
            if (coord, speed) not in done:
                done.add((coord, speed))
                stack.append(new_traj)
            else:
                indepth_search.skip += 1
    return board.trajectory


def breadth_search(board: Board, rule: str) -> SearchType:
    stack = deque([[coord] for coord in board.next_coords()])
    done = set()
    breadth_search.skip = 0
    while stack and not board.win():
        board.trajectory = stack.popleft()

        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            speed = board.speed(new_traj)
            if (coord, speed) not in done:
                done.add((coord, speed))
                stack.append(new_traj)
            else:
                breadth_search.skip += 1
    return board.trajectory


def average_zone(coords: set[Cell]) -> Cell:
    x, y = 0, 0
    for coord in coords:
        x += coord.x
        y += coord.y
    return Cell(x // len(coords), y // len(coords))


def astar(board: Board, rule: str) -> SearchType:
    heap = []
    average_finish_zone = average_zone(board.end)
    done = set()
    astar.skip = 0

    for start in board.start:
        heappush(heap, (distance(start, average_finish_zone), [start]))

    while heap and not board.win():
        _, board.trajectory = heappop(heap)

        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            speed = board.speed(new_traj)
            if (coord, speed) not in done:
                done.add((coord, speed))
                heappush(heap, (distance(coord, average_finish_zone), new_traj))
            else:
                astar.skip += 1
    return board.trajectory

def greedy(board: Board, rule: str) -> SearchType:
    heap = [(0, [start]) for start in board.start]
    done = set()
    greedy.skip = 0

    while heap and not board.win():
        _, board.trajectory = heappop(heap)

        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            speed = board.speed(new_traj)
            if (coord, speed) not in done:
                done.add((coord, speed))
                heappush(heap, (-distance(board.trajectory[-1], coord), new_traj))
            else:
                greedy.skip += 1
    return board.trajectory

def greedy2(board: Board, rule: str) -> SearchType:
    heap = [(1, 0, [start]) for start in board.start]
    done = set()
    greedy2.skip = 0

    while heap and not board.win():
        _, _, board.trajectory = heappop(heap)

        yield board.trajectory

        for coord in next_coords(board, rule):
            new_traj = board.trajectory + [coord]
            speed = board.speed(new_traj)
            if (coord, speed) not in done:
                done.add((coord, speed))
                heappush(heap, (-len(new_traj), -distance(board.trajectory[-1], coord), new_traj))
            else:
                greedy2.skip += 1
    return board.trajectory


SOLVERS = {
    "indepth": indepth_search,
    "breadth": breadth_search,
    "astar": astar,
    "greedy": greedy,
    "greedy2": greedy2
}


def solve(board: Board, solver: callable, c_time: bool, rule: str) -> None:
    gen = solver(board, rule)
    tags = []
    tev = None
    pause, step = False, False
    start, sum_time, attempt = time(), 0, 0
    while tev != "Quitte" and not board.win():
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
                next(gen)
                attempt += 1
            except StopIteration:
                ...

        step = False
        graphic.erase_tags(tags)
        tags = graphic.draw_trajectory(board)
        fltk.mise_a_jour()
    if tev == "Quitte":
        return
    
    print(f"Solution found in {len(board.trajectory)} positions")
    if c_time:
        print(f"Solved in {format_time(time() - start + sum_time)} in {attempt} attempts")
        print(f"Skiped {solver.skip} positions")

    graphic.wait_exit()


def fast_solve(board: Board, solver: callable, c_time: bool, rule: str) -> None:
    gen = solver(board, rule)

    start = time()
    attempt = 0

    while not board.win():
        next(gen)
        attempt += 1

    print(f"Solution found in {len(board.trajectory)} positions")
    if c_time:
        print(f"Solved in {format_time(time() - start)} in {attempt} attempts")
        print(f"Skiped {solver.skip} positions")

    graphic.draw_trajectory(board)
    graphic.wait_exit()
