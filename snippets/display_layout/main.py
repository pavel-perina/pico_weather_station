from PIL import Image
from font_table_full import font_data_6x8
from font_vga_8x16 import font_data_vga_8x16

fb_width = 128
fb_height = 64

indoor_temp = 23.45
indoor_humi = 51.67
indoor_co2  = 844

outdoor_temp = 5
outdoor_feels = 3
outdoor_text = "Clear sky. Light breeze."
outdoor_press = 1024
outdoor_humi = 79
outdoor_dewt = 2
outdoor_wind = 2.6 # m/s
outdoor_wind_dir = 60 # WNW

def framebuffer_to_png(fb, path, upscale=4):
    """
    Convert 128x64 1-bit column-packed framebuffer to a PNG.
    fb: 1024 bytes (128 columns × 8 bytes per column).
    Each byte is a vertical column of 8 pixels.
    """
    if len(fb) != 1024:
        raise ValueError("Framebuffer must contain exactly 1024 bytes.")

    # Create monochrome image
    img = Image.new("1", (fb_width, fb_height))
    pixels = img.load()

    # Iterate through columns
    for line in range(fb_height // 8):           # 8 bytes per column → 64 vertical pixels
        for x in range(fb_width):
            b = fb[line * fb_width + x]
            for ybit in range(8):
                y = line * 8 + ybit
                pixels[x, y] = 1 if (b >> ybit) & 1 else 0

    if upscale > 1:
        img = img.resize((fb_width * upscale, fb_height * upscale), Image.NEAREST)

    img.save(path)


def fb_clear(framebuffer):
    """
    Zero out the byte array
    """    
    framebuffer =  bytearray(b'\x00' * len(framebuffer))


def fb_write_6x8(framebuffer, row:int, x:int, text:str):
    dst_index = row * fb_width + x
    for ch in text:
        src_index = ord(ch)*6
        for x in range(6):
            framebuffer[dst_index] = font_data_6x8[src_index+x]
            dst_index += 1

def fb_blit_column(fb, x, y, column_bytes):
    """
    fb: 1D bytearray framebuffer, column-major, 8px per byte.
    fb_width: width in columns.
    x: column index.
    y: pixel y-position.
    column_bytes: list of N bytes forming one glyph column (top to bottom).
    """

    byte_offset = y >> 3                # which fb byte row it starts in
    shift = y & 7                       # vertical sub-byte shift
    n = len(column_bytes)

    # Preassemble extended 32-bit value containing the whole column shifted
    combined = 0
    for i, b in enumerate(column_bytes):
        combined |= (b << (i * 8))

    combined <<= shift  # apply vertical offset

    # Write out up to n+1 bytes
    for i in range(n + 1):
        out_byte = (combined >> (8 * i)) & 0xFF
        if out_byte == 0:
            continue  # nothing to draw, skip

        fb_index = x + fb_width*(byte_offset + i)
        if fb_index < len(fb):
            fb[fb_index] |= out_byte    # OR-blit


def fb_write_6x8_anywhere(framebuffer, y:int, x:int, text:str):
    column = x
    for ch in text:
        src_index = ord(ch)*6
        for x in range(6):
            fb_blit_column(framebuffer, column, y, memoryview(font_data_6x8)[src_index+x:src_index+x+1])
            column += 1
            
def fb_write_8x16_anywhere(framebuffer, y:int, x:int, text:str):
    column = x
    for ch in text:
        src_index = ord(ch)*8*2 # eg for V it's 86*16=1376
        #src_index = ord(ch)*6
        for x in range(8):
            fb_blit_column(framebuffer, column, y, memoryview(font_data_vga_8x16)[src_index+x*2:src_index+x*2+2])
            column += 1
            


if __name__ == "__main__":
    fb =  bytearray([0x0] * (fb_width * fb_height // 8))
    fb_write_6x8(fb, 0, 36, "28.rij 12:34:56")
    #fb_write_6x8_anywhere(fb, 7, 3, "Good bye.")
    
    fb_write_8x16_anywhere(fb, 14, 48, "21.3")
    fb_write_8x16_anywhere(fb, 30, 48, "46.5")
    fb_write_8x16_anywhere(fb, 46, 48, "0789")
    framebuffer_to_png(fb, "test.png")
