"""The heart of Bitmapy, inside contains the Bitmap class"""

from typing import Optional, Union
import struct
from .types import Color, Coord, Pixel, Area, parse_coord
from .colors import EMPTY, parse_color, blend_color

class Bitmap:
    def __init__(
            self,
            width: int,
            height: int,
            default_color: Color = (255, 255, 255, 255),
            path: Optional[str] = None
        ):
        self.__width = width
        self.__height = height
        self.default_color = default_color
        self.canvas = [[default_color] * width for _ in range(height)]
        self.path = path

    def save(self, path: Optional[str] = None):
        """Saves the bitmap as an image file with `path` name"""
        if path is None:
            if self.path is None:
                raise ValueError("Path is not specified")
            path = self.path

        file_header = b'BM'
        offset = 54  # 14 (file header) + 40 (info header)
        file_size = offset + 4 * self.__width * self.__height
        reserved = 0
        file_header += struct.pack('<IHHI', file_size, reserved, reserved, offset)

        header_info = struct.pack(
            '<IIIHHIIIIII', 40,
            self.__width, self.__height,
            1, 32, 0, 0, 0, 0, 0, 0
        )

        image_data = bytearray(4 * self.__width * self.__height)
        idleft = 0
        for row in reversed(self.canvas):
            for color in row:
                color = parse_color(color)
                image_data[idleft:idleft + 4] = struct.pack('BBBB', color[2], color[1], color[0], color[3])
                idleft += 4

        with open(path, 'wb') as file:
            file.write(file_header)
            file.write(header_info)
            file.write(image_data)

    def draw(self, *pixels: Union[Pixel, Area]):
        """Interprets the arguments as Pixels or Areas and calls `draw_pixel` or `draw_area`
        NOTE: Invalid pixels or area raises ValueError with the \"bad\" argument's position"""
        for i, pixel in enumerate(pixels):
            if len(pixel) == 2:
                self.draw_pixel(*pixel)
            elif len(pixel) == 3:
                self.draw_area(*pixel)
            else:
                raise ValueError(f"Invalid pixel or area: {i + 1}")

    def erase(self, *positions: Union[Coord, Area]):
        """Interprets the arguments as Positions of Areas and calls `erase_pixel` or `erase_area`
        NOTE: Invalid positions or areas raises ValueError with the \"bad\" argument's position"""
        for pos in positions:
            pos = parse_coord(pos)
            if isinstance(pos[0], int):
                self.erase_pixel(pos)
            else:
                self.erase_area(*pos)

    def fill(self, color: Color, position: Coord, tolerancy: int = 0):
        """Fills with `color` from `position` with a certain amout of `tolerancy` from 0 to 255"""
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
            actual_color = self.canvas[ctop][cleft]
            if all(abs(a - b) <= tolerancy for a, b in zip(actual_color, target_color)):
                self.canvas[ctop][cleft] = color
                stack.extend([(cleft-1, ctop), (cleft+1, ctop), (cleft, ctop-1), (cleft, ctop+1)])

    def draw_pixel(self, color: Color, position: Coord):
        """Draws a `color` pixel on the specified `position`"""
        left, top = parse_coord(position)
        color = parse_color(color)
        if 0 <= left < self.__width and 0 <= top < self.__height:
            target = self.canvas[top][left]
            self.canvas[top][left] = blend_color(target, color)

    def erase_pixel(self, position: Coord):
        """Turns the pixel in the `position` into a transparent pixel"""
        left, top = parse_coord(position)
        if 0 <= left < self.__width and 0 <= top < self.__height:
            self.canvas[top][left] = EMPTY

    def draw_area(self, color: Color, start: Coord, end: Coord):
        """Draws an area of `color` from `start` to `end`"""
        start_left, start_top = parse_coord(start)
        end_left, end_top = parse_coord(end)
        for top in range(min(start_top, end_top), max(start_top, end_top) + 1):
            for left in range(min(start_left, end_left), max(start_left, end_left) + 1):
                self.draw_pixel(color, (left, top))

    def erase_area(self, start: Coord, end: Coord):
        """Turns an entire area from `start` to `end` into EMPTY"""
        self.draw_area(EMPTY, start, end)

    def blit(self, bmp: 'Bitmap', from_pos: Coord):
        """Blits another bitmap into the canvas starting `from_pos`"""
        dleft, dtop = parse_coord(from_pos)
        for top, row in enumerate(bmp.canvas):
            for left, color in enumerate(row):
                try:
                    target = self.canvas[dtop + top][dleft + left]
                    self.canvas[dtop + top][dleft + left] = blend_color(target, color)
                except IndexError:
                    pass

    # No draw functions

    def get_scale(self, scale_factor: int) -> 'Bitmap':
        if scale_factor <= 0 or scale_factor - int(scale_factor) != 0:
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

    def get_str(self) -> str:
        lines = ''
        for row in self.canvas:
            for p, pixel in enumerate(row):
                for data in pixel:
                    lines += f'{hex(data)[2:]}' if data != 0 else '00'
                if p < len(row) - 1:
                    lines += ' '
            lines += '\n'
        return lines[:-1]

    def __enter__(self):
        if self.path is None:
            raise ValueError('Path is required for context manager')
        return self

    def __exit__(self, a, b, c):
        if a:
            print(a)
        if b:
            print(b)
        if c:
            print(c)
        self.save(self.path)

    def __repr__(self) -> str:
        if self.path:
            return f'BMP({self.size}, {self.path})'
        return f'BMP({self.size})'
