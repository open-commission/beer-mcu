import uasyncio as asyncio
from machine import Pin
from data.singleton_data import get_data_manager


# ---------------- LED状态控制任务 ----------------
async def led_control_task():
    """LED状态控制任务，根据设备状态控制警告和报警灯
    
    引脚分配：
    - 2:  设备1警告灯
    - 29: 设备2警告灯
    - 3:  设备1报警灯
    - 28: 设备2报警灯
    """
    # 获取数据管理器
    data_mgr = get_data_manager()
    
    # 初始化LED引脚
    warning_leds = {
        'device1_warn': Pin(2, Pin.OUT),   # 设备1警告灯
        'device2_warn': Pin(29, Pin.OUT)   # 设备2警告灯
    }
    
    alarm_leds = {
        'device1_alarm': Pin(3, Pin.OUT),  # 设备1报警灯
        'device2_alarm': Pin(28, Pin.OUT)  # 设备2报警灯
    }
    
    # 上电初始化：所有LED重置为低电平(熄灭)
    for led in list(warning_leds.values()) + list(alarm_leds.values()):
        led.value(0)
    print("✅ 所有LED已初始化为熄灭状态")
    
    # 闪烁状态跟踪
    blink_state = {
        'device1_warn': False,
        'device2_warn': False,
        'device1_alarm': False,
        'device2_alarm': False
    }
    
    while True:
        # 处理设备1警告灯(2号引脚)
        if data_mgr.device1_warn:
            # 警告状态：慢速闪烁(1秒亮1秒灭)
            warning_leds['device1_warn'].value(blink_state['device1_warn'])
            blink_state['device1_warn'] = not blink_state['device1_warn']
            if blink_state['device1_warn']:
                print("⚠️  设备1警告灯闪烁(亮)")
            else:
                print("⚠️  设备1警告灯闪烁(灭)")
        else:
            # 无警告：保持熄灭
            warning_leds['device1_warn'].value(0)
            blink_state['device1_warn'] = False
            print("⚠️  设备1警告灯熄灭")
        
        # 处理设备2警告灯(29号引脚)
        if data_mgr.device2_warn:
            # 警告状态：慢速闪烁(1秒亮1秒灭)
            warning_leds['device2_warn'].value(blink_state['device2_warn'])
            blink_state['device2_warn'] = not blink_state['device2_warn']
            if blink_state['device2_warn']:
                print("⚠️  设备2警告灯闪烁(亮)")
            else:
                print("⚠️  设备2警告灯闪烁(灭)")
        else:
            # 无警告：保持熄灭
            warning_leds['device2_warn'].value(0)
            blink_state['device2_warn'] = False
            print("⚠️  设备2警告灯熄灭")
        
        # 处理设备1报警灯(3号引脚)
        if data_mgr.device1_alarm:
            # 报警状态：快速闪烁(0.3秒亮0.3秒灭)
            alarm_leds['device1_alarm'].value(blink_state['device1_alarm'])
            blink_state['device1_alarm'] = not blink_state['device1_alarm']
            if blink_state['device1_alarm']:
                print("🚨 设备1报警灯快速闪烁(亮)")
            else:
                print("🚨 设备1报警灯快速闪烁(灭)")
        else:
            # 无报警：保持熄灭
            alarm_leds['device1_alarm'].value(0)
            blink_state['device1_alarm'] = False
            print("🚨 设备1报警灯熄灭")
        
        # 处理设备2报警灯(28号引脚)
        if data_mgr.device2_alarm:
            # 报警状态：快速闪烁(0.3秒亮0.3秒灭)
            alarm_leds['device2_alarm'].value(blink_state['device2_alarm'])
            blink_state['device2_alarm'] = not blink_state['device2_alarm']
            if blink_state['device2_alarm']:
                print("🚨 设备2报警灯快速闪烁(亮)")
            else:
                print("🚨 设备2报警灯快速闪烁(灭)")
        else:
            # 无报警：保持熄灭
            alarm_leds['device2_alarm'].value(0)
            blink_state['device2_alarm'] = False
            print("🚨 设备2报警灯熄灭")
        
        # 警告灯闪烁周期：1秒
        await asyncio.sleep(1)


async def led_task():
    """主函数，启动LED状态控制任务"""
    print("🚀 LED状态控制系统开始运行...")

    # 启动LED控制任务
    asyncio.create_task(led_control_task())

    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)