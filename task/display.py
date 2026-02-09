from machine import Pin, I2C
import framebuf, sys
import uasyncio as asyncio

from display.ssd1306 import SSD1306_I2C
from data.singleton_data import get_data_manager


def display_task_1():
    """设备1显示任务 - 显示温度、液位、控制状态、水泵状态"""
    pix_res_x = 128  # SSD1306水平分辨率
    pix_res_y = 64   # SSD1306垂直分辨率

    i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)  # I2C1 (GPIO 26/27)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]  # 获取I2C地址
    if i2c_addr == []:
        print('未找到I2C显示屏')
        return None
    else:
        print("I2C地址      : {}".format(i2c_addr[0]))
        print("I2C配置: {}".format(i2c_dev))

    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    
    # 获取数据管理器
    data_mgr = get_data_manager()
    
    # 显示设备1信息
    oled.fill(0)  # 清屏
    
    # 标题
    oled.text("DEV1 - Brewing", 0, 0)
    
    # 温度显示
    oled.text(f"Temp: {data_mgr.device1_temp:.1f}C", 0, 15)
    
    # 液位状态
    water_status = "FULL" if data_mgr.device1_water else "LOW"
    oled.text(f"Level: {water_status}", 0, 25)
    
    # 控制状态 (加热/制冷)
    control_status = ""
    if data_mgr.device1_heat:
        control_status = "HEAT+"
    elif data_mgr.device1_cool:
        control_status = "COOL-"
    else:
        control_status = "IDLE"
    oled.text(f"Ctrl: {control_status}", 0, 35)
    
    # 水泵状态
    if data_mgr.device1_pump:
        oled.text(f"Pump: {data_mgr.shared_flow:.1f}", 0, 45)
    else:
        oled.text("Pump: OFF", 0, 45)
    
    # 警告报警指示
    alert_text = ""
    if data_mgr.device1_warn:
        alert_text += "W!"
    if data_mgr.device1_alarm:
        alert_text += "A!"
    if alert_text:
        oled.text(alert_text, 90, 0)
    
    oled.show()
    return oled


def display_task_2():
    """设备2显示任务 - 显示温度、液位、控制状态、水泵状态"""
    pix_res_x = 128  # SSD1306水平分辨率
    pix_res_y = 64   # SSD1306垂直分辨率

    i2c_dev = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)  # I2C0 (GPIO 0/1)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]  # 获取I2C地址
    if i2c_addr == []:
        print('未找到I2C显示屏')
        return None
    else:
        print("I2C地址      : {}".format(i2c_addr[0]))
        print("I2C配置: {}".format(i2c_dev))

    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    
    # 获取数据管理器
    data_mgr = get_data_manager()
    
    # 显示设备2信息
    oled.fill(0)  # 清屏
    
    # 标题
    oled.text("DEV2 - Brewing", 0, 0)
    
    # 温度显示
    oled.text(f"Temp: {data_mgr.device2_temp:.1f}C", 0, 15)
    
    # 液位状态
    water_status = "FULL" if data_mgr.device2_water else "LOW"
    oled.text(f"Level: {water_status}", 0, 25)
    
    # 控制状态 (加热/制冷)
    control_status = ""
    if data_mgr.device2_heat:
        control_status = "HEAT+"
    elif data_mgr.device2_cool:
        control_status = "COOL-"
    else:
        control_status = "IDLE"
    oled.text(f"Ctrl: {control_status}", 0, 35)
    
    # 水泵状态
    if data_mgr.device2_pump:
        oled.text(f"Pump: {data_mgr.shared_flow:.1f}", 0, 45)
    else:
        oled.text("Pump: OFF", 0, 45)
    
    # 警告报警指示
    alert_text = ""
    if data_mgr.device2_warn:
        alert_text += "W!"
    if data_mgr.device2_alarm:
        alert_text += "A!"
    if alert_text:
        oled.text(alert_text, 90, 0)
    
    oled.show()
    return oled


async def async_display_task_1():
    """异步封装的设备1显示任务 - 每秒刷新"""
    print("🚀 设备1显示任务开始运行...")
    
    while True:
        try:
            display_task_1()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ 设备1显示任务错误: {e}")
            await asyncio.sleep(1)


async def async_display_task_2():
    """异步封装的设备2显示任务 - 每秒刷新"""
    print("🚀 设备2显示任务开始运行...")
    
    while True:
        try:
            display_task_2()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ 设备2显示任务错误: {e}")
            await asyncio.sleep(1)
