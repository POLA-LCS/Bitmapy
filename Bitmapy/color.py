Color = tuple[int, int, int, int]

def parse_color(color: Color) -> Color:
    if isinstance(color, str) and is_hex(color):
        return get_color_from_hex(color)
    if len(color) == 3:
        color = (*color, 255)
    if len(color) != 4 or not all([data >= 0 and data <= 255 for data in color]):
        raise ValueError(f"Invalid color format: {color}.")
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

    return (int(red), int(green), int(blue), int(alpha * 255))

def get_hex_from_color(color: Color) -> str:
    hex_string = ''
    for data in color:
        hexadecimal = hex(data)[2:]
        if len(hexadecimal) == 1:
            hexadecimal = '0' + hexadecimal
        hex_string += hexadecimal
    return hex_string

def get_color_from_hex(hex_string: str) -> Color:
    color = (int(hex_string[:2], 16), int(hex_string[2:4], 16), int(hex_string[4:6], 16))
    if len(hex_string[:6]) == 2:
        color = (*color, 255)
    return color

def is_hex(hex_num: str) -> bool:
    hex_num = hex_num.lower()
    is_hex_or_not = []
    for char in hex_num:
        is_hex_or_not.append(char in '0123456789abcdef' and len(hex_num) in [6, 8])
    return all(is_hex_or_not)