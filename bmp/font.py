from .get import from_bitmap
from .bitmap import Bitmap

Font = dict[dict[str, Bitmap]]

__fonts: dict[str, Font] = {}

LETTERS = 'abcçdefghijklmnñopqrstuvwxyz'
DIGITS = '0123456789'
GOOD_SYMBOLS = 'ºª!@·#$~%€&¬()=¡`^[+]´¨{,;.-_'
BAD_SYMBOLS = '\\|/?¿\'"*<>'
BAD_REFERENCE = ['left', 'pipe', 'right', 'close', 'open', 'single', 'double', 'multiply', 'lower', 'greater']

def load(name: str, path: str) -> list[str]:
    no_found = []
    font = {
        'lower': {},
        'upper': {},
        'digit': {},
        'symbol': {}
    }
    for letter in LETTERS:
        try:
            font['lower'][letter] = from_bitmap(path + '\\lower\\' + letter + '.bmp')
            font['upper'][letter.upper()] = from_bitmap(path + '\\upper\\' + letter + '.bmp')
        except FileNotFoundError as e:
            no_found.append(e.filename)
            
    for digit in DIGITS:
        try:
            font['digit'][digit] = from_bitmap(path + '\\digit\\' + digit + '.bmp')
        except FileNotFoundError as e:
            no_found.append(e.filename)

    for symbol in GOOD_SYMBOLS:
        try:
            font['symbol'][symbol] = from_bitmap(path + '\\symbol\\' + symbol + '.bmp')
        except FileNotFoundError as e:
            no_found.append(e.filename)
            
    for symbol, reference in zip(BAD_SYMBOLS, BAD_REFERENCE):
        try:
            font['symbol'][symbol] = from_bitmap(path + '\\symbol\\' + reference + '.bmp')
        except FileNotFoundError as e:
            no_found.append(e.filename)
            
    __fonts.setdefault(name, font)
    return no_found
    
def get(name: str):
    return __fonts.get(name, None)