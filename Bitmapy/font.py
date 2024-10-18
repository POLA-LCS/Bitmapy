from .bitmap import Bitmap
from .characters import *

class Font:
    from .get import from_bitmap
    from pathlib import Path
    import os
    def __init__(self, name: str, path: str):
        if not self.Path(path).is_dir():
            raise FileNotFoundError(f'Font directory not found: {path}')
        
        self.name, self.path = name, path
        self.lower: dict[str, Bitmap] = {}
        self.upper: dict[str, Bitmap] = {}
        self.digit: dict[str, Bitmap] = {}
        self.symbol: dict[str, Bitmap] = {}
        
        self.__not_found = []
        
        # Construct paths using os.path.join for better cross-platform compatibility
        lower_path = self.os.path.join(path, 'lower')
        upper_path = self.os.path.join(path, 'upper')
        digit_path = self.os.path.join(path, 'digit')
        symbol_path = self.os.path.join(path, 'symbol')
        
        # Load lowercase letters
        for letter in LETTERS:
            try:
                self.lower[letter] = self.from_bitmap(self.os.path.join(lower_path, f'{letter}.bmp'))
                self.upper[letter.upper()] = self.from_bitmap(self.os.path.join(upper_path, f'{letter}.bmp'))
            except FileNotFoundError as e:
                self.__not_found.append(e.filename)
        
        # Load digits
        for digit in DIGITS:
            try:
                self.digit[digit] = self.from_bitmap(self.os.path.join(digit_path, f'{digit}.bmp'))
            except FileNotFoundError as e:
                self.__not_found.append(e.filename)
        
        # Load symbols
        for symbol in SYMBOLS:
            try:
                self.symbol[symbol] = self.from_bitmap(self.os.path.join(symbol_path, f'{symbol}.bmp'))
            except FileNotFoundError as e:
                self.__not_found.append(e.filename)
                
        for reference in SPECIAL_SYMBOLS:
            try:
                self.symbol[SPECIAL_SYMBOLS[reference]] = self.from_bitmap(self.os.path.join(symbol_path, f'{reference}.bmp'))
            except FileNotFoundError as e:
                self.__not_found.append(e.filename)
        
    def get_text(self, text: str):
        return [self.get_letter(letter) for letter in text]
    
    def get_letter(self, letter: str):
        if letter.islower():
            return self.lower.get(letter)
        elif letter.isupper():
            return self.upper.get(letter)
        elif letter.isdigit():
            return self.digit.get(letter)
        else:
            return self.symbol.get(letter)
    
    @property
    def missing(self):
        return self.__not_found
    
    def __repr__(self) -> str:
        return f'{self.name}(L:{len(self.lower)}, U:{len(self.upper)}, D:{len(self.digit)}, S:{len(self.symbol)})'