# (R, G, B) | (R, G, B, A)
Color = tuple[int, int, int] | tuple[int, int, int, int]

# (LEFT, TOP)
Coord = tuple[int, int]

Pixel = tuple[Color, Coord]
Area = tuple[Color, Coord, Coord]