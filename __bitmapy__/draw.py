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
            
def bitmapy_logo(bmp: Bitmap):
    bmp = Bitmap(10, 10, (0, 0, 0))

    # Draw a yellow square from 2,2 to 9,9
    bmp.draw_area((255, 255, 0), (2, 2), (9, 9))

    # Draw the white corners with cross
    bmp.draw_cross((255, 255, 255), (1, 1), 1)
    bmp.draw_cross((255, 255, 255), (1, 10), 1)
    bmp.draw_cross((255, 255, 255), (10, 1), 1)
    bmp.draw_cross((255, 255, 255), (10, 10), 1)

    bmp.draw(
        # Four black pixels at the corners
        ((0, 0, 0), (2, 2)),
        ((0, 0, 0), (9, 9)),
        ((0, 0, 0), (2, 9)),
        ((0, 0, 0), (9, 2)),
        # Eyes
        ((0, 0, 0), (4, 4)),
        ((0, 0, 0), (7, 4)),
        # Mouth
        ((0, 0, 0), (7, 7)),
        ((0, 0, 0), (4, 7)),
        ((0, 0, 0), (5, 8)),
        ((0, 0, 0), (6, 8)),
    )