import chess
from math import floor
import webbrowser
from threading import Timer

from initialize import config as cf

from app import app





def open_browser(link='http://127.0.0.1:5000/'):
    if not cf.opened:
        #print(opened)
        cf.opened = True
        webbrowser.open_new_tab(f'{link}')
        #webbrowser.open_new(f'{link}')
        print("Browser opened.",cf.opened)
        





def parseMove(move_str,board=cf.board):
    move = board.parse_san(move_str)
    piece = board.piece_at(move.from_square)
    if board.is_en_passant(move):
        moveType = "EnPassant"
    






if __name__ == '__main__':
    Timer(0.5, open_browser).start()
    app.run(debug=False)