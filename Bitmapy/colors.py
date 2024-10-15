from .types import Color

def parse_color(color: Color) -> Color:
    if len(color) == 3:
        color = (*color, 255)
    if len(color) != 4 or not all([data >= 0 and data <= 255 for data in color]):
        raise ValueError(f"Invalid color format: {color}. Color should be a tuple of 3 or 4 integers")
    return color

def blend_color(destination: Color, source: Color) -> Color:
    dest_red, dest_green, dest_blue, dest_alpha = parse_color(destination)
    src_red, src_green, src_blue, src_alpha = parse_color(source)

    src_alpha /= 255
    dest_alpha /= 255
    
    red   = src_red * src_alpha + dest_red * (1 - src_alpha)
    green = src_green * src_alpha + dest_green * (1 - src_alpha)
    blue  = src_blue * src_alpha + dest_blue * (1 - src_alpha)
    alpha = src_alpha + dest_alpha * (1 - src_alpha)
    return (round(red), round(green), round(blue), round(alpha * 255))

MAX = 255
HALF = 127
MIN = 0

EMPTY = (MIN, MIN, MIN, MIN)

BLACK = (MIN, MIN, MIN)
GRAY = GREY = (HALF, HALF, HALF)
WHITE = (MAX, MAX, MAX)

RED  = (MAX, MIN, MIN)
LIME = (MIN, MAX, MIN)
BLUE = (MIN, MIN, MAX)

GREEN = (MIN, HALF, MIN)

YELLOW = (MAX, MAX, MIN)
PURPLE = (MAX, MIN, MAX)
CYAN   = (MIN, MAX, MAX)

ORANGE = (MAX, HALF, MIN)
PINK   = (MAX, 190, 203)

LIGHT_BLUE = (63, 63, MAX)
SKY_BLUE   = (63, 63, 200)

LIGHT_GRAY = LIGHT_GREY = (190, 190, 190)
DARK_GRAY = DARK_GREY  = (67, 67, 67)

