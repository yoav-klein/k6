from flask import Flask, make_response
import time
from time import sleep
import random
import os

app = Flask(__name__)
# API endpoint to get request data


failed_percentage = int(os.getenv('PERCENT_FAILED', '5'))
slow_response_ms = int(os.getenv('SLOW_RESPONSE_MS', '500'))
slow_response_percentage = int(os.getenv('PERCENT_SLOW_RESPONSE', '5'))


@app.route('/api/delay/<int:delay>')
def delay(delay):
    sleep(delay / 1000)
    return "OK"

@app.route('/api/delay/random')
def rand_delay():
    rand_int = random.randint(0, 100)
    if(rand_int < slow_response_percentage):
        sleep(slow_response_ms / 1000)
    else:
        sleep(rand_int / 1000)
    return "OK"

@app.route('/api/random_fail')
def rand_fail():
    rand_int = random.randint(0, 100)
    failed_resp = make_response("Failed", 404)

    if(rand_int < failed_percentage):
        return failed_resp

    return "OK"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
