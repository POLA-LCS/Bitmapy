# Bitmapy
![Bitmap logo.](/smiley_face.bmp)
A work in progress bitmap manager with python.

## Your first RED pixel!

```python
import Bitmapy as bmp

# Bitmap(width, height, default_color = WHITE)
image = bmp.Bitmap(1, 1, (255, 0, 0))

image.save('red_pixel.bmp')
```

## Draw in a bitmap
```python
import Bitmap as bmp

image = bmp.Bitmap(7, 7, (255, 255, 255))

# draw(color, (x, y))
image.draw(WHITE, (3, 7))

image.save('image.bmp')
```

- LEFT   -> x = 0
- TOP    -> y = 0