# Bitmapy
![Bitmap logo.](/smiley_face.bmp)
A work in progress bitmap manager with python.

## Your first RED pixel!

```python
import Bitmapy as bmp

image = bmp.Bitmap(1, 1, (255, 0, 0))

image.save('red_pixel.bmp')
```