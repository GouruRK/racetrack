import src.fltk as fltk
import src.graphic as graphic
from src.board import Board

def play(board: Board):
    ev = None
    event = None
    waiting = False
    tags = []
    coords = None
    
    while event != "Quitte" and not board.win():
        ev = fltk.donne_ev()
        event = fltk.type_ev(ev)
        if not waiting:
            coords = board.next_coords()
            tags.extend(graphic.draw_points(coords, board))
            waiting = True
            
        if event == "ClicGauche":
            cell = graphic.get_cell_from_click(coords, board)
            if cell in coords:
                waiting = False
                graphic.erase_tags(tags)
                board.append(cell)
                tags.extend(graphic.draw_trajectory(board))
        elif event == "Touche":
            touche = fltk.touche(ev)
            if touche == "BackSpace":
                if board.pop():
                    graphic.erase_tags(tags)
                    tags = graphic.draw_trajectory(board)
                    waiting = False
        fltk.mise_a_jour()
    