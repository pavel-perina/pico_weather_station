# This code is responsible for updating framebuffer
# which is the same for SSD1306, PCD8544 displays
# and differs only by frame buffer size.
# 
# Note that code depends on sensors (context)
# and also resolution, displays may vary in row/column
# count.

from global_context import GlobalContext
from font_table_full import font_data
import time 

def fb_clear(ctx:GlobalContext):
    # Zero out the byte array
    ctx.framebuffer =  bytearray(b'\x00' * len(ctx.framebuffer))

def fb_write(ctx:GlobalContext, row:int, x:int, text:str):
    dst_index = row * ctx.fb_width + x
    for ch in text:
        src_index = ord(ch)*6
        for x in range(6):
            ctx.framebuffer[dst_index] = font_data[src_index+x]
            dst_index += 1

class ScreenMain:
    def __init__(self, ctx:GlobalContext):
        print(f"Initializing screen, framebuffer lenght is {len(ctx.framebuffer)}")
        self.last_update = 0
    
    def on_tick(self, ctx:GlobalContext):
        # Handle keyboard

        # Update screen
        if time.ticks_diff(ctx.ticks_ms, self.last_update) > 1000:
            fb_clear(ctx)
            tm = time.localtime()
            fb_write(ctx, 0, 0, f"{tm[3]:02d}:{tm[4]:02d}:{tm[5]:02d} UTC")
            fb_write(ctx, 1, 0, f"Temp: {ctx.scd41_temperature:.2f}\xf8C")
            fb_write(ctx, 2, 0, f"RH:   {ctx.scd41_humidity:.2f} %")
            fb_write(ctx, 3, 0, f"CO2:  {ctx.scd41_co2} ppm")
            fb_write(ctx, 4, 0, f"Temp: {ctx.sht40_temperature:.2f}\xf8C")
            fb_write(ctx, 5, 0, f"   RH:{ctx.sht40_humidity:.2f} %")
            ctx.framebuffer_dirty = True
            self.last_update = ctx.ticks_ms
