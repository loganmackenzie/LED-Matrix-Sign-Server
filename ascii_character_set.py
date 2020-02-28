""" ASCII Character Set and Lookup """
from copy import deepcopy
from ascii_pixel_maps import *

ASCII_SET = [
    [],  # Column 0 (b'0000') is reserved
    [],  # Column 1 (b'0001') is reserved
    # 0010
    [SPACE, EXCLAMATION_POINT, DOUBLE_QUOTE, HASH, DOLLAR, PERCENT, AMPERSAND, SINGLE_QUOTE, OPEN_PARENTHESIS, CLOSE_PARENTHESIS, ASTERISK, PLUS, COMMA, MINUS, PERIOD, SLASH],
    # 0011
    [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, COLON, SEMICOLON, LESS_THAN, EQUALS, GREATER_THAN, QUESTION_MARK],
    # 0100
    [AT_SIGN, CAP_A, CAP_B, CAP_C, CAP_D, CAP_E, CAP_F, CAP_G, CAP_H, CAP_I, CAP_J, CAP_K, CAP_L, CAP_M, CAP_N, CAP_O],
    # 0101
    [CAP_P, CAP_Q, CAP_R, CAP_S, CAP_T, CAP_U, CAP_V, CAP_W, CAP_X, CAP_Y, CAP_Z, OPEN_SQUARE_BRACKET, Y_EQUALS, CLOSE_SQUARE_BRACKET, CARET, UNDERSCORE],
    # 0110
    [GRAVE_ACCENT, LOWER_A, LOWER_B, LOWER_C, LOWER_D, LOWER_E, LOWER_F, LOWER_G, LOWER_H, LOWER_I, LOWER_J, LOWER_K, LOWER_L, LOWER_M, LOWER_N, LOWER_O],
    # 0111
    [LOWER_P, LOWER_Q, LOWER_R, LOWER_S, LOWER_T, LOWER_U, LOWER_V, LOWER_W, LOWER_X, LOWER_Y, LOWER_Z, OPEN_CURLY_BRACE, VERTICAL_BAR, CLOSE_CURLY_BRACE, ARROW_RIGHT, ARROW_LEFT],
    [],  # Column 8 (b'1000') is not supported
    [],  # Column 9 (b'1001') is not supported
    [],  # Column 10 (b'1010') is not supported
    [],  # Column 11 (b'1011') is not supported
    [],  # Column 12 (b'1100') is not supported
    [],  # Column 13 (b'1101') is not supported
    [],  # Column 14 (b'1110') is not supported
    []   # Column 15 (b'1111') is not supported
]


def get_char(character):
    binary = format(ord(character), '0=8b')
    col = int(binary[:4], base=2)
    row = int(binary[4:], base=2)
    # print(f'Binary: {binary}, Row: {row}, Col: {col}')
    return deepcopy(ASCII_SET[col][row])


def lookup(line):
    """ Create the pixel map for a whole line """
    pixel_map = []
    for char in line:
        px_map = get_char(char)
        for i, row in enumerate(px_map):
            if len(pixel_map) > i:
                pixel_map[i] += row
            else:
                pixel_map.append(row)
    return pixel_map


def print_pixel_map(pixel_map, display_zero=' ', display_one='1'):
    """ Print the pixel map """
    for row in pixel_map:
        print(''.join(map(str, row)).replace('0', display_zero).replace('1', display_one))



if __name__ == '__main__':
    while True:
        line = input('Enter a character: ')

        _pixel_map = lookup(line)
        print_pixel_map(_pixel_map)
