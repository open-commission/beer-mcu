import uasyncio as asyncio
import machine, onewire, ds18x20


async def dx_read_task(pin):
    ds_pin = machine.Pin(pin)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

    roms = ds_sensor.scan()
    print('Found DS devices: {} -> {}'.format(pin, roms))

    while True:
        ds_sensor.convert_temp()
        await asyncio.sleep_ms(750)
        for rom in roms:
            print('Found DS devices: {} -> {}'.format(pin, ds_sensor.read_temp(rom)))
        await asyncio.sleep(2)


async def dx_task_1():
    await dx_read_task(9)


async def dx_task_2():
    await dx_read_task(7)