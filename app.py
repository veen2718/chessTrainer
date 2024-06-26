from flask import Flask, jsonify, request, render_template
from math import floor
import os

from initialize import config as cf
from chessfiles import *
from node import *

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
    cf.squareSize = data[0]
    print(f"Squaresize: {cf.squareSize}")
    print('setup finished')

    
    
    app.run()


    return '', 204


@app.route('/setupMoves')
def setupMoves():
    for setupMove in cf.setupMoves:
        move = chess.Move.from_uci(setupMove[0]+setupMove[1])
    
        cf.board.push(move)
        cf.history.append([setupMove[0],setupMove[1]])
        print(f'moved from {setupMove[0]} to {setupMove[1]}')
        
    return jsonify(getBoardAsArray()) 


@app.route('/shutdown',methods=['POST'])
def shutdown():
    cf.histories.append(cf.history)
    #print(cf.histories)
    historyTree = cf.historyTree.getOrigin().toDict()
    print(json.dumps(historyTree,indent=4))
    cf.allData['data'] = historyTree
    with open('data.json', 'w') as dataJson:
        json.dump(cf.allData, dataJson,indent=2)
    displayTree(cf.historyTree)
    os._exit(0)


@app.route('/back')
def back():
    cf.histories.append(cf.history)
    cf.history.pop()
    cf.board = chess.Board()
    for move in cf.history:
        cf.board.push(chess.Move.from_uci(move[0]+move[1]))
    cf.historyTree = cf.historyTree.parent
    print('moved back 1')
    x = getBoardAsArray()
    for i in x:
        print(i)
    print(cf.board)
    displayTree(cf.historyTree)
    return jsonify(getBoardAsArray(cf.board))


@app.route('/click_at', methods=['POST'])
def click_at():
    print("\n")

    pieceXY = request.json
    pieceX = pieceXY[0]
    pieceY = pieceXY[1]

    x = floor(pieceX/cf.squareSize)
    y = floor((8* cf.squareSize - pieceY)/cf.squareSize)
    xNames = ["a", "b", "c", "d", "e", "f","g","h"]
    
    square = xNames[x] + str(y + 1)
    move = None
    if cf.selectedPiece:
        move = cf.selectedPiece + square
    if(x < 8 and y < 8):
        print(f"click at {xNames[x]}{y+1}")
    if not cf.legalMovesSquares or (square not in cf.legalMovesSquares and move not in cf.legalMovesSquares):# If legalmoves is empty => there is no square selected, if square is not in legalMoves => different square selected
        print(cf.legalMovesSquares,"cf.legalMovesSquares",square)
        cf.legalMovesSquares = getLegalMoves(square)
        print(cf.legalMovesSquares,"cf.legalMovesSquares")
        print(f"about to getCoords, cf.legalMovesSquares:{cf.legalMovesSquares}")
        legalMoves2 = [getCoords(square1) for square1 in cf.legalMovesSquares]
        cf.legalMovesSquares = [f"{x[0]}{x[1]}" for x in cf.legalMovesSquares]
        print(cf.legalMovesSquares,"cf.legalMovesSquares")
        cf.selectedPiece = square
        print(f'selected piece at {cf.selectedPiece}')
        return jsonify(legalMoves2,getBoardAsArray(cf.board))
        
    elif square in cf.legalMovesSquares or move in cf.legalMovesSquares: #one of the possible moves has been selected. A move will be made
        os.system('clear')
        print("square in legal moves")
        uci_move = cf.selectedPiece + square
        move = chess.Move.from_uci(uci_move)
        #print(move)
        cf.board.push(move)
        cf.history.append([cf.selectedPiece,square])

        
        cf.historyTree = cf.historyTree.addChild(uci_move)
        displayTree(cf.historyTree.getOrigin())

        print(f'moved from {cf.selectedPiece} to {square}')
        cf.legalMovesSquares = []
        return jsonify([], getBoardAsArray(cf.board)) 
    else:
        print("something went wrong")