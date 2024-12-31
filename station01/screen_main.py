from global_context import GlobalContext
from font_table_full import font_data

def fb_clear(ctx:GlobalContext):
    # Zero out the byte array
    ctx.framebuffer =  bytearray(b'\x00' * len(ctx.framebuffer))

def fb_write(ctx:GlobalContext, row:int, x:int, text:str):
    print(text)
    dst_index = row * ctx.fb_width + x
    for ch in text:
        src_index = ord(ch)*6
        for x in range(6):
            #if (dst_index > 503):
            #    return
            #print(f"{dst_index}, {src_index+x}")
            ctx.framebuffer[dst_index] = font_data[src_index+x]
            dst_index += 1

class ScreenMain:
    def __init__(self, ctx:GlobalContext):
        print(f"Initializing screen, framebuffer lenght is {len(ctx.framebuffer)}")
        self.last_update = 0
    
    def on_tick(self, ctx:GlobalContext):
        # Handle keyboard
        # Update screen
        if (ctx.ticks_ms - self.last_update > 1000):
            fb_clear(ctx)
            fb_write(ctx, 0, 0, "SHT40:")
            fb_write(ctx, 1, 0, f"Temp: {ctx.sht40_temperature*0.001:.2f}\xf8C")
            fb_write(ctx, 2, 0, f"RH:   {ctx.sht40_humidity*0.001:.2f} %")
            fb_write(ctx, 3, 0, "BMP280:")
            fb_write(ctx, 4, 0, f"Temp: {ctx.bmp280_temperature:.2f}\xf8C")
            fb_write(ctx, 5, 0, f"{ctx.bmp280_pressure*0.01:.2f} hPa")
            print("FB up")
            ctx.framebuffer_dirty = True
            self.last_update = ctx.ticks_ms
