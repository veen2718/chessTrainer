import chess
from node import *
from json import load


class Config:
    def __init__(self):
        self.opening = "Sicilian Defense: Hyperaccelerated Dragon"
        with open('data.json', 'r') as dataJson:
            self.allData = load(dataJson)
        self.openingData = self.allData[self.opening]
        self.setupMoves = self.openingData["setup"]


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
        self.historyTree = makeTree(self.openingData["data"])

config = Config()
