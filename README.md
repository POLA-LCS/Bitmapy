# Bitmapy
*The Python's bitmap manager.*

## Currentyle beta 1.12.3 !!!

![Bitmap logo.](./logo.bmp)

### Details
- Like many other graphic design softwares, Bitmapy starts drawing from the
TOP LEFT of the image.
- It is a WIP project so it's liable to bugs or non-wanted behavior.

### Your first RED pixel
```python
from Bitmapy import bmp

# Bitmap(width, height, default_color = WHITE)
image = bmp.Bitmap(1, 1, bmp.RED)

# save(path)
image.save('red_pixel.bmp')
```

### Draw a circle and fill it
```python
import Bitmapy as bmp

circle = bmp.Bitmap(13, 13, bmp.BLACK)

# From module draw, circle(bitmap, color, (center_left, center_top), radius)
bmp.draw.circle(circle, bmp.WHITE, (7, 7), 6)

# Bitmap.fill(color, (left, top), tolerancy = 0)
circle.fill(bmp.LIGHT_GREY, (7, 7), 0)

circle.save('circle.bmp')
```

## Fonts
Bitmapy supports an unlimited set of fonts, those are just bitmaps that are linked with the next symbols:
- Letters from A to Z (lower and uppercase).
- Symbols: ()[]{}¡!-+=.,;_%$€ºª@#&·~¬^´¨`
- Special symbols: ?¿'"*<>\/|

The special symbols are those who can't have a direct file-name relationship like "(" that it's linked with "(.bmp".
This symbols has their own file name:
-   : space
- : : colon
- ? : close
- ¿ : open
- ' : single
- " : double
- * : star
- < : less
- \> : greater
- / : slash
- \ : backslash
- | : pipe

## Font structure
The folder structure of the font is very important, without the next structure, the code will not import your font.

example_font\
├── lower\
│   ├── a.bmp\
│   ├── b.bmp\
│   └── ...\
├── upper\
│   ├── a.bmp\
│   ├── b.bmp\
│   └── ...\
├── digit\
│   ├── 0.bmp\
│   ├── 1.bmp\
│   └── ...\
└── symbol\
    ├── #.bmp\
    ├── open.bmp\
    ├── @.bmp\
    ├── double.bmp\
    └── ...\

## Personalized structure
WORK IN PROGRESS...
