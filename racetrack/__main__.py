from typing import Any

from src.commandline import parse_args, TEXT_MODE, IMAGE_MODE
from src.parser import parse_map
from src.main import play
import src.graphic as graphic
import src.solve as solve
from src.board import Board

import src.fltk as fltk

def initiate_board_mode(args: dict[str, Any], board: list[str]):
    graphic.create_window_board(board)
    graphic.draw_board(board)
    graphic.draw_grid(board)
    
    if args["solve"] is not None:
        solve.main(Board.load_board(board), solve.SOLVERS[args["solve"]])
    else:
        play(Board.load_board(board))

def initiate_image_mode(args: dict[str, Any]):
    board = Board.load_image(args["map"], args["spacing"])
    
    if args["solve"] is not None:
        solve.main(board, solve.SOLVERS[args["solve"]])
    else:
        play(board)

def main():
    args = parse_args()
    if args["mode"] == TEXT_MODE:
        board = parse_map(args["map"])
        initiate_board_mode(args, board)
    else:
        initiate_image_mode()
    

if __name__ == '__main__':
    main()
