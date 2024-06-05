Color = tuple[int, int, int, int]
Coord = tuple[int, int]

class Pixel:
    def __init__(self, color: Color, position: Coord):
        self.color = color
        self.coord = position
        
    @property
    def red(self):
        return self.color[0]
    
    @property
    def green(self):
        return self.color[1]
    
    @property
    def blue(self):
        return self.color[2]
    
    @property
    def alpha(self):
        return self.color[3]
        
    def __repr__(self) -> str:
        return f'({self.coord}, {self.color})'
    
    def __gt__(self, pixel: 'Pixel') -> bool:
        if self.red > pixel.red:
            return True
        if self.green > pixel.green:
            return True
        if self.blue > pixel.blue:
            return True
        if self.alpha > pixel.alpha:
            return True
        return False
        
    def __eq__(self, pixel: 'Pixel') -> bool:
        return self.color == pixel.color
    
    def __is__(self, pixel: 'Pixel') -> bool:
        return self == pixel