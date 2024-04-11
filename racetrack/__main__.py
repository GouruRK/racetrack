from typing import Any

from src.commandline import parse_args, TEXT_MODE, IMAGE_MODE
from src.parser import parse_map
from src.main import play
import src.graphic as graphic
from src.solve import solve, SOLVERS
from src.board import Board

def initiate_board_mode(args: dict[str, Any], board: list[str]):
    graphic.create_window_board(board, args["dim"])
    graphic.draw_board(board, args["dim"])
    graphic.draw_grid(board, args["dim"])
    
    rboard = Board.load_board(board, args["dim"])
    
    if args["solve"] is not None:
        solve(rboard, SOLVERS[args["solve"]], args["opti"])
    else:
        play(rboard)

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
        initiate_image_mode(args)
    

if __name__ == '__main__':
    main()
