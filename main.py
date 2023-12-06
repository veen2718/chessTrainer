from flask import Flask, jsonify, request, render_template



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/get_moves', methods=['POST'])
def get_moves():
    dataRecieved = request.json
    print(dataRecieved)

    x = [input("input")]
    return jsonify(x)

if __name__ == '__main__':
    app.run(debug=True)