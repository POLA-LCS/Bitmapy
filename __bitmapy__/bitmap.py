import struct
from .types import Color, Pixel, Coord

class Bitmap:
    def __init__(self, width: int, height: int, default_color: Color = (255, 255, 255)):
        self.width = width
        self.height = height
        self.default_color = default_color
        self.canvas = [[default_color] * width for _ in range(height)]

    def draw(self, *pixels: Pixel):
        for color, (x, y) in pixels:
            if 1 <= x <= self.width and 1 <= y <= self.height:
                self.canvas[y - 1][x - 1] = color

    def erase(self, *positions: Coord):
        for pos in positions:
            self.draw((self.default_color, pos))
    
    def draw_area(self, color: Color, start_pos: Coord, end_pos: Coord):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                if 1 <= x <= self.width and 1 <= y <= self.height:
                    self.canvas[y - 1][x - 1] = color

    def _colors_are_similar(self, color1: Color, color2: Color, tolerancy: int) -> bool:
        return all(abs(a - b) <= tolerancy for a, b in zip(color1, color2))

    def fill(self, color: Color, position: Coord, tolerancy: int = 0):
        x, y = position
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        target_color = self.canvas[y][x]
        if target_color == color:
            return

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if not (0 <= cx < self.width and 0 <= cy < self.height):
                continue
            if self._colors_are_similar(self.canvas[cy][cx], target_color, tolerancy):
                self.canvas[cy][cx] = color
                stack.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])

    def save(self, path: str):
        file_header = b'BM'
        file_size = 14 + 40 + 4 * self.width * self.height
        reserved = 0
        offset = 14 + 40
        file_header += struct.pack('<IHHI', file_size, reserved, reserved, offset)
        
        header_info = struct.pack('<IIIHHIIIIII', 40, self.width, self.height, 1, 32, 0, 0, 0, 0, 0, 0)
        
        image_data = bytearray(4 * self.width * self.height)
        idx = 0
        for row in reversed(self.canvas):
            for color in row:
                image_data[idx:idx + 4] = struct.pack('BBBB', color[2], color[1], color[0], 255)  # ALPHA 100%
                idx += 4
                
        with open(path, 'wb') as file:
            file.write(file_header)
            file.write(header_info)
            file.write(image_data)
