import struct
from PIL import Image
from .types import *

class Bitmap:
    """## Bitmap\n
    (documentation in process...)"""
    def __init__(self, width: int, height: int, default_color: Color | None = (255, 255, 255)):
        self.width = width
        self.height = height
        self.default_color =  default_color
        self.__canvas = [[default_color] * width for _ in range(height)]

    @property
    def canvas(self):
        return self.__canvas

    def draw(self, *pixels: Pixel):
        """Pixel format: `((r, g, b), (x, y))`"""
        for pix in pixels:
            color = pix[0]
            x, y = pix[1]
            if 1 <= x <= self.width and 1 <= y <= self.height:
                self.__canvas[y - 1][x - 1] = color

    def erase(self, *positions: Coord):
        """Draws in the `default_color` of the bitmap"""
        for pos in positions:
            self.draw((self.default_color, pos))
    
    def draw_area(self, color: Color, from_pos: Coord, to_pos: Coord):
        """Draws an area of `color`, the order of the `from_pos` and `to_pos` is switchable"""
        x1, y1 = from_pos
        x2, y2 = to_pos
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 1 <= x <= self.width and 1 <= y <= self.height:
                    self.__canvas[y-1][x-1] = color

    def draw_cross(self, color: Color, pos: Coord, size: int):
        """Draws a pixel with four other pixels on the sides separated by `size`"""
        self.draw(color, pos)
        self.draw(color, (pos[0] + size, pos[1]))
        self.draw(color, (pos[0] - size, pos[1]))
        self.draw(color, (pos[0], pos[1] - size))
        self.draw(color, (pos[0], pos[1] + size))

    def save(self, path: str):
        """Dumps the bitmap canvas into a file.\n
        Recomendation: `<file>.bmp`"""
        file_header = b'BM'
        file_size = 14 + 40 + 4 * self.width * self.height
        reserved = 0
        offset = 14 + 40
        file_header += struct.pack('<IHHI', file_size, reserved, reserved, offset)
        header_info = struct.pack('<IIIHHIIIIII', 40, self.width, self.height, 1, 32, 0, 0, 0, 0, 0, 0)
        
        image_data = bytearray(4 * self.width * self.height)
        idx = 0
        for row in reversed(self.__canvas):
            for color in row:
                image_data[idx:idx + 4] = struct.pack('BBBB', color[2], color[1], color[0], 255) # ALPHA 100%
                idx += 4
                
        with open(path, 'wb') as file:
            file.write(file_header)
            file.write(header_info)
            file.write(image_data)

def from_bitmap(bitmap_path: str) -> Bitmap:
    with open(bitmap_path, 'rb') as file:
        bmp_data = file.read()

    # header
    file_header = struct.unpack('<2sI2HI', bmp_data[:14])
    
    # header info
    header_info = struct.unpack('<IIIHHIIIIII', bmp_data[14:54])
    _, file_size, _, _, offset = file_header
    
    header_size, width, height, planes, bits_per_pixel, compression, image_size, x_pixels_per_meter, y_pixels_per_meter, colors_used, important_colors = header_info

    if bits_per_pixel != 32:
        raise ValueError("Only 32 bits per pixel bitmaps are valid")

    image_data = bmp_data[offset:]
    canvas = []
    for y in range(height):
        row = []
        for x in range(width):
            idx = (y * width + x) * 4
            b, g, r, a = struct.unpack('BBBB', image_data[idx:idx + 4])
            row.append((r, g, b, a))
        canvas.insert(0, row)

    bitmap = Bitmap(width, height)
    bitmap.canvas = canvas
    return bitmap

def from_image(image_path: str) -> Bitmap:
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    bitmap = Bitmap(width, height)
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            bitmap.canvas[y][x] = (r, g, b, a)
    return bitmap