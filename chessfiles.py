import chess
from initialize import config as cf


def getLegalMoves(pos):
    piecePos = chess.parse_square(pos)
    allMoves = cf.board.generate_legal_moves()
    pieceMoves = [move for move in allMoves if move.from_square == piecePos]
    readableMoves = [[chess.square_name(move.from_square), chess.square_name(move.to_square)] for move in pieceMoves]
    print(readableMoves,'readable moves')
    print(pieceMoves,'piece moves')
    return readableMoves

def getBoardAsArray(board=cf.board):
    boardArray = []
    for rank in range(8):
        row = []
        for file in range(8):
            piece = board.piece_at(chess.square(file,7-rank))
            if piece:
                col = 'w' if piece.color == chess.WHITE else 'b'
                id = (col + piece.symbol()).lower()
                row.append({
                    'id':id,
                    'x':file*cf.squareSize,
                    'y':rank*cf.squareSize
                })
            else:
                row.append(None)
        boardArray.append(row)
    return boardArray

def getCoords(moveList):
    moveStr = moveList[1]
    startSquare = moveList[0]
    print("movestr",moveStr)
    try:
        move = cf.board.parse_san(startSquare + moveStr)
        coord = chess.square_name(move.to_square)
        xNames = ["a", "b", "c", "d", "e", "f","g","h"]
        x = coord[0]
        x = xNames.index(x) * cf.squareSize + cf.squareSize/2
        y = coord[1]
        y = (8-int(y)) * cf.squareSize + cf.squareSize/2
        print([x,y])
        return [x,y]
    except Exception as e:
        print(str(cf.board))
        print(e)