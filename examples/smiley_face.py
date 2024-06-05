from Bitmapy import *

# Declares 10x10 bitmap with a black as the default background color
image = Bitmap(10, 10, BLACK)

# Draw a yellow square from 2,2 to 9,9
image.draw_area(YELLOW, (2, 2), (9, 9))

# Draw the white corners with cross
image.draw_cross(WHITE, (1, 1), 1)
image.draw_cross(WHITE, (1, 10), 1)
image.draw_cross(WHITE, (10, 1), 1)
image.draw_cross(WHITE, (10, 10), 1)

image.draw_many([
    # Four black pixels at the corners
    Pixel(BLACK, (2, 2)),
    Pixel(BLACK, (9, 9)),
    Pixel(BLACK, (2, 9)),
    Pixel(BLACK, (9, 2)),
    # Eyes
    Pixel(BLACK, (4, 4)),
    Pixel(BLACK, (7, 4)),
    # Mouth
    Pixel(BLACK, (7, 7)),
    Pixel(BLACK, (4, 7)),
    Pixel(BLACK, (5, 8)),
    Pixel(BLACK, (6, 8)),
])

def add_tongue():
    Pixel((255, 190, 200), (7, 8))

image.save('smiley_face.bmp')