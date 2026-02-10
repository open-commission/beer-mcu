import uasyncio as asyncio
import machine, onewire, ds18x20
from data.singleton_data import get_data_manager


async def dx_read_task(pin, device_id):
    """
    DS18B20温度读取任务
    
    Args:
        pin: GPIO引脚号
        device_id: 设备ID ('device1' 或 'device2')
    """
    # 获取数据管理器
    data_mgr = get_data_manager()
    
    ds_pin = machine.Pin(pin)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

    roms = ds_sensor.scan()
    print('Found DS devices: {} -> {}'.format(pin, roms))

    while True:
        ds_sensor.convert_temp()
        await asyncio.sleep_ms(750)
        for rom in roms:
            temp = ds_sensor.read_temp(rom)
            print('DS{}温度: {:.2f}°C'.format(pin, temp))
            
            # 更新对应设备的温度数据
            if device_id == 'device1':
                data_mgr.device1_temp = temp
                print('✅ 设备1温度已更新: {:.2f}°C'.format(temp))
            elif device_id == 'device2':
                data_mgr.device2_temp = temp
                print('✅ 设备2温度已更新: {:.2f}°C'.format(temp))
                
        await asyncio.sleep(2)


async def dx_task_1():
    """设备1温度读取任务 (GPIO9)"""
    await dx_read_task(9, 'device1')


async def dx_task_2():
    """设备2温度读取任务 (GPIO7)"""
    await dx_read_task(7, 'device2')