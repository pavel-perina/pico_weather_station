from machine import I2C, SPI, Pin
import time
from global_context import GlobalContext
from sensor_sht40 import Sht40
from sensor_bmp280 import Bmp280
from display_pcd8544 import Display
from screen_main import ScreenMain
#from screen_menu import 

ctx = GlobalContext(I2C(0, sda=Pin(0), scl=Pin(1)), 
                    SPI(1, baudrate=1000000, mosi=Pin(11), sck=Pin(10))
)
display = Display(ctx)
screen_main = ScreenMain(ctx)
sht40 = Sht40()
bmp280 = Bmp280(ctx)
while True:
    # Time stuff
    time.sleep_ms(5)
    ctx.ticks_ms = time.ticks_ms()

    # Read sensors
    sht40.on_tick(ctx)
    bmp280.on_tick(ctx)
    #rtc.on_tick(ctx)

    # Translate keyboard buttons to events
    #keyboard.on_tick(ctx)

    # Data logging stuff
    # logger.on_tick(ctx)
    if (ctx.app == "SCREEN_MAIN"):
        screen_main.on_tick(ctx)

    # Update display from framebuffer if dirty
    display.on_tick(ctx) 
    #print(f"Ticks: {ctx.ticks_ms}, Temp: {ctx.sht40_temperature}")