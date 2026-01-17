# import uasyncio as asyncio
#
# from task.dx180x20 import dx_task_1, dx_task_2
# from task.gpio_reader import gpio_reader_task
# from task.jqc import jqc_task
# from task.led import led_task
# from task.display import display_task_1, display_task_2, async_display_task_1, async_display_task_2
#
#
# async def main():
#     """主函数，同时运行所有任务"""
#     # 创建并启动所有任务
#     # asyncio.create_task(led_task())
#     # asyncio.create_task(async_display_task_1())
#     # asyncio.create_task(async_display_task_2())
#     # asyncio.create_task(jqc_task())
#     # asyncio.create_task(dx_task_1())
#     # asyncio.create_task(dx_task_2())
#     asyncio.create_task(gpio_reader_task())
#
#     # 防止主程序退出
#     while True:
#         await asyncio.sleep(1)
#
#
# # 运行主函数
# asyncio.run(main())


# 测试

import machine
import _thread
import time
import sys

# --- 配置区 ---
# 传感器属性: [当前值, 基础值, 目标值, 步长, 是否激活]
sensors = {
    "1": {"name": "Temp", "curr": 25.0, "base": 25.0, "target": 45.0, "step": 0.5},
    "2": {"name": "Humi", "curr": 50.0, "base": 50.0, "target": 90.0, "step": 2.0},
    "3": {"name": "Lux ", "curr": 200.0, "base": 200.0, "target": 1200.0, "step": 50.0}
}

# 状态设备: [名称, GPIO引脚, 当前状态]
status_devs = {
    "5": {"name": "Relay", "pin": 25, "state": False}  # Pico板载LED在GPIO25
}

# 初始化硬件
for key in status_devs:
    dev = status_devs[key]
    dev["obj"] = machine.Pin(dev["pin"], machine.Pin.OUT)
    dev["obj"].value(dev["state"])

# 全局标志位：控制各传感器的激活状态
active_flags = {key: False for key in sensors}


# --- 任务1: 后台串口监听 (运行在第二个核心) ---
def uart_reader_thread():
    while True:
        # 检查 stdin 是否有字符输入
        char = sys.stdin.read(1)

        # 匹配传感器触发
        if char in active_flags:
            active_flags[char] = not active_flags[char]

        # 匹配状态设备触发
        if char in status_devs:
            dev = status_devs[char]
            dev["state"] = not dev["state"]
            dev["obj"].value(dev["state"])


# 启动第二个核心
_thread.start_new_thread(uart_reader_thread, ())

# --- 主循环: 数值模拟与静默输出 (运行在主核心) ---
print("System started. Send '1','2','3' to ramp, '5' to toggle relay.\n")

while True:
    # 1. 数值平滑演变
    for key, sensor in sensors.items():
        goal = sensor["target"] if active_flags[key] else sensor["base"]

        if sensor["curr"] < goal:
            sensor["curr"] = min(sensor["curr"] + sensor["step"], goal)
        elif sensor["curr"] > goal:
            sensor["curr"] = max(sensor["curr"] - sensor["step"], goal)

    # 2. 串口刷新输出
    output = ">> "
    for key, s in sensors.items():
        output += f"{s['name']}: {s['curr']:.1f} | "

    for key, d in status_devs.items():
        state_str = "ON " if d["state"] else "OFF"
        output += f"{d['name']}: {state_str} "

    # 打印一行
    print(output)

    time.sleep(1)