import uasyncio as asyncio
from machine import Pin
from data.singleton_data import get_data_manager


async def gpio_pin_reader(pin_number, device_id):
    """
    读取指定引脚的高低电平状态并更新设备水位状态
    高电平表示水位异常，低电平表示水位正常
    
    Args:
        pin_number: 要读取的引脚编号
        device_id: 设备ID ('device1' 或 'device2')
    """
    # 获取数据管理器
    data_mgr = get_data_manager()
    
    # 配置引脚为输入模式
    pin = Pin(pin_number, Pin.IN)
    
    while True:
        # 读取引脚状态
        state = pin.value()
        # 高电平表示水位异常，低电平表示正常
        water_level_normal = not state  # 低电平为正常
        
        # 打印引脚状态
        level_status = "正常" if water_level_normal else "异常"
        print("GPIO {} 引脚电平: {} (水位状态: {})".format(pin_number, "高" if state else "低", level_status))
        
        # 更新对应设备的水位和警告状态
        if device_id == 'device1':
            data_mgr.device1_water = water_level_normal
            data_mgr.device1_warn = not water_level_normal  # 水位异常时设置警告
            status_text = "正常" if water_level_normal else "异常"
            print("✅ 设备1水位状态已更新: {}".format(status_text))
        elif device_id == 'device2':
            data_mgr.device2_water = water_level_normal
            data_mgr.device2_warn = not water_level_normal  # 水位异常时设置警告
            status_text = "正常" if water_level_normal else "异常"
            print("✅ 设备2水位状态已更新: {}".format(status_text))
            
        # 等待1秒
        await asyncio.sleep(1)


async def gpio_reader_task():
    """
    GPIO引脚读取任务，同时读取24号和8号引脚的电平状态
    分别对应设备1和设备2的水位检测
    """
    print("🚀 GPIO引脚读取任务开始运行...")
    
    # 创建读取24号引脚的任务 (对应设备1)
    asyncio.create_task(gpio_pin_reader(24, 'device1'))
    # 创建读取8号引脚的任务 (对应设备2)
    asyncio.create_task(gpio_pin_reader(8, 'device2'))
    
    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)