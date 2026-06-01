from sys import argv
from flask import Flask
from Lib.func import Data
import datetime as dt

app = Flask(__name__)

@app.route('/ping')
def api():
    data.increment()
    return {}

@app.route('/stats')
def stats():
    data.increment()
    now = dt.datetime.now() - date
    return {"request" : data.get_request(), "name" : argv[2], "date" : str(now.total_seconds())}


if __name__ == '__main__':
    data = Data()
    name = argv[2]
    date = dt.datetime.now()
    app.run(
        host="127.0.0.1",
        port=argv[1],
        debug = False)