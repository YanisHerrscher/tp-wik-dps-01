from sys import argv
from flask import Flask

app = Flask(__name__)

@app.route('/ping')
def api():
    return {}

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=argv[1],
        debug = False)