#!/usr/bin/env python3
import freetype
import numpy
import codecs

# WARNING: program works for 6x8
font_file   = 'Bm437_HP_100LX_6x8.otb'
font_width  = 6
font_height = 8
chars_to_extract = 256

# Load font and set pixel size
face = freetype.Face(font_file)
face.set_pixel_sizes(0, font_height)

# Prepare output image
image = numpy.zeros((font_height, chars_to_extract*font_width), dtype=numpy.uint8)

for i in range(0, chars_to_extract):
    # Get source bitmap of character
    unicode_index = i
    if (i > 127):
        unicode_index = codecs.decode(bytes([i]), 'cp437')
    face.load_char(unicode_index, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)
    bitmap = face.glyph.bitmap
    # Create target grayscale bitmap
    target = numpy.zeros((font_height,font_width), dtype=numpy.uint8)
    # Bitmap seems valid
    if (bitmap.width == font_width and bitmap.rows == font_height):
        # Go through scan lines
        for src_row in range(0, font_height):
            byte_value = bitmap.buffer[src_row]
            # Go through bits and unpack them
            for bit_index in range(font_width):
                bit = byte_value & (1 << (7 - bit_index))
                target[src_row, bit_index] = 255 if bit else 0
        # Copy target (image of character) to image of whole character map
        image[0:8, i*6:i*6+6] = target

print("font_data = bytearray( \\")
raw_data = bytearray()
# Go through image columns and encode them to bits again -> this matches framebuffer layout of PCD8544 display
for column in range(image.shape[1]):
    value = 0
    for bit_index in range(0,8):
        bit_value = 1 if image[bit_index, column] != 0 else 0
        bit_value = bit_value << bit_index
        value |= bit_value
    if (column % 6 == 0 and column != 0):
        print("' \\")
    if (column % 6 == 0):
        print("    b'", end='')
    print(f"\\x{value:02X}", end='')
    raw_data.append(value)
print("')")

# Save the font file
with open(f'font-{font_width}x{font_height}.bin', 'wb') as file:
    file.write(raw_data)
