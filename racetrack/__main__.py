from typing import Any

from lib import fltk

from src import graphic
from src.board import Board
from src.main import play
from src.parser import parse_args, parse_map
from src.settings import TEXT_MODE
from src.solve import solve, fast_solve, SOLVERS


def initiate_board_mode(args: dict[str, Any], board: list[str]):
    graphic.create_window_board(board, args["dim"])
    graphic.draw_board(board, args["dim"])
    graphic.draw_grid(board, args["dim"])
    fltk.mise_a_jour()
    return Board.load_board(board, args["dim"])


def initiate_image_mode(args: dict[str, Any]):
    image = graphic.create_window_image(args["map"])
    graphic.draw_image_grid(image.width(), image.height(), args["spacing"])
    fltk.mise_a_jour()
    return Board.load_image(image, args["spacing"])


def main():
    args = parse_args()
    if args["mode"] == TEXT_MODE:
        board = parse_map(args["map"])
        board = initiate_board_mode(args, board)
    else:
        board = initiate_image_mode(args)

    if args["solve"] is not None:
        if args["opti"]:
            fast_solve(board, SOLVERS[args["solve"]], args["time"], args["rule"])
        else:
            solve(board, SOLVERS[args["solve"]], args["time"], args["rule"])
    else:
        play(board, args["rule"])


if __name__ == "__main__":
    main()
