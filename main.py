import uasyncio as asyncio
from uart.uart_utils import UARTUtil

from task.dx180x20 import dx_task_1, dx_task_2
from task.gpio_reader import gpio_reader_task
# from task.jqc import jqc_task
from task.led import led_task
from task.display import display_task_1, display_task_2, async_display_task_1, async_display_task_2
from task.pulse_counter import pulse_counter_task
from task.uart_handler import uart_receive_task
from data.singleton_data import serial_output_task


async def main():
    """主函数，同时运行所有任务"""
    print("🚀 啤酒酿造系统启动中...")
    
    # 初始化UART
    uart_util = UARTUtil(
        uart_id=0,
        baudrate=115200,
        tx_pin=12,
        rx_pin=13
    )
    print("✅ UART初始化完成")
    
    # # 创建并启动所有任务
    # # 🖥️ 设备1显示任务
    # asyncio.create_task(async_display_task_1())
    #
    # # 🖥️ 设备2显示任务
    # asyncio.create_task(async_display_task_2())
    #
    # # 📤 串口数据输出任务
    # asyncio.create_task(serial_output_task(uart_util))
    #
    # # 📥 UART数据接收任务
    # asyncio.create_task(uart_receive_task(uart_util))
    #
    # # 💧 脉冲计数任务
    # asyncio.create_task(pulse_counter_task())
    
    # 🔌 其他可选任务（可根据需要启用）
    asyncio.create_task(led_task())
    # asyncio.create_task(jqc_task())
    # asyncio.create_task(dx_task_1())
    # asyncio.create_task(dx_task_2())
    # asyncio.create_task(gpio_reader_task())
    
    print("✅ 所有任务已启动")
    
    # 防止主程序退出
    while True:
        await asyncio.sleep(1)


# 运行主函数
asyncio.run(main())