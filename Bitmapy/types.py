Color = tuple[int, int, int, int]
Coord = tuple[int, int]
Pixel = tuple[Color, Coord]
Area = tuple[Color, Coord, Coord]

def parse_coord(coord: Coord) -> Coord:
    if len(coord) == 1:
        return (coord[0], coord[0])
    if len(coord) == 2:
        return coord
    raise ValueError(f"Invalid coordinate format: {coord}. Should be (LEFT, TOP)")