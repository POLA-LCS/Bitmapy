from os import system
from time import sleep
from typing import Tuple, List
import struct
from PIL import Image

Color = Tuple[int, int, int, int]
Position = Tuple[int, int]
Pixel = Tuple[Color, Position]

class Bitmap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.canvas = [[(255, 255, 255, 0)] * width for _ in range(height)]

    def draw(self, color: Color, pos: Position):
        x, y = pos
        if 1 <= x <= self.width and 1 <= y <= self.height:
            self.canvas[y-1][x-1] = color

    def draw_col(self, color: Color, col: int):
        if 1 <= col <= self.width:
            for y in range(1, self.height + 1):
                self.canvas[y-1][col-1] = color

    def draw_row(self, color: Color, row: int):
        if 1 <= row <= self.height:
            for x in range(1, self.width + 1):
                self.canvas[row-1][x-1] = color

    def draw_area(self, color: Color, from_pos: Position, to_pos: Position):
        x1, y1 = from_pos
        x2, y2 = to_pos
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 1 <= x <= self.width and 1 <= y <= self.height:
                    self.canvas[y-1][x-1] = color

    def erase(self, pos: Position):
        self.draw((255, 255, 255, 0), pos)

    def draw_many(self, pixels: List[Pixel]):
        for color, pos in pixels:
            self.draw(color, pos)

    def save(self, path: str):
        file_header = b'BM'
        file_size = 14 + 40 + 4 * self.width * self.height
        reserved = 0
        offset = 14 + 40
        file_header += struct.pack('<IHHI', file_size, reserved, reserved, offset)
        info_header = struct.pack('<IIIHHIIIIII', 40, self.width, self.height, 1, 32, 0, 0, 0, 0, 0, 0)
        
        image_data = bytearray(4 * self.width * self.height)
        idx = 0
        for row in reversed(self.canvas):
            for color in row:
                image_data[idx:idx + 4] = struct.pack('BBBB', color[2], color[1], color[0], color[3])
                idx += 4
                
        with open(path, 'wb') as f:
            f.write(file_header)
            f.write(info_header)
            f.write(image_data)

    @classmethod
    def from_bitmap(cls, path: str):
        with open(path, 'rb') as f:
            bmp_data = f.read()

        file_header = struct.unpack('<2sI2HI', bmp_data[:14])
        _, file_size, _, _, offset = file_header
        info_header = struct.unpack('<IIIHHIIIIII', bmp_data[14:54])
        header_size, width, height, planes, bits_per_pixel, compression, image_size, x_pixels_per_meter, y_pixels_per_meter, colors_used, important_colors = info_header

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

        bitmap = cls(width, height)
        bitmap.canvas = canvas
        return bitmap

    @classmethod
    def from_image(cls, path: str):
        img = Image.open(path).convert('RGBA')
        width, height = img.size
        bitmap = cls(width, height)
        for y in range(height):
            for x in range(width):
                r, g, b, a = img.getpixel((x, y))
                bitmap.canvas[y][x] = (r, g, b, a)
        return bitmap

# Ejemplo de uso
bmp = Bitmap.from_image('path_to_image.png')
bmp.save('output.bmp')
