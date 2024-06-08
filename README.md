# Bitmapy
![Bitmap logo.](/smiley_face.bmp)
A work in progress bitmap manager with python.

## Details
- Like many other graphic design softwares, Bitmapy starts drawing from the
TOP-LEFT of the image.
- It is a WIP project so it's liable to bugs or non-wanted behavior.

## Your first RED pixel!
```python
import Bitmapy as bmp

# Bitmap(width, height, default_color = WHITE)
image = bmp.Bitmap(1, 1, (255, 0, 0))

# save(path)
image.save('red_pixel.bmp')
```

## Draw a heart
```python
import Bitmap as bmp

heart = bmp.Bitmap(7, 7, WHITE)

# draw(color, (x, y))
heart.draw(
    (bmp.RED, (4, 3)),
    (bmp.RED, (3, 2)),
    (bmp.RED, (5, 2)),
    (bmp.RED, (2, 3)),
    (bmp.RED, (6, 3)),
    (bmp.RED, (2, 4)),
    (bmp.RED, (6, 4)),
    (bmp.RED, (5, 5)),
    (bmp.RED, (3, 5)),
    (bmp.RED, (4, 6))
)

heart.save('heart.bmp')
```

## Draw a spiral
```python
from Bitmapy import *

spiral = Bitmap(10, 10, BLACK)

# draw_area(color, from, to)
spiral.draw_area(WHITE, (2, 2), (9, 9))
spiral.draw_area(BLACK, (3, 3), (8, 8))
spiral.draw_area(WHITE, (4, 4), (7, 7))
spiral.draw_area(BLACK, (5, 5), (6, 6))

spiral.draw(
    (WHITE, (1, 2)),
       (BLACK, (2, 3)),
          (WHITE, (3, 4)),
             (BLACK, (4, 5))
)

spiral.save('spiral.bmp')
```