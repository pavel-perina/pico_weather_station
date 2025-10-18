from global_context import GlobalContext
from font_table_full import font_data
import time 
from framebuf import FrameBuffer, MONO_VLSB

def fb_clear(ctx:GlobalContext):
    # Zero out the byte array
    ctx.framebuffer =  bytearray(b'\x00' * len(ctx.framebuffer))

def fb_write(ctx:GlobalContext, row:int, x:int, text:str):
    #print(text)
    dst_index = row * ctx.fb_width + x
    for ch in text:
        src_index = ord(ch)*6
        for x in range(6):
            ctx.framebuffer[dst_index] = font_data[src_index+x]
            dst_index += 1

def get_time_str():
    tm = time.localtime()
    return f"{tm[2]:0d}.{tm[1]:02d}. {tm[3]:02d}:{tm[4]:02d}:{tm[5]:02d} UTC"


class ScreenMain:
    def __init__(self, ctx:GlobalContext):
        print(f"Initializing screen, framebuffer lenght is {len(ctx.framebuffer)}")
        self.last_update = 0

    def on_tick(self, ctx:GlobalContext):
        # Handle keyboard
        # Update screen
        if time.ticks_diff(ctx.ticks_ms, self.last_update) > 1000:
            """
            fb_clear(ctx)
            fb_write(ctx, 0, 0, "SHT40:")
            fb_write(ctx, 1, 0, f"  Temp: {ctx.sht40_temperature:.2f}\xf8C")
            fb_write(ctx, 2, 0, f"  RH:   {ctx.sht40_humidity:.2f} %")
            fb_write(ctx, 3, 0, "BMP280:")
            fb_write(ctx, 4, 0, f"  Temp: {ctx.bmp280_temperature:.2f}\xf8C")
            fb_write(ctx, 5, 0, f"  {ctx.bmp280_pressure*0.01:.2f} hPa")
            """
            rh = 9 # row height
            fb = FrameBuffer(ctx.framebuffer, 128, 64, MONO_VLSB)
            fb.fill(0)
            #fb.rect(0, 0, 127, rh-1, 1, True)
            #fb.text(get_time_str(), 4, 0, 0)
            fb.text(get_time_str(), 8, 0)
            fb.text("SHT40:", 0, rh)
            fb.text(f"Temp: {ctx.sht40_temperature:.2f} C", 16, 2*rh)
            fb.text(f"RH:   {ctx.sht40_humidity:.2f} %", 16, 3*rh)
            fb.text("BMP280:", 0, 4*rh)
            fb.text(f"Temp: {ctx.bmp280_temperature:.2f} C", 16, 5*rh)
            fb.text(f"{ctx.bmp280_pressure*0.01:.2f} hPa", 16, 6*rh)
            ctx.framebuffer_dirty = True
            self.last_update = ctx.ticks_ms
