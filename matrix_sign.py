""" LED matrix sign """
from threading import Timer
import time

from neopixel import *

from ascii_character_set import lookup
from chess import CHESS_GAME_MOVES


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
        self._color = Color(0, 50, 0)
        self.x_position = 0
        self.y_position = 0
        self._scroll = False
        self.scroll_delay = 0.250       # Scroll display in seconds
        self._brightness = 255          # Set to 0 for darkest and 255 for brightest
        self.transition_delay = 0.010   # Seconds
        self.transition = False         # Transition on display
        self.message_matrix = None

        self.chess_index = 0
        self.chess_move_delay = 2

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
        self._color = self._parse_color(value)
        self._display_message()

    def _parse_color(self, value):
        green = int(value[:2], 16)
        red = int(value[2:4], 16)
        blue = int(value[4:], 16)
        return Color(green, red, blue)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self._display_message()

    @property
    def scroll(self):
        return self._scroll

    @scroll.setter
    def scroll(self, value):
        # Make sure that this doesn't loop
        if value and not self._scroll:
            self.x_position = 0
            self._scroll = True
            self.scrolling()
        elif not value and self._scroll:
            self._scroll = False

    def scrolling(self):
        if self.scroll:
            self.x_position += 1
            array = self._get_message_array(self._get_display_matrix())
            self._display_array(array)
            t = Timer(self.scroll_delay, self.scrolling)
            t.start()

    def fill(self, color):
        for i in range(self.led_matrix.numPixels()):
            self.led_matrix.setPixelColor(i, color)
        self.led_matrix.show()

    def clear(self):
        self.fill(Color(0, 0, 0))

    def _display_message(self):
        """ Display the message """
        self.message_matrix = lookup(self.message)
        array = self._get_message_array(self._get_display_matrix())
        self._display_array(array)

    def _display_array(self, array, use_color=False):
        for i in range(self.led_matrix.numPixels()):
            if use_color and isinstance(array[i], str):
                color = self._parse_color(array[i])
            elif array[i]:
                color = self.color
            else:
                color = Color(0, 0, 0)

            self.led_matrix.setPixelColor(i, color)
            if self.transition:
                self.led_matrix.show()
                time.sleep(self.transition_delay)

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
        if not self.message_matrix:
            return []   # Empty grid array

        message_length = len(self.message_matrix[0])
        if message_length <= self.GRID_WIDTH:
            self.scroll = False
            return self.message_matrix

        self.scroll = True
        self.x_position = self.x_position % message_length
        x_end = (self.x_position + self.GRID_WIDTH) % message_length
        if self.x_position < x_end:
            return [self.message_matrix[i][self.x_position:x_end] for i in range(self.GRID_HEIGHT)]
        return [self.message_matrix[i][self.x_position:] + self.message_matrix[i][:x_end] for i in range(self.GRID_HEIGHT)]

    def chess(self):
        self.message_matrix = CHESS_GAME_MOVES[self.chess_index]
        array = self._get_message_array(self._get_display_matrix())
        self._display_array(array, use_color=True)
        self.chess_index += 1
        if self.chess_index < len(CHESS_GAME_MOVES):
            t = Timer(self.chess_move_delay, self.chess)
            t.start()
