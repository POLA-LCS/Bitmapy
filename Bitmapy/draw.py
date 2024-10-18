from .bitmap import Bitmap
from .types import Color, Coord

def circle(bmp: Bitmap, color: Color, position: Coord, radius: int):
    center_x, center_y = position
    x = 0
    y = radius
    d = 3 - 2 * radius

    def draw_circle_points(bmp: Bitmap, center_x, center_y, x, y, color):
        points = [
            (center_x + x, center_y + y), (center_x - x, center_y + y),
            (center_x + x, center_y - y), (center_x - x, center_y - y),
            (center_x + y, center_y + x), (center_x - y, center_y + x),
            (center_x + y, center_y - x), (center_x - y, center_y - x)
        ]
        for point in points:
            bmp.draw((color, point))

    while y >= x:
        draw_circle_points(bmp, center_x, center_y, x, y, color)
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
            
def bitmapy_logo():
    logo = Bitmap(15, 15, (255, 255, 255))

    from .colors import BLACK
    circle(logo, BLACK, (8, 8), 6)

    logo.fill((255, 255, 0), (8, 8))

    logo.draw(
        # Eyebrows
        (BLACK, (5, 6)), # Left
        (BLACK, (6, 6)),
        (BLACK, (7, 6)),
        (BLACK, (9, 6)), # Right
        (BLACK, (10, 6)),
        (BLACK, (11, 6)),
        # Eyes
        (BLACK, (6, 8)), # Left
        (BLACK, (10, 8)), # Right
        # Mouth
        (BLACK, (6, 10)),
        (BLACK, (7, 11)),
        (BLACK, (8, 11)),
        (BLACK, (9, 11)),
        (BLACK, (10, 10)),
    )
    
    return logo