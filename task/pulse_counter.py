import uasyncio as asyncio
from machine import Pin, Timer
from data.singleton_data import get_data_manager


class PulseCounter:
    """脉冲计数器类，用于读取ZJS201流量传感器的脉冲信号"""
    
    def __init__(self, pin_number=11):
        """
        初始化脉冲计数器
        
        Args:
            pin_number (int): 脉冲输入引脚编号，默认为11号引脚
        """
        self.pin_number = pin_number
        self.pulse_count = 0           # 脉冲计数
        self.last_pulse_time = 0       # 上次脉冲时间
        self.flow_rate = 0.0           # 当前流速 (L/min)
        self.timer = None              # 定时器对象
        
        # ZJS201流量传感器参数
        self.pulses_per_liter = 450    # 每升对应的脉冲数 (根据ZJS201规格)
        self.measurement_interval = 1  # 测量间隔(秒)
        
        # 初始化引脚
        self.setup_pin()
        
    def setup_pin(self):
        """配置脉冲输入引脚"""
        try:
            # 配置为输入模式，启用上拉电阻
            self.pulse_pin = Pin(self.pin_number, Pin.IN, Pin.PULL_UP)
            print(f"✅ 脉冲计数引脚 GPIO{self.pin_number} 初始化成功")
        except Exception as e:
            print(f"❌ 脉冲计数引脚初始化失败: {e}")
            raise
    
    def pulse_callback(self, pin):
        """
        脉冲中断回调函数
        
        Args:
            pin: 触发中断的引脚对象
        """
        # 增加脉冲计数
        self.pulse_count += 1
        
        # 记录当前时间
        import time
        current_time = time.ticks_ms()
        
        # 计算脉冲频率(可选)
        if self.last_pulse_time > 0:
            interval = time.ticks_diff(current_time, self.last_pulse_time)
            # 可以在这里计算瞬时频率
            pass
            
        self.last_pulse_time = current_time
    
    def calculate_flow_rate(self):
        """计算流速"""
        # 计算每分钟流速 (L/min)
        # 脉冲数 / 每升脉冲数 * 60秒 / 测量间隔
        pulses_per_interval = self.pulse_count
        self.flow_rate = (pulses_per_interval / self.pulses_per_liter) * (60 / self.measurement_interval)
        
        # 重置脉冲计数
        self.pulse_count = 0
        
        return self.flow_rate
    
    def start_counting(self):
        """开始脉冲计数"""
        try:
            # 设置上升沿中断触发
            self.pulse_pin.irq(trigger=Pin.IRQ_RISING, handler=self.pulse_callback)
            print(f"🚀 脉冲计数已启动 - 监听GPIO{self.pin_number}")
        except Exception as e:
            print(f"❌ 启动脉冲计数失败: {e}")
    
    def stop_counting(self):
        """停止脉冲计数"""
        try:
            # 禁用中断
            self.pulse_pin.irq(handler=None)
            print("🛑 脉冲计数已停止")
        except Exception as e:
            print(f"❌ 停止脉冲计数失败: {e}")
    
    def get_flow_rate(self):
        """
        获取当前流速
        
        Returns:
            float: 流速值 (L/min)
        """
        return self.flow_rate
    
    def get_pulse_count(self):
        """
        获取当前脉冲计数
        
        Returns:
            int: 脉冲计数
        """
        return self.pulse_count


async def pulse_monitor_task():
    """脉冲监测任务 - 定期计算并更新流速数据"""
    print("🚀 脉冲流量监测任务开始运行...")
    
    # 创建脉冲计数器实例
    pulse_counter = PulseCounter(pin_number=11)
    
    # 获取数据管理器
    data_manager = get_data_manager()
    
    # 开始脉冲计数
    pulse_counter.start_counting()
    
    try:
        while True:
            # 等待测量间隔
            await asyncio.sleep(pulse_counter.measurement_interval)
            
            # 计算流速
            current_flow = pulse_counter.calculate_flow_rate()
            
            # 更新共享流速数据
            data_manager.shared_flow = current_flow
            
            # 输出调试信息
            if current_flow > 0:
                print(f"💧 流量传感器数据 - 脉冲计数: {pulse_counter.pulse_count}, "
                      f"流速: {current_flow:.2f} L/min")
            else:
                print(f"💧 流量传感器待机 - 当前无流量")
                
    except KeyboardInterrupt:
        print("🛑 收到停止信号")
    except Exception as e:
        print(f"❌ 脉冲监测任务错误: {e}")
    finally:
        # 清理资源
        pulse_counter.stop_counting()


async def pulse_counter_task():
    """主脉冲计数任务函数"""
    print("🚀 ZJS201脉冲计数任务启动...")
    
    # 启动脉冲监测任务
    asyncio.create_task(pulse_monitor_task())
    
    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)