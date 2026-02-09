import uasyncio as asyncio

from task.dx180x20 import dx_task_1, dx_task_2
from task.gpio_reader import gpio_reader_task
from task.jqc import jqc_task
from task.led import led_task
from task.display import display_task_1, display_task_2, async_display_task_1, async_display_task_2


async def main():
    """主函数，同时运行所有任务"""
    # 创建并启动所有任务
    # asyncio.create_task(led_task())
    asyncio.create_task(async_display_task_1())
    asyncio.create_task(async_display_task_2())
    # asyncio.create_task(jqc_task())
    # asyncio.create_task(dx_task_1())
    # asyncio.create_task(dx_task_2())
    # asyncio.create_task(gpio_reader_task())

    # 防止主程序退出
    while True:
        await asyncio.sleep(1)


# 运行主函数
asyncio.run(main())