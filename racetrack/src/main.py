import src.graphic as graphic
from src.board import Board

def play(board: Board):
    event = None
    waiting = False
    tags = []
    coords = None
    
    while event != "Quitte" and not board.win():
        if not waiting:
            coords = board.next_coords()
            tags.extend(graphic.draw_points(coords, board))
            waiting = True
        
        event = graphic.wait_next_event()
            
        if event == "ClicGauche":
            cell = graphic.get_cell_from_click(coords, board)
            if cell in coords:
                waiting = False
                graphic.erase_tags(tags)
                board.append(cell)
                tags.extend(graphic.draw_trajectory(board.trajectory, board))
        elif event == "BackSpace":
            if board.pop():
                graphic.erase_tags(tags)
                tags = graphic.draw_trajectory(board.trajectory, board)
                waiting = False
    