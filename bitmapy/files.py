from .bitmap import Bitmap

def write_pixels(bmp: Bitmap):
    with open(bmp.path + '.bmpy', 'w') as file:
        for row in bmp.canvas:
            for pixel in row:
                for data in [hex(data) for data in pixel]:
                    file.write(data + ' ')
            file.write('\n')