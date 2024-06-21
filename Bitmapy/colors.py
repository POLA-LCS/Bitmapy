from .types import Color

def parse_color(color: Color) -> Color:
    if len(color) == 3:
        color = (*color, 255)
    if len(color) != 4 or not all([data >= 0 and data <= 255 for data in color]):
        raise ValueError(f"Invalid color format: {color}. Color should be a tuple of 3 or 4 integers")
    return color

def blend_color(color_a: Color, color_b: Color) -> Color:
    r1, g1, b1, a_alpha = parse_color(color_a)
    r2, g2, b2, b_alpha = parse_color(color_b)

    a_alpha /= 255
    b_alpha /= 255

    r = round((r1 * a_alpha) + (r2 * b_alpha))
    g = round((g1 * a_alpha) + (g2 * b_alpha))
    b = round((b1 * a_alpha) + (b2 * b_alpha))

    a = round((a_alpha + b_alpha * (1 - a_alpha)) * 255)

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    a = max(0, min(255, a))

    return (r, g, b, a)

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

