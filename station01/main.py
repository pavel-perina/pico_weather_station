from machine import I2C, SPI, Pin
import time
from global_context import GlobalContext
from sensor_sht40 import Sht40
from sensor_bmp280 import Bmp280
from display_ssd1306 import Display
from screen_main import ScreenMain
from connection_wifi import Connection
#from screen_menu import

# Pinout is GP0, GP1 (left 1,2) -> sensors i2c
#           GP2, GP3 (left 4,5) -> display i2c
#           GND, 3V3_out (rigt 3, 5) -> power

print("=== PROGRAM START ===")
i2c0 = I2C(0, sda=Pin(0), scl=Pin(1))
ctx = GlobalContext(i2c0,
                    i2c0,                 
                    time.ticks_ms()
                    )
time.sleep_ms(200)
display = Display(ctx)
time.sleep_ms(50)
screen_main = ScreenMain(ctx)
time.sleep_ms(50)
sht40   = Sht40()
time.sleep_ms(50)
bmp280  = Bmp280(ctx)
time.sleep_ms(50)
connection = Connection(ctx)
connection.connect(ctx)
pin_led = Pin("LED", Pin.OUT)

while True:
    # Time stuff (decrease for keyboard debounce handler in the future)
    time.sleep_ms(50)
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
    
    connection.on_tick(ctx)
    # Blinks LED as heartbeat - gets annoying, only for debug
    #pin_led.toggle()