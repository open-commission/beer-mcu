from machine import Pin, I2C
import framebuf, sys

from display.ssd1306 import SSD1306_I2C

def display_task():
    pix_res_x = 128
    pix_res_y = 64

    i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    if i2c_addr == []:
        print('No I2C Display Found')
        sys.exit()
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))

    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)

    buffer = bytearray(
        b"\x00\x00\x00\x00..."
    )

    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

    oled.fill(0)
    oled.blit(fb, 96, 0)
    oled.text("Raspberry Pi", 5, 5)
    oled.text("Pico", 5, 15)
    oled.show()