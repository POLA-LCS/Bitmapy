"""The heart of Bitmapy, inside contains the Bitmap class"""
from .types import Color, Coord, Pixel, Area
from .coord import parse_coord
from .color import parse_color, blend_color
from .colors import EMPTY
from struct import pack

class Bitmap:
    "Bitmap representation class"
    def __init__(
            self,
            width: int,
            height: int,
            background: Color = (255, 255, 255, 255),
            path: str | None = None
        ):
        self._width = width
        self._height = height
        self.background = background
        self.canvas = [[background] * width for _ in range(height)]
        self.path = path

    def save(self, path: str | None = None):
        """Saves the bitmap as an image file with `path` name"""
        if path is None:
            if self.path is None:
                raise ValueError("Path is not specified")
            path = self.path

        bitmap_header = b'BM'
        offset = 54  # 14 (file header) + 40 (info header)
        file_size = offset + 4 * self._width * self._height
        bitmap_header += pack('<IHHI', file_size, 0, 0, offset)

        header_info = pack(
            '<IIIHHIIIIII', 40,
            self._width, self._height,
            1, 32, 0, 0, 0, 0, 0, 0
        )

        image_data = bytearray(4 * self._width * self._height)
        idleft = 0
        for row in reversed(self.canvas):
            for color in row:
                color = parse_color(color)
                image_data[idleft:idleft + 4] = pack('BBBB', color[2], color[1], color[0], color[3])
                idleft += 4

        with open(path, 'wb') as file:
            file.write(bitmap_header)
            file.write(header_info)
            file.write(image_data)

    def draw(self, *pixels: Pixel | Area):
        """Interprets the arguments as Pixels or Areas and calls `draw_pixel` or `draw_area`
        NOTE: Invalid pixels or area raises ValueError with the \"bad\" argument's position"""
        for i, pixel in enumerate(pixels):
            if len(pixel) == 2:
                self.draw_pixel(*pixel)
            elif len(pixel) == 3:
                self.draw_area(*pixel)
            else:
                raise ValueError(f"Invalid pixel or area: {i}")

    def erase(self, *positions: Coord | Area):
        """Interprets the arguments as Positions of Areas and calls `erase_pixel` or `erase_area`
        NOTE: Invalid positions or areas raises ValueError with the \"bad\" argument's position"""
        for pos in positions:
            pos = parse_coord(pos)
            if isinstance(pos[0], int):
                self.erase_pixel(pos)
            else:
                self.erase_area(*pos)

    def fill(self, color: Color, position: Coord, tolerancy: int = 0):
        """Fills with `color` from `position` with a certain amout of `tolerancy` (0 - 255)"""
        left, top = parse_coord(position)
        if not (0 <= left < self._width and 0 <= top < self._height):
            return 0

        if (target_color := self.canvas[top][left]) == color:
            return 0
        
        def is_valid_position(pos):
            return (dest := self.get_pixel(*pos)) is not None and dest != color

        filled = 0
        queue = [(left, top)]
        while queue:
            cleft, ctop = queue.pop(0)
            
            if all(abs(a - t) <= tolerancy for a, t in zip(self.canvas[ctop][cleft], target_color)):
                self.canvas[ctop][cleft] = color
                for next in [(cleft - 1, ctop), (cleft, ctop + 1),
                             (cleft, ctop - 1), (cleft + 1, ctop)]:
                    if next not in queue:
                        if is_valid_position(next):
                            queue.append(next)
            filled += 1
        return filled

    def draw_pixel(self, color: Color, position: Coord):
        """Draws a `color` pixel on the specified `position`"""
        left, top = parse_coord(position)
        color = parse_color(color)
        if 0 <= left < self._width and 0 <= top < self._height:
            if color[-1] != 0:
                target = self.canvas[top][left]
                self.canvas[top][left] = blend_color(target, color)

    def erase_pixel(self, position: Coord):
        """Turns the pixel in the `position` into a transparent pixel"""
        left, top = parse_coord(position)
        if 0 <= left < self._width and 0 <= top < self._height:
            self.canvas[top][left] = self.EMPTY

    def draw_area(self, color: Color, start: Coord, end: Coord):
        """Draws an area of `color` from `start` to `end`"""
        start_left, start_top = parse_coord(start)
        end_left, end_top = parse_coord(end)
        for top in range(min(start_top, end_top), max(start_top, end_top) + 1):
            for left in range(min(start_left, end_left), max(start_left, end_left) + 1):
                self.draw_pixel(color, (left, top))

    def erase_area(self, start: Coord, end: Coord):
        """Turns an entire area from `start` to `end` into EMPTY"""
        self.draw_area(self.EMPTY, start, end)

    def blit(self, bmp: 'Bitmap', from_pos: Coord = (0, 0)):
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
    def get_pixel(self, left: int, top: int):
        """Returns the color of the pixel at the specified position"""
        if 0 > left or left >= self.width or 0 > top or top >= self.height:
            return None
        return self.canvas[top][left]
    
    def get_scale(self, scale_factor: int) -> 'Bitmap':
        if scale_factor <= 0 or scale_factor - int(scale_factor) != 0:
            raise ValueError("Scale factor must be a positive integer.")

        new_width = self._width * scale_factor
        new_height = self._height * scale_factor
        new_canvas = [[self.background] * new_width for _ in range(new_height)]

        for top in range(self._height):
            for x in range(self._width):
                new_color = self.canvas[top][x]
                for dtop in range(scale_factor):
                    for dleft in range(scale_factor):
                        new_canvas[top * scale_factor + dtop][x * scale_factor + dleft] = new_color

        scaled_bitmap = Bitmap(new_width, new_height, self.background)
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
            self.background
        )

        crop_bitmap.canvas = crop_canvas
        return crop_bitmap

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def size(self):
        return self.width, self.height

    def __enter__(self):
        if self.path is None:
            raise ValueError('Path is required for context manager')
        return self

    def __exit__(self, *args):
        for arg in args:
            if arg is not None:
                print(arg)
        self.save(self.path)

    def __repr__(self) -> str:
        if self.path:
            return f'BMP({self.size}, {self.path})'
        return f'BMP({self.width}, {self.height})'
