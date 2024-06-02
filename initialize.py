import chess
from node import *

class Config:
    def __init__(self):
        self.setupMoves = [["e2", "e4"], ["c7", "c5"],["g1","f3"],["g7","g6"]]
        self.mode = 'write'



        self.board = chess.Board()
        self.legalMovesSquares = []
        self.legalMoves = []
        self.selectedPiece = None
        self.squareSize = 1 
        self.opened = False
        self.history = []
        self.histories = []
        

config = Config()
