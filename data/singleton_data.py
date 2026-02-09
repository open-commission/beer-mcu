"""
全局单例数据管理器
负责管理两个设备的数据，并提供显示更新和串口通信接口
"""

import uasyncio as asyncio
import json
from machine import Pin, I2C
from display.ssd1306 import SSD1306_I2C


class SingletonData:
    """全局单例数据管理器"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonData, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # 防止重复初始化
        if self._initialized:
            return
            
        # 设备1数据
        self.device1_temp = 25.0          # 温度
        self.device1_water = False        # 水位状态
        self.device1_heat = False         # 加热开关
        self.device1_pump = False         # 水泵开关
        self.device1_cool = False         # 制冷开关
        self.device1_warn = False         # 警告状态
        self.device1_alarm = False        # 报警状态
        
        # 设备2数据
        self.device2_temp = 25.0          # 温度
        self.device2_water = False        # 水位状态
        self.device2_heat = False         # 加热开关
        self.device2_pump = False         # 水泵开关
        self.device2_cool = False         # 制冷开关
        self.device2_warn = False         # 警告状态
        self.device2_alarm = False        # 报警状态
        
        # 共享数据
        self.shared_flow = 0.0            # 共享流速
        
        # 显示对象
        self.display = None
        self._setup_display()
        
        # 标记已初始化
        self._initialized = True
    
    def _setup_display(self):
        """初始化OLED显示屏"""
        try:
            # 初始化I2C
            i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
            i2c_addr = i2c_dev.scan()
            
            if i2c_addr:
                self.display = SSD1306_I2C(128, 64, i2c_dev)
                print("✅ OLED显示屏初始化成功")
            else:
                print("❌ 未找到OLED显示屏")
        except Exception as e:
            print(f"❌ 显示屏初始化失败: {e}")
    
    def update_from_dict(self, data_dict):
        """
        从字典更新数据
        
        Args:
            data_dict (dict): 包含设备数据的字典
        """
        try:
            # 更新设备1数据
            if 'device1' in data_dict:
                dev1 = data_dict['device1']
                self.device1_temp = float(dev1.get('temp', self.device1_temp))
                self.device1_water = bool(dev1.get('water', self.device1_water))
                self.device1_heat = bool(dev1.get('heat', self.device1_heat))
                self.device1_pump = bool(dev1.get('pump', self.device1_pump))
                self.device1_cool = bool(dev1.get('cool', self.device1_cool))
                self.device1_warn = bool(dev1.get('warn', self.device1_warn))
                self.device1_alarm = bool(dev1.get('alarm', self.device1_alarm))
            
            # 更新设备2数据
            if 'device2' in data_dict:
                dev2 = data_dict['device2']
                self.device2_temp = float(dev2.get('temp', self.device2_temp))
                self.device2_water = bool(dev2.get('water', self.device2_water))
                self.device2_heat = bool(dev2.get('heat', self.device2_heat))
                self.device2_pump = bool(dev2.get('pump', self.device2_pump))
                self.device2_cool = bool(dev2.get('cool', self.device2_cool))
                self.device2_warn = bool(dev2.get('warn', self.device2_warn))
                self.device2_alarm = bool(dev2.get('alarm', self.device2_alarm))
            
            # 更新共享流速
            if 'flow' in data_dict:
                self.shared_flow = float(data_dict['flow'])
                
        except (ValueError, TypeError) as e:
            print(f"❌ 数据更新错误: {e}")
    
    def get_device1_dict(self):
        """获取设备1数据字典"""
        return {
            'temp': self.device1_temp,
            'water': self.device1_water,
            'heat': self.device1_heat,
            'pump': self.device1_pump,
            'cool': self.device1_cool,
            'warn': self.device1_warn,
            'alarm': self.device1_alarm
        }
    
    def get_device2_dict(self):
        """获取设备2数据字典"""
        return {
            'temp': self.device2_temp,
            'water': self.device2_water,
            'heat': self.device2_heat,
            'pump': self.device2_pump,
            'cool': self.device2_cool,
            'warn': self.device2_warn,
            'alarm': self.device2_alarm
        }
    
    def get_all_data_dict(self):
        """获取所有数据字典"""
        return {
            'device1': self.get_device1_dict(),
            'device2': self.get_device2_dict(),
            'flow': self.shared_flow
        }
    
    def update_display(self):
        """更新OLED显示屏内容"""
        if not self.display:
            return
            
        try:
            # 清空屏幕
            self.display.fill(0)
            
            # 显示标题
            self.display.text("Beer Brewing System", 0, 0)
            self.display.text(f"Flow: {self.shared_flow:.1f}", 0, 10)
            
            # 设备1信息 (左侧)
            self.display.text("DEV1:", 0, 25)
            self.display.text(f"T:{self.device1_temp:.1f}", 0, 35)
            status1 = f"W:{'1' if self.device1_water else '0'} H:{'1' if self.device1_heat else '0'}"
            self.display.text(status1, 0, 45)
            status2 = f"P:{'1' if self.device1_pump else '0'} C:{'1' if self.device1_cool else '0'}"
            self.display.text(status2, 0, 55)
            
            # 设备2信息 (右侧)
            self.display.text("DEV2:", 64, 25)
            self.display.text(f"T:{self.device2_temp:.1f}", 64, 35)
            status3 = f"W:{'1' if self.device2_water else '0'} H:{'1' if self.device2_heat else '0'}"
            self.display.text(status3, 64, 45)
            status4 = f"P:{'1' if self.device2_pump else '0'} C:{'1' if self.device2_cool else '0'}"
            self.display.text(status4, 64, 55)
            
            # 警告报警指示 (屏幕顶部)
            warn_text = ""
            if self.device1_warn or self.device2_warn:
                warn_text += "W!"
            if self.device1_alarm or self.device2_alarm:
                warn_text += "A!"
            if warn_text:
                self.display.text(warn_text, 90, 0)
            
            # 刷新显示
            self.display.show()
            
        except Exception as e:
            print(f"❌ 显示更新失败: {e}")
    
    def get_serial_output(self):
        """
        获取串口输出数据
        
        Returns:
            tuple: (设备1JSON字符串, 设备2JSON字符串)
        """
        # 设备1数据
        dev1_data = {
            'device': 'device1',
            'temp': round(self.device1_temp, 2),
            'water': int(self.device1_water),
            'heat': int(self.device1_heat),
            'pump': int(self.device1_pump),
            'cool': int(self.device1_cool),
            'warn': int(self.device1_warn),
            'alarm': int(self.device1_alarm),
            'flow': round(self.shared_flow, 2)
        }
        
        # 设备2数据
        dev2_data = {
            'device': 'device2',
            'temp': round(self.device2_temp, 2),
            'water': int(self.device2_water),
            'heat': int(self.device2_heat),
            'pump': int(self.device2_pump),
            'cool': int(self.device2_cool),
            'warn': int(self.device2_warn),
            'alarm': int(self.device2_alarm),
            'flow': round(self.shared_flow, 2)
        }
        
        return json.dumps(dev1_data), json.dumps(dev2_data)


# 全局单例实例
data_manager = SingletonData()


async def display_refresh_task():
    """显示刷新任务 - 每秒更新一次显示"""
    print("🚀 显示刷新任务开始运行...")
    
    while True:
        try:
            data_manager.update_display()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ 显示刷新任务错误: {e}")
            await asyncio.sleep(1)


async def serial_output_task(uart_util):
    """串口输出任务 - 每秒输出数据"""
    print("🚀 串口输出任务开始运行...")
    
    while True:
        try:
            # 获取JSON数据
            dev1_json, dev2_json = data_manager.get_serial_output()
            
            # 发送设备1数据
            uart_util.send(dev1_json + '\n')
            
            # 发送设备2数据
            uart_util.send(dev2_json + '\n')
            
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ 串口输出任务错误: {e}")
            await asyncio.sleep(1)


def handle_serial_input(json_data):
    """
    处理串口输入数据
    
    Args:
        json_data (str): JSON格式的输入数据
    """
    try:
        # 解析JSON数据
        data = json.loads(json_data)
        
        # 验证数据结构
        if not isinstance(data, dict):
            print("❌ 无效的数据格式")
            return
            
        # 更新全局数据
        data_manager.update_from_dict({'device1': data, 'device2': data, 'flow': data.get('flow', 0)})
        
        print(f"✅ 数据更新成功: {json_data}")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
    except Exception as e:
        print(f"❌ 数据处理错误: {e}")


# 导出函数
def get_data_manager():
    """获取全局数据管理器实例"""
    return data_manager