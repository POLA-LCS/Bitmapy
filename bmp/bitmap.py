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
        offset = 54 # 14 + 40
        file_size = offset + 4 * self.__width * self.__height
        reserved = 0
        file_header += struct.pack('<IHHI', file_size, reserved, reserved, offset)
        
        header_info = struct.pack('<IIIHHIIIIII', 40, self.__width, self.__height, 1, 32, 0, 0, 0, 0, 0, 0)
        
        image_data = bytearray(4 * self.__width * self.__height)
        idx = 0
        for row in reversed(self.canvas):
            for color in row:
                image_data[idx:idx + 4] = struct.pack('BBBB', color[2], color[1], color[0], 255)  # ALPHA 100%
                idx += 4
                
        with open(path, 'wb') as file:
            file.write(file_header)
            file.write(header_info)
            file.write(image_data)
            
    def draw(self, *pixels: Pixel | Area):
        for pixel in pixels:
            if len(pixel) == 2:
                self.draw_pixel(*pixel)
            elif len(pixel) == 3:
                self.draw_square(*pixel)
            else:
                raise ValueError("Invalid pixel or area")
    
    def erase(self, *positions: Coord | tuple[Coord, Coord]):
        for pos in positions:
            if isinstance(pos[0], int):
                self.erase_pixel(pos)
            else:
                self.erase_area(*pos)
                
    def draw_pixel(self, color: Color, position: Coord):
        y, x = position
        if 1 <= x <= self.__width and 1 <= y <= self.__height:
            self.canvas[y - 1][x - 1] = color
    
    def draw_area(self, color: Color, start: Coord, end: Coord):
        start_y, start_x = start
        end_y, end_x = end
        for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                self.draw_pixel(color, (y, x))
                    
    def erase_pixel(self, position: Coord):
        self.draw_pixel(self.default_color, position)
                    
    def erase_area(self, start: Coord, end: Coord):
        self.draw_area(self.default_color, start, end)

    def fill(self, color: Color, position: Coord, tolerancy: int = 0):
        x, y = position
        if not (0 <= x < self.__width and 0 <= y < self.__height):
            return
        
        target_color = self.canvas[y][x]
        if target_color == color:
            return

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if not (0 <= cx < self.__width and 0 <= cy < self.__height):
                continue
            if all(abs(a - b) <= tolerancy for a, b in zip(self.canvas[cy][cx], target_color)):
                self.canvas[cy][cx] = color
                stack.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])

    def scale_by(self, scale_factor: int) -> 'Bitmap':
        """Scales the image by the scale_factor, not floating points allowed"""
        if scale_factor <= 0:
            raise ValueError("Scale factor must be a positive integer.")
        
        new_width = self.__width * scale_factor
        new_height = self.__height * scale_factor
        new_canvas = [[self.default_color] * new_width for _ in range(new_height)]

        for y in range(self.__height):
            for x in range(self.__width):
                new_color = self.canvas[y][x]
                for dy in range(scale_factor):
                    for dx in range(scale_factor):
                        new_canvas[y * scale_factor + dy][x * scale_factor + dx] = new_color

        scaled_bitmap = Bitmap(new_width, new_height, self.default_color)
        scaled_bitmap = new_canvas
        return scaled_bitmap


    def draw_bitmap(self, bmp: 'Bitmap', from_pos: Coord):
        dx, dy = from_pos
        for y, row in enumerate(bmp.canvas):
            for x, color in enumerate(row):
                try:
                    self.canvas[y + dy][x + dx] = color
                except IndexError:
                    pass
                
    def get_crop(self, from_pos: Coord, to_pos: Coord):
        crop_canvas = [self.canvas[y][from_pos[1]:to_pos[1]] for y in range(from_pos[0], to_pos[0])]
        crop_bitmap = Bitmap(
            to_pos[1] - from_pos[1],
            to_pos[0] - from_pos[0],
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