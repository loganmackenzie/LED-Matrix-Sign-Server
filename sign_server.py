#!/usr/bin/env python3
# NeoPixel Matrix Web Server
from flask import Flask

from matrix_sign import MatrixSign


led_sign = MatrixSign()


app = Flask(__name__)


@app.route('/')
def main():
    led_sign.message = 'Home!'
    return 'OK\n', 200


@app.route('/display/<string:message>')
def display(message):
    led_sign.message = message
    return message, 200


@app.route('/clear')
def clear():
    led_sign.clear()
    return 'OK\n', 200


@app.route('/color/<string:color>')
def set_color(color):
    led_sign.color = color
    return 'OK\n', 200


@app.route('/scroll/delay/<float:delay>')
def set_scroll_delay(delay):
    led_sign.scroll_delay = delay
    return 'OK\n', 200


@app.route('/transition/<string:transition')
def set_transition(transition):
    if transition.lower() == 'on':
        led_sign.transition = True
        return 'Transition on', 200
    elif transition.lower() == 'off':
        led_sign.transition = False
        return 'Transition off', 200
    else:
        return 'Could not set transition', 400

@app.route('/transition/delay/<float:delay>')
def set_transition_delay(delay):
    led_sign.display_delay = delay
    return 'OK\n', 200


@app.route('/chess')
def chess():
    led_sign.chess()
    return 'OK\n', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
