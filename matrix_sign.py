""" LED matrix sign """
import time

from neopixel import *

from ascii_character_set import lookup


class MatrixSign:
    """ LED matrix sign """
    GRID_HEIGHT = 8
    GRID_WIDTH = 32

    # NeoPixel LED Strip Configuration
    LED_COUNT = GRID_HEIGHT * GRID_WIDTH    # Number of LED pixels
    LED_PIN        = 18     # GPIO Pin connected to the pixels (18 uses PWM!)
    LED_FREQ_HZ    = 800000 # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10     # DMA channel to use for generating signal (try 10)
    LED_INVERT     = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0      # Set to '1' for GPIOs 13, 19, 41, 45 or 53


    def __init__(self):
        self._message = ''
        self._color = Color(0, 255, 0)
        self.x_position = 0
        self.y_position = 0
        self.scroll = False
        self._brightness = 255      # Set to 0 for darkest and 255 for brightest
        self.display_delay = 0.010  # Seconds
        self.transition = True      # Transition on display
        self.message_matrix = None

        self.led_matrix = Adafruit_NeoPixel(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.brightness,
            self.LED_CHANNEL
        )
        self.led_matrix.begin()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self.led_matrix.setBrightness(self._brightness)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        green = int(value[:2], 16)
        red = int(value[2:4], 16)
        blue = int(color[4:], 16)
        self._color = Color(green, red, blue)
        self._display_message()

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self._display_message()

    def fill(self, color):
        self.led_matrix.fill(color)

    def clear(self):
        self.fill(Color(0, 0, 0))

    def _display_message(self):
        """ Display the message """
        self.message_matrix = lookup(self.message)
        array = self._get_message_array(self._get_display_matrix())

        for i in range(self.led_matrix.numPixels()):
            color = self.color if array[i] else Color(0, 0, 0)
            self.led_matrix.setPixelColor(i, color)
            if self.transition:
                self.led_matrix.show()
                time.sleep(self.display_delay)

        self.led_matrix.show()

    def _get_message_array(self, display_matrix):
        """ Get the 1D array of all the matrix """
        array = [0] * (self.GRID_HEIGHT * self.GRID_WIDTH)
        for y in range(len(display_matrix)):
            for x in range(len(display_matrix[y])):
                if x % 2:
                    index = x * self.GRID_HEIGHT + self.GRID_HEIGHT - y - 1
                else:
                    index = x * self.GRID_HEIGHT + y
                array[index] = display_matrix[y][x]
        return array

    def _get_display_matrix(self):
        """ Get the section of the message that's in the display matrix """
        message_length = len(self.message_matrix[0])
        if message_length <= self.GRID_WIDTH:
            self.scroll = False
            return self.message_matrix
        scroll = True
        x_end = self.x_position + GRID_WIDTH
        if x_end <= message_length:
            return [self.message_matrix[i][self.x_position:x_end] for i in rnage(self.GRID_HEIGHT)]
        x_end = x_end % self.GRID_WIDTH
        return [self.message_matrix[:x_end] + self.message_matrix[self.x_position:] for i in range(self.GRID_HEIGHT)]
