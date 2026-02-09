"""
设备数据存储类
包含两个设备的数据管理，支持温度、水位、加热、水泵、制冷等状态管理
以及警告、报警和共享流速控制
"""

class DeviceData:
    """单个设备数据类"""
    
    def __init__(self, device_id):
        """
        初始化设备数据
        
        Args:
            device_id (str): 设备ID ('device1' 或 'device2')
        """
        self.device_id = device_id
        
        # 温度数据 (模拟量)
        self.temperature = 25.0  # 当前温度
        
        # 开关量状态
        self.water_level_status = False  # 水位状态 (True:正常, False:异常)
        self.heater_switch = False       # 加热开关
        self.pump_switch = False         # 水泵开关
        self.cooling_switch = False      # 制冷开关
        
        # 警告和报警状态
        self.warning_status = False      # 警告状态
        self.alarm_status = False        # 报警状态
    
    def set_temperature(self, temp):
        """
        设置温度值
        
        Args:
            temp (float): 温度值
        """
        self.temperature = float(temp)
    
    def set_water_level_status(self, status):
        """
        设置水位状态
        
        Args:
            status (bool): 水位状态
        """
        self.water_level_status = bool(status)
    
    def set_heater_switch(self, switch_state):
        """
        设置加热开关
        
        Args:
            switch_state (bool): 开关状态
        """
        self.heater_switch = bool(switch_state)
    
    def set_pump_switch(self, switch_state):
        """
        设置水泵开关
        
        Args:
            switch_state (bool): 开关状态
        """
        self.pump_switch = bool(switch_state)
    
    def set_cooling_switch(self, switch_state):
        """
        设置制冷开关
        
        Args:
            switch_state (bool): 开关状态
        """
        self.cooling_switch = bool(switch_state)
    
    def set_warning_status(self, status):
        """
        设置警告状态
        
        Args:
            status (bool): 警告状态
        """
        self.warning_status = bool(status)
    
    def set_alarm_status(self, status):
        """
        设置报警状态
        
        Args:
            status (bool): 报警状态
        """
        self.alarm_status = bool(status)
    
    def get_device_status(self):
        """
        获取设备完整状态信息
        
        Returns:
            dict: 设备状态字典
        """
        return {
            'device_id': self.device_id,
            'temperature': self.temperature,
            'water_level_status': self.water_level_status,
            'heater_switch': self.heater_switch,
            'pump_switch': self.pump_switch,
            'cooling_switch': self.cooling_switch,
            'warning_status': self.warning_status,
            'alarm_status': self.alarm_status
        }
    
    def __str__(self):
        """字符串表示"""
        return f"Device {self.device_id}: Temp={self.temperature}°C, " \
               f"Water={'Normal' if self.water_level_status else 'Low'}, " \
               f"Heater={'ON' if self.heater_switch else 'OFF'}, " \
               f"Pump={'ON' if self.pump_switch else 'OFF'}, " \
               f"Cooling={'ON' if self.cooling_switch else 'OFF'}, " \
               f"Warning={'YES' if self.warning_status else 'NO'}, " \
               f"Alarm={'YES' if self.alarm_status else 'NO'}"


