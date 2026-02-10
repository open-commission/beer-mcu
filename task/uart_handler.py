"""
UART数据接收处理器
负责接收UART数据并根据设备ID更新对应的数据
"""

import uasyncio as asyncio
import json
from data.singleton_data import get_data_manager


def uart_data_handler(json_data):
    """
    UART数据处理函数
    根据设备ID更新对应设备的数据
    
    Args:
        json_data (str): JSON格式的输入数据
    """
    try:
        # 解析JSON数据
        data = json.loads(json_data)
        
        # 验证数据结构
        if not isinstance(data, dict):
            print("❌ 无效的数据格式")
            return False
            
        # 获取设备ID
        device_id = data.get('device')
        if not device_id:
            print("❌ 缺少设备ID字段")
            return False
            
        # 获取数据管理器实例
        data_manager = get_data_manager()
        
        # 根据设备ID更新对应数据
        if device_id == 'device1':
            # 更新设备1数据
            update_device_data(data_manager, data, 'device1')
            print(f"✅ 设备1数据更新成功: temp={data.get('temp', 'N/A')}, water={data.get('water', 'N/A')}")
            return True
            
        elif device_id == 'device2':
            # 更新设备2数据
            update_device_data(data_manager, data, 'device2')
            print(f"✅ 设备2数据更新成功: temp={data.get('temp', 'N/A')}, water={data.get('water', 'N/A')}")
            return True
            
        else:
            print(f"❌ 未知的设备ID: {device_id}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 数据处理错误: {e}")
        return False


def update_device_data(data_manager, data, device_key):
    """
    更新指定设备的数据
    
    Args:
        data_manager: 数据管理器实例
        data (dict): 要更新的数据字典
        device_key (str): 设备键名 ('device1' 或 'device2')
    """
    try:
        # 构造设备数据字典
        device_data = {}
        
        # 更新各个字段，如果不存在则保持原值
        if 'temp' in data:
            device_data['temp'] = float(data['temp'])
        if 'water' in data:
            device_data['water'] = bool(int(data['water'])) if isinstance(data['water'], str) else bool(data['water'])
        if 'heat' in data:
            device_data['heat'] = bool(int(data['heat'])) if isinstance(data['heat'], str) else bool(data['heat'])
        if 'pump' in data:
            device_data['pump'] = bool(int(data['pump'])) if isinstance(data['pump'], str) else bool(data['pump'])
        if 'cool' in data:
            device_data['cool'] = bool(int(data['cool'])) if isinstance(data['cool'], str) else bool(data['cool'])
        if 'warn' in data:
            device_data['warn'] = bool(int(data['warn'])) if isinstance(data['warn'], str) else bool(data['warn'])
        if 'alarm' in data:
            device_data['alarm'] = bool(int(data['alarm'])) if isinstance(data['alarm'], str) else bool(data['alarm'])
        
        # 如果有流速数据，也更新共享流速
        if 'flow' in data:
            data_manager.shared_flow = float(data['flow'])
        
        # 使用数据管理器的更新方法
        if device_key == 'device1':
            data_manager.update_from_dict({'device1': device_data})
        elif device_key == 'device2':
            data_manager.update_from_dict({'device2': device_data})
            
    except (ValueError, TypeError) as e:
        print(f"❌ 设备数据更新错误: {e}")
        raise


async def uart_receive_task(uart_util):
    """
    UART接收任务 - 持续监听并处理接收到的数据
    
    Args:
        uart_util: UART工具实例
    """
    print("🚀 UART数据接收任务开始运行...")
    buffer = ""
    
    while True:
        try:
            # 检查是否有数据可读
            if uart_util.any():
                raw_data = uart_util.safe_read()
                if raw_data:
                    try:
                        # 解码数据
                        text_data = raw_data.decode('utf-8')
                        buffer += text_data
                        
                        # 按行处理数据
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()
                            
                            if line:
                                # 处理完整的JSON行
                                success = uart_data_handler(line)
                                if not success:
                                    print(f"⚠️  数据处理失败: {line}")
                                    
                    except UnicodeDecodeError as e:
                        print(f"❌ 数据解码错误: {e}")
                        buffer = ""  # 清空缓冲区
                        
            # 短暂等待避免过度占用CPU
            await asyncio.sleep_ms(10)
            
        except Exception as e:
            print(f"❌ UART接收任务错误: {e}")
            await asyncio.sleep(1)


# 导出主要函数
__all__ = ['uart_data_handler', 'uart_receive_task']