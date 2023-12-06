from flask import Flask, jsonify, request, render_template
import chess
from math import floor

board = chess.Board()
legalMovesSquares = []
legalMoves = []
selectedPiece = None
squareSize = 1

def getLegalMoves(pos):
    piecePos = chess.parse_square(pos)
    allMoves = board.generate_legal_moves()
    pieceMoves = [move for move in allMoves if move.from_square == piecePos]
    readableMoves = [board.san(move) for move in pieceMoves]
    print(readableMoves)
    print(pieceMoves)
    return readableMoves

def getBoardAsArray(board=board):
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
                    'x':file*squareSize,
                    'y':rank*squareSize
                })
            else:
                row.append(None)
        boardArray.append(row)
    return boardArray

def getCoords(moveStr):
    move = board.parse_san(moveStr)
    coord = chess.square_name(move.to_square)
    xNames = ["a", "b", "c", "d", "e", "f","g","h"]
    x = coord[0]
    x = xNames.index(x) * squareSize + squareSize/2
    y = coord[1]
    y = (8-int(y)) * squareSize + squareSize/2
    print([x,y])
    return [x,y]




def parseMove(move_str,board=board):
    move = board.parse_san(move_str)
    piece = board.piece_at(move.from_square)
    if board.is_en_passant(move):
        moveType = "EnPassant"
    



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getBoard')
def getMoves():
    return jsonify(getBoardAsArray())

@app.route('/setup',methods=['POST'])
def setup():
    data = request.json
    global squareSize
    squareSize = data[0]
    print(f"Squaresize: {squareSize}")
    return '', 204

@app.route('/click_at', methods=['POST'])
def click_at():
    global legalMoves
    global legalMovesSquares
    global selectedPiece
    global board

    pieceXY = request.json
    pieceX = pieceXY[0]
    pieceY = pieceXY[1]

    x = floor(pieceX/squareSize)
    y = floor((8* squareSize - pieceY)/squareSize)
    xNames = ["a", "b", "c", "d", "e", "f","g","h"]
    
    square = xNames[x] + str(y + 1)

    if(x < 8 and y < 8):
        print(f"click at {xNames[x]}{y+1}")
    if not legalMovesSquares or square not in legalMovesSquares:# If legalmoves is empty => there is no square selected, if square is not in legalMoves => different square selected
        legalMovesSquares = getLegalMoves(square)
        legalMoves2 = [getCoords(square) for square in legalMovesSquares]
        selectedPiece = square
        print(f'selected piece at {selectedPiece}')
        return jsonify(legalMoves2,getBoardAsArray())
        
    elif square in legalMovesSquares:
        uci_move = selectedPiece + square
        move = chess.Move.from_uci(uci_move)
        board.push(move)
        print(f'moved from {selectedPiece} to {square}')
        return jsonify([], getBoardAsArray()) 



if __name__ == '__main__':
    app.run(debug=True)