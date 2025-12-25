from PIL import Image

def pbm_to_column_bytes(img_path, glyph_width, glyph_height, verbose=False):
    """
    Convert a monochrome image to column-major byte array.

    img_path: path to PBM/PNG/etc
    glyph_width: width of each glyph in pixels
    glyph_height: height of each glyph in pixels
    returns: list of bytes
    """

    img = Image.open(img_path).convert("1")  # ensure monochrome
    w, h = img.size
    pixels = img.load()

    glyphs_per_row = w // glyph_width
    rows_of_glyphs = h // glyph_height
    bytes_per_column = (glyph_height + 7) // 8

    out_bytes = []

    for gy in range(rows_of_glyphs):
        for gx in range(glyphs_per_row):
            # iterate over each glyph
            for x in range(glyph_width):
                col_bytes = []
                for b in range(bytes_per_column):
                    byte = 0
                    for bit in range(8):
                        y = gy * glyph_height + b * 8 + bit
                        if y >= (gy+1)*glyph_height:
                            continue
                        px = gx * glyph_width + x
                        if pixels[px, y]:
                            byte |= 1 << bit
                    col_bytes.append(byte)
                out_bytes.extend(col_bytes)
    if verbose:
        print(f"Generated {len(out_bytes)} bytes for {glyphs_per_row*rows_of_glyphs} glyphs")
    return out_bytes


def to_python_array(byte_list, name="font_data", width=16):
    """Convert byte list to Python array string"""
    lines = []
    for i in range(0, len(byte_list), width):
        line = ", ".join(f"0x{b:02X}" for b in byte_list[i:i+width])
        lines.append(line)
    return f"{name} = bytearray([\n" + ",\n".join(lines) + "\n])"


def to_cpp_array(byte_list, name="font_data", width=16):
    """Convert byte list to C++ const uint8_t array string"""
    lines = []
    for i in range(0, len(byte_list), width):
        line = ", ".join(f"0x{b:02X}" for b in byte_list[i:i+width])
        lines.append(line)
    return f"const uint8_t {name}[] = {{\n" + ",\n".join(lines) + "\n}};"


if __name__ == "__main__":
    # Example usage:
    # 256x8 font table, 6px wide glyphs, 8px high
    bytes_out = pbm_to_column_bytes("font.pbm", glyph_width=6, glyph_height=8, verbose=True)
    
    py_array = to_python_array(bytes_out, "font_data_6x8")
    cpp_array = to_cpp_array(bytes_out, "font_data_6x8")
    
    # Write Python array
    with open("font_6x8.py", "w") as f:
        f.write(py_array)
    
    # Write C++ array
    with open("font_6x8.h", "w") as f:
        f.write(cpp_array)