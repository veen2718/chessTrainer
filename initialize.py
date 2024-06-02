import chess


class Config:
    def __init__(self):
        self.board = chess.Board()
        self.legalMovesSquares = []
        self.legalMoves = []
        self.selectedPiece = None
        self.squareSize = 1 
        self.opened = False
        self.history = []

config = Config()
