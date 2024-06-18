from ..get import from_bitmap
from ..bitmap import Bitmap
from pathlib import Path
import os

LETTERS = 'abcçdefghijklmnñopqrstuvwxyz'
DIGITS = '0123456789'
SYMBOLS = list('()[]{}¡!-+=.,;_%$€ºª@#&·~¬^´¨`')
SPECIAL_SYMBOLS = {
    'space': ' ',
    'close': '?',
    'open': '¿',
    'single': "'",
    'double': '"',
    'start': '*',
    'less': '<',
    'greater': '>',
    'backslash': '\\',
    'slash': '/',
    'pipe': '|'
}

class Font:
    def __init__(self, name: str, path: str):
        if not Path(path).is_dir():
            raise FileNotFoundError(f'Font directory not found: {path}')
        
        self.name, self.path = name, path
        self.lower: dict[str, Bitmap] = {}
        self.upper: dict[str, Bitmap] = {}
        self.digit: dict[str, Bitmap] = {}
        self.symbol: dict[str, Bitmap] = {}
        
        self.__not_found = []
        
        # Construct paths using os.path.join for better cross-platform compatibility
        lower_path = os.path.join(path, 'lower')
        upper_path = os.path.join(path, 'upper')
        digit_path = os.path.join(path, 'digit')
        symbol_path = os.path.join(path, 'symbol')
        
        # Load lowercase letters
        for letter in LETTERS:
            try:
                self.lower[letter] = from_bitmap(os.path.join(lower_path, f'{letter}.bmp'))
                self.upper[letter.upper()] = from_bitmap(os.path.join(upper_path, f'{letter}.bmp'))
            except FileNotFoundError as e:
                self.__not_found.append(e.filename)
        
        # Load digits
        for digit in DIGITS:
            try:
                self.digit[digit] = from_bitmap(os.path.join(digit_path, f'{digit}.bmp'))
            except FileNotFoundError as e:
                self.__not_found.append(e.filename)
        
        # Load symbols
        for symbol in SYMBOLS:
            try:
                self.symbol[symbol] = from_bitmap(os.path.join(symbol_path, f'{symbol}.bmp'))
            except FileNotFoundError as e:
                self.__not_found.append(e.filename)
                
        for reference in SPECIAL_SYMBOLS:
            try:
                self.symbol[SPECIAL_SYMBOLS[reference]] = from_bitmap(os.path.join(symbol_path, f'{reference}.bmp'))
            except FileNotFoundError as e:
                self.__not_found
        
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

    def __hash__(self):
        hash_value = 1
        for ch in self.name:
            hash_value += (hash_value[-1] / int(ch))
        return hash_value