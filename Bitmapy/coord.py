Coord = tuple[int, int]

def parse_coord(coord: Coord | int) -> Coord:
    if isinstance(coord, int):
        return (coord, coord)
    if len(coord) > 2:
        raise ValueError(f"Invalid coordinate format: {coord}. Should be (LEFT, TOP)")
    return coord if len(coord) == 2 else (coord[0], coord[0])