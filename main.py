from flask import Flask, jsonify, request, render_template
import chess
from math import floor
import os
import webbrowser
from threading import Timer




board = chess.Board()
legalMovesSquares = []
legalMoves = []
selectedPiece = None
squareSize = 1 
opened = False
history = []

def open_browser(link='http://127.0.0.1:5000/'):
    global opened
    if not opened:
        #print(opened)
        opened = True
        webbrowser.open_new_tab(f'{link}')
        #webbrowser.open_new(f'{link}')
        print("Browser opened.",opened)
        


def getLegalMoves(pos):
    piecePos = chess.parse_square(pos)
    allMoves = board.generate_legal_moves()
    pieceMoves = [move for move in allMoves if move.from_square == piecePos]
    readableMoves = [[chess.square_name(move.from_square), chess.square_name(move.to_square)] for move in pieceMoves]
    print(readableMoves,'readable moves')
    print(pieceMoves,'piece moves')
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

def getCoords(moveList):
    moveStr = moveList[1]
    startSquare = moveList[0]
    print("movestr",moveStr)
    try:
        move = board.parse_san(startSquare + moveStr)
        coord = chess.square_name(move.to_square)
        xNames = ["a", "b", "c", "d", "e", "f","g","h"]
        x = coord[0]
        x = xNames.index(x) * squareSize + squareSize/2
        y = coord[1]
        y = (8-int(y)) * squareSize + squareSize/2
        print([x,y])
        return [x,y]
    except Exception as e:
        print(str(board))
        print(e)



def parseMove(move_str,board=board):
    move = board.parse_san(move_str)
    piece = board.piece_at(move.from_square)
    if board.is_en_passant(move):
        moveType = "EnPassant"
    



app = Flask(__name__)





@app.route('/')
def index():
    global host
    print('starting...')
    host = request.host
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
    print('setup finished')
    

    pid = os.getpid()
    with open("server.pid", "w") as f:
        f.write(str(pid))
    print(f"Starting server with PID {pid}")
    app.run()


    return '', 204

@app.route('/shutdown',methods=['POST'])
def shutdown():

    print(history)
    os._exit(0)


@app.route('/click_at', methods=['POST'])
def click_at():
    print("\n")
    global legalMoves
    global legalMovesSquares
    global selectedPiece
    global board
    global history

    pieceXY = request.json
    pieceX = pieceXY[0]
    pieceY = pieceXY[1]

    x = floor(pieceX/squareSize)
    y = floor((8* squareSize - pieceY)/squareSize)
    xNames = ["a", "b", "c", "d", "e", "f","g","h"]
    
    square = xNames[x] + str(y + 1)
    move = None
    if selectedPiece:
        move = selectedPiece + square
    if(x < 8 and y < 8):
        print(f"click at {xNames[x]}{y+1}")
    if not legalMovesSquares or (square not in legalMovesSquares and move not in legalMovesSquares):# If legalmoves is empty => there is no square selected, if square is not in legalMoves => different square selected
        print(legalMovesSquares,"legalmovessquares",square)
        legalMovesSquares = getLegalMoves(square)
        print(legalMovesSquares,"legalmovessquares")
        print(f"about to getCoords, legalMovesSquares:{legalMovesSquares}")
        legalMoves2 = [getCoords(square1) for square1 in legalMovesSquares]
        legalMovesSquares = [f"{x[0]}{x[1]}" for x in legalMovesSquares]
        print(legalMovesSquares,"legalmovessquares")
        selectedPiece = square
        print(f'selected piece at {selectedPiece}')
        return jsonify(legalMoves2,getBoardAsArray())
        
    elif square in legalMovesSquares or move in legalMovesSquares: #one of the possible moves has been selected. A move will be made
        os.system('clear')
        print("square in legal moves")
        uci_move = selectedPiece + square
        move = chess.Move.from_uci(uci_move)
        #print(move)
        board.push(move)
        history.append([selectedPiece,square])
        print(f'moved from {selectedPiece} to {square}')
        legalMovesSquares = []
        return jsonify([], getBoardAsArray()) 
    else:
        print("something went wrong")



if __name__ == '__main__':
    Timer(0.5, open_browser).start()
    app.run(debug=False)