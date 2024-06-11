from .bitmap import Bitmap, Color, Coord

def circle(bmp: Bitmap, color: Color, position: Coord, radius: int):
    center_x, center_y = position
    x = 0
    y = radius
    d = 3 - 2 * radius

    def draw_circle_points(bmp, center_x, center_y, x, y, color):
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

    circle(logo, (0, 0, 0), (8, 8), 6)

    logo.fill((255, 255, 0), (8, 8))

    logo.draw(
        # Eyebrows
        ((0, 0, 0), (5, 6)), # Left
        ((0, 0, 0), (6, 6)),
        ((0, 0, 0), (7, 6)),
        ((0, 0, 0), (9, 6)), # Right
        ((0, 0, 0), (10, 6)),
        ((0, 0, 0), (11, 6)),
        # Eyes
        ((0, 0, 0), (6, 8)), # Left
        ((0, 0, 0), (10, 8)), # Right
        # Mouth
        ((0, 0, 0), (6, 10)),
        ((0, 0, 0), (10, 10)),
        ((0, 0, 0), (7, 11)),
        ((0, 0, 0), (8, 11)),
        ((0, 0, 0), (9, 11)),
    )
    
    return logo