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
    logo = Bitmap(13, 13, (255, 255, 255))

    circle(logo, (0, 0, 0), (7, 7), 6)

    logo.fill((255, 255, 0), (7, 7))

    logo.draw(
        # Eyebrows
        ((0, 0, 0), (4, 5)), # Left
        ((0, 0, 0), (5, 5)),
        ((0, 0, 0), (6, 5)),
        ((0, 0, 0), (8, 5)), # Right
        ((0, 0, 0), (9, 5)),
        ((0, 0, 0), (10, 5)),
        # Eyes
        ((0, 0, 0), (5, 7)), # Left
        ((0, 0, 0), (9, 7)), # Right
        # Mouth
        ((0, 0, 0), (5, 9)),
        ((0, 0, 0), (9, 9)),
        ((0, 0, 0), (6, 10)),
        ((0, 0, 0), (7, 10)),
        ((0, 0, 0), (8, 10)),
    )
    
    return logo