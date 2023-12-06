from flask import Flask, jsonify, request, render_template
import chess

board = chess.Board()

squareSize = None

def getMoves(pos):
    piecePos = chess.parse_square(pos)
    allMoves = board.generate_legal_moves()
    pieceMoves = [move for move in allMoves if move.from_square == piecePos]
    readableMoves = [board.san(move) for move in pieceMoves]
    print(readableMoves)
    print(pieceMoves)

app = Flask(__name__)

getMoves('e2')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup',methods=['POST'])
def setup():
    data = request.json
    global squareSize
    squareSize = data[0]
    print(f"Squaresize: {squareSize}")

@app.route('/get_moves', methods=['POST'])
def get_moves():
    dataRecieved = request.json
    print(dataRecieved)
    x = [input("input")]


    
if __name__ == '__main__':
    app.run(debug=True)