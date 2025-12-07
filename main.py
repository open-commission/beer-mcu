import utime
import asyncio

from adc.adc_utils import init_adc, read_adc_value

from machine import Pin, I2C
import framebuf, sys

from display.ssd1306 import SSD1306_I2C

import machine, onewire, ds18x20, time
from auart.uart_utils import UARTUtil, uart_reader


def uart_callback(data):
    """
    UART接收回调函数
    """
    print("接收到UART数据:", data)


async def main_loop():
    try:
        print("开始初始化 UART(0)...")

        uart_point = UARTUtil(uart_id=0, baudrate=115200)

        print("UART(0) 初始化成功")

        i = 0
        while True:
            uart_point.send("Hello {}\n".format(i))
            print("发送数据:", "Hello {}".format(i))
            i += 1
            await asyncio.sleep(1)

    except Exception as e:
        print("UART 初始化异常:", e)


def main():
    print("测试程序开始运行11...")

    asyncio.run(main_loop())

    print("测试程序开始运行22...")

    # adc = init_adc(27)
    #
    # print("开始读取ADC值...")
    #
    # while True:
    #     # 读取ADC值和电压
    #     adc_value, voltage = read_adc_value(adc)
    #
    #     # 输出ADC值和电压
    #     print("ADC值:", adc_value, "电压: {:.2f}V".format(voltage))
    #
    #     utime.sleep(1)

    # display (原样保留你注释代码)
    # pix_res_x = 128
    # pix_res_y = 64
    #
    # i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
    # i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    # if i2c_addr == []:
    #     print('No I2C Display Found')
    #     sys.exit()
    # else:
    #     print("I2C Address      : {}".format(i2c_addr[0]))
    #     print("I2C Configuration: {}".format(i2c_dev))
    #
    # oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    #
    # buffer = bytearray(
    #     b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00..."
    # )
    #
    # fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    #
    # oled.fill(0)
    # oled.blit(fb, 96, 0)
    # oled.text("Raspberry Pi", 5, 5)
    # oled.text("Pico", 5, 15)
    # oled.show()

    # ds12x20 原样保留注释
    # ds_pin = machine.Pin(28)
    # ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    #
    # roms = ds_sensor.scan()
    # print('Found DS devices: ', roms)
    #
    # while True:
    #     ds_sensor.convert_temp()
    #     time.sleep_ms(750)
    #     for rom in roms:
    #         print(ds_sensor.read_temp(rom))
    #     time.sleep(2)


if __name__ == "__main__":
    main()
