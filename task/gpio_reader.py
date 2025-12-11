import uasyncio as asyncio
from machine import Pin


async def gpio_pin_reader(pin_number):
    """
    读取指定引脚的高低电平状态
    
    Args:
        pin_number: 要读取的引脚编号
    """
    # 配置引脚为输入模式
    pin = Pin(pin_number, Pin.IN)
    
    while True:
        # 读取引脚状态
        state = pin.value()
        # 打印引脚状态
        print("GPIO {} 引脚电平: {}".format(pin_number, "高" if state else "低"))
        # 等待1秒
        await asyncio.sleep(1)


async def gpio_reader_task():
    """
    GPIO引脚读取任务，同时读取22号和8号引脚的电平状态
    """
    print("🚀 GPIO引脚读取任务开始运行...")
    
    # 创建读取24号引脚的任务
    asyncio.create_task(gpio_pin_reader(24))
    # 创建读取8号引脚的任务
    asyncio.create_task(gpio_pin_reader(8))
    
    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)