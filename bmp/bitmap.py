import struct
from .types import Color, Pixel, Area, Coord

class Bitmap:
    def __init__(self, width: int, height: int, default_color: Color = (255, 255, 255)):
        self.__width = width
        self.__height = height
        self.default_color = default_color
        self.canvas = [[default_color] * width for _ in range(height)]
            
    def save(self, path: str):
        file_header = b'BM'
        offset = 54  # 14 (file header) + 40 (info header)
        file_size = offset + 4 * self.__width * self.__height
        reserved = 0
        file_header += struct.pack('<IHHI', file_size, reserved, reserved, offset)
        
        header_info = struct.pack('<IIIHHIIIIII', 40, self.__width, self.__height, 1, 32, 0, 0, 0, 0, 0, 0)
        
        image_data = bytearray(4 * self.__width * self.__height)
        idleft = 0
        for row in reversed(self.canvas):
            for color in row:
                image_data[idleft:idleft + 4] = struct.pack('BBBB', color[2], color[1], color[0], 255)  # RGBA with Alpha = 255
                idleft += 4
                
        with open(path, 'wb') as file:
            file.write(file_header)
            file.write(header_info)
            file.write(image_data)

    def draw(self, *pixels: Pixel | Area):
        for pixel in pixels:
            if len(pixel) == 2:
                self.draw_pixel(*pixel)
            elif len(pixel) == 3:
                self.draw_area(*pixel)
            else:
                raise ValueError("Invalid pixel or area")
    
    def erase(self, *positions: Coord | tuple[Coord, Coord]):
        for pos in positions:
            if isinstance(pos[0], int):
                self.erase_pixel(pos)
            else:
                self.erase_area(*pos)

    def fill(self, color: Color, position: Coord, toleranctop: int = 0):
        left, top = position
        if not (0 <= left < self.__width and 0 <= top < self.__height):
            return

        target_color = self.canvas[top][left]
        if target_color == color:
            return

        stack = [(left, top)]
        while stack:
            cleft, ctop = stack.pop()
            if not (0 <= cleft < self.__width and 0 <= ctop < self.__height):
                continue
            actual_color = self.canvas[ctop][cleft][:3]
            target_color = target_color[:3]
            if all(abs(a - b) <= toleranctop for a, b in zip(actual_color, target_color)):
                self.canvas[ctop][cleft] = color
                stack.extend([(cleft - 1, ctop), (cleft + 1, ctop), (cleft, ctop - 1), (cleft, ctop + 1)])
                
    def draw_pixel(self, color: Color, position: Coord):
        left, top = position
        if 1 <= left <= self.__width and 1 <= top <= self.__height:
            self.canvas[top - 1][left - 1] = color
                
    def draw_area(self, color: Color, start: Coord, end: Coord):
        start_left, start_top = start
        end_left, end_top = end
        for top in range(min(start_top, end_top), max(start_top, end_top) + 1):
            for x in range(min(start_left, end_left), max(start_left, end_left) + 1):
                self.draw_pixel(color, (top, x))

    def erase_pixel(self, position: Coord):
        self.draw_pixel((0, 0, 0, 0), position)

    def erase_area(self, start: Coord, end: Coord):
        self.draw_area((0, 0, 0, 0), start, end)

    def draw_bitmap(self, bmp: 'Bitmap', from_pos: Coord):
        dleft, dtop = from_pos
        for top, row in enumerate(bmp.canvas):
            for left, color in enumerate(row):
                try:
                    self.canvas[top + dtop][left + dleft] = color
                except IndexError:
                    pass

    # No draw functions

    def get_scale(self, scale_factor: int) -> 'Bitmap':
        if scale_factor <= 0:
            raise ValueError("Scale factor must be a positive integer.")
        
        new_width = self.__width * scale_factor
        new_height = self.__height * scale_factor
        new_canvas = [[self.default_color] * new_width for _ in range(new_height)]

        for top in range(self.__height):
            for x in range(self.__width):
                new_color = self.canvas[top][x]
                for dtop in range(scale_factor):
                    for dleft in range(scale_factor):
                        new_canvas[top * scale_factor + dtop][x * scale_factor + dleft] = new_color

        scaled_bitmap = Bitmap(new_width, new_height, self.default_color)
        scaled_bitmap.canvas = new_canvas
        return scaled_bitmap

    def get_crop(self, from_pos: Coord, to_pos: Coord):
        left, top = from_pos
        right, bottom = to_pos
        crop_canvas = [
            [self.canvas[t][l] for l in range(left - 1, right)]
            for t in range(top - 1, bottom)
        ]

        crop_bitmap = Bitmap(
            right - left + 1,
            bottom - top + 1,
            self.default_color
        )
        
        crop_bitmap.canvas = crop_canvas
        return crop_bitmap

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def size(self):
        return self.width, self.height

    def __repr__(self) -> str:
        lines = ''
        for row in self.canvas:
            for p, pixel in enumerate(row):
                for data in pixel:
                    lines += f'{hex(data)[2:]}' if data != 0 else f'00'
                if p < len(row) - 1:
                    lines += ' '
            lines += '\n'
        return lines[:-1]