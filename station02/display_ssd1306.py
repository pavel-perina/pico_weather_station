# TODO
# SSD display initialization and loop

from machine import I2C

class Display:

    def __init(self, ctx):
        # TODO: init code
        pass

    def on_tick(self, ctx):
        if ctx.framebuffer_dirty:
            # TODO: send framebuf

            ctx.framebuffer_dirty = False