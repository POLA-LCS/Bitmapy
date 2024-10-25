from .bitmap import Bitmap

def from_bitmap(bitmap_path: str):
    import struct
    with open(bitmap_path, 'rb') as file:
        bmp_data = file.read()

    # header
    file_header = struct.unpack('<2sI2HI', bmp_data[:14])
    # header info
    header_info = struct.unpack('<IIIHHIIIIII', bmp_data[14:54])
    
    _, file_size, _, _, offset = file_header
    header_size, width, height, planes, bits_per_pixel, compression, image_size, x_pixels_per_meter, y_pixels_per_meter, colors_used, important_colors = header_info

    if bits_per_pixel != 32:
        raise ValueError("Only 32 bits per pixel bitmaps are valid")

    image_data = bmp_data[offset:]
    canvas = []
    for y in range(height):
        row = []
        for x in range(width):
            idx = (y * width + x) * 4
            b, g, r, a = struct.unpack('BBBB', image_data[idx:idx + 4])
            row.append((r, g, b, a))
        canvas.insert(0, row)

    bitmap = Bitmap(width, height)
    bitmap.canvas = canvas
    return bitmap

def from_image(image_path: str):
    from .bitmap import Bitmap
    from PIL import Image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    bitmap = Bitmap(width, height)
    print(img, bitmap)
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            bitmap.canvas[y][x] = (r, g, b, a)
    return bitmap