class DataManager:
    """数据管理类 - 管理两个设备和共享流速"""
    
    def __init__(self):
        """初始化数据管理器"""
        # 创建两个设备实例
        self.device1 = DeviceData('device1')
        self.device2 = DeviceData('device2')
        
        # 共享流速 (模拟量)
        self.flow_rate = 0.0  # 流速值
    
    def set_flow_rate(self, rate):
        """
        设置共享流速
        
        Args:
            rate (float): 流速值
        """
        self.flow_rate = float(rate)
    
    def get_flow_rate(self):
        """
        获取共享流速
        
        Returns:
            float: 当前流速值
        """
        return self.flow_rate
    
    def get_device(self, device_id):
        """
        获取指定设备对象
        
        Args:
            device_id (str): 设备ID ('device1' 或 'device2')
            
        Returns:
            DeviceData: 设备对象
            
        Raises:
            ValueError: 当设备ID无效时
        """
        if device_id == 'device1':
            return self.device1
        elif device_id == 'device2':
            return self.device2
        else:
            raise ValueError(f"无效的设备ID: {device_id}")
    
    def get_all_devices_status(self):
        """
        获取所有设备状态信息
        
        Returns:
            dict: 包含所有设备状态和共享流速的字典
        """
        return {
            'device1': self.device1.get_device_status(),
            'device2': self.device2.get_device_status(),
            'shared_flow_rate': self.flow_rate
        }
    
    def update_device_temperature(self, device_id, temperature):
        """
        更新指定设备温度
        
        Args:
            device_id (str): 设备ID
            temperature (float): 温度值
        """
        device = self.get_device(device_id)
        device.set_temperature(temperature)
    
    def update_device_switch(self, device_id, switch_type, state):
        """
        更新指定设备的开关状态
        
        Args:
            device_id (str): 设备ID
            switch_type (str): 开关类型 ('water_level', 'heater', 'pump', 'cooling')
            state (bool): 开关状态
        """
        device = self.get_device(device_id)
        
        switch_map = {
            'water_level': device.set_water_level_status,
            'heater': device.set_heater_switch,
            'pump': device.set_pump_switch,
            'cooling': device.set_cooling_switch
        }
        
        if switch_type in switch_map:
            switch_map[switch_type](state)
        else:
            raise ValueError(f"无效的开关类型: {switch_type}")
    
    def update_device_alert(self, device_id, alert_type, status):
        """
        更新指定设备的警告/报警状态
        
        Args:
            device_id (str): 设备ID
            alert_type (str): 警告类型 ('warning', 'alarm')
            status (bool): 状态值
        """
        device = self.get_device(device_id)
        
        if alert_type == 'warning':
            device.set_warning_status(status)
        elif alert_type == 'alarm':
            device.set_alarm_status(status)
        else:
            raise ValueError(f"无效的警告类型: {alert_type}")
    
    def get_system_summary(self):
        """
        获取系统概要信息
        
        Returns:
            str: 格式化的系统状态字符串
        """
        summary = f"=== 系统状态概要 ===\n"
        summary += f"共享流速: {self.flow_rate}\n"
        summary += f"\n设备1状态:\n{self.device1}\n"
        summary += f"\n设备2状态:\n{self.device2}\n"
        summary += "=" * 20
        
        return summary
    
    def __str__(self):
        """字符串表示"""
        return self.get_system_summary()


# 使用示例和测试代码
if __name__ == "__main__":
    # 创建数据管理器实例
    data_manager = DataManager()
    
    # 设置初始数据
    data_manager.set_flow_rate(15.5)
    data_manager.update_device_temperature('device1', 28.3)
    data_manager.update_device_temperature('device2', 26.7)
    
    # 设置设备开关状态
    data_manager.update_device_switch('device1', 'water_level', True)
    data_manager.update_device_switch('device1', 'heater', True)
    data_manager.update_device_switch('device1', 'pump', False)
    data_manager.update_device_switch('device1', 'cooling', False)
    
    data_manager.update_device_switch('device2', 'water_level', True)
    data_manager.update_device_switch('device2', 'heater', False)
    data_manager.update_device_switch('device2', 'pump', True)
    data_manager.update_device_switch('device2', 'cooling', True)
    
    # 设置警告报警状态
    data_manager.update_device_alert('device1', 'warning', False)
    data_manager.update_device_alert('device1', 'alarm', False)
    data_manager.update_device_alert('device2', 'warning', True)
    data_manager.update_device_alert('device2', 'alarm', False)
    
    # 输出系统状态
    print(data_manager.get_system_summary())
    
    # 获取特定设备状态
    print("\n设备1详细状态:")
    print(data_manager.device1.get_device_status())
    
    print("\n设备2详细状态:")
    print(data_manager.device2.get_device_status())
    
    # 获取所有数据
    print("\n完整数据结构:")
    import json
    print(json.dumps(data_manager.get_all_devices_status(), indent=2, ensure_ascii=False))