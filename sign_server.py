#!/usr/bin/env python3
# NeoPixel Matrix Web Server
from flask import Flask

from matrix_sign import MatrixSign


led_sign = MatrixSign()


app = Flask(__name__)


@app.route('/')
def main():
    led_sign.message = 'Home!'


@app.route('/display/<string:message>')
def display(message):
    led_sign.message = message


@app.route('/clear')
def clear():
    led_sign.clear()


@app.route('/color/<string:color>')
def set_color(color):
    led_sign.color = color


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
