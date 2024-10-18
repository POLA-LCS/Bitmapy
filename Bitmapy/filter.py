from .bitmap import Bitmap

def random_noise(input: Bitmap, noise_range: int, rainbow = False) -> Bitmap:
    from random import randint
    """`noise_range` means the pixel is going to change\n
    in a random range between `-noise_range` and `noise_range`\n
    `rainbow`: r, g, b are change individually by different random values inside the range"""
    output = Bitmap(input.width, input.height, (0, 0, 0, 0))
    for left in range(input.width):
        for top in range(input.height):
            r, g, b, _ = input.get_pixel(left, top)
            if rainbow:
                r += randint(-noise_range, noise_range)
                g += randint(-noise_range, noise_range)
                b += randint(-noise_range, noise_range)
            else:
                random_value = randint(-noise_range, noise_range)
                r += random_value
                g += random_value
                b += random_value
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))
            output.draw_pixel((r, g, b, 255), (left, top))
    return output
