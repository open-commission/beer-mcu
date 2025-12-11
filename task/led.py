import uasyncio as asyncio
from machine import Pin


# ---------------- GPIO 流水灯任务 ----------------
async def led_sequence_task():
    """LED流水灯任务，使GPIO2、3、29、28上的LED依次点亮"""
    leds = [
        Pin(2, Pin.OUT),
        Pin(3, Pin.OUT),
        Pin(29, Pin.OUT),
        Pin(28, Pin.OUT)
    ]

    # 初始化所有LED为低电平
    for led in leds:
        led.value(0)

    while True:
        # 正向点亮：依次点亮每个LED
        for i in range(len(leds)):
            leds[i].value(1)  # 当前LED置高电平
            await asyncio.sleep(0.3)
            leds[i].value(0)  # 当前LED置低电平

        # 反向点亮：从倒数第二个到第一个点亮（避免重复点亮最后一个）
        for i in range(len(leds) - 2, -1, -1):
            leds[i].value(1)  # 当前LED置高电平
            await asyncio.sleep(0.3)
            leds[i].value(0)  # 当前LED置低电平


# ---------------- 主函数 ----------------
async def led_task():
    """主函数，启动LED流水灯任务"""
    print("🚀 LED流水灯程序开始运行...")

    # 启动LED流水灯任务
    asyncio.create_task(led_sequence_task())

    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)