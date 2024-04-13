from typing import Any

from src.parser import parse_map
from src.main import play
import src.graphic as graphic
from src.solve import solve, SOLVERS
from src.board import Board
from src.settings import *
from src.commandline import parse_args

def initiate_board_mode(args: dict[str, Any], board: list[str]):
    graphic.create_window_board(board, args["dim"])
    graphic.draw_board(board, args["dim"])
    graphic.draw_grid(board, args["dim"])
    
    rboard = Board.load_board(board, args["dim"])
    
    if args["solve"] is not None:
        solve(rboard, SOLVERS[args["solve"]], args["opti"], args["rule"])
    else:
        play(rboard, args["rule"])

def initiate_image_mode(args: dict[str, Any]):
    image = graphic.create_window_image(args["map"])
    graphic.draw_image_grid(image.width(), image.height(), args["spacing"])
    
    board = Board.load_image(image, args["spacing"])
    
    if args["solve"] is not None:
        solve(board, SOLVERS[args["solve"]], args["opti"], args["rule"])
    else:
        play(board, args["rule"])

def main():
    args = parse_args()
    if args["mode"] == TEXT_MODE:
        board = parse_map(args["map"])
        initiate_board_mode(args, board)
    else:
        initiate_image_mode(args)
    
if __name__ == '__main__':
    main()
