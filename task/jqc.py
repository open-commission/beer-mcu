import uasyncio as asyncio
from machine import Pin
from data.singleton_data import get_data_manager


# ---------------- JQC继电器控制任务 ----------------
async def jqc_control_task():
    """JQC继电器控制任务，根据设备状态控制对应的继电器
    
    引脚分配：
    - 14: 设备1制冷 (特殊：通电0.5s断电2s循环)
    - 15: 设备2制冷 (特殊：通电0.5s断电2s循环)
    - 17: 设备1制热
    - 18: 设备2制热
    - 19: 设备1水泵
    - 20: 设备2水泵
    """
    # 获取数据管理器
    data_mgr = get_data_manager()
    
    # 初始化继电器引脚
    relay_pins = {
        'device1_cool': Pin(14, Pin.OUT),  # 设备1制冷
        'device2_cool': Pin(15, Pin.OUT),  # 设备2制冷
        'device1_heat': Pin(17, Pin.OUT),  # 设备1制热
        'device2_heat': Pin(18, Pin.OUT),  # 设备2制热
        'device1_pump': Pin(19, Pin.OUT),  # 设备1水泵
        'device2_pump': Pin(20, Pin.OUT)   # 设备2水泵
    }
    
    # 上电初始化：所有继电器重置为低电平(关闭)
    for pin in relay_pins.values():
        pin.value(0)
    print("✅ 所有继电器已初始化为关闭状态")
    
    # 特殊继电器状态跟踪(用于14和15的循环控制)
    cool_cycle_state = {
        'device1_cool': False,  # False表示等待通电，True表示等待断电
        'device2_cool': False
    }
    
    while True:
        # 处理设备1制冷继电器(14号引脚) - 特殊循环控制
        if data_mgr.device1_cool:
            if not cool_cycle_state['device1_cool']:  # 等待通电阶段
                relay_pins['device1_cool'].value(1)
                cool_cycle_state['device1_cool'] = True
                print("🔌 设备1制冷继电器(14) 通电")
            else:  # 等待断电阶段
                relay_pins['device1_cool'].value(0)
                cool_cycle_state['device1_cool'] = False
                print("🔌 设备1制冷继电器(14) 断电")
        else:
            # 制冷关闭时，确保继电器为低电平
            relay_pins['device1_cool'].value(0)
            cool_cycle_state['device1_cool'] = False
            print("🔌 设备1制冷继电器(14) 关闭")
        
        # 处理设备2制冷继电器(15号引脚) - 特殊循环控制
        if data_mgr.device2_cool:
            if not cool_cycle_state['device2_cool']:  # 等待通电阶段
                relay_pins['device2_cool'].value(1)
                cool_cycle_state['device2_cool'] = True
                print("🔌 设备2制冷继电器(15) 通电")
            else:  # 等待断电阶段
                relay_pins['device2_cool'].value(0)
                cool_cycle_state['device2_cool'] = False
                print("🔌 设备2制冷继电器(15) 断电")
        else:
            # 制冷关闭时，确保继电器为低电平
            relay_pins['device2_cool'].value(0)
            cool_cycle_state['device2_cool'] = False
            print("🔌 设备2制冷继电器(15) 关闭")
        
        # 处理设备1制热继电器(17号引脚) - 普通开关控制
        if data_mgr.device1_heat:
            relay_pins['device1_heat'].value(1)
            print("🔌 设备1制热继电器(17) 开启")
        else:
            relay_pins['device1_heat'].value(0)
            print("🔌 设备1制热继电器(17) 关闭")
        
        # 处理设备2制热继电器(18号引脚) - 普通开关控制
        if data_mgr.device2_heat:
            relay_pins['device2_heat'].value(1)
            print("🔌 设备2制热继电器(18) 开启")
        else:
            relay_pins['device2_heat'].value(0)
            print("🔌 设备2制热继电器(18) 关闭")
        
        # 处理设备1水泵继电器(19号引脚) - 普通开关控制
        if data_mgr.device1_pump:
            relay_pins['device1_pump'].value(1)
            print("🔌 设备1水泵继电器(19) 开启")
        else:
            relay_pins['device1_pump'].value(0)
            print("🔌 设备1水泵继电器(19) 关闭")
        
        # 处理设备2水泵继电器(20号引脚) - 普通开关控制
        if data_mgr.device2_pump:
            relay_pins['device2_pump'].value(1)
            print("🔌 设备2水泵继电器(20) 开启")
        else:
            relay_pins['device2_pump'].value(0)
            print("🔌 设备2水泵继电器(20) 关闭")
        
        # 等待0.5秒后检查下一个循环
        await asyncio.sleep(0.5)


async def jqc_task():
    """主函数，启动JQC继电器控制任务"""
    print("🚀 JQC继电器控制系统开始运行...")

    # 启动继电器控制任务
    asyncio.create_task(jqc_control_task())

    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)