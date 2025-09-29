from flask import Flask, make_response
import time
from time import sleep
import random

app = Flask(__name__)
# API endpoint to get request data

@app.route('/api/delay/<int:delay>')
def delay(delay):
    sleep(delay / 1000)
    return "OK"

@app.route('/api/delay/random')
def rand_delay():
    rand_int = random.randint(50, 1000)
    sleep(rand_int / 1000)
    return "OK"


@app.route('/api/random_fail')
def rand_fail():
    rand_int = random.randint(1, 100)
    resp = make_response("Failed", 404)
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
