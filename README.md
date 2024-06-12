# Bitmapy
*A work in progress bitmap manager with python.*

## Today in version 1.5 !!!

![Bitmap logo.](./logo.bmp)

## Details
- Like many other graphic design softwares, Bitmapy starts drawing from the
TOP-LEFT of the image.
- It is a WIP project so it's liable to bugs or non-wanted behavior.

## Your first RED pixel
```python
from Bitmapy import bmp

# Bitmap(width, height, default_color = WHITE)
image = bmp.Bitmap(1, 1, bmp.RED)

# save(path)
image.save('red_pixel.bmp')
```