from machine import Pin, SPI
import time

class Display:

    def __init__(self, ctx):
        #init pins
        self.spi = SPI(1, baudrate=2_000_000, sck=Pin(14), mosi=Pin(15))
        self.dc = Pin(12)
        self.cs = Pin(13) #N/C
        self.rst = Pin(11)
        self.dc.init(Pin.OUT, value=0)
        self.rst.init(Pin.OUT, value=0)

        time.sleep_ms(1)
        self.rst.value(1)
        time.sleep_ms(1)

        self.flipX = False
        self.flipY = True
        contrast = 0x00

        initCommands=[
            0xE2,                           # Software reset
            0xA2|0x01,                      # LCD bias 0:1/9 1:1/7
            0x81,                           # Electronic volume (contrast) mode
            (contrast&0x3f),                # Contrast value: 0x00-0x3F (default 0x1F - in my experience 0 works best)
            0x20|0x03,                      # Voltage regulator ratio: 0x00-0x07 (3.0-6.5V)
            0x28|0x07,                      # Power control: booster+regulator+follower all on
            0xA0|(0x01 if self.flipX else 0x00), # Segment direction: 0=normal, 1=reversed (flip X)
            0xC0|(0x08 if self.flipY else 0x00), # Common output direction: 0=normal, 8=reversed (flip Y)
            0x40|0x00,                      # Display start line: 0x40-0x7F (line 0-63)
            0xAE|0x01,                      # Display on/off, 0=off,1=on
        ]

        self.writeCommands(initCommands)

    # Write command(s)
    def writeCommands(self, cmd):
        self.cs.value(0)    # Enable device
        self.dc.value(0)    # Command mode
        self.spi.write(bytearray(cmd))
        self.dc.value(1)    # Disable device

    # Write framebuffer data
    def writeData(self, data):
        self.cs.value(0)
        self.dc.value(1)    # Display data mode
        self.spi.write(data)
        self.dc.value(1)

    def show(self, buffer):
        self.writeCommands([0x40|0x00])  # Set start line to 0
        for line in range(8):
            self.writeCommands([
                0xB0 | line,    # Set line (0-7)
                0x10 | 0x00,    # Set column address high nibble
                0x00 | (0x04 if self.flipX else 0x00),    # Set column address low  nibble
            ])
            # Write pages data (8 rows, 128 columns)
            self.writeData(buffer[(128*line):(128*line+128)])

    def on_tick(self, ctx):
        if ctx.framebuffer_dirty:
            self.show(ctx.framebuffer)


# Make this runnable
# Blinks LED and toggles display between black and text
if __name__ == "__main__":
    from framebuf import FrameBuffer, MONO_VLSB
    print("Running as standalone script")
    disp = Display(None)
    buffer=bytearray(128*64//8)
    fb = FrameBuffer(buffer, 128, 64, MONO_VLSB)
    led = Pin("LED", Pin.OUT)

    while(True):
        led.toggle()
        fb.fill(255)
        disp.show(buffer)

        time.sleep(1)

        led.toggle()
        fb.fill(0)
        fb.text("Sitronix ST7567",0,0)
        disp.show(buffer)

        time.sleep(5)