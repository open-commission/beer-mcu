import uasyncio as asyncio
from machine import Pin


# ---------------- 继电器顺序切换任务 ----------------
async def jqc_sequence_task():
    """继电器顺序切换任务，从第一个到第六个依次切换"""
    jqcs = [
        Pin(14, Pin.OUT),
        Pin(15, Pin.OUT),
        Pin(17, Pin.OUT),
        Pin(18, Pin.OUT),
        Pin(19, Pin.OUT),
        Pin(20, Pin.OUT)
    ]

    # 初始化所有继电器为低电平
    for jqc in jqcs:
        jqc.value(0)

    while True:
        # 从第一个到第六个依次切换继电器
        for i in range(len(jqcs)):
            jqcs[i].value(1)  # 当前继电器置高电平
            await asyncio.sleep(1)
            jqcs[i].value(0)  # 当前继电器置低电平
            await asyncio.sleep(0.1)  # 短暂间隔确保完全关闭


# ---------------- 主函数 ----------------
async def jqc_task():
    """主函数，启动继电器顺序切换任务"""
    print("🚀 继电器顺序切换程序开始运行...")

    # 启动继电器顺序切换任务
    asyncio.create_task(jqc_sequence_task())

    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)