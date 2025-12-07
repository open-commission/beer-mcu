import machine, onewire, ds18x20, time

def dx_task():
    ds_pin = machine.Pin(28)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)

    while True:
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            print(ds_sensor.read_temp(rom))
        time.sleep(2)