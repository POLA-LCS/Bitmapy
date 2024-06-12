from . import get, Bitmap

fonts: dict[str, dict[str, Bitmap]] = {}

LETTERS = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

def load(name: str, path: str):
    font: dict[str, Bitmap] = {}
    for l in LETTERS:
        try:
            font_upper = get.from_bitmap(path + '\\upper\\' + l + '.bmp')
        except FileNotFoundError:
            font_upper = None
        try:
            font_lower = get.from_bitmap(path + '\\lower\\' + l + '.bmp')
        except FileNotFoundError:
            font_lower = None
            
        font[l] = font_upper
        font[l.lower()] = font_lower
    fonts[name] = font
    
def get_letter(font_name: str, letter: str) -> Bitmap | None:
    if font := fonts.get(font_name):
        return font.get(letter)
    return None

def get_text(font_name: str, text: str) -> list[Bitmap | None] | None:
    if font := fonts.get(font_name):
        return [font.get(letter) for letter in text]
    return None